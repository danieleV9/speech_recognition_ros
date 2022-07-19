#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16MultiArray, String
import numpy as np
import time

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, Wav2Vec2ProcessorWithLM, WavLMForCTC
from datasets import load_dataset
import soundfile as sf
import torch

# Init node
rospy.init_node('speech_recognition_node', anonymous=True)
pub1 = rospy.Publisher('voice_data', Int16MultiArray, queue_size=1)
pub2 = rospy.Publisher('voice_txt', String, queue_size=1)

# load model and tokenizer
#path_to_model = "/home/dvalentino5/Scrivania/cogrob/cogrob_ws/src/ros_audio_pkg/src/models/wavlm-base-plus-ft-cv3"
path_to_model = "/models/wawlm-base-plus-cv/"
processor = Wav2Vec2Processor.from_pretrained(path_to_model)
model = WavLMForCTC.from_pretrained(path_to_model)

#rospy.wait_for_service('gtts_server') # when we use Audacious as output for text-to-speech
rospy.wait_for_service('tts_server') # when we use Pepper as output for text-to-speech

# this is called from the background thread
def callback(audio):
    data = np.array(audio.data,dtype=np.int16)
    #print(type(data))

    try:
        spoken_text = speech2text(np.double(data))
        print("Output of the ASR module: " + spoken_text[0])
        pub1.publish(audio) # Publish audio only if it contains words
        pub2.publish(spoken_text[0])
    except:
        print("I did not understand what you said")

def listener():
    rospy.Subscriber("mic_data", Int16MultiArray, callback)
    rospy.spin()

# Transcription with our models

def speech2text(data):          
    start = time.time()
    # tokenize
    input_values = processor(data, return_tensors="pt", padding="longest", sampling_rate=16_000).input_values  # Batch size 1

    # retrieve logits
    logits = model(input_values).logits

    # take argmax and decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
    #print(transcription)
    end = time.time()
    print("Inference time: " + str(end - start))
    return transcription


if __name__ == '__main__':
    listener()



# def speech2text_with_lm(data):
#     from datasets import load_dataset
#     from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, Wav2Vec2ProcessorWithLM
#     import torch

#     model_id = "/home/dvalentino5/Scrivania/cogrob/cogrob_ws/src/ros_audio_pkg/src/models/wav2vec2-base-960h-4-gram"

#     model = Wav2Vec2ForCTC.from_pretrained(model_id)
#     processor = Wav2Vec2ProcessorWithLM.from_pretrained(model_id)

#     input_values = processor(data, return_tensors="pt", sampling_rate=16000).input_values

#     with torch.no_grad():
#         logits = model(input_values).logits

#     transcription = processor.batch_decode(logits.numpy()).text
#     return transcription