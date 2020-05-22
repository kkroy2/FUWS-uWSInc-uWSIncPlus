import time

from Parameters.userDefined import UserDefined
from Parameters.FileInfo import FileInfo
from UtilityTechniques.DataPreProcessing import PreProcess
from UtilityTechniques.ProbabilityWeightAssign import WeightAssign
from Parameters.ProgramVariable import ProgramVariable
from UtilityTechniques.WAMCalculation import WAMCalculation
from Parameters.Variable import Variable
from FUWSeq.FUWSequence import FUWSequence
from UWSIncPlus.uWSIncPlus import uWSIncPlus
from DynamicTrie.Trie import Trie, TrieNode


if __name__ == '__main__':

    # initialize user given parameters by default values.
    UserDefined.min_sup = 0.2
    UserDefined.wgt_factor = 1.0
    Variable.mu = 0.7

    # code to take input values for the parameters which are used in our proposed algorithm
    UserDefined.min_sup = float(input('Please enter minimum support(e.g. 0.2): '))
    UserDefined.wgt_factor = float(input('weight factor(e.g. 1.0): '))
    Variable.mu = float(input('and buffer ratio, mu(e.g. 0.70): '))

    # initialize file information where you wish to save the outputs of the algorithm
    prefix = '/result'
    fname = input('Enter the path for the data which has to be in specified format: ')
    FileInfo.set_initial_file_info(fname, prefix+'/fs.txt', prefix+'/sfs.txt', prefix+'/pfs.txt')
    FileInfo.ls = open(prefix+'/ls.txt', 'w')
    FileInfo.time_info = open(prefix+'/time_info_plus_v0.txt', 'w')

    # Set the number of increments
    num_of_increment = 2

    start_time = time.time()

    # Preprocess initial dataset in the way that is described in our algorithm
    PreProcess().doProcess()

    # Assign weights of all items. Here, we have provided two ways to do that-
    # one is to assign weight to each item manually
    # second to assign weights to all items using randomly generate weights following normal distribution
    previous_time = time.time()
    wgt_assign_obj = WeightAssign()
    wgt_assign_obj.assign(ProgramVariable.itemList)         # using generated weights
    # we provide a weight file named as 'weights.csv' in 'Files' folder.
    # You can change the file but make sure that you name the file exactly same as the given name

    # wgt_assign_obj.manual_assign()            # this is for manual way to assign weight

    # we provided a file named as 'manual_weights.txt' in 'Files' folder
    # In that file you can assign weight to each item manually. This is to inform you that
    # file contains an item and its weight separated by an space in each line
    # Don't forget to update accordingly if you wish

    # WAM will be calculated && DataBase size will be initialized
    WAMCalculation.update_WAM()
    Variable.size_of_dataset = len(ProgramVariable.uSDB)

    # Run FUWS algorithm to get FS and SFS from initial datasets and store store them into USeq-Trie
    fsfss_trie_root_node, total_candidates = FUWSequence().douWSequence()
    fsfss_trie = Trie(fsfss_trie_root_node)
    fsfss_trie.update_trie(fsfss_trie.root_node)
    fsfss_trie.trie_into_file(fsfss_trie.root_node, '')

    cur_time = time.time()
    FileInfo.time_info.write(str(cur_time-previous_time))
    FileInfo.time_info.write('\n')

    ls_trie = Trie(TrieNode(False, None, None, 0.0, False))         # Initialize the trie to store LFS

    FileInfo.fs.write('\n ----------- \n')
    FileInfo.sfs.write('\n ----------- \n')
    FileInfo.pfs.write('\n ----------- \n')
    FileInfo.ls.write('\n ----------- \n')

    previous_time = time.time()
    inc_array = list()
    count_fs = 0
    inc_array.append(count_fs)

    uwsincplus = uWSIncPlus(fsfss_trie, ls_trie)
    # FileInfo.fs.close()
    # FileInfo.sfs.close()
    # FileInfo.ls.close()

    for i in range(1, num_of_increment+1):
        # fname = prefix + '/inc_' + str(i) + '.data'
        fname = input("Enter the path for "+str('i')+'-th increment data: ', )
        FileInfo.initial_dataset = open(fname, 'r')

        PreProcess().doProcess()
        wgt_assign_obj.assign(ProgramVariable.itemList)

        # wgt_assign_obj.manual_assign()

        ProgramVariable.pre_upto_sum = WAMCalculation.upto_sum
        ProgramVariable.pre_upto_wSum = WAMCalculation.upto_wSum
        WAMCalculation.upto_wSum = 0.0
        WAMCalculation.upto_sum = 0.0

        WAMCalculation.update_WAM()

        ProgramVariable.pre_upto_sum += WAMCalculation.upto_sum
        ProgramVariable.pre_upto_wSum += WAMCalculation.upto_wSum
        WAMCalculation.upto_wSum = ProgramVariable.pre_upto_wSum
        WAMCalculation.upto_sum = ProgramVariable.pre_upto_sum

        uwsincplus.uWSIncPlusMethod(UserDefined.min_sup*2)

        cur_time = time.time()
        FileInfo.time_info.write(str(cur_time-previous_time))
        FileInfo.time_info.write('\n')

        FileInfo.fs.write('\n ----------- \n')
        FileInfo.sfs.write('\n ----------- \n')
        FileInfo.pfs.write('\n ----------- \n')
        FileInfo.ls.write('\n ----------- \n')

    end_time = time.time()
    FileInfo.time_info.close()