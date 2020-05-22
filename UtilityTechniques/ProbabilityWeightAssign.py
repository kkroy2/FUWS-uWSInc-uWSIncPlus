from Parameters.ProgramVariable import ProgramVariable


class ProbabilityAssign():

    dataFile = None
    probsFile = None
    whereToWrite = None

    def __init__(self):
        # self.whereToWrite = open(where, 'w')
        # self.probsFile = open(probsfile, 'r')
        # self.dataFile = open(datafile, 'r')
        pass

    def Assigning(self):
        previous = self.probsFile.tell()
        cnt = 0
        for data in self.dataFile:
            # print(data)
            seq = '('
            item = ''
            for ch in data:
                if ch == ' ' or ch == '\n':
                    if len(item) > 0:
                        item = int(item)
                        # print(item == -2)
                        if item == -1:
                            seq = seq[:len(seq)-1]+')'+'('
                        elif item == -2:
                            # print(seq)
                            if seq[len(seq)-1] == '(':
                                seq = seq[:len(seq)-1]
                            else:
                                seq = seq[:len(seq) - 1]
                                seq += ')'
                            self.whereToWrite.write(seq)
                            self.whereToWrite.write('\n')
                            break
                        else:
                            self.probsFile.seek(previous)
                            prb = self.probsFile.readline().strip()
                            if prb == "":
                                self.probsFile.seek(0)
                                prb = self.probsFile.readline().strip()
                            # print(self.probsFile.tell())
                            previous = self.probsFile.tell()
                            seq += str(item)+':'+str(prb)+','
                            cnt += 1
                        item = ''
                else:
                    item += ch
        self.whereToWrite.close()
        return


class WeightAssign():
    wgt_file = open('../Files/weights.csv','r')
    current_point = wgt_file.tell()
    @staticmethod
    def assign(itms):
        WeightAssign.wgt_file.seek(WeightAssign.current_point)
        for itm in itms:
            if itm not in ProgramVariable.wgt_dic:
                wgt = WeightAssign.wgt_file.readline().strip()
                if wgt == "":
                    WeightAssign.wgt_file.seek(0)
                    wgt = WeightAssign.wgt_file.readline().strip()
                wgt = float(wgt)
                ProgramVariable.wgt_dic[itm] = wgt
                WeightAssign.current_point = WeightAssign.wgt_file.tell()

    @staticmethod
    def manual_assign():
        wgt_file = open('../Files/manual_weights.csv', 'r')
        for itms in wgt_file:
            ProgramVariable.wgt_dic[str(itms[0])] = float(itms[1])


class checkCSV():
    file = None
    @staticmethod
    def run():
        cnt = 0
        for val in checkCSV.file:
            cnt += 1
            if (val =='\n') or (val==' '):
                print(val , cnt, ' here ')