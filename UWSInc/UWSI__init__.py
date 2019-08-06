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

    prefix_all = '../Files/FIFA80/v2'
    prefix = prefix_all + '/FIFA80_p'
    num_of_increment = 10

    UserDefined.min_sup = 0.08
    UserDefined.wgt_factor = 0.8
    Variable.mu = 0.75

    fname = prefix+'0.txt'
    FileInfo.set_initial_file_info(fname, prefix_all+'/fs05.txt', prefix_all+'/sfs05.txt')
    FileInfo.time_info = open(prefix_all+'/time_info_v05.txt', 'w')

    start_time = time.time()
    # preprocess the input file
    PreProcess().doProcess()
    # initialize the parameters
    previous_time = time.time()
    wgt_assign_obj = WeightAssign()
    wgt_assign_obj.assign(ProgramVariable.itemList)
    WAMCalculation.update_WAM()

    Variable.size_of_dataset = len(ProgramVariable.uSDB)
    # print(len(ProgramVariable.uSDB))
    fsfss_trie_root_node = UWSequence().douWSequence()
    fsfss_trie = Trie(fsfss_trie_root_node)
    fsfss_trie.update_trie(fsfss_trie.root_node)
    fsfss_trie.trie_into_file(fsfss_trie.root_node, '')
    FileInfo.fs.write('\n \n')
    FileInfo.sfs.write('\n \n')


    cur_time = time.time()
    FileInfo.time_info.write(str(cur_time-previous_time))
    FileInfo.time_info.write('\n')
    previous_time = time.time()
    FileInfo.sfs.close()
    FileInfo.fs.close()
    uwsinc = uWSInc(fsfss_trie, )
    for i in range(1, num_of_increment):
        FileInfo.fs = open(prefix_all+'/fs'+str(i)+'.txt','w')
        FileInfo.sfs = open(prefix_all+'/sfs'+str(i)+'.txt', 'w')
        fname = prefix+str(i)+'.txt'

        IncPreProcess(fname).preProcess()
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
    FileInfo.time_info.close()