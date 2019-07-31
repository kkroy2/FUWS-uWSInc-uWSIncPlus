from Parameters.ProgramVariable import ProgramVariable


class IncPreProcess():
    def __init__(self, file):
        self.file = open(file, 'r')
        # self.preProcess()
        ProgramVariable.uSDB = []
        ProgramVariable.inc_cnt_dic = dict()
        ProgramVariable.inc_itm_list = list()
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
                    apSeq.append(apItemSet)
                    apItemSet = []
                    val = ''

                elif ch is ':':
                    item = val
                    if str(item) not in ProgramVariable.inc_itm_list:
                        ProgramVariable.inc_itm_list.append(str(item))
                    if str(item) not in ProgramVariable.inc_cnt_dic:
                        ProgramVariable.inc_cnt_dic[str(item)] = 1
                    else:
                        ProgramVariable.inc_cnt_dic[str(item)] += 1
                    val = ''

                elif ch is ',':
                    apItemSet.append([str(item), float(val)])
                    val = ''

                elif ch is '(':
                    val = ''

                else:
                    val += ch

            ProgramVariable.uSDB.append(apSeq)

        for seq in ProgramVariable.uSDB:
            print(seq)
        print(len(ProgramVariable.uSDB), 'appended dataset size why ')
        return

