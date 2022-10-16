import os
import codecs

orth_path = 'datasets/english/english_orth'
merged_file = 'datasets/english/english_merged.txt'

    
merged = codecs.open(merged_file,'rb','utf-8')
sources = []
word_list =[]

for line in merged:
    
    parts = line.strip().split()
    
    lemma = parts[0]
    form = parts[1]
    lemma_phon = parts[2]
    form_phon = parts[3]
    reg = parts[4]
    sources.append(lemma)
    word_list.append({lemma: (form, lemma_phon, form_phon, reg)})
    

generated_merged = 'Experiments/cross_validation/english_merged_new.txt'
with open(generated_merged, 'a') as ff:
    for feature in sorted(os.listdir(orth_path)):
        orth_deeper_path = f'{orth_path}/{feature}'
        if 'src' in feature:
            src = codecs.open(orth_deeper_path, 'rb', 'utf-8')
            for line in src:
                word =''.join(line.split())
                if word in sources:
                    index = sources.index(word)
                    

                    word_form =word_list[index][word][0]
                    word_phon =word_list[index][word][1]
                    word_phon_form = word_list[index][word][2]
                    regu = word_list[index][word][3]

                    ff.write(f'{word}\t{word_form}\t{word_phon}\t{word_phon_form}\t{regu}\n')





