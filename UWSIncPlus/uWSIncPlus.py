from FUWSeq.FUWSequence import FUWSequence
from Parameters.Variable import Variable
from Parameters.ProgramVariable import ProgramVariable
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
        tmp_root_node, tot_candidates = FUWSequence().douWSequence()
        self.cur_ls_trie = Trie(tmp_root_node)

        # load and update upto threshold and the size of the dataset

        for i in range(0, len(ProgramVariable.uSDB)):
            self.fssfs_trie.update_support(self.fssfs_trie.root_node, None, 0.0, 0, i)

        previous_data_set += len(ProgramVariable.uSDB)
        ProgramVariable.uSDB = ProgramVariable.pre_uSDB
        for i in range(0, len(ProgramVariable.uSDB)):
            self.cur_ls_trie.update_support(self.cur_ls_trie.root_node, None, 0.0, 0, i)

        # Merging tries
        self.fssfs_trie.merge_ls_with_fssfs_trie(self.cur_ls_trie.root_node, self.fssfs_trie.root_node)
        self.cur_ls_trie = None

        # update tries
        self.fssfs_trie.traverse_trie(self.fssfs_trie.root_node)
        self.fssfs_trie.update_trie(self.fssfs_trie.root_node)

        UserDefined.min_sup = previous_threshold
        Variable.size_of_dataset = previous_data_set
        Variable.WAM = ProgramVariable.pre_upto_wSum/ProgramVariable.pre_upto_sum

        # writing tries to file
        self.fssfs_trie.trie_into_file(self.fssfs_trie.root_node, '')
        return

    def uWSIncPlusMethod(self, local_min_sup):

        # store upto threshold and the size of the dataset
        previous_threshold = UserDefined.min_sup
        previous_data_set = Variable.size_of_dataset

        # set the min_sup by given local min sup
        UserDefined.min_sup = local_min_sup
        Variable.size_of_dataset = len(ProgramVariable.uSDB)
        tmp_root_node, tot_candidates = FUWSequence().douWSequence()

        self.cur_ls_trie = Trie(tmp_root_node)
        self.cur_ls_trie.printFSSFS(self.cur_ls_trie.root_node, '')

        for i in range(0, len(ProgramVariable.uSDB)):
            self.fssfs_trie.update_support(self.fssfs_trie.root_node, None, 0.0, 0, i)

        # Merging tries
        self.fssfs_trie.merge_ls_with_fssfs_trie(self.cur_ls_trie.root_node, self.fssfs_trie.root_node)
        self.cur_ls_trie = None

        # update tries
        self.fssfs_trie.traverse_trie(self.fssfs_trie.root_node)
        self.fssfs_trie.update_trie(self.fssfs_trie.root_node)

        current_threshold = ThresholdCalculation.get_semi_wgt_exp_sup()

        UserDefined.min_sup = previous_threshold
        Variable.size_of_dataset = previous_data_set
        Variable.size_of_dataset += len(ProgramVariable.uSDB)
        Variable.WAM = ProgramVariable.pre_upto_wSum / ProgramVariable.pre_upto_sum

        # writing tries to file
        self.fssfs_trie.printPFS(self.fssfs_trie.root_node, '', ThresholdCalculation.get_semi_wgt_exp_sup(), current_threshold)
        self.fssfs_trie.trie_into_file(self.fssfs_trie.root_node, '')

        return

