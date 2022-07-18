#!/usr/bin/env python
from pepper_nodes.srv import Text2Speech, Text2SpeechResponse
from naoqi import ALProxy
import rospy
IP = "10.0.1.207" # 10.0.1.230
PORT = 9559

def handle_tts(req):
    tts = ALProxy("ALTextToSpeech", IP, PORT) # ALAnimatedSpeech
    tts.setLanguage("English")
    #tts.setParameter("speed",105)
    text = req.speech
    try:
        tts.say(text)
    except:
        tts = ALProxy("ALTextToSpeech", IP, PORT)
        tts.say(text)

    return Text2SpeechResponse("ACK0")

def tts_server():
    rospy.init_node('tts_service')
    s = rospy.Service('tts_server', Text2Speech, handle_tts)
    print("Ready to performe tts.")
    rospy.spin()

if __name__ == "__main__":
    try:
        tts_server()
    except rospy.ROSInterruptException:
        pass