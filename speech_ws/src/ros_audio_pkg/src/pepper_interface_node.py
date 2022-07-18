#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16MultiArray, String
import numpy as np
from pepper_nodes.srv import TextToSpeechGTTS, Text2Speech

# Init node
rospy.init_node('pepper_interface_node', anonymous=True)
#tts = rospy.ServiceProxy('gtts_server', TextToSpeechGTTS) #gTTS with Audacious
tts = rospy.ServiceProxy('tts_server', Text2Speech) #TTS with Pepper
pub = rospy.Publisher('tts_ack', String, queue_size=1)

def callback(text):
    resp_tts = tts(text.data)
    if resp_tts.ack == "ACK0":
        print("gtts ok")
        pub.publish(resp_tts.ack)
    else:
        print("Error with gtts")
        pub.publish(resp_tts.ack)

def listener():
    rospy.Subscriber("voice_txt", String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()