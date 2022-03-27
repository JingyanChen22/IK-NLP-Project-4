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
example of lemmaDict, key 'hebben':
{
 'regular': False,
 'PRS': {'SG': {1:'heb', 2:'hebt',3:'heeft'}, 'PL': 'liggen'},
 'PST': {'SG': {1:'had', 2:'had',3:'had'}, 'PL': 'hadden'}
}

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
            try:
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

if __name__ == "__main__":
    createDatasets('pron')
    print("Let me show you some examples")
    
    print("\nGet the pronouncation of the Dutch word 'lays':")
    print("pron['ligt'] -", pron['ligt']) # 'l I x t'
    


    print("\n\n\nShow the LEMMA 'hebben' (to have)")
    print("lemmaDict['hebben'] -", lemmaDict['hebben'])
    # {
    #  'regular': False,
    #  'PRS': {'SG': {1:'heb', 2:'hebt',3:'heeft'}, 'PL': 'liggen'},
    #  'PST': {'SG': {1:'had', 2:'had',3:'had'}, 'PL': 'hadden'}
    # }

    print("\nShow me the past tense 2sg of the LEMMA 'hebben' (to have)") # = 'had'
    print("lemmaDict['hebben']['PST']['SG'][2] -", lemmaDict['hebben']['PST']['SG']['2']) # 'had'


    
    print("\n\n\nShow the WORDFORM 'zwijgt' (to be silence):")
    print("orthoDict['zwijgt'] -", orthoDict['zwijgt'])
    # {'pron': 'z w K x t', 'regular': False, 'past': {'pron': 'z w e x', 'ortho': 'zweeg'}}
    
    print("\nShow me the past tense 'zwijgT' (keeps silence)")  # = 'zweeg' (kept silence)
    print("orthoDict['zwijgt']['past']['ortho'] - ", orthoDict['zwijgt']['past']['ortho']) # 'zweeg' (kept silence)

    print("\nShow me the past tense 'zwijgEN' (keep silence)")  # = 'zweeg' (kept silence)
    print("orthoDict['zwijgen']['past']['ortho'] - ", orthoDict['zwijgen']['past']['ortho']) # 'zwegen' (kept silence)

    print("\n'Merkt' belongs to the REGULAR verb 'merken', so orthoDict['merkt']['regular'] is", orthoDict['merkt']['regular']) # True



    print("\n\n\nShow the WORDFORM 'z w K x t' (ki:p sAilEns):") # = 'z w e x' (kEpt sAilEns)
    print("phonDict['z w K x t'] -", phonDict['z w K x t'])
    # {'pron': 'z w K x t', 'regular': False, 'past': {'pron': 'z w e x', 'ortho': 'zweeg'}}

    print("\nShow me the past tense 'zwijgt' (keeps silence)") # 'z w e x' (kEpt sAilEns)
    print("phonDict['z w K x t']['past']['pron'] - ", phonDict['z w K x t']['past']['pron']) # 'z w e x' (kEpt sAilEns)
   
    print(pron['slapen'])
    print("\n'Slapen' is a wordform of the IRREGULAR verb 'slapen', so phonDict['s l a p @']['regular'] is", phonDict['s l a p @']['regular']) # False
    
