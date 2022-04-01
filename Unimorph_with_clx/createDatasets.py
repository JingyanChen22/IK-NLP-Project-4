# -*- coding: utf-8 -*-
import codecs
# Python 2: import cPickle
import _pickle as cPickle
import random
from collections import defaultdict
import pandas as pd
import sys
import os 

try:
    language = sys.argv[1]
except IndexError:
    print("Command line argument required: [english|dutch|german]")

try:
    phonORortho = sys.argv[2]
except IndexError:
    print("Command line argument required: [phon|orth]")


os.chdir(os.path.dirname(os.path.realpath(__file__)) + os.sep + language)

#set up output file
folder = language + '_' + phonORortho + os.sep
fout_src_train = codecs.open(folder + 'src_train.txt','wb','utf-8')
fout_tgt_train = codecs.open(folder + 'tgt_train.txt','wb','utf-8')
fout_src_valid = codecs.open(folder + 'src_valid.txt','wb','utf-8')
fout_tgt_valid = codecs.open(folder + 'tgt_valid.txt','wb','utf-8')
fout_src_test = codecs.open(folder + 'src_test.txt','wb','utf-8')
fout_tgt_test = codecs.open(folder + 'tgt_test.txt','wb','utf-8')

#read in  data
fin = codecs.open(language + '_merged.txt','rb','utf-8')

sources = []
targets = []

if phonORortho == 'phon':
    lemmaPart = 2
    formPart = 3
elif phonORortho == 'orth':
    lemmaPart = 0
    formPart = 1
for line in fin:
    parts = line.strip().split()
    lemma = parts[lemmaPart]
    form = parts[formPart]
    sources.append(' '.join(lemma))
    targets.append(' '.join(form))
fin.close()

# as advised on https://stackoverflow.com/questions/31011631/python-2-3-object-of-type-zip-has-no-len
# I changed zip( into list(zip((
pairs = list(zip(sources,targets))
random.seed(123)
random.shuffle(pairs)

#split into train and test
train = pairs[:int(.8*len(pairs))]
valid = pairs[int(.8*len(pairs)):int(.9*len(pairs))]
test = pairs[int(.9*len(pairs)):]

#write the outputs
for s,t in train:
    fout_src_train.write(s + '\n')
    fout_tgt_train.write(t + '\n')

for s,t in valid:
    fout_src_valid.write(s + '\n')
    fout_tgt_valid.write(t + '\n')

for s,t in test:
    fout_src_test.write(s + '\n')
    fout_tgt_test.write(t + '\n')



fout_src_train.close()
fout_tgt_train.close()
fout_src_valid.close()
fout_tgt_valid.close()
fout_src_test.close()
fout_tgt_test.close()

print('Train/test/valid saved to', language + os.sep + folder)
