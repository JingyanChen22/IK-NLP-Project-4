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
with open('NL-pron-freq.txt') as reader:
    for line in reader:
        currentWord = line.split('\t')
        pron[currentWord[0]] = currentWord[2].strip('\n')
        freq[currentWord[0]] = int(currentWord[1])

# we need a temporary dictionairy for the lemma's
lemmaDict = {} # or defaultdict(lambda:{'PRS': {'SG': {1:'<unk>', 2:'<unk>',3:'<unk>'}, 'PL': '<unk>'},'PST': {'SG': {1:'<unk>', 2:'<unk>',3:'<unk>'}, 'PL': '<unk>'}})
'''
example of lemmaDict, key 'hebben':
{
 'freq': 15
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
                        regular = 'reg'
                    else:
                        regular = 'irreg'
                    newEntry = {lemma : {'regular': regular, tense: {'SG': {person : word}}}}
                else:
                    newEntry = {lemma : {tense: {'SG': {person : word}}}}
                update(lemmaDict, newEntry)
            elif number == 'PL':
                newEntry = {lemma : {'freq': freq[lemma], tense: {'PL': word}}}
                update(lemmaDict, newEntry)

'''
orthoDict = {}
#example of Dutch key 'ligt': {'pron': 'lIxt'}, {'PST': {'pron' : 'lAx', 'ortho' : 'lag'}}
#example of non-extistent English key 'swims': {'pron': 'swIms'}, {'pst': {'pron' : 'swEm', 'ortho' : 'swam'}}
#so, orthoDict['swims']['pron'] gives: 'swIms'
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
                newOrthoEntry = {PRS: {'pron': pron[PRS], 'freq': freq[lemma], 'lemma': lemma, 'regular': lemmaDict[lemma]['regular'], 'past': {'pron': pron[PST], 'ortho': PST}}}
                update(orthoDict, newOrthoEntry)
                
            except KeyError: # some words may not be in the pronounciation dictionairy
                pass
            #update(orthoDict, newOrthoEntry)
'''

def saveDataset(minfreq=-99):
    '''
    with open('dutch_merged.txt', 'w') as file:
        for k in orthoDict:
            if orthoDict[k]['freq'] >= int(minfreq):
                # the format of english_merged.txt of the original experiment:
                file.write(k + '\t' + orthoDict[k]['past']['ortho'] + '\t' + orthoDict[k]['pron'] + '\t' + orthoDict[k]['past']['pron'] + '\t' + orthoDict[k]['regular'] + '\n')
    print("Saved to dutch_merged.txt")
    '''

    with open('dutch_bylemma_orth.txt', 'w') as orthFile, open('dutch_bylemma_phon.txt', 'w') as phonFile:
        # {
        #  'freq': 15
        #  'regular': False,
        #  'PRS': {'SG': {1:'heb', 2:'hebt',3:'heeft'}, 'PL': 'liggen'},
        #  'PST': {'SG': {1:'had', 2:'had',3:'had'}, 'PL': 'hadden'}
        # }

        wordformcount = 0
        for lemma in lemmaDict:
            try:
                sg1pron = sg2pron = sg3pron = plpron = ''
                sg1orth = sg2orth = sg3orth = plorth = ''
                try:
                    if freq[lemmaDict[lemma]['PRS']['SG']['1']] > int(minfreq):
                        sg1pron = '\t' + pron[lemmaDict[lemma]['PRS']['SG']['1']] + ';' + pron[lemmaDict[lemma]['PST']['SG']['1']]
                        sg1orth = '\t' + lemmaDict[lemma]['PRS']['SG']['1'] + ';' + lemmaDict[lemma]['PST']['SG']['1']
                        wordformcount += 1
                except KeyError:
                    sg1pron = ''
                    sg1orth = ''
                try:
                    if freq[lemmaDict[lemma]['PRS']['SG']['2']] > int(minfreq):
                        sg2pron = '\t' + pron[lemmaDict[lemma]['PRS']['SG']['2']] + ';' + pron[lemmaDict[lemma]['PST']['SG']['2']]
                        sg2orth = '\t' + lemmaDict[lemma]['PRS']['SG']['2'] + ';' + lemmaDict[lemma]['PST']['SG']['2']
                        wordformcount += 1
                except KeyError:
                    sg2pron = ''
                    sg2orth = ''
                try:
                    if freq[lemmaDict[lemma]['PRS']['SG']['3']] > int(minfreq):
                        sg3pron = '\t' + pron[lemmaDict[lemma]['PRS']['SG']['3']] + ';' + pron[lemmaDict[lemma]['PST']['SG']['3']]
                        sg3orth = '\t' + lemmaDict[lemma]['PRS']['SG']['3'] + ';' + lemmaDict[lemma]['PST']['SG']['3']
                        wordformcount += 1
                except KeyError:
                    sg3pron = ''
                    sg3orth = ''
                if sg2orth == sg3orth: # jij loopt/ hij loopt
                    sg3orth = ''
                    sg3pron = ''
                    if sg2orth != '':
                        wordformcount -= 1
                try:
                    if freq[lemmaDict[lemma]['PRS']['PL']] > int(minfreq):
                        plpron = '\t' + pron[lemmaDict[lemma]['PRS']['PL']]      + ';' + pron[lemmaDict[lemma]['PST']['PL']]
                        plorth = '\t' + lemmaDict[lemma]['PRS']['PL']      + ';' + lemmaDict[lemma]['PST']['PL']
                        wordformcount += 1
                except KeyError:
                    plpron = ''
                    plorth = ''
                    
                if sg1pron + sg2pron + sg3pron + plpron != '':
                    phonFile.write(pron[lemma] + '\t' + str(lemmaDict[lemma]['freq']) + '\t' + lemmaDict[lemma]['regular'] +
                               sg1pron + sg2pron + sg3pron + plpron + '\n')
                    orthFile.write(lemma + '\t' + str(lemmaDict[lemma]['freq']) + '\t' + lemmaDict[lemma]['regular'] +
                               sg1orth + sg2orth + sg3orth + plorth + '\n')

            except KeyError:
                pass
            
        print(wordformcount, "wordforms saved to dutch_bylemma_orth.txt and to dutch_bylemma_phon.txt")

def examples():
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

    
    '''
    print("\n\n\nShow the WORDFORM 'zwijgt' (to be silence):")
    print("orthoDict['zwijgt'] -", orthoDict['zwijgt'])
    
    print("\nShow me the past tense 'zwijgT' (keeps silence)")  # = 'zweeg' (kept silence)
    print("orthoDict['zwijgt']['past']['ortho'] - ", orthoDict['zwijgt']['past']['ortho']) # 'zweeg' (kept silence)

    print("\nShow me the past tense 'zwijgEN' (keep silence)")  # = 'zweeg' (kept silence)
    print("orthoDict['zwijgen']['past']['ortho'] - ", orthoDict['zwijgen']['past']['ortho']) # 'zwegen' (kept silence)

    print("\n'Merkt' belongs to the REGULAR verb 'merken', so orthoDict['merkt']['regular'] is", orthoDict['merkt']['regular']) # True
    print("'Slapen' belongs to the IRREGULAR verb 'slapen', so orthoDict['slapen']['regular'] is", orthoDict['slapen']['regular']) # False
    '''    



if __name__ == "__main__":
    try:
        saveDataset(sys.argv[1])
    except IndexError:
        saveDataset(-1)
