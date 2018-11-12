# -*- coding: utf8 -*-
import codecs
import glob
from tqdm import tqdm
from pypinyin import pinyin, Style
from shutil import copyfile


def text2pinyin(sent):
    testing_text = pinyin(sent, style=Style.TONE3)
    testing_text = [x[0] for x in testing_text]
    # convert de->de5
    tmp = []
    for p in testing_text:
        if not p[-1].isdigit() and p[0].isalpha():
            tmp.append(p + '5')
        else:
            tmp.append(p)
    testing_text = " ".join(tmp)
    return testing_text


symbols = [u"？", u"、", u"。"]


def clean_symbols(sent):
    for sym in symbols:
        sent = sent.replace(sym, "")
    sent = sent.replace(u"，", u",")
    return sent.strip()
# main


print "Generating fake-THCS format dataset"
folder = "dada"
dataset_folder = "dataset"
wavs_list = glob.glob(folder + "/*.wav")

for wav in tqdm(wavs_list):
    name = wav[:-4]
    f = codecs.open(name + ".txt", "r", encoding='utf8')
    line = f.readline()
    p = text2pinyin(line)
    p = clean_symbols(p)
    # write into dataset folder
    wav_name = wav.split("/")[1]
    f = codecs.open(
        dataset_folder +
        "/" +
        wav_name +
        ".trn",
        'w',
        encoding="utf8")
    f.write(line + "\n")
    f.write(p + "\n")
    f.close()
    # copy wav
    copyfile(wav, dataset_folder + "/" + wav_name)
