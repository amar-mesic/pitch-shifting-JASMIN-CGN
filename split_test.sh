# <description>
#
# This bash script is used to create a split of the test set, creating the necessary directories that need to be placed under `asr_*/data/`.
# The split is conducted on: gender, age group, nativity, and component.
# This shell script is run in conjunction with the `create_train_test.sh` script which uses this script to create the test set, then moves them to the mentioned designated directory.
# This script can be run from any directory as long as it has access to the kaldi ASR.

# Here provide the suffix of the ASR directory, generally, the suffix to the ASR dir is the same as the suffix for the augmented .wav files
ASR="sd50"
# Provide the directory to the location where the script will run
ORIGDIR="/tudelft.net/staff-bulk/ewi/insy/SpeechLab/RP2022/amesic/kaldi/egs/jasmin_amesic/asr_$ASR/split"

YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${YELLOW}SPLITTING THE TEST SET BY AGE, GENDER, AND NATIVITY${NC}"

# Enter the working directory and create a file where we input the necessary info for the speakers in order to split by the attributes. We do this only for speakers in the test set.
cd $ORIGDIR
FILENAME="ids-with-relevant-feats.txt"

cat $ORIGDIR/../orig_data/meta/speakers.txt | grep -Fw -f std_split/test-ids.txt | awk '{print $1, $3, $5, $6}' > $FILENAME

# we also link to the direcotry inside our asr which contains the data files for the whole of JASMIN, we will use only that of the speakers of the test set.
DATA="$ORIGDIR/../orig_data/jas_All/"

# Split on the two gender
# split on gender - valueset: M, F
rm -r gender
mkdir gender
grep -E "^[^ ]+[[:space:]]M.+$" $FILENAME | awk '{print $1}' > gender/male-test-ids.txt
grep -E "^[^ ]+[[:space:]]F.+$" $FILENAME | awk '{print $1}' > gender/female-test-ids.txt

# split on the age groups
# split on age group - valueset: [1..5]
rm -r age
mkdir age
for i in {1..5}
do
	grep -E "^.+[[:space:]]$i$" $FILENAME | awk '{print $1}' > age/$i-test-ids.txt
done

# split on nativity
# split on birthplace/nativity - valueset: N-[0-9]{0,4}, [A-Z]{3}
rm -r nativity
mkdir nativity
grep -E "^.+[[:space:]]N-[0-9]{0,4}[[:space:]].$" $FILENAME | awk '{print $1}' > nativity/native-test-ids.txt
grep -E "^.+[[:space:]][A-Z]{3}[[:space:]].$" $FILENAME | awk '{print $1}' > nativity/nonnative-test-ids.txt

rm $FILENAME

# split on the component
# split speech in the two types, speech and conversational
rm -r comp
mkdir comp
comp_p="comp/comp-p.txt"
ls /tudelft.net/staff-bulk/ewi/insy/SpeechLab/RP2022/JASMIN/Data/data/audio/wav/comp-p/nl/ | sed 's+.wav++' > $comp_p
grep -f std_split/test-ids.txt $DATA/segments | grep -f $comp_p | awk -F'-' '{print $2}' | uniq > comp/compp-test-audiofiles.txt
rm $comp_p

comp_q="comp/comp-q.txt"
ls /tudelft.net/staff-bulk/ewi/insy/SpeechLab/RP2022/JASMIN/Data/data/audio/wav/comp-q/nl/ | sed 's+.wav++' > $comp_q
grep -f std_split/test-ids.txt $DATA/segments | grep -f $comp_q | awk -F'-' '{print $2}' | uniq > comp/compq-test-audiofiles.txt
rm $comp_q


# for each attribute on which we split, we have a directory in which the test directory is located.
# we now create the segments, wav.scp, text, and utt2spk; these are the necessary files. Afterwards, we flatten the directory structure, and relocate all files to the `asr_*/data` dir
# Here the test sets can be prepared and used by kaldi for testing on these attributes.
for subset in gender/* age/* nativity/* comp/*
do
	dir=$(echo $subset | cut -d '-' -f 1,2)
        #	| cut -f 2 -d '/'
        rm -r $ORIGDIR/$dir
	mkdir $dir
	grep -Fw -f $subset $DATA/segments > $dir/segments
        # wav identifiers are dependent on  these IDs
        cat $dir/segments | awk '{print $2}' | sort | uniq > wav_prep
        grep -Fw -f wav_prep $DATA/wav.scp > $dir/wav.scp
        rm wav_prep
	grep -Fw -f $subset $DATA/text > $dir/text
        grep -Fw -f $subset $DATA/utt2spk > $dir/utt2spk

	rm $subset

	flat_dir=$(echo $dir | cut -f 2 -d '/')
	cp -r $dir $ORIGDIR/../data/
	echo $dir

	echo -e "created test set for $dir\nNumber of segments: $(cat $dir/segments | wc -l)\n\n"
done


echo  -e "${GREEN}Data prep DONE!${NC}"
