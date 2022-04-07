#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections.abc
from collections import defaultdict
import sys

import os 
os.chdir(os.path.dirname(os.path.realpath(__file__)))

"""
Examples:
    pron['ligt'] gives 'l I x t'
    English: pronounciation of the Dutch word 'lays'
    
    lemmaDict['hebben'] gives:
    {
     'regular': False,
     'PRS': {'SG': {1:'heb', 2:'hebt',3:'heeft'}, 'PL': 'liggen'},
     'PST': {'SG': {1:'had', 2:'had',3:'had'}, 'PL': 'hadden'}
    }
    - lemmaDict['hebben']['PST']['SG']['2'] gives 'had'
      English: past tense 2sg of 'to have' is 'had'
    
    orthoDict['zwijgt'] gives
    {'pron': 'z w K x t', 'regular': False, 'past': {'pron': 'z w e x', 'ortho': 'zweeg'}}
    - orthoDict['zwijgt']['past']['ortho'] gives 'zweeg'
      English: the past tense of 'keeps silence' is 'kept silence'
    - 'Merken' is a regular verb, so orthoDict['merkt']['regular'] gives 'True'

@author: Arjan
"""
# from https://stackoverflow.com/a/3233356
def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


### read pronounciation of all verbs into pronDict
pron = {}
freq = defaultdict(lambda:-1)
with open('EN-pron-freq.txt') as reader:
    for line in reader:
        currentWord = line.split('\t')
        pron[currentWord[0]] = currentWord[2].strip('\n')
        freq[currentWord[0]] = int(currentWord[1])

# we need a temporary dictionairy for the lemma's
lemmaDict = {} # or defaultdict(lambda:{'PRS': {'SG': {1:'<unk>', 2:'<unk>',3:'<unk>'}, 'PL': '<unk>'},'PST': {'SG': {1:'<unk>', 2:'<unk>',3:'<unk>'}, 'PL': '<unk>'}})
'''
example of lemmaDict, key 'have':
{
 'freq': 15
 'regular': False,
 'PRS': 'has',
 'PST': 'had',
 'NFIN': 'have'}
}


have	had	V;PST
have	has	V;3;SG;PRS
have	have	V;NFIN

live	lives	V;3;SG;PRS
live	live	V;NFIN
live	lived	V;PST

'''
with open('unimorph-wordforms.txt') as reader:
    for line in reader:
        currentWordForm = line.split('\t')
        lemma = currentWordForm[0].strip()  # abonneren
        word = currentWordForm[1].strip()   # abonneert
        pos = currentWordForm[2].strip() # V;IND;PRS;3;SG
        if pos[0] == 'V':
            if pos in ['V;3;SG;PRS', 'V;NFIN', 'V;PST']: # yes, add this item to lemmaDict
                tense = pos.split(';')[-1]
                if tense == 'PST':
                    # ending with 'ed', but still irregular are variants of bled, bred, led, fled, fed
                    if word in ('bled', 'bred', 'led', 'misled', 'fled', 'fed', 'breastfed', 'force-fed', 'bottle-fed', 'force-fed', 'bottle-fed'):
                        regular = 'irreg'
                    elif word[-2:] == 'ed':
                        regular = 'reg'
                    else:
                        regular = 'irreg'
                    newEntry = {lemma : {'regular': regular, 'PST': word}}
                else: # tense is prs or nfin
                    newEntry = {lemma : {tense: word}}
                update(lemmaDict, newEntry)
            if pos == 'V;NFIN': # check frequency of infinitive
                newEntry = {lemma : {'freq': freq[lemma]}}
                update(lemmaDict, newEntry)

orthoDict = {}
#example of Dutch key 'ligt': {'pron': 'lIxt'}, {'PST': {'pron' : 'lAx', 'ortho' : 'lag'}}
#example of non-extistent English key 'swims': {'pron': 'swIms'}, {'pst': {'pron' : 'swEm', 'ortho' : 'swam'}}
#so, orthoDict['swims']['pron'] gives: 'swIms'
with open('unimorph-wordforms.txt') as reader:
    for line in reader:
        currentWordForm = line.split('\t')  # example:
        lemma = currentWordForm[0].strip()  # abonneren
        word = currentWordForm[1].strip()   # abonneert
        pos = currentWordForm[2].strip() # V;IND;PRS;3;SG
        if pos in ['V;3;SG;PRS', 'V;NFIN']: # yes, add this item to phonDict/orthoDict
            tense = pos.split(';')[-1]
            if 'PST' in lemmaDict[lemma]:
                PRS = word
                PST = lemmaDict[lemma]['PST']

                try:
                    newOrthoEntry = {PRS: {'pron': pron[PRS], 'lemma': lemma, 'freq':freq[lemma], 'regular': lemmaDict[lemma]['regular'], 'past': {'pron': pron[PST], 'ortho': PST}}}
                    update(orthoDict, newOrthoEntry)
                except KeyError: # some words may not be in the pronounciation dictionairy
                    pass
 
def saveDataset(minfreq=-99):
    '''
    with open('english_merged.txt', 'w') as file:
        for k in orthoDict:
            if orthoDict[k]['freq'] >= int(minfreq):
                # the format of english_merged.txt of the original experiment:
                file.write(k + '\t' + orthoDict[k]['past']['ortho'] + '\t' + orthoDict[k]['pron'] + '\t' + orthoDict[k]['past']['pron'] + '\t' + orthoDict[k]['regular'] + '\n')

    print("Saved to english_merged.txt")
    '''
    with open('english_bylemma_orth.txt', 'w') as orthFile, open('english_bylemma_phon.txt', 'w') as phonFile, open('english_merged.txt', 'w') as mergedFile:
        # example of lemmaDict, key 'have':
        # {
        #  'freq': 15
        #  'regular': False,
        #  'PRS': 'has',
        #  'PST': 'had',
        #  'NFIN': 'have'}
        # }

        wordformcount = 0
        for lemma in lemmaDict:
            try:
                prspron = nfinpron = prsorth = nfinorth = ''
                if lemmaDict[lemma]['freq'] >= int(minfreq):
                    try:
                        if freq[lemmaDict[lemma]['PRS']] > int(minfreq):
                            prspron = '\t' +  pron[lemmaDict[lemma]['PRS']]  + ';' + pron[lemmaDict[lemma]['PST']]
                            prsorth = '\t' + lemmaDict[lemma]['PRS']  + ';' + lemmaDict[lemma]['PST']
                            wordformcount += 1
                    except KeyError:
                        prspron = ''
                        prsorth = ''
                    try:
                        if freq[lemmaDict[lemma]['NFIN']] > int(minfreq):
                            nfinpron = '\t' + pron[lemmaDict[lemma]['NFIN']] + ';' + pron[lemmaDict[lemma]['PST']]
                            nfinorth = '\t' + lemmaDict[lemma]['NFIN'] + ';' + lemmaDict[lemma]['PST']
                            wordformcount += 1
                    except KeyError:
                        nfinpron = ''
                        nfinorth = ''

                    if prspron + nfinpron != '':
                        phonFile.write(pron[lemma] + '\t' + str(lemmaDict[lemma]['freq']) + '\t' + lemmaDict[lemma]['regular'] +
                                   prspron + nfinpron + '\n')
                        orthFile.write(lemma + '\t' + str(lemmaDict[lemma]['freq']) + '\t' + lemmaDict[lemma]['regular'] +
                                   prsorth + nfinorth + '\n')
                        
                        
                        # creating the old-fashioned Pinker english_merged.txt
                        try: # 'PRS'
                            mergedFile.write(lemmaDict[lemma]['PRS'] + '\t' + lemmaDict[lemma]['PST']
                                             + '\t' + pron[lemmaDict[lemma]['PRS']]  + '\t' + pron[lemmaDict[lemma]['PST']]
                                             + '\t' + lemmaDict[lemma]['regular'] + '\n')
                        except KeyError:
                            pass
                        try: # 'NFIN'
                            mergedFile.write(lemmaDict[lemma]['NFIN'] + '\t' + lemmaDict[lemma]['PST']
                                             + '\t' + pron[lemmaDict[lemma]['NFIN']]  + '\t' + pron[lemmaDict[lemma]['PST']]
                                             + '\t' + lemmaDict[lemma]['regular'] + '\n')
                        except KeyError:
                            pass
                        
            except KeyError:
                pass

        print(wordformcount, "wordforms saved to english_bylemma_orth.txt and to english_bylemma_phon.txt")


if __name__ == "__main__":
    try:
        saveDataset(sys.argv[1])
    except IndexError:
        saveDataset(-1)
