from Parameters.FileInfo import FileInfo
from Parameters.ProgramVariable import ProgramVariable


class PreProcess():

    def __init__(self):
        ProgramVariable.uSDB = []
        ProgramVariable.pSDB = []
        ProgramVariable.itemList = list()
        ProgramVariable.cnt_dic = dict()
        pass

    def doProcess(self):
        itemList = list()
        uSDB= []
        pSDB = []
        seqMap = dict()
        cntMap = dict()

        for seq in FileInfo.initial_dataset:
            pSeq = []
            uSeq = []
            rseq = seq[::-1]

            tnewSeqList = []
            item = ''
            val = 0.0
            seqMap = dict()

            uItemSet = []

            for ch in rseq:
                if ch is ' ':
                    ch = ''
                elif ch is ')':
                    tnewSeqList = []
                    uItemSet = []

                elif ch is ':':
                    item = item.strip()
                    item = item[::-1]
                    item = item.strip()
                    if len(item) == 0:
                        item = 0.0
                    item = float(item)
                    val = item
                    item = ''

                elif ch is ',':
                    item = item[::-1]
                    uItemSet.append([item, val])
                    if item in seqMap:
                        seqMap[item] = max(seqMap[item], val)
                    else:
                        seqMap[item] = val

                    if item not in itemList:
                        itemList.append(item)
                    val = seqMap[item]
                    tnewSeqList.append([item, val])

                    item = ''
                elif ch is '(':
                    item = item[::-1]
                    if item in seqMap:
                        seqMap[item] = max(seqMap[item], val)
                    else:
                        seqMap[item] = val

                    if item not in itemList:
                        itemList.append(str(item))
                    if item not in cntMap:
                        cntMap[item] = 1
                    else:
                        cntMap[item] += 1

                    uItemSet.append([item, val])
                    val = seqMap[item]
                    tnewSeqList.append([item, val])
                    tnewSeqList = tnewSeqList[::-1]
                    tnewSeqList.sort()
                    pSeq.append(tnewSeqList)
                    uItemSet = uItemSet[::-1]
                    uItemSet.sort()
                    uSeq.append(uItemSet)
                    item = ''
                else:
                    item += ch

            uSDB.append(uSeq[::-1])
            pSDB.append(pSeq[::-1])
            ProgramVariable.uSDB = uSDB
            ProgramVariable.pSDB = pSDB
            ProgramVariable.itemList = itemList
            ProgramVariable.cnt_dic = cntMap
            # print(ProgramVariable.uSDB)
            # print(' printing at Preprocessing after uSDB')
            # print(ProgramVariable.pSDB)
            # print(' printing  itemlist')
            # print(ProgramVariable.itemList)
            # print('weight ')
            # print(ProgramVariable.cnt_dic)
        return





