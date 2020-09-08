#!/usr/bin/env python

import sys,time
import rospy
import numpy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32
P = 30
I = 1
D = 1
theta = 0
mc = 28.93
mw = 5.449
l = 0.1242
cmd_vel = "/cmd_vel"
Imu_topic = "/imu"
AInertial= [0,0,1]

def dcmtoEuler(Rmatrix):

	return [numpy.arctan2(Rmatrix[0][1],Rmatrix[0][0])*(180*100/314),numpy.arcsin(Rmatrix[0][2])*(180*100/314),numpy.arctan2(Rmatrix[1][2],Rmatrix[2][2])*(180*100/314)]

def integrate(Rminus,Bminus,gyros,accels,accelInertial,deltaT):
	Kp_a=20
	Ki_a=1
	
	accels = accels/numpy.linalg.norm(accels)
	accelInertial = accelInertial/numpy.linalg.norm(accelInertial)
	gyrorads = numpy.multiply(gyros,math.pi/180)
	gyroInputWithBias = numpy.subtract(gyrorads ,Bminus)
	
	wmeas_a = numpy.matmul(rcross(accels),numpy.matmul(numpy.matrix.transpose(numpy.array(Rminus)), accelInertial))
	
	gyroInputWithFeedback = numpy.add(gyroInputWithBias,Kp_a*wmeas_a)
	
	bdot=-Ki_a*wmeas_a
    
	Rplus = numpy.matmul(Rminus,Rexp(numpy.multiply(gyroInputWithFeedback,deltaT)))
	Bplus = numpy.add(Bminus,numpy.multiply(bdot,deltaT))
	
	return [Rplus,Bplus]

def Rexp(w):
	wnorm = numpy.linalg.norm(w)
	rx = rcross([w[0],w[1],w[2]])
	s = numpy.sinc(wnorm/2)
	c = numpy.cos(wnorm/2)
	return (numpy.add([[1,0,0],[0,1,0],[0,0,1]],numpy.add(numpy.multiply(s*c,rx),numpy.multiply((s*s/2),numpy.matmul(rx,rx)))))

def rcross(r):
	return [[0,-r[2],r[1]],[r[2],0,-r[0]],[-r[1],r[0],0]]

class controller:
	def __init__(self,Pin,Iin,Din):
		self.Kp = Pin
		self.Ki = Iin
		self.Kd = Din
		self.desiredAngle = theta
		self.integrator = 0
		self.prevError = 0
		self.Time = rospy.get_time()
		self.prevTime = self.Time
		self.prevAngVel = 0
	def update(self,angle,prevVel):

		self.Time = rospy.get_time()
		timeDiff = self.Time -self.prevTime
		timeDiff = 0.02
		#if timeDiff >= 0.02:

		error = (angle*3.1415/180) - self.desiredAngle
		dE = (error - self.prevError)
		iE = error * self.integrator
		self.integrator = self.integrator + error

		proportional = self.Kp * error
		derivative = self.Kd * dE/timeDiff
		integral = self.Ki * iE*timeDiff

		PID = -(proportional + integral + derivative)
		#xvel = (-mc*l*(PID-self.prevAngVel))/(2*mw-mc)+prevVel
		self.prevError = error
		#print("angvelocities")
		#print(self.prevAngVel)
		#print(PID)
		#print(prevVel)
		#print(angle)
		self.prevAngVel = PID
		
		#return xvel
		return PID
		#else:
		#	return 0

class Balance:
	def __init__(self):
		print "INITIALIZING NODES \r\n"
		self.pub= rospy.Publisher(cmd_vel,Twist,queue_size=1)
		#while self.pub.get_num_connections() == 0:
		#	rospy.sleep(1)
		#	print "waiting for connection /r/n"
		self.subscriber = rospy.Subscriber(Imu_topic,Imu,self.callback)
		
		self.PID = controller(20,0.1,0.1)
		self.PID2 = controller(20,0.1,0.1)
		self.Rmatrix = numpy.array([[1,0,0],[0,1,0],[0,0,1]])
		self.Bias = numpy.array([0,0,0])
		self.prevxvel = 0
	def callback(self,data):
		setPoint = 0
		gyro = [data.angular_velocity.x,data.angular_velocity.y,data.angular_velocity.z]
		accel = [data.linear_acceleration.x,data.linear_acceleration.y,data.linear_acceleration.z]
		temp = integrate(self.Rmatrix,self.Bias,gyro,accel,AInertial,0.02)
		self.Rmatrix = temp[0]
		self.Bias = temp[1]
		Euler = dcmtoEuler(self.Rmatrix)
		xvel = self.PID.update(Euler[2],self.prevxvel)
		
		vel = Twist()
		if xvel > 0.5:
			xvel = 0.5
		elif xvel < -0.5:
			xvel = -0.5
		
		#print(xvel)

		#xvel = self.PID2.update(xvel,self.prevxvel)

		#if xvel > 0.5:
		#	xvel = 0.5
		#elif xvel < -0.5:
		#	xvel = -0.5
		
		vel.linear.x = xvel
		
		vel.linear.y = 0

		vel.linear.z = 0
		vel.angular.x = 0
		vel.angular.y = 0
		vel.angular.z = 0
		#print("x = "+str(xvel))
		self.prevxvel = xvel
		self.pub.publish(vel)
		
if __name__ == '__main__':
	print "STARTING CODE \r\n"
	rospy.init_node('Balance',anonymous=False)
	ic = Balance()
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print "Stopping"
