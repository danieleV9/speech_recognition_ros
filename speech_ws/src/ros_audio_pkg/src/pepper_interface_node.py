#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16MultiArray, String
import numpy as np
from pepper_nodes.srv import ExecuteJS, Text2Speech, LoadUrl
from flask import Flask

# Init node
rospy.init_node('pepper_interface_node', anonymous=True)

#tts = rospy.ServiceProxy('gtts_server', TextToSpeechGTTS) #gTTS with Audacious
tts = rospy.ServiceProxy('tts_server', Text2Speech) #TTS with Pepper
tablet = rospy.ServiceProxy('tablet_server', LoadUrl) # Pepper tablet
pub = rospy.Publisher('tts_ack', String, queue_size=1)

def callback(text):
    resp_tts = tts(text.data)
    resp_tablet = tablet(text.data)
    print(resp_tts.ack)
    print(resp_tablet.ack)
    if resp_tts.ack == "ACK0":
        print("tts ok")
    else:
        print("Error with tts")
    pub.publish(resp_tts.ack)

def listener():
    rospy.Subscriber("voice_txt", String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()