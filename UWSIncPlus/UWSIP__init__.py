import time

from Parameters.userDefined import UserDefined
from Parameters.FileInfo import FileInfo
from UtilityTechniques.DataPreProcessing import PreProcess
from UtilityTechniques.ProbabilityWeightAssign import WeightAssign
from Parameters.ProgramVariable import ProgramVariable
from UtilityTechniques.WAMCalculation import WAMCalculation
from Parameters.Variable import Variable
from FUWSequence.UWSequence import UWSequence
from UWSIncPlus.uWSIncPlus import uWSIncPlus
from DynamicTrie.Trie import Trie, TrieNode

if __name__ == '__main__':
    # take file input
    # fname = '../sign/v0/sign_pp0.txt'
    # fname = '../Files/dataset.txt'
    fname = '../LEVIATHAN/v0/LEVIATHAN_v0_pp0.txt'

    UserDefined.min_sup = 0.1
    UserDefined.wgt_factor = 0.8
    FileInfo.set_initial_file_info(fname, '../Files/FSplus.txt', '../Files/SFSplus.txt')
    FileInfo.ls = open('../Files/ls.txt', 'w')
    FileInfo.time_info = open('time_info_plus.txt', 'w')

    start_time = time.time()
    # preprocess the input file
    PreProcess().doProcess()
    # initialize the parameters
    previous_time = time.time()
    wgt_assign_obj = WeightAssign()
    wgt_assign_obj.assign(ProgramVariable.itemList)
    # wgt_assign_obj.manual_assign()
    WAMCalculation.update_WAM()
    Variable.mu = 0.6
    Variable.size_of_dataset = len(ProgramVariable.uSDB)
    fsfss_trie_root_node = UWSequence().douWSequence()
    fsfss_trie = Trie(fsfss_trie_root_node)
    fsfss_trie.update_trie(fsfss_trie.root_node)
    fsfss_trie.trie_into_file(fsfss_trie.root_node, '')

    cur_time = time.time()
    FileInfo.time_info.write(str(cur_time-previous_time))
    FileInfo.time_info.write('\n')
    ls_trie = Trie(TrieNode(False, None, None, 0.0, False))
    # prefix = '../sign/v0/sign_pp'
    prefix = '../LEVIATHAN/v0/LEVIATHAN_v0_pp'

    FileInfo.fs.write('\n \n')
    FileInfo.sfs.write('\n \n')
    previous_time = time.time()
    uwsincplus = uWSIncPlus(fsfss_trie, ls_trie)

    for i in range(1, 11):
        fname = prefix+str(i)+'.txt'
        FileInfo.initial_dataset = open(fname, 'r')
        # FileInfo.initial_dataset = open(prefix, 'r')
        PreProcess().doProcess()
        wgt_assign_obj.assign(ProgramVariable.itemList)
        # wgt_assign_obj.manual_assign()
        WAMCalculation.update_WAM()
        uwsincplus.uWSIncPlusMethod(UserDefined.min_sup*2)
        cur_time = time.time()
        FileInfo.time_info.write(str(cur_time-previous_time))
        FileInfo.time_info.write('\n')
        previous_time = time.time()
        print('Increment No. ', i)

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

    FileInfo.fs.close()
    FileInfo.sfs.close()
    FileInfo.ls.close()

    end_time = time.time()
    print(start_time, end_time, end_time-start_time)
