python dutch/createDutch_merged.py
python createDatasets.py dutch phon
python createDatasets.py dutch orth

echo

python english/createEnglish_merged.py
python createDatasets.py english phon
python createDatasets.py english orth

echo

python german/createGerman_merged.py
python createDatasets.py german phon
python createDatasets.py german orth
