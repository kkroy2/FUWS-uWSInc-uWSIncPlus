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
    fname = '../sign/v0/sign_pp0.txt'

    UserDefined.min_sup = 0.4
    UserDefined.wgt_factor = 1
    FileInfo.set_initial_file_info(fname, '../Files/FS.txt', '../Files/SFS.txt')

    # preprocess the input file
    PreProcess().doProcess()
    # initialize the parameters
    wgt_assign_obj = WeightAssign()
    wgt_assign_obj.assign(ProgramVariable.itemList)
    WAMCalculation.update_WAM()
    Variable.mu = 0.8
    Variable.size_of_dataset = len(ProgramVariable.uSDB)
    fsfss_trie_root_node = UWSequence().douWSequence()
    fsfss_trie = Trie(fsfss_trie_root_node)
    prefix = '../sign/v0/sign_pp'

    uwsinc = uWSInc(fsfss_trie, )
    for i in range(1, 13):
        fname = prefix+str(i)+'.txt'
        IncPreProcess(fname).preProcess()
        print(ProgramVariable.uSDB)
        print(len(ProgramVariable.uSDB), ' At here uwsi')
        wgt_assign_obj.assign(ProgramVariable.inc_itm_list)
        WAMCalculation.update_WAM()
        uwsinc.uWSIncMethod()


