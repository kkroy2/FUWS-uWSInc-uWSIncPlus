class DP():
    dpArray = None
    apSDB = None
    file = None
    curSeq = None
    curDBSize = 0.0

    def __init__(self, file):
        self.file = open(file, 'r')
        self.apSDB = []
        self.preProcess()
        pass

    def setReadfile(self, file):
        self.file = open(file, 'r')
        self.apSDB = []
        self.preProcess()

    def preProcess(self):
        for seq in self.file:
            apSeq = []
            val = ''
            apItemSet = []

            for ch in seq:
                if ch is ' ':
                    continue
                elif ch is ')':
                    if val is None:
                        val = 0.0
                    # print(val, 'print at DP preproccess')
                    val = float(val)
                    apItemSet.append([str(item), val])
                    apSeq.append(apItemSet)
                    apItemSet = []
                    val = ''

                elif ch is ':':
                    item = val
                    val = ''
                    # print(item, "here print")

                elif ch is ',':
                    # print(item, 'found item')
                    apItemSet.append([str(item), float(val)])
                    val = ''

                elif ch is '(':
                    val = ''

                else:
                    val += ch
                    # print(ch, ' adding')

            # print(newSeq)
            self.apSDB.append(apSeq)

        # for seq in self.apSDB:
        #     print(seq)
        # print(len(self.apSDB), 'appended dataset size')
        self.curDBSize = len(self.apSDB)
        return

    def supportEvaluation(self, curSeq):
        expSupport = 0.0

        for i in range(0, len(self.apSDB)):
            ln = len(self.apSDB[i])
            row = len(curSeq)

            col = 0
            for seq in self.apSDB[i]:
                col = max(col, len(seq))

            self.dpArray = [[[[-1 for flag in range(0, 2 + 1)] for k in range(0, col + 1)] for i in range(0, ln + 1)]
                            for j in range(0, row + 1)]

            self.curSeq = curSeq
            expSupport += self.evaluationDP(0, 0, 0, False, i)
        return expSupport

    def evaluationDP(self, i, j, k, iE, trnId):
        if i >= len(self.curSeq):
            return 1.0
        if j >= len(self.apSDB[trnId]):
            return -10000000.0
        if iE and k >= len(self.apSDB[trnId][j]) and self.curSeq[i] != ')':
            return -1000000.0

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