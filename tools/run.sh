#!/bin/bash
# Copyright 2015-2017   David Snyder
#                2015   Johns Hopkins University (Author: Daniel Garcia-Romero)
#                2015   Johns Hopkins University (Author: Daniel Povey)
# Apache 2.0.
#
# See README.txt for more info on data required.
# Results (EERs) are inline in comments below.



. cmd.sh
. path.sh
set -e
dataType=UBK
dataDir=../files_$dataType
mfccdir=../mfcc_$dataType
vaddir=../vad_$dataType

echo $dataType
echo $dataDir
echo $mfccdir
echo $vaddir


#: '
steps/make_mfcc.sh --mfcc-config conf/mfcc.conf --nj 4 --cmd "$train_cmd" \
  $dataDir exp/make_mfcc $mfccdir

sid/compute_vad_decision.sh --nj 4 --cmd "$train_cmd" \
  $dataDir exp/make_vad $vaddir
#'
