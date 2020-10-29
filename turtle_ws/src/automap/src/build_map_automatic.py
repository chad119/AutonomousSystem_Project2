#!/usr/bin/env python


import rospy
import math
import tf
# pub
# -cmd_vel
from geometry_msgs.msg import Twist

# sub
# -map
from nav_msgs.msg import OccupancyGrid
# -scan
from sensor_msgs.msg import LaserScan
# -slam_out_pose
from geometry_msgs.msg import PoseStamped

# param
SAFE_DIS=0.3
SIDE_DIS=0.2
LIN_VEL =0.035
ANG_VEL =0.3 

# sub map data
m_d=[]
def getmap(data):
    global m_d
    m_d=data.data
    m_d=list(m_d)

# sub scan data
rg=[]
def scaninfo(data):
    global rg
    rg=data.ranges
    rg=list(rg)
    for i in range(len(rg)):
	if rg[i] == float('Inf'):
	    rg[i] = 3.5

# sub slam_out_pose data
px=0
py=0
qx=0
qy=0
qz=0
qw=0
yaw=0.0
def slamPose(data):
    global px,py,qx,qy,qz,qw,yaw
    px=data.pose.position.x
    py=data.pose.position.y
    pz=data.pose.position.z
    qx=data.pose.orientation.x
    qy=data.pose.orientation.y
    qz=data.pose.orientation.z
    qw=data.pose.orientation.w
    quaternion = (qx,qy,qz,qw)
    euler = tf.transformations.euler_from_quaternion(quaternion)
    yaw = euler[2]

#other function
# stop funtion    
def stop_cond():
    #find unknown cell index
    unknown=[i for i,x in enumerate(m_d) if x==-1]
    count=[]
    
    for i in unknown:
	if not (i%2048==0 or i%2048==2047 or i//2048==0 or i//2048==2047):
	    if m_d[i+1]==0 or m_d[i-1]==0 or m_d[i+2048]==0 or m_d[i-2048]==0:
		count.append(i)
    print "unknow:", len(count)
    #threshold
    if len(count)<25:
	return True
    return False
   
#main function
def build_map_automatic():
    rospy.init_node('build_map_automatic', anonymous=True)
    rospy.Subscriber('slam_out_pose', PoseStamped, slamPose)
    rospy.Subscriber('map', OccupancyGrid, getmap)
    rospy.Subscriber('scan', LaserScan, scaninfo)
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    rate = rospy.Rate(1)
    print('start!')
    while not rospy.is_shutdown():
	move_cmd=Twist()
	if len(rg)==0:
	    while True:
	        move_cmd.linear.x=0
	        move_cmd.angular.z=0
	        pub.publish(move_cmd)
	        rate.sleep()
	        if len(rg)!=0:
		    break
	if rg[0]>SAFE_DIS:
	    #left sensor close=> right turn
	    if rg[30]<SIDE_DIS:
		print "right"
		if rg[30]<rg[330]:
		    #while True:
			print "rightRRR"
			move_cmd.linear.x=0
			move_cmd.angular.z=-0.5*ANG_VEL
			pub.publish(move_cmd)
			rate.sleep()
			#if rg[30]>=SIDE_DIS:
			#    break
		else:
		    #while True:
			print "rightLLL"
			move_cmd.linear.x=0
			move_cmd.angular.z=0.7*ANG_VEL
			pub.publish(move_cmd)
			rate.sleep()
			#if rg[30]<rg[330]:
			#    break
	    #right sensor close=> left turn
	    elif rg[330]<SIDE_DIS:
		print "left"
		if rg[330]<rg[30]:
		    #while True:
			print "leftLLL"
			move_cmd.linear.x=0
			move_cmd.angular.z=0.7*ANG_VEL
			pub.publish(move_cmd)
			rate.sleep()
			#if rg[330]>=SIDE_DIS:
			#    break
		else:
		    #while True:
			print "leftRRR"
			move_cmd.linear.x=0
			move_cmd.angular.z=-0.5*ANG_VEL
			pub.publish(move_cmd)
			rate.sleep()
			#if rg[330]<rg[30]:
			#    break
	    else:
		#while True:
		    #dis = rg[0]-SAFE_DIS
		    #move_cmd.linear.x=dis*LIN_VEL/(3.5-SAFE_DIS)
		    move_cmd.linear.x=LIN_VEL
		    move_cmd.angular.z=0
		    pub.publish(move_cmd)
		    rate.sleep()
		    #if rg[0]<SAFE_DIS:
		#	break
	else:
	    if rg[30]>rg[330]:
		#while True:
		    move_cmd.linear.x=0
		    move_cmd.angular.z=0.7*ANG_VEL
		    pub.publish(move_cmd)
		    rate.sleep()
	        #    if rg[30]<=rg[330]:
		#        break
	    else:
		#while True:
		    move_cmd.linear.x=0
		    move_cmd.angular.z=-0.5**ANG_VEL
		    pub.publish(move_cmd)
		    rate.sleep()
	        #    if rg[30]>rg[330]:
		#        break
	if stop_cond():
	    move_cmd.linear.x=0
	    move_cmd.angular.z=0
	    pub.publish(move_cmd)
	    rate.sleep()
	    print "STOP!!!!!"
	    print "Please use >>rosrun map_server map_saver -f ~/map"
	    break
if __name__=='__main__':
    try:
	build_map_automatic()
    except rospy.ROSInterruptException:
	pass



