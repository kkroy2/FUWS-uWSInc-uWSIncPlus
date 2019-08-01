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
    fname = '../Files/dataset.txt'
    UserDefined.min_sup = 0.2
    UserDefined.wgt_factor = .8
    FileInfo.set_initial_file_info(fname, '../Files/FS.txt', '../Files/SFS.txt')

    # preprocess the input file
    PreProcess().doProcess()
    # initialize the parameters
    start_time = time.time()
    wgt_assign_obj = WeightAssign()
    wgt_assign_obj.manual_assign()
    WAMCalculation.update_WAM()
    Variable.mu = 0.6

    Variable.size_of_dataset = len(ProgramVariable.uSDB)
    fsfss_trie_root_node = UWSequence().douWSequence()
    fsfss_trie = Trie(fsfss_trie_root_node)
    fsfss_trie.update_trie(fsfss_trie.root_node)
    fsfss_trie.trie_into_file(fsfss_trie.root_node, '')
    FileInfo.fs.write('\n \n')
    FileInfo.sfs.write('\n \n')
    prefix = '../Files/increment.txt'
    uwsinc = uWSInc(fsfss_trie, )
    # for i in range(1, 13):
    #     fname = prefix+str(i)+'.txt'
    IncPreProcess(prefix).preProcess()
        # print(ProgramVariable.uSDB)
        # print(len(ProgramVariable.uSDB), ' At here uwsi')
    wgt_assign_obj.assign(ProgramVariable.inc_itm_list)
    WAMCalculation.update_WAM()
    uwsinc.uWSIncMethod()
    FileInfo.fs.close()
    FileInfo.sfs.close()
    end_time = time.time()
    print(start_time, end_time, end_time-start_time)
