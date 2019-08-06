import math,random
import os
import errno


class SeqDatabase:

    datasetID = 0 #classVariable, shared to all instances

    def __init__(self, inputFileName = None):
        SeqDatabase.datasetID+= 0.5
        # SeqDatabase.datasetCount = SeqDatabase.datasetCount // 2
        self.seqCount = 0
        self.totalDistItem = 0
        self.maxEventLen = 0
        self.itemRepo = []
        self.seqLengths = []
        self.numEvents = []
        self.avgEventLengthsInSeqs = []
        self.numDistItems = []

        if inputFileName is None:
            self.inputFile = input("Enter File Name: ")
        else:
            self.inputFile = inputFileName

        self.datasetName = ""
        if self.inputFile.endswith(".txt"):
            self.datasetName = self.inputFile[:-4]

        self.countingThings(self.inputFile)

    def countingThings(self, inFile):

        with open(inFile,"r") as f:
            for line in f:
                line = line.replace("-2","").replace("\r","").replace("\n","")
                if line=="":
                    continue

                self.seqCount += 1
                events = line.split("-1")
                localDistItems = []
                eLengths = []
                for e in events:
                    if e==" " or e=="":
                        break
                    e = e.strip()
                    eitems = e.split(" ")
                    eLen = 0
                    for ei in eitems:
                        eLen+=1
                        if ei not in self.itemRepo:
                            self.itemRepo.append(ei)
                        if ei not in localDistItems:
                            localDistItems.append(ei)
                    eLengths.append(eLen)
                    if eLen>self.maxEventLen:
                        self.maxEventLen = eLen


                self.seqLengths.append(sum(eLengths))
                self.numEvents.append(eLengths.__len__())
                self.avgEventLengthsInSeqs.append(sum(eLengths)/(eLengths.__len__()*1.0))
                self.numDistItems.append(localDistItems.__len__())

        self.totalDistItem = self.itemRepo.__len__()
        self.seqCount = self.seqLengths.__len__()
        self.avgSeqLen = sum(self.seqLengths) / (1.0 * self.seqCount)
        self.avgEventsPerSeq = sum(self.numEvents) / (1.0 * self.seqCount)
        self.avgEventLen = sum(self.avgEventLengthsInSeqs) / (1.0 * self.seqCount)
        self.avgDistItems = sum(self.numDistItems)/(1.0* self.seqCount)

    def convertFile(self,sameEventProbability, convertSize = None):

        def groupItems():

            convertedItems = {}
            # groupSize = int(input("Enter ItemGroup Size: "))
            if convertSize is None:
                totalGrp = int(input("Enter Converted Itemset Size (0 for no_change): "))
            else:
                totalGrp = convertSize

            # totalGrp = math.floor(self.totalDistItem/groupSize*1.0)
            if totalGrp == 0:
                for i in self.itemRepo:
                    convertedItems[i] = i
                return convertedItems

            for i in self.itemRepo:
                # groupID = math.ceil(int(i) * 1.0 / groupSize)
                groupID = hash(i) % totalGrp + 1
                # groupID = math.ceil(random.uniform(1,totalGrp))
                convertedItems[i] = groupID

            # print(convertedItems)
            return convertedItems

        convertedItems = groupItems()

        # outFile = input("Output file name (grouped, multi-length events) : ")

        outFilename = self.datasetName+"_s.txt"
        fileLocation = "../Files/"+self.datasetName+str(sameEventProbability)+"/"+outFilename
        if not os.path.exists(os.path.dirname(fileLocation)):
            try:
                os.makedirs(os.path.dirname(fileLocation))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(self.inputFile,"r") as f, open(fileLocation,"w+") as out:
            for line in f:
                line = line.replace("\r", "").replace("\n", "")
                if line == "":
                    continue
                parts = line.split(" ")
                partsNew = []
                currEvent = []

                for ei in parts:
                    # print(a)
                    if ei == "-1":
                        p = random.randint(1, 100)
                        # print(p)
                        if p > sameEventProbability:
                            #new event
                            partsNew.append(ei.__str__())
                            currEvent.clear()
                    else:
                        if ei=="-2":
                            partsNew.append(ei)
                            continue
                        eii = convertedItems.get(ei)
                        if eii not in currEvent:
                            currEvent.append(eii)
                            partsNew.append(eii.__str__())
                        else: # duplicate item in current event, so start new event from here
                            partsNew.append("-1")
                            partsNew.append(eii.__str__())
                            currEvent.clear()
                            currEvent.append(eii)

                line = " ".join(partsNew)
                out.write(line)
                out.write("\n")

        return fileLocation


    def autoPartition(self,inFile,_outFileTitle=None):

        numPartitions = []

        dns = self.datasetName.split("/")
        dn = '../Files/'+dns[2]
        # dn = dns[len(dns)-1]
        # if dn.endswith(".txt"):
        #     dn = dn.replace(".txt","")

        if _outFileTitle is None:
            _outFileTitle = dns[2] # dataset name
            # _outFileTitle = input("Enter Title of the  output files: ").__str__().strip()

        types = ['v0','v1','v2','v3']

        def getIncSize(type,dbSize):
            r = dbSize
            if type=="v0" or type=="v2": #small inc
                low = math.floor(dbSize*0.05)
                high = math.floor(dbSize*0.10)
                r = int(random.randrange(low,high))
            else: #large inc
                low = math.floor(dbSize * 0.30)
                high = math.floor(dbSize * 0.60)
                r = int(random.randrange(low, high))
            return r

        for type in types:
            f = open(inFile, "r")
            # outFileTitle = dn+"/"+type+"/"+_outFileTitle+"_"+type
            outFileTitle = dn + "/" + type + "/" + _outFileTitle

            # p0_size = self.seqCount
            print("__________For Type__________"+type)

            if type=="v0" or type=="v1": #small p_0
                p0_size = math.floor(self.seqCount * 0.7) #50% of total uSDB
            else: #small p_0
                p0_size = math.floor(self.seqCount * 0.8)

            print("Initial Size (p_0): "+p0_size.__str__())

            outFileName = outFileTitle + "_p0.txt"

            if not os.path.exists(os.path.dirname(outFileName)):
                try:
                    os.makedirs(os.path.dirname(outFileName))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            out = open(outFileName, "w+")
            for lines in range(0, p0_size):
                seq = f.readline()
                out.write(seq)
            out.close()

            rem_size = self.seqCount - p0_size
            incCount = 0
            while rem_size>0:
                incCount+=1
                inc_size = min(getIncSize(type,p0_size),rem_size)
                rem_size -= inc_size
                if rem_size<0.03*p0_size:
                    inc_size+=rem_size
                    rem_size = 0

                print("p_"+incCount.__str__()+": "+inc_size.__str__())
                outFileName = outFileTitle+"_p"+incCount.__str__()+".txt"
                out = open(outFileName,"w+")
                for lines in range(0, inc_size):
                    seq = f.readline()
                    out.write(seq)
                out.close()
            numPartitions.append(incCount)

            f.close()
            print("#_______________________________________________#")


        return numPartitions

    def describeDataset(self):

        def suggestMinSup(avgSeqLen, totalDistItem):
            min_sup = round(avgSeqLen * 100 / float(totalDistItem), 3)
            return min_sup.__str__() + " %"

        Title = "Serial,Dataset_Name,dbSize,avglen,maxLen,minLen," \
                "totalDistItem,avgDistItem,maxDistItem,minDistItem," \
                "avgEvPerSeq,avgEvLen,maxEvLen," \
                "suggested_MinSup"
        result = int(SeqDatabase.datasetID).__str__() + "," + self.inputFile + "," + self.seqCount.__str__() + "," \
                 + self.avgSeqLen.__str__() +"," + max(self.seqLengths).__str__() +"," + min(self.seqLengths).__str__() +"," \
                 + self.totalDistItem.__str__() +"," + self.avgDistItems.__str__() +"," + max(self.numDistItems).__str__() +"," + min(self.numDistItems).__str__() +"," \
                 + self.avgEventsPerSeq.__str__() +"," + self.avgEventLen.__str__() +"," + self.maxEventLen.__str__() +"," \
                 + suggestMinSup(self.avgSeqLen,self.totalDistItem)

        heads = Title.split(",")
        body = result.split(",")

        # print("_______________________________________________")
        for i in range(0,heads.__len__()):
            if type(body.__getitem__(i)) is list:
                continue
            buffer = ("%s : %s"% (heads.__getitem__(i), body.__getitem__(i)))
            print(buffer)

        print("*_______________________________________________*")

        return result
