python dutch/createDutch_merged.py -1
python createDatasets.py dutch phon
python createDatasets.py dutch orth

python english/createEnglish_merged.py -1
python createDatasets.py english phon
python createDatasets.py english orth

python german/createGerman_merged.py -1
python createDatasets.py german phon
python createDatasets.py german orth
