
from PrepareDataset import SeqDB
from UtilityTechniques.ProbabilityWeightAssign import ProbabilityAssign, checkCSV

import os,errno

if __name__=='__main__':



    datasets = [
                "SIGN.txt"
                ,"LEVIATHAN.txt"
                # ,"BIBLE.txt"
                # ,"FIFA.txt"
                # ,"accidents_seq.txt"
                ,"BMS2.txt"
                 ]

    convertSize = [
                    0,
                   1000
                   # ,1500
                   # ,300
                   # ,0
                   ,400
                   ]

    title = "Serial,Dataset_Name,dbSize,avglen,maxLen,minLen," \
                "totalDistItem,avgDistItem,maxDistItem,minDistItem," \
                "avgEvPerSeq,avgEvLen,maxEvLen," \
                "suggested_MinSup"

    for sameEventProb in [50, 80]:

        print("______________________Same Event Probability______________________",sameEventProb)

        fname = "../Files" + "/datasetStudy"+ str(sameEventProb) +".csv"
        if not os.path.exists(os.path.dirname(fname)):
            try:
                os.makedirs(os.path.dirname(fname))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        f = open(fname, "w+")
        # f_out = open("info.txt","w+")
        f.write(title)
        f.write("\n")
        f.close()

        for i in range(0,datasets.__len__()):

            f = open(fname,"a")

            sdb = SeqDB.SeqDatabase(datasets[i])
            sdb.describeDataset()

            newFile = sdb.convertFile(sameEventProb, convertSize[i])
            print(newFile)

            newSDB = SeqDB.SeqDatabase(newFile)
            r = newSDB.describeDataset()

            #probabilty assign
            probs = '../Files/probs.csv'
            read = newFile
            with_prob = newFile.replace(".txt", "p.txt")
            # ProbabilityAssign(read, probs, with_prob).Assigning()
            PA = ProbabilityAssign()
            PA.probsFile = open(probs, 'r')
            PA.whereToWrite = open(with_prob, 'w')
            PA.dataFile = open(read, 'r')
            PA.Assigning()

            numPartitions = newSDB.autoPartition(with_prob)

            f.write(r)
            f.write("\n")
            f.close()
