import re

# Credit to author upon which this script was based: Alves Marinov, TU Delft
# This document serves to edit the meta files needed to to train and test a kaldi ASR.

# First we read in the original meta files
f = open('../../data/train/wav.scp', 'r')
f1 = open('../../data/train/utt2spk', 'r')
f2 = open('../../data/train/segments', 'r')
f3 = open('../../data/train/text', 'r')

lines = f.readlines()
lines1 = f1.readlines()
lines2 = f2.readlines()
lines3 = f3.readlines()


# The suffixes are added to the augmented .wav files, and we add the corresponding
# suffix to the reference of the file within the meta files.
# Note that this script assumes the file suffix is the same as the asr_* directory suffix.
# For however many suffixes i.e. augmentations are needed, a list accomodates them all.
# INSERT FILENAME SUFFIX HERE
suffixes = ["ps", "sd"]

for suffix in suffixes:

    # Open up a writing stream to wirte to the meta files for augmented data
    wr = open('../../data/train/{}-wav.scp'.format(suffix), 'w')
    wr1 = open('../../data/train/{}-utt2spk'.format(suffix), 'w')
    wr2 = open('../../data/train/{}-segments'.format(suffix), 'w')
    wr3 = open('../../data/train/{}-text'.format(suffix), 'w')

    # In each of the meta files, carry out the necessary substitutions.
    for line in lines:
        appended = re.sub(r'fn......', r'\g<0>{}'.format(suffix), line)
        lol = re.sub(r'RP2022/JASMIN/Data/data/audio/wav/comp-p/nl/',
                     r'RP2022/amesic/kaldi/egs/jasmin_amesic/asr_{}/aug_audio/comp-p/'.format(suffix), appended)
        lol = re.sub(r'RP2022/JASMIN/Data/data/audio/wav/comp-q/nl/',
                     r'RP2022/amesic/kaldi/egs/jasmin_amesic/asr_{}/aug_audio/comp-q/'.format(suffix), lol)
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

    wr.close()
    wr1.close()
    wr2.close()
    wr3.close()

# close the writing streams
f.close()
f1.close()
f2.close()
f3.close()
