def convertToSeqData(itemDataFile,outFile=None): #whole itemset transaction is an event (sequence)
    if outFile is None:
        outFile = itemDataFile.replace('_util.txt','_s.txt')
    count  = 0
    with open(itemDataFile,"r") as f, open(outFile,"w") as out:
        for line in f:
            count+=1
            line = line.replace("\r", "").replace("\n", "")
            while line.endswith(' '):
                line = line.strip()
            parts = line.split(':')
            line_seq = parts[0]
            print(line)
            print(line_seq)
            line_seq = line_seq+' -1 -2\n'
            print('')
            out.write(line_seq)

    print('total',count)

convertToSeqData("chainstore_util.txt")