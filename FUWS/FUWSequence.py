import copy
from DynamicTrie.Trie import TrieNode
from FUWS.FUWSProcess import FUWSProcess
from Parameters.Variable import Variable
from UtilityTechniques.ThresholdCalculation import ThresholdCalculation
from Parameters.ProgramVariable import ProgramVariable
from Parameters.FileInfo import FileInfo


class FUWSequence():
    candi_root_node = None
    array = []
    imp_root_node = None

    def __init__(self):
        self.candi_root_node = TrieNode(False, None, None, 0.0, False)      # Initialization
        pass

    def douWSequence(self):

        allItmDic = self.determination_projection()         # find all items and their corresponding projections
        max_weight = 0.0
        copied_dic = copy.deepcopy(allItmDic)

        for itm in sorted(allItmDic):
            if allItmDic[itm][2] + Variable.eps >= ThresholdCalculation.get_semi_wgt_exp_sup():
                copied_dic[itm] = allItmDic[itm]
                max_weight = max(max_weight, allItmDic[itm][0])

        allItmDic = copy.deepcopy(copied_dic)
        copied_dic = None

        for item in sorted(allItmDic):      # iterate over all potential extendable items to start from 1-length pattern
            sWeight, maxPr, wExpSupTop, prjSDB = allItmDic[item]

            if wExpSupTop + Variable.eps >= ThresholdCalculation.get_semi_wgt_exp_sup():
                cur_seq = list()
                cur_seq.append(str(item))
                newNode = TrieNode(True, 'S', item, 0.0, False)
                if (item, 'S') not in self.candi_root_node.descendants:
                    self.candi_root_node.descendants[(item, 'S')] = newNode

                FUWSProcess().douWSProcess(prjSDB, newNode, copy.deepcopy(cur_seq), maxPr, sWeight, 1)

        total_candidates = self.candidateTrieTraversal(self.candi_root_node, '')
        for i in range(0, len(ProgramVariable.uSDB)):
            self.actualSupportCalculation(self.candi_root_node, 0.0, None, 0, i)
        self.check_actual_fs_sfs(self.candi_root_node)
        return self.candi_root_node, total_candidates

    def candidateTrieTraversal(self, curNode, curSeq):
        if curNode.extnType == 'I' and curNode.label is not None:
            curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
        elif curNode.label is not None:
            curSeq = curSeq + '(' + curNode.label + ')'
        tmp_count = 0
        if curNode.marker:
            print(curSeq)
            tmp_count += 1
            curNode.supportValue = 0.0
        for dscnt in curNode.descendants.values():
            tmp_count += self.candidateTrieTraversal(dscnt, curSeq)
        return tmp_count

    def actualSupportCalculation(self, cur_node, seq_wgt, array, cur_ln, trn_id):
        tmp_root_node = None
        if array is not None and len(cur_node.descendants) > 0:
            self.array = array
            self.imp_root_node = ImplicitNode()
            tmp_root_node = self.imp_root_node
            self.ImpSegmentTreeBuild(trn_id)

        for dscnt in cur_node.descendants.values():
            tmp_cur_ln = cur_ln
            tmp_array = []
            tmp_seq_wgt = seq_wgt
            if array is None:
                tmp_array = self.forINIT(dscnt.label, trn_id)
                mx = 0.0
                for tp in tmp_array:
                    mx = max(mx, tp[1])
                tmp_seq_wgt += float(ProgramVariable.wgt_dic.get(dscnt.label))
                tmp_cur_ln += 1
                dscnt.supportValue += (mx*tmp_seq_wgt)/float(tmp_cur_ln)
            else:
                if dscnt.extnType == 'I':
                    tmp_array = self.forItemExtn(dscnt.label, array, trn_id)
                    mx = 0.0
                    for tp in tmp_array:
                        mx = max(mx, tp[1])
                    tmp_seq_wgt += float(ProgramVariable.wgt_dic.get(dscnt.label))
                    tmp_cur_ln += 1.0
                    dscnt.supportValue += (mx*tmp_seq_wgt)/float(tmp_cur_ln)
                elif dscnt.extnType == 'S':
                    self.imp_root_node = tmp_root_node
                    tmp_array = self.forSeqExtn(dscnt.label, trn_id)
                    mx = 0.0
                    for tp in tmp_array:
                        mx = max(mx, tp[1])
                    tmp_seq_wgt += float(ProgramVariable.wgt_dic.get(dscnt.label))
                    tmp_cur_ln += 1.0
                    dscnt.supportValue += (mx * tmp_seq_wgt)/float(tmp_cur_ln)
            self.actualSupportCalculation(dscnt, tmp_seq_wgt, tmp_array, tmp_cur_ln, trn_id)
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

    def forItemExtn(self, item, item_set_pos, trn_id):
        exp_val_array = []
        for pos in item_set_pos:
            if len(ProgramVariable.uSDB[trn_id][pos[0]]) <= 3:
                for itm in ProgramVariable.uSDB[trn_id][pos[0]]:
                    if itm[0] == item:
                        exp_val_array.append([pos[0], pos[1]*itm[1]])
            else:
                left = 0
                right = len(ProgramVariable.uSDB[trn_id][pos[0]])-1
                while left <= right:
                    mid = (left + right) // 2
                    itm = ProgramVariable.uSDB[trn_id][pos[0]][mid]
                    if itm[0] == item:
                        exp_val_array.append([pos[0], pos[1]*itm[1]])
                        break
                    elif itm[0] < item:
                        left = mid+1
                    else:
                        right = mid-1
        return exp_val_array

    def imp_tree_update(self, node, beg, end, pos, val):
        if (beg == pos) and (pos == end):
            node.val = val
            return
        mid = (beg + end) // 2

        if node.left is None:
            node.left = ImplicitNode()
        if node.right is None:
            node.right = ImplicitNode()

        if pos <= mid:
            self.imp_tree_update(node.left, beg, mid, pos, val)
        else:
            self.imp_tree_update(node.right, mid + 1, end, pos, val)
        node.val = max(node.left.val, node.right.val)
        return

    def ImpSegmentTreeBuild(self, trn_id):
        ln = len(ProgramVariable.uSDB[trn_id])
        for pos in self.array:
            self.imp_tree_update(self.imp_root_node, 0, ln - 1, pos[0], pos[1])
        return

    def ImpMRQ(self, node, beg, end, l, r):
        if (l > r) or (node is None):
            return 0.0

        if (beg == l) and (end == r):
            return node.val

        mid = (beg + end) // 2

        ret_l = self.ImpMRQ(node.left, beg, mid, l, min(mid, r))
        ret_r = self.ImpMRQ(node.right, mid+1, end, max(mid+1, l), r)

        return max(ret_l, ret_r)

    def forSeqExtn(self, item, trn_id):
        exp_val_array = []
        for i in range(0, len(ProgramVariable.uSDB[trn_id])):
            itms = ProgramVariable.uSDB[trn_id][i]
            if len(itms) <= 3:
                for itm in itms:
                    if itm[0] == item:
                        val = self.ImpMRQ(self.imp_root_node, 0, len(ProgramVariable.uSDB[trn_id])-1, 0, i - 1)
                        exp_val_array.append([i, val*itm[1]])
            else:
                left = 0
                right = len(ProgramVariable.uSDB[trn_id][i])-1
                while left <= right:
                    mid = (left + right) // 2
                    itm = ProgramVariable.uSDB[trn_id][i][mid]
                    if itm[0] == item:
                        val = self.ImpMRQ(self.imp_root_node, 0, len(ProgramVariable.uSDB[trn_id])-1, 0, i - 1)
                        exp_val_array.append([i, val*itm[1]])
                        break
                    elif ProgramVariable.uSDB[trn_id][i][mid][0] < item:
                        left = mid + 1
                    else:
                        right = mid - 1
        return exp_val_array


class ImplicitNode():
    def __init__(self):
        self.val = 0.0
        self.left = None
        self.right = None
