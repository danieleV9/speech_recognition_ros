#!/usr/bin/python
# coding=utf-8
import rospy
import qi
from speech_pkg.srv import *
import argparse
from lang_settings import AVAILABLE_LANGS
import sys
import time


def callback(req):
    out_str = str(req.s)
    with open("/home/files/res.txt", "a") as fil:
        fil.write("*"*30)
        fil.write(out_str)
        fil.write("*" * 30)
        fil.write("\n")
    print(out_str)
    say(out_str)
    return TalkerResponse(True)

def connect_robot():
    # Connect to the robot
    print("Connecting to robot...")
    session = qi.Session()
    session.connect('tcp://%s:9559' % IP )  # Robot IP
    print("Robot connected")

    motion_service = session.service("ALMotion")
    motion_service.wakeUp()

    #TextToSpeech service
    tts = session.service("ALTextToSpeech")
    tts.setLanguage("Italian" if args.lang == "ita" else "English")
    tts.say("Hello")
    return tts

def say(out_str):
    try:
        tts.say(out_str)
    except Exception:
        session = qi.Session()
        session.connect('tcp://%s:9559' % IP )

        tts = session.service("ALTextToSpeech")
        tts.setLanguage("Italian" if args.lang == "ita" else "English")
        tts.say(out_str)
    # time.sleep(0.5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", required=True, dest="lang", type=str)
    parser.add_argument("--ip", required=True, dest="ip", type=str)
    args, unknown = parser.parse_known_args(args=rospy.myargv(argv=sys.argv)[1:])
    IP = args.ip
    if args.lang not in AVAILABLE_LANGS:
        raise Exception("Selected lang not available.\nAvailable langs:", AVAILABLE_LANGS)
    tts = connect_robot()
    rospy.init_node('talker')

    rospy.Service('speech_service', Talker, callback)

    rospy.spin()