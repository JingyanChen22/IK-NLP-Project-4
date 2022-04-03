python dutch/createDutch_merged.py 0
python createDatasets.py dutch phon
python createDatasets.py dutch orth

echo

python english/createEnglish_merged.py 0
python createDatasets.py english phon
python createDatasets.py english orth

echo

python german/createGerman_merged.py 1
python createDatasets.py german phon
python createDatasets.py german orth
