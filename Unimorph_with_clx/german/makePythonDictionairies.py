#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections.abc
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
    
    pronDict['z w K x t'] gives
    {'pron': 'z w K x t', 'regular': False, 'past': {'pron': 'z w e x', 'ortho': 'zweeg'}}
    - pronDict['z w K x t']['past']['pron'] gives 'z w e x'
      English: the past tense of 'ki:p sAilEns' is 'kEpt sAilEns'
    - 'Slapen' is a regular verb, so orthoDict['s l a : p']['regular'] gives 'False'

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
pron = {} # or defaultdict(lambda:"<unk>")
with open('presentTenseClx.txt') as reader:
    for line in reader:
        currentWord = line.split('\t')
        pron[currentWord[0]] = currentWord[1]

with open('pastTenseClx.txt') as reader:
    for line in reader:
        currentWord = line.split('\t')
        pron[currentWord[0]] = currentWord[1]


# we need a temporary dictionairy for the lemma's
lemmaDict = {} # or defaultdict(lambda:{'PRS': {'SG': {1:'<unk>', 2:'<unk>',3:'<unk>'}, 'PL': '<unk>'},'PST': {'SG': {1:'<unk>', 2:'<unk>',3:'<unk>'}, 'PL': '<unk>'}})
'''
POS-tags to ignore:
    machen	machen	V;SBJV;PRS;1;PL
    machen	machen	V;SBJV;PRS;3;PL
    machen	mache	V;SBJV;PRS;1;SG
    machen	mache	V;SBJV;PRS;3;SG
    machen	machest	V;SBJV;PRS;2;SG
    machen	machet	V;SBJV;PRS;2;PL
    machen	mach	V;IMP;2;SG
    machen	machten	V;SBJV;PST;1;PL
    machen	machten	V;SBJV;PST;3;PL
    machen	machte	V;SBJV;PST;1;SG
    machen	machte	V;SBJV;PST;3;SG
    machen	machtest	V;SBJV;PST;2;SG
    machen	machtet	V;SBJV;PST;2;PL
    machen	macht	V;IMP;2;PL
    machen	gemacht	V.PTCP;PST
    machen	machend	V.PTCP;PRS
    machen	machen	V;NFIN


example of lemmaDict, key 'machen':
{
 'regular': False,
 'PRS': {'SG': {1:'mache', 2:'machst',3:'macht'}, 'PL': {1:'machen', 2:'macht', 3:'machen'}},
 'PST': {'SG': {1:'machte', 2:'machtest',3:'machte'}, 'PL': {1:'machten', 2:'machtet', 3:'machten'}}
}

machen	mache	V;IND;PRS;1;SG
machen	machst	V;IND;PRS;2;SG
machen	macht	V;IND;PRS;3;SG


machen	machen	V;IND;PRS;1;PL
machen	macht	V;IND;PRS;2;PL
machen	machen	V;IND;PRS;3;PL

machen	machte	V;IND;PST;1;SG
machen	machtest	V;IND;PST;2;SG
machen	machte	V;IND;PST;3;SG

machen	machten	V;IND;PST;1;PL
machen	machtet	V;IND;PST;2;PL
machen	machten	V;IND;PST;3;PL
'''
with open('unimorph-wordforms.txt') as reader:
    for line in reader:
        currentWordForm = line.split('\t')
        lemma = currentWordForm[0].strip()  # abonneren
        word = currentWordForm[1].strip()   # abonneert
        pos = currentWordForm[2].split(';') # V;IND;PRS;3;SG
        if pos[0] == 'V' and pos[1] == 'IND':
            tense = pos[2].strip()
            person = pos[3].strip()
            number = pos[4].strip()
            newEntry = {lemma : {tense: {number: {person: word}}}}
            update(lemmaDict, newEntry)
            if tense == 'PST' and person in ['1','3'] and number == 'SG': # machTE, so regular
                if word[-2:] == 'te':
                    regular = True
                else:
                    regular = False
                newEntry = {lemma : {'regular': regular}}
                update(lemmaDict, newEntry)

### create two dictionaries
orthoDict = {}
#example of Dutch key 'ligt': {'pron': 'lIxt'}, {'PST': {'pron' : 'lAx', 'ortho' : 'lag'}}
#example of non-extistent English key 'swims': {'pron': 'swIms'}, {'pst': {'pron' : 'swEm', 'ortho' : 'swam'}}
#so, orthoDict['swims']['pron'] gives: 'swIms'

phonDict = {}
#example of Dutch key 'lIxt': {'ortho': 'ligt'}, {'past': {'pron' : 'lAx', 'ortho' : 'lag'}}
#example of non-existent English key 'swIms': {'ortho': 'swIms'}, {'PST': {'pron' : 'swEm', 'ortho' : 'swam'}}
#so, phonDict['swIms']['past']['ortho'] gives: 'swam'

with open('unimorph-wordforms.txt') as reader:
    for line in reader:
        currentWordForm = line.split('\t')  # example:
        lemma = currentWordForm[0].strip()  # abonneren
        word = currentWordForm[1].strip()   # abonneert
        pos = currentWordForm[2].split(';') # V;IND;PRS;3;SG
        if pos[0] == 'V' and pos[1] == 'IND' and pos[2] == 'PRS':
            person = pos[3].strip()
            number = pos[4].strip()
            try:
                PRS = word
                PST = lemmaDict[lemma]['PST'][number][person]

                newOrthoEntry = {PRS: {'regular': lemmaDict[lemma]['regular'], 'past': {'ortho': PST}}}
                update(orthoDict, newOrthoEntry)

                newOrthoEntry = {PRS: {'pron': pron[PRS], 'regular': lemmaDict[lemma]['regular'], 'past': {'pron': pron[PST], 'ortho': PST}}}
                update(orthoDict, newOrthoEntry)

                newPhonEntry = {pron[PRS]: {'ortho': PRS, 'regular': lemmaDict[lemma]['regular'], 'past': {'pron': pron[PST], 'ortho': PST}}}
                update(phonDict, newPhonEntry)     
            except KeyError: # some words may not be in the pronounciation dictionairy
                pass                          
            
def createDatasets(kindOfDataSet):
    dataset = []
    if kindOfDataSet == 'ortho':
        dict = orthoDict
    elif kindOfDataSet == 'pron':
        dict = phonDict
        
    for word in dict:
        dataset.append((word, dict[word]['past'][kindOfDataSet], dict[word]['regular']))
    return dataset
