class PIDController:
	
	def __init__(self, P, I, D, theta):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.desiredAngle = theta
        self.integrator = 0
        self.prevError = 0

    def update(self,angle):
    	error = angle - self.desiredAngle

    	dE = error - self.prevError
    	iE = error * self.integrator
    	self.integrator = self.integrator + error

    	proportional = self.Kp * error
    	derivative = self.Kd * dE
    	integral = self.Ki * iE

    	PID = proportional + integral + derivative
    	return PID