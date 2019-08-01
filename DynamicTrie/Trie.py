import copy
from Parameters.ProgramVariable import ProgramVariable
from Parameters.Variable import Variable
from Parameters.FileInfo import FileInfo
from UtilityTechniques.ThresholdCalculation import ThresholdCalculation


class Trie():
    root_node = None
    cur_ls_trie = None
    array = None

    def __init__(self, root_node):
        self.root_node = root_node
        pass

    def setlsTrie(self, lstrie):
        self.cur_ls_trie = lstrie
        return

    # def openFile(self):
    #     self.FSwhereToWrite.op

    # def buildTrie(self):
    #     return

    def update_support(self, cur_node, cur_arr, cur_swgt, cur_trn):
        tmp_root_node = None
        if cur_arr is not None:
            self.array = cur_arr
            self.imp_root_node = ImplicitNode()
            tmp_root_node = self.imp_root_node
            self.ImpSegmentTreeBuild(cur_trn)

        for dscnt in cur_node.descendants.values():
            tmp_array = []
            tmp_seq_wgt = cur_swgt
            if cur_arr is None:
                tmp_array = self.forINIT(dscnt.label, cur_trn)
                mx = 0.0
                for tp in tmp_array:
                    mx = max(mx, tp[1])
                tmp_seq_wgt += float(ProgramVariable.wgt_dic.get(dscnt.label))
                dscnt.supportValue += (mx * tmp_seq_wgt)
            else:
                if dscnt.extnType == 'I':
                    tmp_array = self.forItemExtn(dscnt.label, cur_arr, cur_trn)
                    mx = 0.0
                    for tp in tmp_array:
                        mx = max(mx, tp[1])
                    tmp_seq_wgt += float(ProgramVariable.wgt_dic.get(dscnt.label))
                    dscnt.supportValue += (mx * tmp_seq_wgt)
                elif dscnt.extnType == 'S':
                    self.imp_root_node = tmp_root_node
                    tmp_array = self.forSeqExtn(dscnt.label, cur_trn)
                    mx = 0.0
                    for tp in tmp_array:
                        mx = max(mx, tp[1])
                    tmp_seq_wgt += float(ProgramVariable.wgt_dic.get(dscnt.label))
                    dscnt.supportValue += (mx * tmp_seq_wgt)
            self.update_support(dscnt, tmp_array,tmp_seq_wgt, cur_trn)

    def traverse_trie(self, cur_node):
        if cur_node.supportValue + Variable.eps >= ThresholdCalculation.get_semi_wgt_exp_sup():
            cur_node.marker = True
        else:
            cur_node.marker = False
        for dscnt in cur_node.descendants.values():
            self.traverse_trie(dscnt)
        return

    def update_trie(self, cur_node):
        tmp_dscnt = copy.deepcopy(cur_node.descendants)
        cur_node.descendants = dict()
        for dscnt_key, dscnt_value in tmp_dscnt.items():
            childs = self.update_trie(dscnt_value)
            if childs > 0:
                cur_node.descendants[dscnt_key] = dscnt_value
        return len(cur_node.descendants) + cur_node.marker

    def merge_two_ls_trie(self, cur_node_pre, cur_node_cur):
        # print('\n printing at merge two ls trie.........\n')
        cur_node_cur.supportValue += cur_node_pre.supportValue
        for dscnt in cur_node_pre.descendants:
            if dscnt in cur_node_cur.descendants:
                self.merge_two_ls_trie(cur_node_pre.descendants[dscnt], cur_node_cur.descendants[dscnt])
        return

    def merge_ls_with_fssfs_trie(self, cur_node_ls, cur_node_fssfs):
        cur_node_ls.supportValue = 0
        cur_node_ls.marker = False
        for dscnt in cur_node_ls.descendants:
            if dscnt in cur_node_fssfs.descendants:
                self.merge_ls_with_fssfs_trie(cur_node_ls.descendants[dscnt], cur_node_fssfs.descendants[dscnt])
            elif cur_node_ls.descendants[dscnt].supportValue + Variable.eps >= ThresholdCalculation.get_semi_wgt_exp_sup():
                self.insert_node(cur_node_fssfs, dscnt, cur_node_ls.descendants[dscnt].supportValue)
                self.merge_ls_with_fssfs_trie(cur_node_ls.descendants[dscnt], cur_node_fssfs.descendants[dscnt])
        return

    def insert_node(self, cur_node, cur_tuple, support_value):
        label, extn_type = cur_tuple
        new_node = TrieNode(True, extn_type, label, support_value, True)
        cur_node.descendants[cur_tuple] = new_node
        return

    def update(self, curNode, curSeq, i, support):
        if i == len(curSeq) - 1:
            curNode.supportValue += support
            return
        if curSeq[i] == '(' or curSeq[i] == ')':
            self.update(curNode, curSeq, i + 1, support)
        else:
            if curSeq[i - 1] == '(':
                self.update(curNode.descendants[(curSeq[i], 'S')], curSeq, i + 1, support)
            else:
                self.update(curNode.descendants[(curSeq[i], 'I')], curSeq, i + 1, support)
        return

    def insertion(self, curNode, curSeq, i, support):
        # print(curSeq, ' curSeq at insertion ...........')
        if i == len(curSeq) - 1:
            curNode.marker = True
            curNode.supportValue = float(support)
            return

        if curSeq[i] == '(' or curSeq[i] == ')':
            self.insertion(curNode, curSeq, i + 1, support)
        else:
            # print(curSeq[i-1], curSeq[i], ' printing at insertion function...........')
            # print(curNode.descendants)
            if curSeq[i - 1] == '(':
                if (curSeq[i], 'S') not in curNode.descendants:
                    newNode = TrieNode(False, 'S', curSeq[i], 0.0, False)
                    curNode.descendants[(curSeq[i], 'S')] = newNode
                self.insertion(curNode.descendants[(curSeq[i], 'S')], curSeq, i + 1, support)
            else:
                # print(i, 'I')
                if (curSeq[i], 'I') not in curNode.descendants:
                    newNode = TrieNode(False, 'I', curSeq[i], 0.0, False)
                    curNode.descendants[(curSeq[i], 'I')] = newNode
                self.insertion(curNode.descendants[(curSeq[i], 'I')], curSeq, i + 1, support)
        return

    def deletion(self, curNode, curSeq, i):
        if i == len(curSeq) - 1:
            curNode.supportValue = 0.0
            curNode.marker = False
            return
        if curSeq[i] == '(' or curSeq[i] == ')':
            self.deletion(curNode, curSeq, i + 1)
        else:
            if curSeq[i - 1] == '(':
                nextNode = curNode.descendants[(curSeq[i], 'I')]
                self.deletion(nextNode, i + 1)
                if len(nextNode.descendants) == 0:
                    curNode.descendants.pop((curSeq[i], 'I'))
            else:
                nextNode = curNode.descendants[(curSeq[i], 'S')]
                self.deletion(nextNode, i + 1)
                if len(nextNode.descendants) == 0:
                    curNode.descendants.pop((curSeq[i], 'S'))
        return

    def trie_into_file(self, curNode, curSeq):
        if curNode.extnType == 'I' and curNode.label is not None:
            curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
        elif curNode.label is not None:
            curSeq = curSeq + '(' + curNode.label + ')'
        if curNode.marker:
            curNode.updateflag = False
            if curNode.supportValue + Variable.eps >= ThresholdCalculation.get_wgt_exp_sup():
                FileInfo.fs.write(curSeq)
                FileInfo.fs.write(' ')
                FileInfo.fs.write(str(curNode.supportValue))
                FileInfo.fs.write('\n')
            else:
                FileInfo.sfs.write(curSeq)
                FileInfo.sfs.write(' ')
                FileInfo.sfs.write(str(curNode.supportValue))
                FileInfo.sfs.write('\n')
        for dscnt in curNode.descendants.values():
            self.trie_into_file(dscnt, curSeq)
        return

    def trieIntoFilePS(self, curNode, curSeq):
        if curNode.extnType == 'I' and curNode.label is not None:
            curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
        elif curNode.label is not None:
            curSeq = curSeq + '(' + curNode.label + ')'
        if curNode.marker:
            FileInfo.ls.write(curSeq)
            FileInfo.ls.write(' ')
            FileInfo.ls.write(str(curNode.supportValue))
            FileInfo.ls.write('\n')
        for dscnt in curNode.descendants.values():
            self.trieIntoFilePS(dscnt, curSeq)
        return

    def printFSSFS(self, curNode, curSeq):
        if curNode.extnType == 'I' and curNode.label is not None:
            curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
        elif curNode.label is not None:
            curSeq = curSeq + '(' + curNode.label + ')'
        if curNode.marker:
            print('Current Seg: '+ curSeq, " : ", curNode.supportValue )
        for dscnt in curNode.descendants.values():
            self.printFSSFS(dscnt, curSeq)
        return

    def printPFS(self, curNode, curSeq):
        # print('function is calling !!')
        if curNode.extnType == 'I' and curNode.label is not None:
            curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
        elif curNode.label is not None:
            curSeq = curSeq + '(' + curNode.label + ')'
        if curNode.marker:
            print(curSeq, " current seq with ", curNode.supportValue )
        for dscnt in curNode.descendants.values():
            self.printPFS(dscnt, curSeq)
        return

    def updateWithInsertion(self, curNode, curSeq, i, support):
        if i == len(curSeq) - 1:
            # print(i, ' Markedddddddddd', curSeq)
            curNode.marker = True
            curNode.updateflag = True
            # print(curNode.supportValue, 'before updateing with insertion')
            curNode.supportValue += float(support)
            # print(curNode.supportValue, 'after updating with insertion')
            return
        if curSeq[i] == '(' or curSeq[i] == ')':
            self.updateWithInsertion(curNode, curSeq, i + 1, support)
        else:
            if curSeq[i - 1] == '(':
                # print(i, 'S')
                if (curSeq[i], 'S') not in curNode.descendants.keys():
                    newNode = TrieNode(False, 'S', curSeq[i], 0.0, False)
                    curNode.descendants[(curSeq[i], 'S')] = newNode
                self.updateWithInsertion(curNode.descendants[(curSeq[i], 'S')], curSeq, i + 1, support)
            else:
                # print(i, 'I')
                if (curSeq[i], 'I') not in curNode.descendants.keys():
                    newNode = TrieNode(False, 'I', curSeq[i], 0.0, False)
                    curNode.descendants[(curSeq[i], 'I')] = newNode
                self.updateWithInsertion(curNode.descendants[(curSeq[i], 'I')], curSeq, i + 1, support)
        return

    def updateWithlsTrieBuild(self, cur_node, cur_seq):
        tmp_cur_seq = copy.deepcopy(cur_seq)
        if cur_node.extnType == 'I' and cur_node.label is not None:
            if len(cur_seq)==0:
                print(cur_node.label, cur_node.extnType)
            tmp_cur_seq.pop()
            tmp_cur_seq.append(cur_node.label)
            tmp_cur_seq.append(')')

        elif cur_node.label is not None:
            tmp_cur_seq.append('(')
            tmp_cur_seq.append(cur_node.label)
            tmp_cur_seq.append(')')

        if cur_node.marker is False and cur_node.label is not None:
            self.cur_ls_trie.insertion(self.cur_ls_trie.root_node, tmp_cur_seq, 0, float(cur_node.supportValue))

        tmp_dscnt = copy.deepcopy(cur_node.descendants)
        cur_node.descendants = dict()
        for dscnt_key, dscnt_value in tmp_dscnt.items():
            childs = self.updateWithlsTrieBuild(dscnt_value, cur_seq)
            if childs > 0:
                cur_node.descendants[dscnt_key] = dscnt_value
        return len(cur_node.descendants) + cur_node.marker

    def deleteWholeTrie(self, curNode):
        for dscnt in curNode.descendants.values():
            self.deleteWholeTrie(dscnt)
        curNode.descendants.clear()
        return

    def searchSupport(self, curNode, curSeq, i):
        if i == len(curSeq)-1:
            return curNode.supportValue
        if curSeq[i] == '(' or curSeq[i] == ')':
            return self.searchSupport(curNode, curSeq, i+1)
        else:
            if curSeq[i - 1] == '(':
                if (curSeq[i], 'S') in curNode.descendants:
                    return self.searchSupport(curNode.descendants[(curSeq[i], 'S')], curSeq, i + 1)
                else:
                    return 0.0
            else:
                if (curSeq[i], 'I') in curNode.descendants:
                    return self.searchSupport(curNode.descendants[(curSeq[i], 'I')], curSeq, i + 1)
                else:
                    return 0.0

    def forINIT(self, item, trnId):
        expValArray = []
        for i in range(0, len(ProgramVariable.uSDB[trnId])):
            if len(ProgramVariable.uSDB[trnId][i]) <= 3:
                for itm in ProgramVariable.uSDB[trnId][i]:
                    if itm[0] == item:
                        expValArray.append([i, itm[1]])
            else:
                left = 0
                right = len(ProgramVariable.uSDB[trnId][i]) - 1
                while left <= right:
                    mid = (left + right) // 2
                    itm = ProgramVariable.uSDB[trnId][i][mid]
                    if itm[0] == item:
                        expValArray.append([i, itm[1]])
                        break
                    elif itm[0] < item:
                        left = mid + 1
                    else:
                        right = mid - 1
        return expValArray

    def findFSandSFS(self, curNode, curSeq):
        if curNode.extnType == 'I' and curNode.label is not None:
            curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
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

    def determinationProjection(self):
        allItmDic = dict()
        # for seq in Parameters.pSDB:
        for i in range(0, len(ProgramVariable.pSDB)):
            tmpItmDic = dict()
            for j in range(0, len(ProgramVariable.pSDB[i])):
                for k in range(0, len(ProgramVariable.pSDB[i][j])):
                    itm = ProgramVariable.pSDB[i][j][k]
                    if itm[0] not in tmpItmDic:
                        tmpItmDic[itm[0]] = [itm[1], [i, j, k]]
            for itm in tmpItmDic:
                if itm not in allItmDic:
                    # print(itm)
                    itm_wgt = float(ProgramVariable.wgt_dic.get(itm))
                    allItmDic[itm] = [itm_wgt, float(tmpItmDic[itm][0]), float(tmpItmDic[itm][0]) * float(itm_wgt),
                                      []]
                    allItmDic[itm][3].append(tmpItmDic[itm][1])
                else:
                    allItmDic[itm][1] = max(allItmDic[itm][1], float(tmpItmDic[itm][0]))
                    allItmDic[itm][2] += float(tmpItmDic[itm][0]) * allItmDic[itm][0]
                    allItmDic[itm][3].append(tmpItmDic[itm][1])
        return allItmDic

    def forItemExtn(self, item, item_set_pos, trn_id):
        exp_val_array = []
        for pos in item_set_pos:
            if len(ProgramVariable.uSDB[trn_id][pos[0]]) <= 3:
                for itm in ProgramVariable.uSDB[trn_id][pos[0]]:
                    if itm[0] == item:
                        exp_val_array.append([pos[0], pos[1] * itm[1]])
            else:
                left = 0
                right = len(ProgramVariable.uSDB[trn_id][pos[0]]) - 1
                while left <= right:
                    mid = (left + right) // 2
                    itm = ProgramVariable.uSDB[trn_id][pos[0]][mid]
                    if itm[0] == item:
                        exp_val_array.append([pos[0], pos[1] * itm[1]])
                        break
                    elif itm[0] < item:
                        left = mid + 1
                    else:
                        right = mid - 1
        return exp_val_array

    def imp_tree_update(self, node, beg, end, pos, val):
        if beg == pos and pos == end:
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
        # print(node, beg, end)
        for pos in self.array:
            self.imp_tree_update(self.imp_root_node, 0, len(ProgramVariable.uSDB[trn_id]) - 1, pos[0], pos[1])
        return

    def ImpMRQ(self, node, beg, end, l, r):

        if (l > r) or (node is None):
            return 0.0
        if beg == l and end == r:
            return node.val
        mid = (beg + end) // 2

        ret_l = self.ImpMRQ(node.left, beg, mid, l, min(mid, r))
        ret_r = self.ImpMRQ(node.right, mid + 1, r, max(mid + 1, l), r)
        return max(ret_l, ret_r)

    def forSeqExtn(self, item, trn_id):
        exp_val_array = []
        for i in range(0, len(ProgramVariable.uSDB[trn_id])):
            itms = ProgramVariable.uSDB[trn_id][i]
            if len(itms) <= 3:
                for itm in itms:
                    if itm[0] == item:
                        val = self.ImpMRQ(self.imp_root_node, 0, len(ProgramVariable.uSDB[trn_id]), 0, i - 1)
                        exp_val_array.append([i, val * itm[1]])
            else:
                left = 0
                right = len(ProgramVariable.uSDB[trn_id][i]) - 1
                while left <= right:
                    mid = (left + right) // 2
                    itm = ProgramVariable.uSDB[trn_id][i][mid]
                    if itm[0] == item:
                        val = self.ImpMRQ(self.imp_root_node, 0, len(ProgramVariable.uSDB[trn_id]), 0, i - 1)
                        exp_val_array.append([i, val * itm[1]])
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


class TrieNode():
    marker = False
    extnType = None
    label = None
    supportValue = 0.0
    descendants = None
    updateflag = False

    def __init__(self, marker, extnType, label, support, flag):
        self.marker = marker
        self.extnType = extnType
        self.label = label
        self.supportValue = support
        self.descendants = dict()
        self.updateflag = flag
        return
