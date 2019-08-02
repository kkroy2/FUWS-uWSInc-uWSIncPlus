import time

from Parameters.userDefined import UserDefined
from Parameters.FileInfo import FileInfo
from UtilityTechniques.DataPreProcessing import PreProcess
from UtilityTechniques.ProbabilityWeightAssign import WeightAssign
from Parameters.ProgramVariable import ProgramVariable
from UtilityTechniques.WAMCalculation import WAMCalculation
from Parameters.Variable import Variable
from FUWSequence.UWSequence import UWSequence
from DynamicTrie.IncrementalPreprocess import IncPreProcess
from UWSInc.uWSInc import uWSInc
from DynamicTrie.Trie import Trie, TrieNode


if __name__ == '__main__':
    # take file input
    # fname = '../sign/v0/sign_pp0.txt'
    # fname = '../Files/dataset.txt'
    fname = '../LEVIATHAN/v0/LEVIATHAN_v0_pp0.txt'

    UserDefined.min_sup = 0.1
    UserDefined.wgt_factor = 0.8
    FileInfo.set_initial_file_info(fname, '../Files/FS.txt', '../Files/SFS.txt')
    FileInfo.time_info = open('../Files/time_info.txt' , 'w')
    start_time = time.time()
    # preprocess the input file
    PreProcess().doProcess()
    # initialize the parameters
    previous_time = time.time()
    wgt_assign_obj = WeightAssign()
    wgt_assign_obj.assign(ProgramVariable.itemList)
    WAMCalculation.update_WAM()
    Variable.mu = 0.6

    Variable.size_of_dataset = len(ProgramVariable.uSDB)
    fsfss_trie_root_node = UWSequence().douWSequence()
    fsfss_trie = Trie(fsfss_trie_root_node)
    fsfss_trie.update_trie(fsfss_trie.root_node)
    fsfss_trie.trie_into_file(fsfss_trie.root_node, '')
    FileInfo.fs.write('\n \n')
    FileInfo.sfs.write('\n \n')
    prefix = '../LEVIATHAN/v0/LEVIATHAN_v0_pp'
    cur_time = time.time()
    FileInfo.time_info.write(str(cur_time-previous_time))
    FileInfo.time_info.write('\n')
    previous_time = time.time()

    uwsinc = uWSInc(fsfss_trie, )
    for i in range(1, 11):
        fname = prefix+str(i)+'.txt'
        IncPreProcess(fname).preProcess()
        # print(ProgramVariable.cnt_dic)
        # print(ProgramVariable.uSDB)
        # print(len(ProgramVariable.uSDB), ' At here uwsi')
        wgt_assign_obj.assign(ProgramVariable.itemList)
        WAMCalculation.update_WAM()
        uwsinc.uWSIncMethod()
        cur_time = time.time()
        FileInfo.time_info.write(str(cur_time - previous_time))
        FileInfo.time_info.write('\n')
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

    FileInfo.fs.close()
    FileInfo.sfs.close()
    end_time = time.time()
    print(start_time, end_time, end_time-start_time)
