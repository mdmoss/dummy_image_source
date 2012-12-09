#!/usr/bin/python
import roslib; roslib.load_manifest('dummy_image_source')
import rospy
from sensor_msgs.msg import CompressedImage
import glob
import os
from random import choice
import time
import math

import config

def dummy_image_source():
    pub = rospy.Publisher('dummy_images/compressed', CompressedImage)
    rospy.init_node('dummy_image_source')
    while not rospy.is_shutdown():

        if rospy.has_param('dummy_image_source/image'):
            try:
                image_handle = load_image(rospy.get_param('dummy_image_source/image'))
            except:
                rospy.logwarn("Problem loading image") 
            else:
                publish_image(pub, image_handle)
                print "Image Sent"
        elif rospy.has_param('dummy_image_source/image_dir'):
            try:
                image_handle = random_image_from_dir(rospy.get_param('dummy_image_source/image_dir'))
            except:
                rospy.logwarn("Problem loading image from directory") 
            else:
                publish_image(pub, image_handle)
                print "Image Sent"
        else:
            rospy.logwarn("No image source definied in 'image' or 'image_dir' params")
           
        rospy.sleep(rospy.get_param('dummy_image_source/sleep_time', config.DEFAULT_SLEEP_TIME))

def load_image(image):
    return open(image, 'rb')

def random_image_from_dir(directory):
    path = os.path.normpath(directory) + os.sep
    images = glob.glob(path + '*.jpg')
    return load_image(choice(images))

def publish_image(pub, image_handle):
    image = CompressedImage()
    image.data = image_handle.read()
    image.format = 'jpeg'
    image.header.seq = 0
    image.header.stamp.secs = math.floor(time.time())
    image.header.stamp.nsecs = 0
    image.header.frame_id = "0"
    pub.publish(image)

if __name__ == '__main__':
    try:
        dummy_image_source()
    except rospy.ROSInterruptException:
        pass
