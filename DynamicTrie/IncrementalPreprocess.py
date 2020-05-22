from Parameters.ProgramVariable import ProgramVariable


class IncPreProcess():          # this is used to preprocess each increments which is same as preprocess method
    def __init__(self, file):
        self.file = open(file, 'r')
        ProgramVariable.uSDB = []
        ProgramVariable.cnt_dic = dict()
        ProgramVariable.itemList = list()
        pass

    def preProcess(self):
        for seq in self.file:
            apSeq = []
            val = ''
            apItemSet = []
            item = None

            for ch in seq:
                if ch is ' ':
                    continue
                elif ch is ')':
                    if val is None:
                        val = 0.0
                    val = float(val)
                    apItemSet.append([str(item), val])
                    apItemSet.sort()
                    apSeq.append(apItemSet)
                    apItemSet = []
                    val = ''

                elif ch is ':':
                    item = val
                    if str(item) not in ProgramVariable.itemList:
                        ProgramVariable.itemList.append(str(item))

                    if str(item) not in ProgramVariable.cnt_dic:
                        ProgramVariable.cnt_dic[str(item)] = 1
                    else:
                        ProgramVariable.cnt_dic[str(item)] += 1
                    val = ''

                elif ch is ',':
                    # print(item, val, ' Print at preprocess')
                    apItemSet.append([str(item), float(val)])
                    val = ''

                elif ch is '(':
                    val = ''

                else:
                    val += ch

            ProgramVariable.uSDB.append(apSeq)
        return

