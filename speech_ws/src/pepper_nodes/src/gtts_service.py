#!/usr/bin/env python3
from gtts import gTTS 
import subprocess
from pepper_nodes.srv import TextToSpeechGTTS, TextToSpeechGTTSResponse
import rospy
from std_msgs.msg import String
import librosa
import time


def handle_gtts(req):
    #print("Sto parlando tramite gTTS")
    text = req.text
    if text == "" or text==" ":
        text = "please, repeat"
    tts = gTTS(text=text, lang='en')
    tts.save("tts_output_audio.mp3")
    #print("tutto fatto, file gtts salvato!")
    process = subprocess.run(["audacious", "tts_output_audio.mp3"])
    code = process.returncode
    duration = librosa.get_duration(filename="tts_output_audio.mp3")
    print("Duration of the input: " + str(duration))
    #time.sleep(duration)
    #subprocess.run(["killall", "audacious"])
    return TextToSpeechGTTSResponse("ACK"+str(code))

def gtts_server():
    rospy.init_node('gtts_service')
    s = rospy.Service('gtts_server', TextToSpeechGTTS, handle_gtts)
    print("Ready to performe gtts.")
    rospy.spin()

if __name__ == "__main__":
    gtts_server()