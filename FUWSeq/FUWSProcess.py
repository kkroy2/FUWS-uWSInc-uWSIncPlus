import copy

from DynamicTrie.Trie import TrieNode
from Parameters.ProgramVariable import ProgramVariable
from UtilityTechniques.ThresholdCalculation import ThresholdCalculation
from Parameters.Variable import Variable


class FUWSProcess():

    def __init__(self):
        pass

    def douWSProcess(self, pSDB, curNode, cur_itm_set, max_pr, mxWgt, curLen):
        cur_itm_set.sort()
        # ************* should  check carefully the following portion**************

        allItmDic = self.DetermineProjection(pSDB, cur_itm_set, False)
        # False means it is for Item-Extension
        # print('Prefix: ', cur_itm_set, 'maxPr: ', max_pr, 'sWgt: ', mxWgt)
        # print('Projected Database: ', pSDB)
        # print('Item Extension: ', allItmDic)
        # print('--------------------')

        max_weight = 0.0
        itm_wgt = 0.0
        copied_dic = copy.deepcopy(allItmDic)
        for itm in sorted(allItmDic):
            itm_wgt = ProgramVariable.wgt_dic.get(itm)
            if (allItmDic[itm][0]*itm_wgt) + Variable.eps >= ThresholdCalculation.get_semi_wgt_exp_sup():
                copied_dic[itm] = allItmDic[itm]
                max_weight = max(max_weight, itm_wgt)
        allItmDic = copy.deepcopy(copied_dic)
        copied_dic = None

        for item in sorted(allItmDic):
            sum_sup, imax_pro, prjSDB = allItmDic[item]
            itm_wgt = ProgramVariable.wgt_dic.get(item)
            tmp_sWgt = max(mxWgt, max_weight)
            tmp_cur_len = curLen + 1
            expSupportTop = (sum_sup * max_pr * tmp_sWgt)
            # print(expSupportTop, item)
            if expSupportTop + Variable.eps >= ThresholdCalculation.get_semi_wgt_exp_sup():
                # print('wExpSupCap: ', expSupportTop, ' for i-item ', item)
                tcurItmSt = copy.deepcopy(cur_itm_set)
                tcurItmSt.append(str(item))
                # print('I-extendable: ', tcurItmSt, expSupportTop)
                newNode = TrieNode(True, 'I', item, 0.0, False)
                if (item, 'I') not in curNode.descendants:
                    curNode.descendants[(item, 'I')] = newNode
                print('wExpSupCap: ', round(expSupportTop, 2), 'maxPr: ', round(max_pr* imax_pro, 2), 'maxWgt: ', round(max(mxWgt, itm_wgt), 2), ' for i-item ', item)
                self.douWSProcess(prjSDB, newNode, copy.deepcopy(tcurItmSt), max_pr * imax_pro, max(itm_wgt, mxWgt), tmp_cur_len)

        allItmDic = self.DetermineProjection(pSDB, cur_itm_set, True)
        # True means it is for Sequence-Extension
        # print('Prefix: ', cur_itm_set, 'maxPr: ', max_pr, 'sWgt: ', mxWgt)
        # print('Projected Database: ', pSDB)
        # print('Sequence Extension: ', allItmDic)
        # print('------------------------')

        max_weight = 0.0
        itm_wgt = 0.0
        copied_dic = copy.deepcopy(allItmDic)
        for itm in sorted(allItmDic):
            itm_wgt = ProgramVariable.wgt_dic.get(itm)
            if (allItmDic[itm][0] * itm_wgt) + Variable.eps >= ThresholdCalculation.get_semi_wgt_exp_sup():
                copied_dic[itm] = allItmDic[itm]
                max_weight = max(max_weight, itm_wgt)
        allItmDic = copy.deepcopy(copied_dic)
        copied_dic = None

        for item in sorted(allItmDic):
            sup_sum, imax_pro, prjSDB = allItmDic[item]
            itm_wgt = ProgramVariable.wgt_dic.get(item)
            tmp_cur_len = curLen + 1
            tmp_sWgt = max(mxWgt, max_weight)
            expSupportTop = (sup_sum * max_pr * tmp_sWgt)
            # print(sup_sum, max_pr, tmp_sWgt)
            # expSupportTop = (sup_sum * imax_pro * max_pr * tmp_sWgt) / tmp_cur_len
            # print('expSupportTop : ', expSupportTop, ' for ', item, ' tmp_swt: ', tmp_sWgt)
            if expSupportTop + Variable.eps >= ThresholdCalculation.get_semi_wgt_exp_sup():
                tcurItmSt = copy.deepcopy(cur_itm_set)
                tcurItmSt.append(str(item))

                newNode = TrieNode(True, 'S', item, 0.0, False)
                if (item, 'S') not in curNode.descendants:
                    curNode.descendants[(item, 'S')] = newNode
                print('wExpSupCap: ', round(expSupportTop, 2), 'maxPr: ', round(max_pr* imax_pro, 2), 'maxWgt: ', round(max(mxWgt, itm_wgt), 2),
                      ' for s-item ', item)
                self.douWSProcess(prjSDB, newNode, copy.deepcopy(tcurItmSt), max_pr * imax_pro, max(mxWgt, itm_wgt), tmp_cur_len)
        return

    def DetermineProjection(self, prjSDB, cur_item_set, sExtn):
        allItmDic = dict()
        if sExtn:
            for info in prjSDB:
                I, J, K = info
                tmpItmDic = dict()
                for j in range(J+1, len(ProgramVariable.pSDB[I])):
                    itemset = ProgramVariable.pSDB[I][j]
                    for k in range(0, len(itemset)):
                        if itemset[k][0] not in tmpItmDic:
                            tmpItmDic[itemset[k][0]] = [itemset[k][1], [I, j, k]]
                for itm in tmpItmDic:
                    if itm not in allItmDic:
                        allItmDic[itm] = [float(tmpItmDic[itm][0]), tmpItmDic[itm][0], []]
                        allItmDic[itm][2].append(tmpItmDic[itm][1])
                    else:
                        allItmDic[itm][0] += float(tmpItmDic[itm][0])
                        allItmDic[itm][1] = max(allItmDic[itm][1], tmpItmDic[itm][0])
                        allItmDic[itm][2].append(tmpItmDic[itm][1])
            return allItmDic

        else:
            for info in prjSDB:
                I, J, K = info
                tmpItmDic = dict()
                for k in range(K+1, len(ProgramVariable.pSDB[I][J])):
                    itm = ProgramVariable.pSDB[I][J][k]
                    if itm[0] not in tmpItmDic:
                        tmpItmDic[itm[0]] = [itm[1], [I, J, k]]

                for j in range(J+1, len(ProgramVariable.pSDB[I])):
                    itemset = ProgramVariable.pSDB[I][j]
                    found = -1
                    if len(cur_item_set) < len(itemset):
                        for k in range(0, len(cur_item_set)):
                            found = -1
                            if cur_item_set[k] != itemset[k]:
                                break
                            found = len(cur_item_set)

                    if found != -1:
                        for k in range(found, len(itemset)):
                            itm = itemset[k]
                            if itm[0] not in tmpItmDic:
                                tmpItmDic[itm[0]] = [itm[1], [I, J, k]]

                for itm in tmpItmDic:
                    # print(itm, tmpItmDic[itm])
                    if itm not in allItmDic:
                        allItmDic[itm] = [float(tmpItmDic[itm][0]), tmpItmDic[itm][0], []]
                        allItmDic[itm][2].append(tmpItmDic[itm][1])
                    else:
                        allItmDic[itm][0] += float(tmpItmDic[itm][0])
                        allItmDic[itm][1] = max(allItmDic[itm][1], tmpItmDic[itm][0])
                        allItmDic[itm][2].append(tmpItmDic[itm][1])
            return allItmDic