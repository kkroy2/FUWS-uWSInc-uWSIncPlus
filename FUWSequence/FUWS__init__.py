import time

from Parameters.Variable import Variable
from Parameters.FileInfo import FileInfo
from Parameters.userDefined import UserDefined
from UtilityTechniques.WAMCalculation import WAMCalculation
from UtilityTechniques.DataPreProcessing import PreProcess
from FUWSequence.UWSequence import UWSequence
from UtilityTechniques.ProbabilityWeightAssign import WeightAssign
from Parameters.ProgramVariable import ProgramVariable

if __name__ == '__main__':

    # initialize user given parameters
    UserDefined.min_sup = 0.2
    UserDefined.wgt_factor = 0.8

    # initialize file info
    FileInfo.initial_dataset = open('../Files/increment.txt', 'r')
    FileInfo.fs = open('../Files/initialFS.txt', 'w')
    FileInfo.sfs = open('../Files/initialSFS.txt', 'w')

    # Dataset Preprocessing
    PreProcess().doProcess()
    # for seq in ProgramVariable.pSDB:
    #     print(seq)

    print('Preprocess Done!')

    # Weight Assigning
    # WeightAssign.assign(ProgramVariable.itemList)
    WeightAssign.manual_assign()
    print('Weight Assign Done')

    #WAM calculation && DataBase size update
    WAMCalculation.update_WAM()
    Variable.mu = 0.6
    Variable.size_of_dataset = len(ProgramVariable.uSDB)
    print(Variable.size_of_dataset, ' size of dataset')
    print('WAM Done')
    start_time = time.time()
    UWSequence().douWSequence()
    
    FileInfo.fs.close()
    FileInfo.sfs.close()
    end_time = time.time()

    print(start_time, end_time, end_time-start_time)



