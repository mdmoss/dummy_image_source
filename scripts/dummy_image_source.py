#!/usr/bin/python
import roslib; roslib.load_manifest('dummy_image_source')
import rospy
from sensor_msgs.msg import CompressedImage
import glob
import os
from random import choice

import config

def dummy_image_source():
    pub = rospy.Publisher('dummy_images', CompressedImage)
    rospy.init_node('dummy_image_source')
    while not rospy.is_shutdown():

        if rospy.has_param('image'):
            try:
                image_handle = load_image(rospy.get_param('image'))
            except:
                rospy.logwarn("Problem loading image") 
            else:
                publish_image(pub, image_handle)
        elif rospy.has_param('image_dir'):
            try:
                image_handle = random_image_from_dir(rospy.get_param('image_dir'))
            except:
                rospy.logwarn("Problem loading image from directory") 
            else:
                publish_image(pub, image_handle)
        else:
            rospy.logwarn("No image source definied in 'image' or 'image_dir' params")
           
        sleep_time = config.DEFAULT_SLEEP_TIME
        if rospy.has_param('sleep_time'):
            sleep_time = rospy.get_param('sleep_time')
        rospy.sleep(sleep_time)

def load_image(image):
    return open(image, 'rb')

def random_image_from_dir(directory):
    path = os.path.normpath(directory) + os.sep
    images = glob.glob(path + '*.jpg')
    return load_image(choice(image))

if __name__ == '__main__':
    try:
        dummy_image_source()
    except rospy.ROSInterruptException:
        pass
