import rospy
import csv
from std_msgs.msg import String
Cvfile = 'CV.csv'
Cyclespeed = 200
class CV:	
	pub = rospy.Publisher(CV,String,queue_size=1)
	rospy.init_node('CVdata',anonymous=False)
	rate = rospy.Rate(Cyclespeed)

	with open('CV.csv', newline='')as Cvfile:
		Cvcommands = csv.reader(Cvfile)
		while True:
			for row in Cvcommands:
				Cvout = row[0]+row[1]
				if(Cvout != 'RightLeft')
					rospy.loginfo(row)
					pub.publish(row)
					rate.sleep()

if __name__ = '__main__':
	print "publishing computer vision output"
	try:
		CV()
	except KeyboardInterrupt:
		pass
