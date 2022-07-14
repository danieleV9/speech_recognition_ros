#!/usr/bin/python3
import numpy as np
from speech_pkg.srv import Transcription, TranscriptionResponse
from settings import pepper, global_utils
import torch
import rospy
import sys
from pathlib import Path
import argparse
import tensorflow as tf
from lang_settings import AVAILABLE_LANGS

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, WavLMForCTC
from datasets import load_dataset


class Transcriber:
    def __init__(self, lang):
        # self.model = ModelID((None,1))
        # print(tf.__version__)
        # base_path = Path(global_utils.get_curr_dir(__file__)).parent.joinpath("nosynt_cos_mean_75")
        # exp_dir = base_path.joinpath("distiller_ita_no_synt.h5")
        # self.model.load_weights("distiller_ita_no_synt.h5")
        # self.model = self.load_model(lang)
        # self.model = self.model.eval()
        '''if torch.cuda.is_available():
            self.model = self.model.cuda()
        else:
            self.model = self.model.cpu()
        '''
        self.init_node()

    def _pcm2float(self, sound: np.ndarray):
        abs_max = np.abs(sound).max()
        sound = sound.astype('float32')
        if abs_max > 0:
            sound *= 1 / abs_max
        sound = sound.squeeze()  # depends on the use case
        return sound

    def _numpy2tensor(self, signal: np.ndarray):
        signal_size = signal.size
        signal_torch = torch.as_tensor(signal, dtype=torch.float32)
        signal_size_torch = torch.as_tensor(signal_size, dtype=torch.int64)
        return signal_torch, signal_size_torch

    def convert(self, signal):
        signal = np.array(signal)
        signal_nw = self._pcm2float(signal)
        return signal_nw

    def transcribe_audio(self, signal: np.ndarray):
        # x=np.reshape(signal,(1,signal.shape[0],1))
        # _,y=self.model.predict(x)
        # #print(y[0])
        # l=[]
        # for ele in y[0]:
        #     l.append("{:.13f}".format(float(ele)))
        # yPredMax =  np.argmax(y)
        # return yPredMax,l[yPredMax]
        path_to_model = "/models/wawlm-base-plus-cv/"

        # load model and tokenizer
        processor = Wav2Vec2Processor.from_pretrained(path_to_model)
        model = WavLMForCTC.from_pretrained(path_to_model)

        # tokenize
        input_values = processor(signal, return_tensors="pt", padding="longest", sampling_rate=16_000).input_values  # Batch size 1

        # retrieve logits
        logits = model(input_values).logits

        # take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = processor.batch_decode(predicted_ids)
        print(transcription)
        out_str = "You said: "
        transcription = out_str
        return transcription

    def parse_req(self, req):
        signal = self.convert(req.data.data)
        audio_transcription = self.transcribe_audio(signal)
        return TranscriptionResponse(audio_transcription)

    def init_node(self):
        rospy.init_node('transcriber')
        s = rospy.Service('transcriber_service', Transcription, self.parse_req)
        rospy.spin()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", required=True, dest="lang", type=str)
    args, unknown = parser.parse_known_args(args=rospy.myargv(argv=sys.argv)[1:])
    if args.lang not in AVAILABLE_LANGS:
        raise Exception("Selected lang not available.\nAvailable langs:", AVAILABLE_LANGS)
    transcriber = Transcriber(args.lang)