from Parameters.ProgramVariable import ProgramVariable
from Parameters.Variable import Variable


class WAMCalculation():
    upto_wSum = 0.0
    upto_sum = 0.0

    @staticmethod
    def update_WAM():
        for itm in ProgramVariable.cnt_dic:
            wgt = ProgramVariable.wgt_dic(itm)
            cnt = ProgramVariable.cnt_dic(itm)
            WAMCalculation.upto_sum += cnt
            WAMCalculation.upto_wSum += (cnt*wgt)
        Variable.WAM = WAMCalculation.upto_wSum / WAMCalculation.upto_sum
        pass

