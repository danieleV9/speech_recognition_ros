#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16MultiArray, String
import numpy as np
import os
import time
import speech_recognition as sr

# Init node
pub = rospy.Publisher('mic_data', Int16MultiArray, queue_size=1)
rospy.init_node('microphone_node', anonymous=True)

# Initialize a Recognizer
r = sr.Recognizer()

# Audio source
m = sr.Microphone(device_index=None, sample_rate=16000)

# #clear the output
# clear = lambda: os.system('clear')

# Calibration within the environment
print("Calibrating...")
with m as source:
    r.adjust_for_ambient_noise(source,duration=3)  
print("Calibration finished")

rospy.wait_for_service('gtts_server') # when we use Audacious as output for text-to-speech

# this is called from the background thread
def callback(audio):
    data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
    data_to_send = Int16MultiArray()
    data_to_send.data = data
    pub.publish(data_to_send)
    

if __name__ == '__main__':
    while not rospy.is_shutdown():
        with m as source:
            #clear()
            print("Please, say something")
            audio = r.listen(source, phrase_time_limit=5) # obtain audio from the microphone
        callback(audio)
        print("Audio obtained")
        rospy.wait_for_message('tts_ack',String)