import random


def convertToSeqData(itemDataFile,outFile=None):
    if outFile is None:
        outFile = itemDataFile.replace('.txt','_seq.txt')
    with open(itemDataFile,"r") as f, open(outFile,"w") as out:
        for line in f:
            line = line.replace("\r", "").replace("\n", "")
            events = line.split(" ")
            transfomed = []
            for e in events:
                if e==" " or e=="":
                    continue
                transfomed.append(e)
                p = random.randrange(1,100)
                # if p>50:
                    #start new event
                    # transfomed.append("-1")
                transfomed.append("-1")

            # if transfomed[transfomed.__len__()-1]!="-1":
            #     transfomed.append("-1")
            transfomed.append("-2")
            line = " ".join(transfomed)
            out.write(line)
            out.write("\n")


# convertToSeqData("accidents.txt")