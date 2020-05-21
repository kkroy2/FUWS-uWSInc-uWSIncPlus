import time

from Parameters.userDefined import UserDefined
from Parameters.FileInfo import FileInfo
from UtilityTechniques.DataPreProcessing import PreProcess
from UtilityTechniques.ProbabilityWeightAssign import WeightAssign
from Parameters.ProgramVariable import ProgramVariable
from UtilityTechniques.WAMCalculation import WAMCalculation
from Parameters.Variable import Variable
from FUWSeq.FUWSequence import FUWSequence
from UtilityTechniques.DataPreProcessing import PreProcess
from UWSInc.uWSInc import uWSInc
from DynamicTrie.Trie import Trie, TrieNode
from UtilityTechniques.ThresholdCalculation import ThresholdCalculation


if __name__ == '__main__':
    # take file input
    # fname = '../sign/v0/sign_pp0.txt'
    # fname = '../Files/dataset.txt'

    prefix_all = '../SimulationAll'

    prefix = prefix_all + '/result/Inc'
    num_of_increment = 2

    UserDefined.min_sup = 0.2
    UserDefined.wgt_factor = 1.0
    Variable.mu = 0.7

    fname = prefix_all+'/initial.data'
    FileInfo.set_initial_file_info(fname, prefix+'/fs.txt', prefix+'/sfs.txt', prefix+'/pfs.txt')
    FileInfo.time_info = open(prefix_all+'/time_info_v05.txt', 'w')

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
    # print(len(ProgramVariable.uSDB))
    fsfss_trie_root_node , total_candidate = FUWSequence().douWSequence()
    fsfss_trie = Trie(fsfss_trie_root_node)
    fsfss_trie.update_trie(fsfss_trie.root_node)
    fsfss_trie.trie_into_file(fsfss_trie.root_node, '')
    FileInfo.fs.write('\n ----------- \n')
    FileInfo.sfs.write('\n ---------- \n')

    print('Threshold: ', round(ThresholdCalculation.get_wgt_exp_sup(), 2))

    cur_time = time.time()
    FileInfo.time_info.write(str(cur_time-previous_time))
    FileInfo.time_info.write('\n')
    inc_array = list()
    # FileInfo.fs.close()
    # FileInfo.fs = open(prefix_all + '/fs' + str(0) + '.txt', 'r')
    # count_fs = 0
    # for seq in FileInfo.fs:
    #     count_fs += 1
    # inc_array.append(count_fs)

    previous_time = time.time()
    # FileInfo.sfs.close()
    # FileInfo.fs.close()
    uwsinc = uWSInc(fsfss_trie, )
    for i in range(1, num_of_increment+1):
        # FileInfo.fs = open(prefix_all+'/fs'+str(i)+'.txt','w')
        # FileInfo.sfs = open(prefix_all+'/sfs'+str(i)+'.txt', 'w')
        fname = prefix_all+'/inc_'+str(i)+'.data'
        FileInfo.initial_dataset = open(fname, 'r')
        PreProcess().doProcess()

        print(Variable.size_of_dataset, ' Before')
        Variable.size_of_dataset += len(ProgramVariable.uSDB)
        print(Variable.size_of_dataset, ' After')
        wgt_assign_obj.assign(ProgramVariable.itemList)
        WAMCalculation.update_WAM()
        print(Variable.WAM, ' :WAM')
        print(round(ThresholdCalculation.get_wgt_exp_sup(),2), round(ThresholdCalculation.get_semi_wgt_exp_sup(),2), ' : Threshold')
        uwsinc.uWSIncMethod()

        cur_time = time.time()
        FileInfo.time_info.write(str(cur_time - previous_time))
        FileInfo.time_info.write('\n')

        # FileInfo.fs.close()
        # FileInfo.fs = open(prefix_all + '/fs' + str(i) + '.txt', 'r')
        # count_fs = 0
        # for seq in FileInfo.fs:
        #     count_fs += 1
        # inc_array.append(count_fs)

        previous_time = time.time()
        print('Increment No. ', i)

    #
    # fname = '../Files/increment.txt'
    # IncPreProcess(fname).preProcess()
    # print(ProgramVariable.cnt_dic)
    # # print(ProgramVariable.uSDB)
    # # print(len(ProgramVariable.uSDB), ' At here uwsi')
    # wgt_assign_obj.assign(ProgramVariable.itemList)
    # WAMCalculation.update_WAM()
    # uwsinc.uWSIncMethod()
    # cur_time = time.time()
    # FileInfo.time_info.write(str(cur_time - previous_time))
    # FileInfo.time_info.write('\n')
    # previous_time = time.time()
    # # print('Increment No. ', i)

        # FileInfo.fs.close()
        # FileInfo.sfs.close()
        FileInfo.fs.write('\n ----------- \n')
        FileInfo.sfs.write('\n ---------- \n')
    end_time = time.time()
    print(inc_array)
    print(round(ThresholdCalculation.get_wgt_exp_sup(), 2), round(ThresholdCalculation.get_semi_wgt_exp_sup(), 2), " at final round")
    print(start_time, end_time, end_time-start_time)
    FileInfo.time_info.close()