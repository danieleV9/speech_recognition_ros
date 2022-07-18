#!/usr/bin/env python
from pepper_nodes.srv import Text2Speech, Text2SpeechResponse
import qi
import rospy
IP = "10.0.1.207" # 10.0.1.230
PORT = 9559

def callback(req):
    out_str = str(req.text)
    with open("/home/files/res.txt", "a") as fil:
        fil.write("*"*30)
        fil.write(out_str)
        fil.write("*" * 30)
        fil.write("\n")
    print(out_str)
    say(out_str)
    return Text2SpeechResponse("ACK0")

def connect_robot():
    # Connect to the robot
    print("Connecting to robot...")
    session = qi.Session()
    session.connect('tcp://%s:9559' % IP )  # Robot IP
    print("Robot connected")

    motion_service = session.service("ALMotion")
    motion_service.wakeUp()

    #TextToSpeech service
    tablet = session.service("ALTabletService")
    tablet.loadApplication("pepper_nodes/src/j-tablet-browser")
    tablet.showWebview()
    return tablet

def say(out_str):
    try:
        tts.say(out_str)
    except Exception:
        session = qi.Session()
        session.connect('tcp://%s:9559' % IP )
        tts = session.service("ALTextToSpeech")
        tts.setLanguage("English")
        tts.say(out_str)
    # time.sleep(0.5)

if __name__ == "__main__":
    tablet = connect_robot()
    rospy.init_node('tablet_service')
    rospy.Service('tablet_server', Text2Speech, callback)
    print("Ready to update the tablet screen.")
    rospy.spin()