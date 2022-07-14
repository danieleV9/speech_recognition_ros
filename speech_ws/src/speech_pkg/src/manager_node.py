#!/usr/bin/python3
from multiprocessing import Manager
import rospy
from speech_pkg.srv import *
import time

def run(req):
    res = transcribe(req.data)
    out_string = res.s
    print("You said: " + out_string)
    #res = speech(out_string)
    #return ManagerResponse(res.flag)
    return ManagerResponse(True)

if __name__ == "__main__":
    rospy.init_node('manager')
    rospy.wait_for_service('transcriber_service')
    #rospy.wait_for_service('speech_service')
    rospy.Service('manager_service', Manager, run)
    transcribe = rospy.ServiceProxy('transcriber_service', Transcription)
    #speech = rospy.ServiceProxy('speech_service', Talker)
    rospy.spin()