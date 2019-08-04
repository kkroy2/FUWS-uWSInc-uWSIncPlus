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
                wgt = float(WeightAssign.wgt_file.readline().strip())
                if wgt == "":
                    WeightAssign.wgt_file.seek(0)
                    wgt = float(WeightAssign.wgt_file.readline().strip())
                ProgramVariable.wgt_dic[itm] = wgt
                WeightAssign.current_point = WeightAssign.wgt_file.tell()

    @staticmethod
    def manual_assign():
        ProgramVariable.wgt_dic['a'] = 0.8
        ProgramVariable.wgt_dic['b'] = 1.0
        ProgramVariable.wgt_dic['c'] = 0.9
        ProgramVariable.wgt_dic['d'] = 0.3
        ProgramVariable.wgt_dic['e'] = 0.7
        ProgramVariable.wgt_dic['f'] = 0.9
        ProgramVariable.wgt_dic['g'] = 0.8


class checkCSV():
    file = None
    @staticmethod
    def run():
        cnt = 0
        for val in checkCSV.file:
            cnt += 1
            if (val =='\n') or (val==' '):
                print(val , cnt, ' here ')