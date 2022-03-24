from makeWordListDutch import createDatasets

orthoList = createDatasets('ortho')
print(orthoList[:5]) # print 5 examples

pronList = createDatasets('pron')
print(pronList[:5]) # print 5 examples
