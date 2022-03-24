from makeWordListDutch import createDatasets

orthoList = createDatasets('ortho')
print(orthoList[:6]) # print 5 examples

pronList = createDatasets('pron')
print(pronList[:6]) # print 5 examples

print("\nThere are", len(orthoList), "orthographical wordpairs.")
print("\nThere are", len(pronList), "phonetical wordpairs.")