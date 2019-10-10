import random


def convertToSeqData_a(itemDataFile,outFile=None): #each item is an event
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

def convertToSeqData_b(itemDataFile,outFile=None): #whole itemset transaction is an event (sequence)
    if outFile is None:
        outFile = itemDataFile.replace('.txt','_s.txt')
    count  = 0
    with open(itemDataFile,"r") as f, open(outFile,"w") as out:
        for line in f:
            count+=1
            line = line.replace("\r", "").replace("\n", "")
            while line.endswith(' '):
                line = line.strip()
            print(line)
            line = line+' -1 -2\n'
            print(line)
            out.write(line)
            # out.write("\n")
    print('total',count)

convertToSeqData_b("OnlineRetail.txt")