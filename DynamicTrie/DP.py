
class DP():
    dpArray = None
    apSDB = None
    file = None
    curSeq = None
    curDBSize = 0.0
    dp = None

    def __init__(self, db):
        self.apSDB = db
        pass

    def supportEvaluation(self, curSeq):            # calculate WES using Dynamic programming that used in uWSequence
        expSupport = 0.0

        for i in range(0, len(self.apSDB)):
            self.curSeq = curSeq
            self.dp = [[-1 for col in range(0, len(self.curSeq)+1)] for row in range(0, len(self.apSDB[i])+1)]
            ret_val = self.evaluate_support(i, 0, 0)
            expSupport += ret_val

        return expSupport

    def evaluationDP(self, i, j, k, iE, trnId):
        if i >= len(self.curSeq):
            return 1.0
        if j >= len(self.apSDB[trnId]):
            return 0.0
        if iE and k >= len(self.apSDB[trnId][j]) and self.curSeq[i] != ')':
            return 0.0

        if self.dpArray[i][j][k][iE] != -1:
            return self.dpArray[i][j][k][iE]

        retValue = 0.0

        if not iE:
            retValue = max(retValue, self.evaluationDP(i, j + 1, 0, iE, trnId))

        if self.curSeq[i] == '(':
            retValue = max(retValue, self.evaluationDP(i + 1, j, k, True, trnId))

        elif self.curSeq[i] == ')':
            retValue = max(retValue, self.evaluationDP(i + 1, j + 1, 0, False, trnId))

        elif iE:
            if str(self.curSeq[i]) == str(self.apSDB[trnId][j][k][0]):
                retValue = max(retValue, self.evaluationDP(i + 1, j, k + 1, iE, trnId) * float(self.apSDB[trnId][j][k][1]))
            else:
                retValue = max(retValue, self.evaluationDP(i, j, k + 1, iE, trnId))
        self.dpArray[i][j][k][iE] = retValue

        return retValue

    def evaluate_support(self, trn_id, i, j):
        if j >= len(self.curSeq):
            return 1.0
        if i >= len(self.apSDB[trn_id]):
            return 0.0

        if self.dp[i][j] != -1:
            return self.dp[i][j]

        ret_val = 0.0
        ret_val = max(ret_val, self.evaluate_support(trn_id, i+1, j))
        flag, support = self.isIn(self.curSeq[j], self.apSDB[trn_id][i])
        if flag:
            ret_val = max(ret_val, self.evaluate_support(trn_id, i+1, j+1) * support)
        return ret_val

    def isIn(self, cur_pttn, cur_trn):
        i = 0
        j = 0
        support = 1.0
        while (i < len(cur_pttn)) and (j < len(cur_trn)):
            if cur_pttn[i] == cur_trn[j][0]:
                support *= cur_trn[j][1]
                i += 1
                j += 1

            elif cur_pttn[i] < cur_trn[j][0]:
                return False, 0.0
            else:
                j += 1
        if i >= len(cur_pttn):
            return True, support
        else:
            return False, 0.0
