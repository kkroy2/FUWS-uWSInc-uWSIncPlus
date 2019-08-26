import time

from Parameters.Variable import Variable
from Parameters.FileInfo import FileInfo
from Parameters.userDefined import UserDefined
from UtilityTechniques.ThresholdCalculation import ThresholdCalculation
from UtilityTechniques.WAMCalculation import WAMCalculation
from UtilityTechniques.DataPreProcessing import PreProcess
from FUWSequence.FUWSequence import FUWSequence
from UtilityTechniques.ProbabilityWeightAssign import WeightAssign
from Parameters.ProgramVariable import ProgramVariable
from DynamicTrie.Trie import Trie


def update_database(saveFROM, saveTO):
    with open(saveFROM,"r") as sf, open(saveTO,"a") as st:
        for line in sf:
            st.write(line)


def update_database_init(saveFROM, saveTO):
    with open(saveFROM,"r") as sf, open(saveTO,"w") as st:
        for line in sf:
            st.write(line)


if __name__ == '__main__':
    # initialize user given parameters
    prefix_all = '../retail_partitioned/retail_p20_4'
    number_of_increment = 5

    UserDefined.min_sup = 0.0025
    UserDefined.wgt_factor = 0.8
    Variable.mu = 0.5

    FileInfo.time_info = open(prefix_all+'/time_info_naive.txt', 'w')
    start_time = time.time()
    previous_usdb = []
    previous_psdb = []
    inc_array = list()
    for i in range(0, number_of_increment):
    # initialize file info
        previous_time = time.time()
        FileInfo.initial_dataset = open(prefix_all+'/retail_'+str(i)+'.txt', 'r')
        FileInfo.fs = open(prefix_all+'/fs_naive'+str(i)+'.txt', 'w')
        FileInfo.sfs = open(prefix_all+'/sfs_naive'+str(i)+'.txt', 'w')

    # Dataset Preprocessing
        PreProcess().doProcess()

        WeightAssign.assign(ProgramVariable.itemList)

        #WAM calculation && DataBase size update
        WAMCalculation.update_WAM()

        Variable.size_of_dataset += len(ProgramVariable.uSDB)
        print(Variable.size_of_dataset, ' : Size of dataset')
        ProgramVariable.uSDB += previous_usdb
        ProgramVariable.pSDB += previous_psdb
        print(len(ProgramVariable.pSDB), ' : check the value with previous one')
        # print()
        print('WAM: ', Variable.WAM)
        print('Threshold: ', ThresholdCalculation.get_wgt_exp_sup(), ThresholdCalculation.get_semi_wgt_exp_sup(), ' at uWSeq')
        root_node = FUWSequence().douWSequence()
        fssfs_trie = Trie(root_node)
        fssfs_trie.update_trie(fssfs_trie.root_node)
        fssfs_trie.trie_into_file(fssfs_trie.root_node, '')

        FileInfo.fs.close()
        FileInfo.sfs.close()

        end_time = time.time()
        FileInfo.time_info.write(str(end_time-previous_time))
        FileInfo.time_info.write('\n')
        previous_psdb = ProgramVariable.pSDB
        previous_usdb = ProgramVariable.uSDB
        print('Increment No', i)
        FileInfo.fs = open(prefix_all + '/fs_naive' + str(i) + '.txt', 'r')
        count_fs = 0
        for seq in FileInfo.fs:
            count_fs += 1
        inc_array.append(count_fs)

    end_time = time.time()
    print(inc_array)
    print(ThresholdCalculation.get_wgt_exp_sup(), ThresholdCalculation.get_semi_wgt_exp_sup(), " at final round")
    print(start_time, end_time, end_time-start_time)



