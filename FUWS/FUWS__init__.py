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

    # initialize user given parameters by default values.
    UserDefined.min_sup = 0.2
    UserDefined.wgt_factor = 1.0
    Variable.mu = 0.70

    # code to take input values for the parameters which are used in our proposed algorithm
    UserDefined.min_sup = float(input('Please enter minimum support(e.g. 0.2): '))
    UserDefined.wgt_factor = float(input('weight factor(e.g. 1.0): '))
    Variable.mu = float(input('and buffer ratio, mu(e.g. 0.70): '))

    print('----------------------------------------------------------------')

    # initialize file information where you wish to save the outputs of the algorithm
    prefix = '/result'

    data_path = input('Enter the path for the data which has to be in specified format: ')
    FileInfo.initial_dataset = open(data_path, 'r')             # Open the dataset file
    FileInfo.fs = open(prefix + '/FS.txt', 'w')                 # file will be used to save FS
    FileInfo.sfs = open(prefix + '/SFS.txt', 'w')               # to save SFS

    # Preprocess dataset in the way that is described in our algorithm
    PreProcess().doProcess()

    # Assign weights of all items. Here, we have provided two ways to do that-
    # one is to assign weight to each item manually
    # second to assign weights to all items using randomly generate weights following normal distribution

    WeightAssign.assign(ProgramVariable.itemList)               # using generated weights

    # we provide a weight file named as 'weights.csv' in 'Files' folder.
    # You can change the file but make sure that you name the file exactly same as the given name

    WeightAssign.manual_assign()        # this is for manual way to assign weight

    # we provided a file named as 'manual_weights.txt' in 'Files' folder
    # In that file you can assign weight to each item manually. This is to inform you that
    # file contains an item and its weight separated by an space in each line
    # Don't forget to update accordingly if you wish

    # WAM will be calculated && DataBase size will be been updated

    WAMCalculation.update_WAM()
    Variable.size_of_dataset = len(ProgramVariable.uSDB)

    start_time = time.time()

    root_node, total_candidates = FUWSequence().douWSequence()      # To find the potential candidate patterns

    fssfs_trie = Trie(root_node)                                    # Patterns are stored into USeq-Trie

    fssfs_trie.update_trie(fssfs_trie.root_node)                    # calculate actual WES and remove false patterns

    fssfs_trie.trie_into_file(fssfs_trie.root_node, '')             # write the desired patterns (FS & SFS) into files

    FileInfo.fs.close()
    FileInfo.sfs.close()

    end_time = time.time()

    print('Total required time(in Seconds): ', end_time-start_time)



