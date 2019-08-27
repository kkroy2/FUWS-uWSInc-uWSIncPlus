import copy
from DynamicTrie.Trie import TrieNode
from Parameters.Variable import Variable
from UtilityTechniques.ThresholdCalculation import ThresholdCalculation
from Parameters.ProgramVariable import ProgramVariable
from UWSeq.UWSProcess import UWSProcess
from Parameters.FileInfo import FileInfo
from DynamicTrie.DP import DP


class UWSequence():
    candi_root_node = None
    array = []
    imp_root_node = None

    def __init__(self):
        self.candi_root_node = TrieNode(False, None, None, 0.0, False)
        # def __init__(self, marker, extnType, label, support, flag):
        pass

    def douWSequence(self):

        allItmDic = self.determination_projection()
        for item in sorted(allItmDic):
            sWeight, maxPr, wExpSupTop, prjSDB = allItmDic[item]
            if wExpSupTop + Variable.eps >= ThresholdCalculation.get_semi_wgt_exp_sup():
                cur_seq = list()
                cur_seq.append(str(item))
                newNode = TrieNode(True, 'S', item, 0.0, False)
                if (item, 'S') not in self.candi_root_node.descendants:
                    self.candi_root_node.descendants[(item, 'S')] = newNode

                UWSProcess().douWSProcess(prjSDB, newNode, copy.deepcopy(cur_seq), maxPr, sWeight, 1)

        total_candidates = self.candidateTrieTraversal(self.candi_root_node, '')
        print("Candidate Generated: ", total_candidates)
        print(ThresholdCalculation.get_wgt_exp_sup(), ' Support Threshold')
        # for i in range(0, len(ProgramVariable.uSDB)):
        #     self.actualSupportCalculation(self.candi_root_node, 0.0, 0, i)
        self.actualSupportCalculation(self.candi_root_node, [], 0.0, 0)
        self.check_actual_fs_sfs(self.candi_root_node)
        return self.candi_root_node, total_candidates

    def candidateTrieTraversal(self, curNode, curSeq):
        if curNode.extnType == 'I' and curNode.label is not None:
            curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
        elif curNode.label is not None:
            curSeq = curSeq + '(' + curNode.label + ')'
        tmp_count = 0
        if curNode.marker:
            # print(curSeq, " current seq with ", curNode.supportValue)
            tmp_count += 1
            curNode.supportValue = 0.0
        for dscnt in curNode.descendants.values():
            tmp_count += self.candidateTrieTraversal(dscnt, curSeq)
        return tmp_count

    def actualSupportCalculation(self, cur_node, cur_seq, seq_wgt, cur_ln):

        if cur_node.extnType == 'I' and cur_node.label is not None:
            # cur_seq = cur_seq[:len(cur_seq) - 1] + cur_node.label + ')'
            cur_seq[len(cur_seq)-1].append(cur_node.label)
        elif cur_node.label is not None:
            # cur_seq = cur_seq + '(' + cur_node.label + ')'
            cur_seq.append([cur_node.label])
        tmp_count = 0
        if cur_node.marker:
            # print(curSeq, " current seq with ", curNode.supportValue)
            tmp_count += 1
            ret_support = DP(ProgramVariable.uSDB).supportEvaluation(cur_seq)
            # print(ret_support)
            cur_node.supportValue += (ret_support * seq_wgt) / float(cur_ln)
            # print('Support Calculation done for: ', cur_seq, ': ', cur_node.supportValue)

        for dscnt in cur_node.descendants.values():
            tmp_cur_seq = copy.deepcopy(cur_seq)
            # tmp_cur_seq.append(dscnt.label)
            tmp_cur_ln = cur_ln
            tmp_seq_wgt = seq_wgt
            tmp_seq_wgt += float(ProgramVariable.wgt_dic.get(dscnt.label))
            tmp_cur_ln += 1

            self.actualSupportCalculation(dscnt, tmp_cur_seq, tmp_seq_wgt, tmp_cur_ln)

        return

    def forINIT(self, item, trn_id):
        exp_val_array = []
        for i in range(0, len(ProgramVariable.uSDB[trn_id])):
            if len(ProgramVariable.uSDB[trn_id][i]) <= 3:
                for itm in ProgramVariable.uSDB[trn_id][i]:
                    if itm[0] == item:
                        exp_val_array.append([i, itm[1]])
            else:
                left = 0
                right = len(ProgramVariable.uSDB[trn_id][i]) - 1
                while left <= right:
                    mid = (left + right) // 2
                    itm = ProgramVariable.uSDB[trn_id][i][mid]
                    if itm[0] == item:
                        exp_val_array.append([i, itm[1]])
                        break
                    elif itm[0] < item:
                        left = mid + 1
                    else:
                        right = mid - 1
        return exp_val_array

    def findFSandSFS(self, curNode, curSeq):
        if curNode.extnType == 'I' and curNode.label is not None:
            curSeq = curSeq[:len(curSeq) - 1] + ', '+ curNode.label + ')'
        elif curNode.label is not None:
            curSeq = curSeq + '(' + curNode.label + ')'
        if curNode.marker:
            # print(curNode.supportValue, self.minExpSupport, Parameters.miu, curSeq,' At Find FS and SFS')
            if curNode.supportValue + Variable.eps >= ThresholdCalculation.get_wgt_exp_sup():
                FileInfo.fs.write(''.join(curSeq))
                FileInfo.fs.write(' ')
                FileInfo.fs.write(str(curNode.supportValue))
                FileInfo.fs.write('\n')
            elif curNode.supportValue + Variable.eps >= ThresholdCalculation.get_semi_wgt_exp_sup():
                FileInfo.sfs.write(''.join(curSeq))
                FileInfo.sfs.write(' ')
                FileInfo.sfs.write(str(curNode.supportValue))
                FileInfo.sfs.write('\n')
        for dscnt in curNode.descendants.values():
            self.findFSandSFS(dscnt, curSeq)
        return

    def check_actual_fs_sfs(self, curNode):
        curNode.marker = False
        if curNode.supportValue + Variable.eps >= ThresholdCalculation.get_wgt_exp_sup():
            curNode.marker = True
        elif curNode.supportValue + Variable.eps >= ThresholdCalculation.get_semi_wgt_exp_sup():
            curNode.marker = True
        for dscnt in curNode.descendants.values():
            self.check_actual_fs_sfs(dscnt)
        return

    def determination_projection(self):
        allItmDic = dict()
        for i in range(0, len(ProgramVariable.pSDB)):
            tmpItmDic = dict()
            for j in range(0, len(ProgramVariable.pSDB[i])):
                for k in range(0, len(ProgramVariable.pSDB[i][j])):
                    itm = ProgramVariable.pSDB[i][j][k]
                    if itm[0] not in tmpItmDic:
                        tmpItmDic[itm[0]] = [itm[1], [i, j, k]]
            for itm in tmpItmDic:
                if itm not in allItmDic:
                    itm_wgt = float(ProgramVariable.wgt_dic.get(itm))
                    allItmDic[itm] = [itm_wgt, float(tmpItmDic[itm][0]), float(tmpItmDic[itm][0])*float(itm_wgt), []]
                    allItmDic[itm][3].append(tmpItmDic[itm][1])
                else:
                    allItmDic[itm][1] = max(allItmDic[itm][1], float(tmpItmDic[itm][0]))
                    allItmDic[itm][2] += float(tmpItmDic[itm][0])*allItmDic[itm][0]
                    allItmDic[itm][3].append(tmpItmDic[itm][1])
        return allItmDic
