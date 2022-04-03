# -*- coding: utf-8 -*-
import codecs
# Python 2: import cPickle
import _pickle as cPickle
import random
random.seed(123)
from collections import defaultdict
import pandas as pd
import sys
import os 

language = sys.argv[1]    # [english|dutch|german]
phonORortho = sys.argv[2] # [phon|orth]

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
fin = codecs.open(language + '_bylemma_' + phonORortho + '.txt','rb','utf-8')

sources = []
targets = []
lowfreqSources = []
lowfreqTargets = []
#frequencies = []
numberOfLines = 0
numberOfWordforms = 0
for line in fin:
    parts = line.strip().split()
    freq = int(parts[1])
    prs = [item.split(';')[0] for item in parts[3:]]
    pst = [item.split(';')[1] for item in parts[3:]]
    
    numberOfLines += 1
    numberOfWordforms += len(prs)
    
    if freq >= 1:
        sources.append(' '.join(prs))
        targets.append(' '.join(pst))
    else:
        lowfreqSources.append(' '.join(prs))
        lowfreqTargets.append(' '.join(pst))
    #frequencies.append(int(freq))
fin.close()

meanNumberOfWordforms = numberOfWordforms/(len(sources)+len(lowfreqSources))
totalWordforms = 6108
totalLemmas = totalWordforms / meanNumberOfWordforms
lemmasStillNeeded = int(totalLemmas - len(sources))
lowfreqItemstoadd = random.choices(list(zip(lowfreqSources,lowfreqTargets)), k = lemmasStillNeeded)

pairs = list(zip(sources,targets)) + lowfreqItemstoadd
random.shuffle(pairs)

#split into train and test
train = pairs[:int(.8*len(pairs))]
valid = pairs[int(.8*len(pairs)):int(.9*len(pairs))]
test = pairs[int(.9*len(pairs)):]

#write the outputs
sList = []
tList = []
for s,t in train:
    s = s.split(' ')
    t = t.split(' ')
    sList.extend(s)
    tList.extend(t)
shuffledTrain = list(zip(sList,tList))
random.seed(123)
random.shuffle(shuffledTrain)
for s,t in shuffledTrain:
    s = s.replace(' ', '\n')
    t = t.replace(' ', '\n')
    s = " ".join(s)
    t = " ".join(t)
    fout_src_train.write(s + '\n')
    fout_tgt_train.write(t + '\n')

sList = []
tList = []
for s,t in valid:
    s = s.split(' ')
    t = t.split(' ')
    sList.extend(s)
    tList.extend(t)
shuffledValid = list(zip(sList,tList))
random.seed(123)
random.shuffle(shuffledValid)
for s,t in shuffledValid:
    s = s.replace(' ', '\n')
    t = t.replace(' ', '\n')
    s = " ".join(s)
    t = " ".join(t)
    fout_src_valid.write(s + '\n')
    fout_tgt_valid.write(t + '\n')

sList = []
tList = []
for s,t in test:
    s = s.split(' ')
    t = t.split(' ')
    sList.extend(s)
    tList.extend(t)
shuffledTest = list(zip(sList,tList))
random.seed(123)
random.shuffle(shuffledTest)
for s,t in shuffledTest:
    s = s.replace(' ', '\n')
    t = t.replace(' ', '\n')
    s = " ".join(s)
    t = " ".join(t)
    fout_src_test.write(s + '\n')
    fout_tgt_test.write(t + '\n')

fout_src_train.close()
fout_tgt_train.close()
fout_src_valid.close()
fout_tgt_valid.close()
fout_src_test.close()
fout_tgt_test.close()

print(int(len(pairs)*meanNumberOfWordforms), "wordforms are selected and spread across test/train/valid in the folder:", language + os.sep + folder)
