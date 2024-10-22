import time

from FUWS.FUWSequence import FUWSequence
from Parameters.Variable import Variable
from Parameters.FileInfo import FileInfo
from Parameters.userDefined import UserDefined
from UtilityTechniques.WAMCalculation import WAMCalculation
from UtilityTechniques.DataPreProcessing import PreProcess
from UtilityTechniques.ProbabilityWeightAssign import WeightAssign
from Parameters.ProgramVariable import ProgramVariable
from DynamicTrie.Trie import Trie

if __name__ == '__main__':

    # initialize user given parameters
    # UserDefined.min_sup = 0.7
    # UserDefined.wgt_factor = 0.8
    # Variable.mu = .75
    #
    # # initialize file info
    # # prefix = '../Files/Test'
    # # FileInfo.initial_dataset = open(prefix + '/sample.txt', 'r')
    # # FileInfo.fs = open(prefix + '/initialFS.txt', 'w')
    # # FileInfo.sfs = open(prefix + '/initialSFS.txt', 'w')
    #
    # prefix = '../Files/SIGN50'
    # FileInfo.initial_dataset = open(prefix + '/SIGN_sp.txt', 'r')
    # FileInfo.fs = open(prefix + '/initialFS.txt', 'w')
    # FileInfo.sfs = open(prefix + '/initialSFS.txt', 'w')
    #
    #
    # # Dataset Preprocessing
    # PreProcess().doProcess()
    # # for seq in ProgramVariable.pSDB:
    # #     print(seq, ' Print at Nothing')
    #
    # print('Preprocess Done!')
    #
    # # Weight Assigning
    # WeightAssign.assign(ProgramVariable.itemList)
    # # WeightAssign.manual_assign()
    # print('Weight Assign Done')
    #
    # #WAM calculation && DataBase size update
    # WAMCalculation.update_WAM()
    #
    # Variable.size_of_dataset = len(ProgramVariable.uSDB)
    # print(Variable.size_of_dataset, ' size of dataset')
    # print('WAM Done')
    # start_time = time.time()
    # root_node, total_candidates = UWSequence().douWSequence()
    # fssfs_trie = Trie(root_node)
    # # fssfs_trie.update_trie(fssfs_trie.root_node)
    # total_num_patterns = fssfs_trie.trie_into_file(fssfs_trie.root_node, '')
    #
    # FileInfo.fs.close()
    # FileInfo.sfs.close()
    # end_time = time.time()
    #
    # print('Total Candidates: ', total_candidates)
    # print('Total Patterns: ', total_num_patterns)
    # print('Total Times: ', start_time, end_time, end_time-start_time)

    # initialize user given parameters
    UserDefined.min_sup = 0.2
    UserDefined.wgt_factor = 1.0
    Variable.mu = 0.7

    # initialize file info
    prefix = 'result'
    FileInfo.initial_dataset = open('initial.data', 'r')
    FileInfo.fs = open(prefix + '/FS.txt', 'w')
    FileInfo.sfs = open(prefix + '/SFS.txt', 'w')
    FileInfo.pfs = open(prefix + '/pfs.txt', 'w')

    # Dataset Preprocessing
    PreProcess().doProcess()
    # for seq in ProgramVariable.pSDB:
    #     print(seq, ' Print at Nothing')

    print('Preprocess Done!')

    # Weight Assigning
    # WeightAssign.assign(ProgramVariable.itemList)
    WeightAssign.manual_assign()
    print('Weight Assign Done')

    # WAM calculation && DataBase size update
    WAMCalculation.update_WAM()

    Variable.size_of_dataset = len(ProgramVariable.uSDB)
    print(Variable.size_of_dataset, ' size of dataset')
    print('WAM Done')
    start_time = time.time()
    root_node, total_candidates = FUWSequence().douWSequence()
    fssfs_trie = Trie(root_node)
    fssfs_trie.update_trie(fssfs_trie.root_node)
    fssfs_trie.trie_into_file(fssfs_trie.root_node, '')

    FileInfo.fs.close()
    FileInfo.sfs.close()
    end_time = time.time()

    print(start_time, end_time, end_time - start_time)