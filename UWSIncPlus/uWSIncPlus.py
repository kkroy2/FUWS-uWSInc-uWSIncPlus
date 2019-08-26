from FUWSequence.FUWSequence import FUWSequence
from Parameters.Variable import Variable
from Parameters.ProgramVariable import ProgramVariable
from Parameters.FileInfo import FileInfo
from DynamicTrie.Trie import Trie
from Parameters.userDefined import UserDefined
from UtilityTechniques.ThresholdCalculation import ThresholdCalculation


class uWSIncPlus():
    uWSeq = None
    fssfs_trie = None
    cur_ls_trie = None
    pre_ls_trie =None

    def __init__(self, fssfstrie, lstrie):
        self.fssfs_trie = fssfstrie
        self.pre_ls_trie = lstrie
        return

    def onlyForFirstIncrement(self, local_min_sup):
        previous_threshold = UserDefined.min_sup
        previous_data_set = Variable.size_of_dataset

        # set the min_sup by given local min sup
        UserDefined.min_sup = local_min_sup
        Variable.size_of_dataset = len(ProgramVariable.uSDB)
        self.cur_ls_trie = Trie(FUWSequence().douWSequence())

        # load and update upto threshold and the size of the dataset

        for i in range(0, len(ProgramVariable.uSDB)):
            self.fssfs_trie.update_support(self.fssfs_trie.root_node, None, 0.0, 0, i)

        print(self.cur_ls_trie.printPFS(self.cur_ls_trie.root_node, ''), ' : Before update')
        previous_data_set += len(ProgramVariable.uSDB)
        ProgramVariable.uSDB = ProgramVariable.pre_uSDB
        for i in range(0, len(ProgramVariable.uSDB)):
            self.cur_ls_trie.update_support(self.cur_ls_trie.root_node, None, 0.0, 0, i)

        print(self.cur_ls_trie.printPFS(self.cur_ls_trie.root_node, ''), ' : After update')

        # Merging tries
        # self.cur_ls_trie.merge_pre_ls_trie_with_fssfs(self.pre_ls_trie.root_node, self.cur_ls_trie.root_node)
        self.fssfs_trie.merge_ls_with_fssfs_trie(self.cur_ls_trie.root_node, self.fssfs_trie.root_node)
        self.cur_ls_trie = None

        # update tries
        self.fssfs_trie.traverse_trie(self.fssfs_trie.root_node)
        self.fssfs_trie.update_trie(self.fssfs_trie.root_node)
        # self.fssfs_trie.cur_ls_trie = self.cur_ls_trie
        # self.fssfs_trie.updateWithlsTrieBuild(self.fssfs_trie.root_node, [])
        # self.cur_ls_trie.update_trie(self.cur_ls_trie.root_node)

        UserDefined.min_sup = previous_threshold
        Variable.size_of_dataset = previous_data_set
        Variable.WAM = ProgramVariable.pre_upto_wSum/ProgramVariable.pre_upto_sum

        # Variable.size_of_dataset += len(ProgramVariable.uSDB)

        # writing tries to file
        self.fssfs_trie.trie_into_file(self.fssfs_trie.root_node, '')
        # FileInfo.fs.write('\n \n')
        # FileInfo.sfs.write('\n \n')
        return

    def uWSIncPlusMethod(self, local_min_sup):

        # store upto threshold and the size of the dataset
        previous_threshold = UserDefined.min_sup
        previous_data_set = Variable.size_of_dataset

        # set the min_sup by given local min sup
        UserDefined.min_sup = local_min_sup
        Variable.size_of_dataset = len(ProgramVariable.uSDB)
        self.cur_ls_trie = Trie(FUWSequence().douWSequence())

        for i in range(0, len(ProgramVariable.uSDB)):
            self.fssfs_trie.update_support(self.fssfs_trie.root_node, None, 0.0, 0, i)

        # Merging tries
        self.fssfs_trie.merge_ls_with_fssfs_trie(self.cur_ls_trie.root_node, self.fssfs_trie.root_node)
        self.cur_ls_trie = None

        # update tries
        self.fssfs_trie.traverse_trie(self.fssfs_trie.root_node)
        self.fssfs_trie.update_trie(self.fssfs_trie.root_node)

        UserDefined.min_sup = previous_threshold
        Variable.size_of_dataset = previous_data_set
        Variable.size_of_dataset += len(ProgramVariable.uSDB)
        Variable.WAM = ProgramVariable.pre_upto_wSum / ProgramVariable.pre_upto_sum
        print('Database size at this point: ', Variable.size_of_dataset)
        print('WAM: ', Variable.WAM)
        # writing tries to file
        print('Threshold: ', ThresholdCalculation.get_wgt_exp_sup(), ThresholdCalculation.get_semi_wgt_exp_sup(),
              ' at uWSeq')
        self.fssfs_trie.trie_into_file(self.fssfs_trie.root_node, '')

        return

