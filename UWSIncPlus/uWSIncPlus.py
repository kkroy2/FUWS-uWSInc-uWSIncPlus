from FUWSequence.UWSequence import UWSequence
from Parameters.Variable import Variable
from Parameters.ProgramVariable import ProgramVariable
from Parameters.FileInfo import FileInfo
from DynamicTrie.Trie import Trie
from Parameters.userDefined import UserDefined


class uWSIncPlus():
    uWSeq = None
    fssfs_trie = None
    cur_ls_trie = None
    pre_ls_trie =None

    def __init__(self, fssfstrie, lstrie):
        self.fssfs_trie = fssfstrie
        self.pre_ls_trie = lstrie
        return

    def uWSIncPlusMethod(self):
        # initialize the threshold for finding the local set of frequent sequences
        previous_threshold = UserDefined.min_sup
        UserDefined.min_sup = UserDefined.min_sup*1.5
        previous_data_set = Variable.size_of_dataset
        Variable.size_of_dataset = len(ProgramVariable.uSDB)
        self.cur_ls_trie = Trie(UWSequence().douWSequence())
        # print(self.cur_ls_trie.root_node, ' get root node at uwsincPls')
        # self.cur_ls_trie.printPFS(self.cur_ls_trie.root_node,'')
        UserDefined.min_sup = previous_threshold
        Variable.size_of_dataset = previous_data_set
        Variable.size_of_dataset += len(ProgramVariable.uSDB)

        for i in range(0 , len(ProgramVariable.uSDB)):
            self.fssfs_trie.update_support(self.fssfs_trie.root_node, None, 0.0, i)

        # print(' Before merging two ls trie............ \n \n')
        # self.cur_ls_trie.printPFS(self.cur_ls_trie.root_node, '')

        self.cur_ls_trie.merge_two_ls_trie(self.pre_ls_trie.root_node, self.cur_ls_trie.root_node)
        # print(' After merging two ls trie............ \n ')
        # self.cur_ls_trie.printPFS(self.cur_ls_trie.root_node, '')
        # print('\n Print done \n')
        self.fssfs_trie.merge_ls_with_fssfs_trie(self.cur_ls_trie.root_node, self.fssfs_trie.root_node)

        self.fssfs_trie.traverse_trie(self.fssfs_trie.root_node)
        self.fssfs_trie.cur_ls_trie = self.cur_ls_trie
        self.fssfs_trie.updateWithlsTrieBuild(self.fssfs_trie.root_node, [])

        self.cur_ls_trie.update_trie(self.cur_ls_trie.root_node)
        # self.fssfs_trie.update_trie(self.fssfs_trie.root_node)
        self.fssfs_trie.trie_into_file(self.fssfs_trie.root_node, '')
        FileInfo.fs.write('\n \n')
        FileInfo.sfs.write('\n \n')

        # self.cur_ls_trie.printPFS(self.cur_ls_trie.root_node, '')
        # print(" finally got the ls trie ")
        self.cur_ls_trie.trieIntoFilePS(self.cur_ls_trie.root_node, '')
        FileInfo.ls.write('\n \n')
        self.pre_ls_trie = self.cur_ls_trie

        return

