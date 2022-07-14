#!/usr/bin/python3
from multiprocessing import Manager
import rospy
from speech_pkg.srv import *
import time

def run(req):
    start = time.time()
    res = transcribe(req.data)
    end = time.time()
    total = end - start
    print("The time of inference is: " + str(total))
    out_string = res.s
    print(out_string)
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