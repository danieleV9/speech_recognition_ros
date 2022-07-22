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
    str_text = str(text.data)
    str_text = str_text.replace(" im "," i'm ")
    str_text = str_text.replace("im ","i'm ")
    str_text = str_text.replace(" dont "," don't ")
    str_text = str_text.replace("whats ","what's")
    str_text = str_text.replace("piper ","pepper ")
    str_text = str_text.replace("peppe ","pepper ")
    str_text = str_text.replace("beppe ","pepper ")
    if str_text == "" or str_text == " ":
        str_text = "You did not speak"
        pepper_resp = "You did not speak"

    if str_text == "good morning do you remember me":
        pepper_resp = "Of course, you are Daniele"
    if str_text == "are you ready to perform speech recognition":
        pepper_resp = "Yes, I'm already doing it actually"
    if str_text == "i am hungry book me the nearest restaurant":
        pepper_resp = "OK, for how many people?"
    if str_text == "i need a table for five people" or str_text == "i need a table for 5 people":
        pepper_resp = "OK, I booked a table for five at Pigreco"
    if str_text == "thank you":
        pepper_resp = "you are welcome, would you like to hear some music in the meantime?"
    if str_text == "play my favorite playlist on google music":
        pepper_resp = "OK, good listening, anything else I can do for you?"
    if str_text == "no thanks see you soon":
        pepper_resp = "bye-bye"

    resp_tablet = tablet(str_text)
    resp_tts = tts(pepper_resp)
    #resp_tts = tts(str_text)
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