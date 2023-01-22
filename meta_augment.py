import re

f = open('../../data/train/wav.scp', 'r')
f1 = open('../../data/train/utt2spk', 'r')
f2 = open('../../data/train/segments', 'r')
f3 = open('../../data/train/text', 'r')

wr = open('../../data/train/aug-wav.scp', 'w')
wr1 = open('../../data/train/aug-utt2spk', 'w')
wr2 = open('../../data/train/aug-segments', 'w')
wr3 = open('../../data/train/aug-text', 'w')

lines = f.readlines()
lines1 = f1.readlines()
lines2 = f2.readlines()
lines3 = f3.readlines()

suffix = "sd"

for line in lines:
    appended = re.sub(r'fn......', r'\g<0>{}'.format(suffix), line)
    lol = re.sub(r'RP2022/JASMIN/Data/data/audio/wav/comp-p/nl/',
                 r'RP2022/amesic/kaldi/egs/jasmin_amesic/asr_sd/aug_audio/comp-p/', appended)
    lol = re.sub(r'RP2022/JASMIN/Data/data/audio/wav/comp-q/nl/',
                 r'RP2022/amesic/kaldi/egs/jasmin_amesic/asr_sd/aug_audio/comp-q/', lol)
    wr.write(lol)

for line in lines1:
    appended = re.sub(r'fn......', r'\g<0>{}'.format(suffix), line)
    wr1.write(appended)

for line in lines2:
    appended = re.sub(r'fn......', r'\g<0>{}'.format(suffix), line)
    wr2.write(appended)

for line in lines3:
    appended = re.sub(r'fn......', r'\g<0>{}'.format(suffix), line)
    wr3.write(appended)

f.close()
f1.close()
f2.close()
f3.close()

wr.close()
wr1.close()
wr2.close()
wr3.close()
