import random,math,os,errno
from PrepareDataset import SeqDB


def lineCount(inFile):
    f = open(inFile, 'r')
    cnt = 0
    for line in f:
        if line == '\n' or line.strip() == '':
            break
        cnt += 1
    return cnt



def manualPartition(inFile,dataset_name,fileTitle):

    totalSeq = lineCount(inFile)
    print(totalSeq)

    p0_percentage = int(input('p0_size (%uSDB): '))
    p0_size = math.ceil(float(p0_percentage / 100) * totalSeq)

    remLines = totalSeq - p0_size

    nInc = int(input("How many increments? : "))
    print('approx inc %:',(float(remLines)/nInc)/p0_size*100,' inc-size: ',(remLines//nInc))
    outFolder = '../Files/'+dataset_name+'/'+fileTitle+'_'+str(p0_percentage)+'_'+str(nInc)+'/'
    # outFolder = '/home/hhmoon/Desktop/Dataset for use/'+fileTitle+'_p'+str(p0_percentage)+'_'+str(nInc)+'/'

    if not os.path.exists(os.path.dirname(outFolder)):
        try:
            os.makedirs(os.path.dirname(outFolder))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    partitionInfoFile = open(outFolder + 'partitionInfo.txt', 'w')
    partitionInfoFile.write("p_0, " + p0_size.__str__() + '\n')

    inc_percentage =[]
    sz = []
    sz.append(p0_size)
    for i in range(1, nInc+1):
        # incLow = float(input('incsize low bound: '))
        # incHigh = float(input('incsize high bound: '))

        if i==nInc:
            incSize = remLines
            print("increment" + str(i) + " size :" + str(incSize) )
        else:
            incSize = int(input("increment" + str(i) + " size (<=" + (remLines).__str__() + "):"))
            if incSize > remLines:
                incSize = remLines
                print("increment" + str(i) + " size :" + str(incSize))

        partitionInfoFile.write("p" + str(i) + "," + str(incSize) + '\n')
        remLines = remLines - incSize
        sz.append(incSize)
        inc_percentage.append(float(incSize)/p0_size)


    f = open(inFile, "r")
    # curPos = f.tell()
    for i in range(0,len(sz)):
        outFile = outFolder +fileTitle+ "_" + str(i)+ ".txt"
        out = open(outFile, "w")
        for lines in range(0, sz[i]):
            seq = f.readline()
            out.write(seq)
        out.close()
    f.close()


    partitionInfoFile.write('average increment size, '
                            + str(round(sum(inc_percentage)/len(inc_percentage),4)*100) + '% p0_size\n')

    partitionInfoFile.close()




    print("#_______________________________________________#")



#call
inFile = input('Input File Path: ')
dataset_name = input('dataset name: ')
# outTitle = input('Out Title: ')
while(int(input('Enter 0 to continue: '))==0):
    manualPartition(inFile,dataset_name.strip(), dataset_name.strip())