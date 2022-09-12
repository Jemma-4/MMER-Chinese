import _thread
import argparse
import functools
import os
import time
import tkinter.messagebox
import wave
from tkinter.filedialog import *

import pyaudio

from data_utils.audio_process import AudioInferProcess
from utils.audio_vad import crop_audio_vad
from utils.predict import Predictor
from utils.utility import add_arguments, print_arguments

parser = argparse.ArgumentParser(description=__doc__)
add_arg = functools.partial(add_arguments, argparser=parser)
add_arg('use_gpu',          bool,   True,   "是否使用GPU预测")
add_arg('enable_mkldnn',    bool,   False,  "是否使用mkldnn加速")
add_arg('beam_size',        int,    300,    "集束搜索解码相关参数，搜索的大小，范围:[5, 500]")
add_arg('alpha',            float,  1.2,    "集束搜索解码相关参数，LM系数")
add_arg('beta',             float,  0.35,   "集束搜索解码相关参数，WC系数")
add_arg('cutoff_prob',      float,  0.99,   "集束搜索解码相关参数，剪枝的概率")
add_arg('cutoff_top_n',     int,    40,     "集束搜索解码相关参数，剪枝的最大值")
add_arg('mean_std_path',    str,    './dataset/mean_std.npz',      "数据集的均值和标准值的npy文件路径")
add_arg('vocab_path',       str,    './dataset/zh_vocab.txt',      "数据集的词汇表文件路径")
add_arg('model_dir',        str,    './models/infer/',             "导出的预测模型文件夹路径")
add_arg('lang_model_path',  str,    './lm/zh_giga.no_cna_cmn.prune01244.klm',   "集束搜索解码相关参数，语言模型文件路径")
add_arg('decoding_method',  str,    'ctc_greedy',    "结果解码方法，有集束搜索(ctc_beam_search)、贪婪策略(ctc_greedy)", choices=['ctc_beam_search', 'ctc_greedy'])
args = parser.parse_args()
print_arguments(args)


class SpeechRecognitionApp:
    def __init__(self, window: Tk, args):
        self.window = window
        self.wav_path = None
        self.predicting = False
        self.playing = False
        self.recording = False
        self.stream = None
        self.to_an = True
        # 最大录音时长
        self.max_record = 20
        # 录音保存的路径
        self.output_path = 'dataset/record'
        # 创建一个播放器
        self.p = pyaudio.PyAudio()
        # 指定窗口标题
        self.window.title("夜雨飘零语音识别")
        # 固定窗口大小
        self.window.geometry('870x500')
        self.window.resizable(False, False)
        # 识别短语音按钮
        self.short_button = Button(self.window, text="选择短语音识别", width=20, command=self.predict_audio_thread)
        self.short_button.place(x=10, y=10)
        # 识别长语音按钮
        self.long_button = Button(self.window, text="选择长语音识别", width=20, command=self.predict_long_audio_thread)
        self.long_button.place(x=170, y=10)
        # 录音按钮
        self.record_button = Button(self.window, text="录音识别", width=20, command=self.record_audio_thread)
        self.record_button.place(x=330, y=10)
        # 播放音频按钮
        self.play_button = Button(self.window, text="播放音频", width=20, command=self.play_audio_thread)
        self.play_button.place(x=490, y=10)
        # 输出结果文本框
        self.result_label = Label(self.window, text="输出日志：")
        self.result_label.place(x=10, y=70)
        self.result_text = Text(self.window, width=120, height=30)
        self.result_text.place(x=10, y=100)
        # 转阿拉伯数字控件
        self.an_frame = Frame(self.window)
        self.check_var = BooleanVar()
        self.to_an_check = Checkbutton(self.an_frame, text='中文数字转阿拉伯数字', variable=self.check_var, command=self.to_an_state)
        self.to_an_check.grid(row=0)
        self.to_an_check.select()
        self.an_frame.grid(row=1)
        self.an_frame.place(x=700, y=10)

        # 获取数据生成器，处理数据和获取字典需要
        self.audio_process = AudioInferProcess(vocab_filepath=args.vocab_path, mean_std_filepath=args.mean_std_path)

        # 获取识别器中文数字转阿拉伯数字
        self.predictor = Predictor(model_dir=args.model_dir, audio_process=self.audio_process,
                                   decoding_method=args.decoding_method, alpha=args.alpha, beta=args.beta,
                                   lang_model_path=args.lang_model_path, beam_size=args.beam_size,
                                   cutoff_prob=args.cutoff_prob, cutoff_top_n=args.cutoff_top_n, use_gpu=args.use_gpu,
                                   enable_mkldnn=args.enable_mkldnn)

    # 是否中文数字转阿拉伯数字
    def to_an_state(self):
        self.to_an = self.check_var.get()

    # 预测短语音线程
    def predict_audio_thread(self):
        if not self.predicting:
            self.wav_path = askopenfilename(filetypes=[("音频文件", "*.wav"), ("音频文件", "*.mp3")], initialdir='./dataset')
            if self.wav_path == '': return
            self.result_text.delete('1.0', 'end')
            self.result_text.insert(END, "已选择音频文件：%s\n" % self.wav_path)
            self.result_text.insert(END, "正在识别中...\n")
            _thread.start_new_thread(self.predict_audio, (self.wav_path, ))
        else:
            tkinter.messagebox.showwarning('警告', '正在预测，请等待上一轮预测结束！')

    # 预测短语音
    def predict_audio(self, wav_path):
        self.predicting = True
        try:
            start = time.time()
            score, text = self.predictor.predict(audio_path=wav_path, to_an=self.to_an)
            self.result_text.insert(END, "消耗时间：%dms, 识别结果: %s, 得分: %d\n" % (
            round((time.time() - start) * 1000), text, score))
        except Exception as e:
            print(e)
        self.predicting = False

    # 预测长语音线程
    def predict_long_audio_thread(self):
        if not self.predicting:
            self.wav_path = askopenfilename(filetypes=[("音频文件", "*.wav"), ("音频文件", "*.mp3")], initialdir='./dataset')
            if self.wav_path == '': return
            self.result_text.delete('1.0', 'end')
            self.result_text.insert(END, "已选择音频文件：%s\n" % self.wav_path)
            self.result_text.insert(END, "正在识别中...\n")
            _thread.start_new_thread(self.predict_long_audio, (self.wav_path, ))
        else:
            tkinter.messagebox.showwarning('警告', '正在预测，请等待上一轮预测结束！')

    # 预测长语音
    def predict_long_audio(self, wav_path):
        self.predicting = True
        try:
            start = time.time()
            # 分割长音频
            audios_path = crop_audio_vad(wav_path)
            texts = ''
            scores = []
            # 执行识别
            for i, audio_path in enumerate(audios_path):
                score, text = self.predictor.predict(audio_path=audio_path, to_an=self.to_an)
                texts = texts + '，' + text
                scores.append(score)
                self.result_text.insert(END, "第%d个分割音频, 得分: %d, 识别结果: %s\n" % (i, score, text))
            self.result_text.insert(END, "=====================================================\n")
            self.result_text.insert(END, "最终结果，消耗时间：%d, 得分: %d, 识别结果: %s\n" %
                                    (round((time.time() - start) * 1000), sum(scores) / len(scores), texts))
        except Exception as e:
            print(e)
        self.predicting = False

    # 录音识别线程
    def record_audio_thread(self):
        if not self.playing and not self.recording:
            self.result_text.delete('1.0', 'end')
            _thread.start_new_thread(self.record_audio, ())
        else:
            if self.playing:
                tkinter.messagebox.showwarning('警告', '正在录音，无法播放音频！')
            else:
                # 停止播放
                self.recording = False

    def record_audio(self):
        self.record_button.configure(text='停止录音')
        self.recording = True
        # 录音参数
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 16000

        # 打开录音
        self.stream = self.p.open(format=format,
                                  channels=channels,
                                  rate=rate,
                                  input=True,
                                  frames_per_buffer=chunk)
        self.result_text.insert(END, "正在录音...\n")
        start = time.time()
        frames = []
        while True:
            if not self.recording:break
            data = self.stream.read(chunk)
            frames.append(data)
            if len(frames) % 15 == 0:
                self.result_text.insert(END, "已录音%.2f秒\n" % (time.time() - start))
            if (time.time() - start) > self.max_record:
                self.result_text.insert(END, "录音已超过最大限制时长，强制停止录音！")
                break

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
        save_path = os.path.join(self.output_path, '%s.wav' % str(int(time.time())))
        wf = wave.open(save_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(self.p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        self.recording = False
        self.result_text.insert(END, "录音已结束，录音文件保存在：%s\n" % save_path)
        # 识别录音
        self.result_text.insert(END, "正在识别中...\n")
        self.wav_path = save_path
        self.predict_audio(self.wav_path)
        self.record_button.configure(text='录音识别')

    # 播放音频线程
    def play_audio_thread(self):
        if self.wav_path is None or self.wav_path == '':
            tkinter.messagebox.showwarning('警告', '音频路径为空！')
        else:
            if not self.playing and not self.recording:
                _thread.start_new_thread(self.play_audio, ())
            else:
                if self.recording:
                    tkinter.messagebox.showwarning('警告', '正在录音，无法播放音频！')
                else:
                    # 停止播放
                    self.playing = False

    # 播放音频
    def play_audio(self):
        self.play_button.configure(text='停止播放')
        self.playing = True
        CHUNK = 1024
        wf = wave.open(self.wav_path, 'rb')
        # 打开数据流
        self.stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                                  channels=wf.getnchannels(),
                                  rate=wf.getframerate(),
                                  output=True)
        # 读取数据
        data = wf.readframes(CHUNK)
        # 播放
        while data != b'':
            if not self.playing:break
            self.stream.write(data)
            data = wf.readframes(CHUNK)
        # 停止数据流
        self.stream.stop_stream()
        self.stream.close()
        self.playing = False
        self.play_button.configure(text='播放音频')


tk = Tk()
myapp = SpeechRecognitionApp(tk, args)

if __name__ == '__main__':
    tk.mainloop()
