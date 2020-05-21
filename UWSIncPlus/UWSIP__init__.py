import time

from Parameters.userDefined import UserDefined
from Parameters.FileInfo import FileInfo
from UtilityTechniques.ThresholdCalculation import ThresholdCalculation
from UtilityTechniques.DataPreProcessing import PreProcess
from UtilityTechniques.ProbabilityWeightAssign import WeightAssign
from Parameters.ProgramVariable import ProgramVariable
from UtilityTechniques.WAMCalculation import WAMCalculation
from Parameters.Variable import Variable
from FUWSeq.FUWSequence import FUWSequence
from UWSIncPlus.uWSIncPlus import uWSIncPlus
from DynamicTrie.Trie import Trie, TrieNode


if __name__ == '__main__':
    # take file input
    # fname = '../sign/v0/sign_pp0.txt'
    # fname = '../Files/dataset.txt'

    prefix_all = '../SimulationAll'

    prefix = prefix_all + '/result/Plus'
    num_of_increment = 2

    UserDefined.min_sup = 0.2
    UserDefined.wgt_factor = 1.0
    Variable.mu = 0.7

    fname = prefix_all+'/initial.data'
    FileInfo.set_initial_file_info(fname, prefix+'/fs.txt', prefix+'/sfs.txt', prefix+'/pfs.txt')
    FileInfo.ls = open(prefix+'/ls.txt', 'w')
    FileInfo.time_info = open(prefix_all+'/time_info_plus_v0.txt', 'w')

    start_time = time.time()

    # preprocess the input file
    PreProcess().doProcess()

    # initialize the parameters
    previous_time = time.time()
    wgt_assign_obj = WeightAssign()
    # wgt_assign_obj.assign(ProgramVariable.itemList)

    wgt_assign_obj.manual_assign()
    WAMCalculation.update_WAM()
    Variable.size_of_dataset = len(ProgramVariable.uSDB)

    fsfss_trie_root_node, total_candidates = FUWSequence().douWSequence()
    fsfss_trie = Trie(fsfss_trie_root_node)
    fsfss_trie.update_trie(fsfss_trie.root_node)
    fsfss_trie.trie_into_file(fsfss_trie.root_node, '')

    cur_time = time.time()
    FileInfo.time_info.write(str(cur_time-previous_time))
    FileInfo.time_info.write('\n')
    ls_trie = Trie(TrieNode(False, None, None, 0.0, False))
    print('Threshold: ', round(ThresholdCalculation.get_wgt_exp_sup(),2))
    # prefix = '../sign/v0/sign_pp'

    FileInfo.fs.write('\n ----------- \n')
    FileInfo.sfs.write('\n ----------- \n')
    FileInfo.pfs.write('\n ----------- \n')
    FileInfo.ls.write('\n ----------- \n')

    previous_time = time.time()
    inc_array = list()
    # FileInfo.fs.close()
    # FileInfo.fs = open(prefix_all + '/fsplus' + str(0) + '.txt', 'r')
    count_fs = 0
    # for seq in FileInfo/
    inc_array.append(count_fs)

    uwsincplus = uWSIncPlus(fsfss_trie, ls_trie)
    # FileInfo.fs.close()
    # FileInfo.sfs.close()
    # FileInfo.ls.close()

    for i in range(1, num_of_increment+1):
        fname = prefix_all + '/inc_' + str(i) + '.data'
        FileInfo.initial_dataset = open(fname, 'r')
        # FileInfo.fs = open(prefix_all+'/fsplus'+str(i)+'.txt', 'w')
        # FileInfo.sfs = open(prefix_all+'/sfsplus' + str(i) + '.txt', 'w')
        # FileInfo.ls = open(prefix_all+'/lsplus' + str(i) + '.txt', 'w')

        # FileInfo.initial_dataset = open(prefix, 'r')
        # if i == 1:
        #     ProgramVariable.pre_uSDB = ProgramVariable.uSDB

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
        #
        # if i == 1:
        #     # ProgramVariable.pre_uSDB = ProgramVariable.uSDB
        #     uwsincplus.onlyForFirstIncrement(UserDefined.min_sup*2)
        #     ProgramVariable.pre_uSDB = list()
        #
        # else:
        uwsincplus.uWSIncPlusMethod(UserDefined.min_sup*2)

        cur_time = time.time()
        FileInfo.time_info.write(str(cur_time-previous_time))
        FileInfo.time_info.write('\n')
        # FileInfo.fs.close()
        # FileInfo.fs = open(prefix_all + '/fsplus' + str(i) + '.txt', 'r')
        # count_fs = 0
        # for seq in FileInfo.fs:
        #     count_fs += 1
        # inc_array.append(count_fs)
        # previous_time = time.time()
        # print('Increment No. ', i)

    # fname = '../Files/increment.txt'
    # FileInfo.initial_dataset = open(fname, 'r')
    # # FileInfo.initial_dataset = open(prefix, 'r')
    # PreProcess().doProcess()
    # print(ProgramVariable.cnt_dic)
    # wgt_assign_obj.assign(ProgramVariable.itemList)
    # # wgt_assign_obj.manual_assign()
    # WAMCalculation.update_WAM()
    # uwsincplus.uWSIncPlusMethod()
    # cur_time = time.time()
    # FileInfo.time_info.write(str(cur_time-previous_time))
    # FileInfo.time_info.write('\n')
    # previous_time = time.time()
    # # print('Increment No. ', i)

        # FileInfo.fs.close()
        # FileInfo.sfs.close()
        # FileInfo.ls.close()
        FileInfo.fs.write('\n ----------- \n')
        FileInfo.sfs.write('\n ----------- \n')
        FileInfo.pfs.write('\n ----------- \n')
        FileInfo.ls.write('\n ----------- \n')

    end_time = time.time()
    print(inc_array)
    print(ThresholdCalculation.get_wgt_exp_sup(), ThresholdCalculation.get_semi_wgt_exp_sup(), " at final round")
    print(start_time, end_time, end_time-start_time)
    FileInfo.time_info.close()
    # while True:
    #     ok = 1