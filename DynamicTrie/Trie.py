import copy

# class Trie():
#     rootNode = None
#     supportDP = None
#     FSwhereToWrite = None
#     SFSwhereToWrite = None
#     readFromWhere = None
#     lsTrie = None
#
#     def __init__(self, FSwritefile, SFSwritefile, readfile):
#         self.FSwhereToWrite = open(FSwritefile, 'w')
#         self.SFSwhereToWrite = open(SFSwritefile, 'w')
#         self.readFromWhere = readfile
#         self.rootNode = TrieNode(False, None, None, 0.0, False)
#         self.supportDP = DP(self.readFromWhere)
#         pass
#
#     def setlsTrie(self, lstrie):
#         self.lsTrie = lstrie
#         return
#
#     # def openFile(self):
#     #     self.FSwhereToWrite.op
#
#     # def buildTrie(self):
#     #     return
#
#     def traverseTrie(self, curNode, curSeq, supportThreshold):
#
#         if curNode.extnType == 'I' and curNode.label is not None:
#             # curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
#             curSeq.pop()
#             curSeq.append(curNode.label)
#             curSeq.append(')')
#
#         elif curNode.label is not None:
#             # curSeq = curSeq + '(' + curNode.label + ')'
#             curSeq.append('(')
#             curSeq.append(curNode.label)
#             curSeq.append(')')
#
#         if curNode.marker:
#             # print(curSeq, " current seq ", curNode.updateflag)
#             if curNode.updateflag is False:
#                 newSupport = self.supportDP.supportEvaluation(copy.deepcopy(curSeq))
#                 self.update(self.rootNode, copy.deepcopy(curSeq), 0, newSupport)
#
#             curNode.updateflag = False
#             if supportThreshold + self.supportDP.curDBSize*Parameters.min_sup*Parameters.miu > curNode.supportValue + Parameters.eps:
#                 curNode.marker = False
#         for dscnt in curNode.descendants.values():
#             self.traverseTrie(dscnt, copy.deepcopy(curSeq), supportThreshold)
#         return
#
#     def update(self, curNode, curSeq, i, support):
#         if i == len(curSeq) - 1:
#             curNode.supportValue += support
#             return
#         if curSeq[i] == '(' or curSeq[i] == ')':
#             self.update(curNode, curSeq, i + 1, support)
#         else:
#             if curSeq[i - 1] == '(':
#                 self.update(curNode.descendants[(curSeq[i], 'S')], curSeq, i + 1, support)
#             else:
#                 self.update(curNode.descendants[(curSeq[i], 'I')], curSeq, i + 1, support)
#         return
#
#     def insertion(self, curNode, curSeq, i, support):
#
#         if i == len(curSeq) - 1:
#             curNode.marker = True
#             curNode.supportValue = float(support)
#             return
#
#         if curSeq[i] == '(' or curSeq[i] == ')':
#             self.insertion(curNode, curSeq, i + 1, support)
#         else:
#             if curSeq[i - 1] == '(':
#                 if (curSeq[i], 'S') not in curNode.descendants:
#                     newNode = TrieNode(False, 'S', curSeq[i], 0.0, False)
#                     curNode.descendants[(curSeq[i], 'S')] = newNode
#                 self.insertion(curNode.descendants[(curSeq[i], 'S')], curSeq, i + 1, support)
#             else:
#                 # print(i, 'I')
#                 if (curSeq[i], 'I') not in curNode.descendants:
#                     newNode = TrieNode(False, 'I', curSeq[i], 0.0, False)
#                     curNode.descendants[(curSeq[i], 'I')] = newNode
#                 self.insertion(curNode.descendants[(curSeq[i], 'I')], curSeq, i + 1, support)
#         return
#
#     def deletion(self, curNode, curSeq, i):
#         if i == len(curSeq) - 1:
#             curNode.supportValue = 0.0
#             curNode.marker = False
#             return
#         if curSeq[i] == '(' or curSeq[i] == ')':
#             self.deletion(curNode, curSeq, i + 1)
#         else:
#             if curSeq[i - 1] == '(':
#                 nextNode = curNode.descendants[(curSeq[i], 'I')]
#                 self.deletion(nextNode, i + 1)
#                 if len(nextNode.descendants) == 0:
#                     curNode.descendants.pop((curSeq[i], 'I'))
#             else:
#                 nextNode = curNode.descendants[(curSeq[i], 'S')]
#                 self.deletion(nextNode, i + 1)
#                 if len(nextNode.descendants) == 0:
#                     curNode.descendants.pop((curSeq[i], 'S'))
#         return
#
#     def updateTrie(self, curNode):
#
#         tmpDscnt = copy.deepcopy(curNode.descendants)
#         curNode.descendants = dict()
#         for dscntKey, dscntValue in tmpDscnt.items():
#             childs = self.updateTrie(dscntValue)
#             if childs > 0:
#                 curNode.descendants[dscntKey] = dscntValue
#
#         return len((curNode.descendants)) + curNode.marker
#
#     def trieIntoFile(self, curNode, curSeq):
#         if curNode.extnType == 'I' and curNode.label is not None:
#             curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
#         elif curNode.label is not None:
#             curSeq = curSeq + '(' + curNode.label + ')'
#         if curNode.marker:
#             curNode.updateflag = False
#             if curNode.supportValue + Parameters.eps >= Parameters.getMinExpSup():
#                 self.FSwhereToWrite.write(curSeq)
#                 self.FSwhereToWrite.write(' ')
#                 self.FSwhereToWrite.write(str(curNode.supportValue))
#                 self.FSwhereToWrite.write('\n')
#             else:
#                 self.SFSwhereToWrite.write(curSeq)
#                 self.SFSwhereToWrite.write(' ')
#                 self.SFSwhereToWrite.write(str(curNode.supportValue))
#                 self.SFSwhereToWrite.write('\n')
#
#         for dscnt in curNode.descendants.values():
#             self.trieIntoFile(dscnt, curSeq)
#         return
#
#     def trieIntoFilePS(self, curNode, curSeq):
#         if curNode.extnType == 'I' and curNode.label is not None:
#             curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
#         elif curNode.label is not None:
#             curSeq = curSeq + '(' + curNode.label + ')'
#         if curNode.marker:
#             self.FSwhereToWrite.write(curSeq)
#             self.FSwhereToWrite.write(' ')
#             self.FSwhereToWrite.write(str(curNode.supportValue))
#             self.FSwhereToWrite.write('\n')
#
#         for dscnt in curNode.descendants.values():
#             self.trieIntoFilePS(dscnt, curSeq)
#         return
#
#     def printFSSFS(self, curNode, curSeq):
#         if curNode.extnType == 'I' and curNode.label is not None:
#             curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
#         elif curNode.label is not None:
#             curSeq = curSeq + '(' + curNode.label + ')'
#         if curNode.marker:
#             print('Current Seg: '+ curSeq, " : ", curNode.supportValue )
#         for dscnt in curNode.descendants.values():
#             self.printFSSFS(dscnt, curSeq)
#         return
#
#     def printPFS(self, curNode, curSeq):
#         if curNode.extnType == 'I' and curNode.label is not None:
#             curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
#         elif curNode.label is not None:
#             curSeq = curSeq + '(' + curNode.label + ')'
#         if curNode.marker:
#             print(curSeq, " current seq with ", curNode.supportValue )
#         for dscnt in curNode.descendants.values():
#             self.printPFS(dscnt, curSeq)
#         return
#
#     def updateWithInsertion(self, curNode, curSeq, i, support):
#         if i == len(curSeq) - 1:
#             # print(i, ' Markedddddddddd', curSeq)
#             curNode.marker = True
#             curNode.updateflag = True
#             # print(curNode.supportValue, 'before updateing with insertion')
#             curNode.supportValue += float(support)
#             # print(curNode.supportValue, 'after updating with insertion')
#             return
#         if curSeq[i] == '(' or curSeq[i] == ')':
#             self.updateWithInsertion(curNode, curSeq, i + 1, support)
#         else:
#             if curSeq[i - 1] == '(':
#                 # print(i, 'S')
#                 if (curSeq[i], 'S') not in curNode.descendants.keys():
#                     newNode = TrieNode(False, 'S', curSeq[i], 0.0, False)
#                     curNode.descendants[(curSeq[i], 'S')] = newNode
#                 self.updateWithInsertion(curNode.descendants[(curSeq[i], 'S')], curSeq, i + 1, support)
#             else:
#                 # print(i, 'I')
#                 if (curSeq[i], 'I') not in curNode.descendants.keys():
#                     newNode = TrieNode(False, 'I', curSeq[i], 0.0, False)
#                     curNode.descendants[(curSeq[i], 'I')] = newNode
#                 self.updateWithInsertion(curNode.descendants[(curSeq[i], 'I')], curSeq, i + 1, support)
#         return
#
#     def updateWithlsTrieBuild(self, curNode, curSeq):
#         # print(curNode.label, ' ', curSeq, " innnnnnnn")
#         if curNode.extnType == 'I' and curNode.label is not None:
#             # curSeq = curSeq[:len(curSeq) - 1] + curNode.label + ')'
#             curSeq.pop()
#             curSeq.append(curNode.label)
#             curSeq.append(')')
#
#         elif curNode.label is not None:
#             # curSeq = curSeq + '(' + curNode.label + ')'
#             curSeq.append('(')
#             curSeq.append(curNode.label)
#             curSeq.append(')')
#
#         if curNode.marker is False and curNode.label is not None:
#             # print(curSeq, " current seq lsTrie ", curNode.label)
#             self.lsTrie.insertion(self.lsTrie.rootNode, copy.deepcopy(curSeq), 0, float(curNode.supportValue))
#         for dscnt in curNode.descendants.values():
#             self.updateWithlsTrieBuild(dscnt, copy.deepcopy(curSeq))
#         return
#
#     def deleteWholeTrie(self, curNode):
#         for dscnt in curNode.descendants.values():
#             self.deleteWholeTrie(dscnt)
#         curNode.descendants.clear()
#         return
#
#     def searchSupport(self, curNode, curSeq, i):
#         if i == len(curSeq)-1:
#             return curNode.supportValue
#         if curSeq[i] == '(' or curSeq[i] == ')':
#             return self.searchSupport(curNode, curSeq, i+1)
#         else:
#             if curSeq[i - 1] == '(':
#                 if (curSeq[i], 'S') in curNode.descendants:
#                     return self.searchSupport(curNode.descendants[(curSeq[i], 'S')], curSeq, i + 1)
#                 else:
#                     return 0.0
#             else:
#                 if (curSeq[i], 'I') in curNode.descendants:
#                     return self.searchSupport(curNode.descendants[(curSeq[i], 'I')], curSeq, i + 1)
#                 else:
#                     return 0.0


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
