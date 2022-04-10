# NLP-Modern-Neural-Networks-Meet-Linguistic-Theory
This is the group project for the course Natural Language Processing. 


## Description

This repository has two main folders: ```datasets``` and ```experiments```.  


* The ```datasets``` folder contains code for creating German, Dutch and English corpus.
* The ```experiments``` folder contains the experiment code, parameter.yaml file and replicable output.

### 1. Preparing the datasets
You can prepare all datasets by running ```sh ./createALLdatasets.sh``` from within the folder ```datasets```. For English, German and Dutch a list of all available lemma's with their wordforms is saved to ```[english|dutch|german]_bylemma_[orth|phon].txt```<p>
  After that, 6100 wordforms are chosen and saved to ```[src|tgt]_[train|test|valid].txt```
  
### 2. Running the experiments
The ```experiments``` folder contains the experiments that replicate the two experiments in the paper Kirov & Cotterell (2018), and also include experiments using new generated English, German and Dutch data. You can run the experiments by starting from ```experiment_1.ipynb``` for replication and ```experiments.ipynb``` for extension. 
