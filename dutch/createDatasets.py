from makePythonDictionairies import createDatasets

orthoList = createDatasets('ortho')
print("\nThere are", len(orthoList), "orthographical wordpairs:")
print("   PRESENT:     PAST:    REGULAR:")
print(orthoList[:6], "and so on...") # print 6 examples

pronList = createDatasets('pron')
print("\nThere are", len(pronList), "phonetical wordpairs:")
print("   PRESENT:       PAST:       REGULAR:")
print(pronList[:6], "and so on...") # print 6 examples
