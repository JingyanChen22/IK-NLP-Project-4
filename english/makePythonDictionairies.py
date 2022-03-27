#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import collections.abc
TODO: READING POS TAGS
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
example of lemmaDict, key 'hebben':
{
 'regular': False,
 'PRS': {'SG': {1:'heb', 2:'hebt',3:'heeft'}, 'PL': 'liggen'},
 'PST': {'SG': {1:'had', 2:'had',3:'had'}, 'PL': 'hadden'}
}

have	had	V;PST
have	had	V;V.PTCP;PST
have	has	V;3;SG;PRS
have	have	V;NFIN
have	having	V;V.PTCP;PRS

live	lived	V;PST
live	lived	V;V.PTCP;PST
live	lives	V;3;SG;PRS
live	live	V;NFIN
live	living	V;V.PTCP;PRS


V;IND;PRS;1;SG  heb
V;IND;PRS;2;SG  hebt
V;IND;PRS;3;SG  heeft

V;IND;PRS;PL    hebben

V;IND;PST;1;SG  had
V;IND;PST;2;SG  had
V;IND;PST;3;SG  had

V;IND;PST;PL    hadden
'''
with open('unimorph-wordforms.txt') as reader:
    for line in reader:
        currentWordForm = line.split('\t')
        lemma = currentWordForm[0].strip()  # abonneren
        word = currentWordForm[1].strip()   # abonneert
        pos = currentWordForm[2].split(';') # V;IND;PRS;3;SG
        if pos[0] == 'V' and pos[1] == 'IND':
            tense = pos[2]
            number = pos[-1].strip()
            if number == 'SG':
                person = pos[3]
                if tense == 'PST':
                    if word[-2:] == 'te' or word[-2:] == 'de':
                        regular = True
                    else:
                        regular = False
                    newEntry = {lemma : {'regular': regular, tense: {'SG': {person : word}}}}
                else:
                    newEntry = {lemma : {tense: {'SG': {person : word}}}}
                update(lemmaDict, newEntry)
            elif number == 'PL':
                newEntry = {lemma : {tense: {'PL': word}}}
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
        if pos[0] == 'V' and pos[1] == 'IND':
            tense = pos[2]
            number = pos[-1].strip()
            if number == 'SG':
                person = pos[3]
                if tense == 'PRS':
                    PRS = word
                    PST = lemmaDict[lemma]['PST']['SG'][person]
                elif tense == 'PST':
                    PST = word
                    PRS = lemmaDict[lemma]['PRS']['SG'][person]
            else: # number == 'PL'
                if tense == 'PRS':
                    PRS = word
                    PST = lemmaDict[lemma]['PST']['PL']
                elif tense == 'PST':
                    PST = word
                    PRS = lemmaDict[lemma]['PRS']['PL']

            try:
                newOrthoEntry = {PRS: {'pron': pron[PRS], 'regular': lemmaDict[lemma]['regular'], 'past': {'pron': pron[PST], 'ortho': PST}}}
                newPhonEntry = {pron[PRS]: {'ortho': PRS, 'regular': lemmaDict[lemma]['regular'], 'past': {'pron': pron[PST], 'ortho': PST}}}
                update(phonDict, newPhonEntry)
                update(orthoDict, newOrthoEntry)
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
