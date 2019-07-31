from Parameters.userDefined import UserDefined
from Parameters.FileInfo import FileInfo
from UtilityTechniques.DataPreProcessing import PreProcess
from UtilityTechniques.ProbabilityWeightAssign import WeightAssign
from Parameters.ProgramVariable import ProgramVariable
from UtilityTechniques.WAMCalculation import WAMCalculation
from Parameters.Variable import Variable
from FUWSequence.UWSequence import UWSequence
from DynamicTrie.IncrementalPreprocess import IncPreProcess
from UWSIncPlus.uWSIncPlus import uWSIncPlus
from DynamicTrie.Trie import Trie, TrieNode

if __name__ == '__main__':
    # take file input
    fname = '../sign/v0/sign_pp0.txt'

    UserDefined.min_sup = 0.4
    UserDefined.wgt_factor = 1
    FileInfo.set_initial_file_info(fname, '../Files/FSplus.txt', '../Files/SFSplus.txt')
    FileInfo.ls = open('../Files/ls.txt', 'w')

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
    ls_trie = Trie(TrieNode(False, None, None, 0.0, False))
    prefix = '../sign/v0/sign_pp'

    uwsincplus = uWSIncPlus(fsfss_trie, ls_trie)

    for i in range(1, 13):
        fname = prefix+str(i)+'.txt'
        FileInfo.initial_dataset = open(fname, 'r')
        PreProcess().doProcess()
        wgt_assign_obj.assign(ProgramVariable.itemList)
        WAMCalculation.update_WAM()
        uwsincplus.uWSIncPlusMethod()

    FileInfo.fs.close()
    FileInfo.sfs.close()
    FileInfo.ls.close()

