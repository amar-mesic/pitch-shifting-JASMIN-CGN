#!/bin/bash
# <description>
# Credit to Alves Marinov from whom this script was adapted
#
# This bash script is used to generate the train and test sets upon which the kaldi ASR works
# This script can be run from any directory as long as it has access to the kaldi ASR.

SCRIPTLOC=$(pwd)
# Here provide the suffix of the ASR directory,
# generally, the suffix to the ASR dir is the same as the suffix for the augmented .wav files
ASR="sd50"
# ORIGDIR refers to the location where the script will be run by changing directory
ORIGDIR="/tudelft.net/staff-bulk/ewi/insy/SpeechLab/RP2022/amesic/kaldi/egs/jasmin_amesic/asr_$ASR/orig_data/scripts"
# ORIGDATA is the directory where metadata files are located for the whole of the JASMIN-CGN corpus
# We will extract the relevant data needed for our region.
ORIGDATA="${ORIGDIR}/../jas_All"

YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

cd $ORIGDATA
echo -e "Current dir is ${ORIGDATA}"
echo -e "${YELLOW}Deleting previously existing train and test directories...${NC}"
# remove any previously existing directories. This way the script can be rerun easily.
rm -r ../../data/train
rm -r train/
rm -r ../../data/test
rm -r test/

echo -e "${YELLOW}Extracting 4 main files (segments, wav, text, utt2spk)_region for the region based on manual data split of train and test!${NC}"
# This file is explained in the README.md more thoroughly. It containes the train set speaker IDs
# so that we can create the metadata files such that the ASR is trained only on data from these speakers.
FILENAME="$ORIGDIR/../../split/std_split/train-ids.txt"
mkdir train
cd train

# Using the speaker IDs, we create the corresponding metadata files
grep -Fw -f $FILENAME ../segments > segments
# wav identifiers are dependent on  these IDs
cat segments | awk '{print $2}' > wav_prep
grep -Fw -f wav_prep ../wav.scp > wav.scp
grep -Fw -f $FILENAME ../text > text
grep -Fw -f $FILENAME ../utt2spk > utt2spk

rm wav_prep


# The same process for making the `train/` directory is applied for the test directory.
# Of course a file with the IDs of speakers from the test set is needed.
cd ..
FILENAME="$ORIGDIR/../../split/std_split/test-ids.txt"
mkdir test
cd test


grep -Fw -f $FILENAME ../segments > segments
# wav identifiers are dependent on  these IDs
cat segments | awk '{print $2}' > wav_prep
grep -Fw -f wav_prep ../wav.scp > wav.scp
grep -Fw -f $FILENAME ../text > text
grep -Fw -f $FILENAME ../utt2spk > utt2spk

rm wav_prep

cd ..
cp -r train/ ../../data/
cp -r test/ ../../data/

cd ../../data/train/

# If combining data from multiple other augmentations, such as [-30%, +30%], set $COMBINE to 1, else 0.
COMBINE=0

if [ $COMBINE == 1 ]
then
  # Copy the metadata files for each [parameter of the] augmentation applied.
  # The code can be expanded to allow for an arbitray amount of augmentations,
  # but currently it is hardcoded for an upward and downward pitch shift.
	cp segments ps-segments
	cp text ps-text
	cp utt2spk ps-utt2spk
	cp wav.scp ps-wav.scp
	
	cp segments sd-segments
	cp text sd-text
	cp utt2spk sd-utt2spk
	cp wav.scp sd-wav.scp

	# This script, which is documented, edits the files to allow the ASR to make use of the augmented training data.
	python $ORIGDIR/meta_augment_combine.py

	#we append all the data to the original metadata files since it needs to be in one file.
	echo -e "ps lines: $(cat ps-segments | wc -l)"
	cat ps-segments >> segments
	cat ps-utt2spk >> utt2spk
	cat ps-text >> text
	cat ps-wav.scp >> wav.scp
	
	echo -e "sd lines: $(cat sd-segments | wc -l)"
	cat sd-segments >> segments
	cat sd-utt2spk >> utt2spk
	cat sd-text >> text
	cat sd-wav.scp >> wav.scp

	# remove the files created since their info has been stored.
	ls | grep -E "^((ps)|(sd))" | xargs rm

else
  # alternatively only augment once.
	cp segments aug-segments
	cp text aug-text
	cp utt2spk aug-utt2spk
	cp wav.scp aug-wav.scp

	# This code could be redundant if the python script can accept an arbitrary amount of augmentations.
	python $ORIGDIR/meta_augment.py

	echo -e "aug lines: $(cat aug-segments | wc -l)"
	echo "wav first line: $(head wav.scp -n 1)"
	echo "aug-wav first line: $(head aug-wav.scp -n 1)"

	cat aug-segments >> segments
	cat aug-utt2spk >> utt2spk
	cat aug-text >> text
	cat aug-wav.scp >> wav.scp

	ls | grep -E "^aug" | xargs rm

fi


# Run the script which creates test directories seperated on speaker attributes.
cd $SCRIPTLOC
./split_test.sh

cd $ORIGDIR/../../

# An important step in preparing the data for the ASR is to run the
# `utils/fix_data_dir.sh` script, which comes with kaldi, on all training/test directories
./utils/fix_data_dir.sh data/train
./utils/fix_data_dir.sh data/test

for test_dir in data/*-test
do
	echo -e "Prepping test dir: $test_dir"
	./utils/fix_data_dir.sh $test_dir
done


echo  -e "${GREEN}Data prep DONE!${NC}"
