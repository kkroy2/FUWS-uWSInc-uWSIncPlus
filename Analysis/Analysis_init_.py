import time
from DynamicTrie.IncrementalPreprocess import IncPreProcess
from UWSInc.uWSInc import uWSInc
from Parameters.userDefined import UserDefined
from Parameters.FileInfo import FileInfo
from UtilityTechniques.ThresholdCalculation import ThresholdCalculation
from UtilityTechniques.DataPreProcessing import PreProcess
from UtilityTechniques.ProbabilityWeightAssign import WeightAssign
from Parameters.ProgramVariable import ProgramVariable
from UtilityTechniques.WAMCalculation import WAMCalculation
from Parameters.Variable import Variable
from FUWSeq.FUWSequence import FUWSequence as UWSequence
from UWSIncPlus.uWSIncPlus import uWSIncPlus
from DynamicTrie.Trie import Trie, TrieNode
import os, errno, math, random


def ffopen(fileLocation, mode, title=None):
    # if not os.path.exists(os.path.dirname(fileLocation)):
    if not os.path.exists(fileLocation):
        try:
            os.makedirs(os.path.dirname(fileLocation))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
        f = open(fileLocation, mode)
        if title is not None:
            f.write(title)
        f.close()


    f = open(fileLocation, mode)
    return f


if __name__ == '__main__':

    dataset_name = input('dataset name (eg. sign):').strip()
    input_folder = '../' + input('input folder (relative path): ').strip() #+'Files/sign/sign_50_5'.
    # outputFolder = '../Files/result' #'/home/hhmoon/Desktop/Dataset for use/Result'

    threshold = []
    for i in range(0,5):
        threshold.append(float(input('theshold'+str(i)+':')))

    mu = [0.8,.7,.6, 0.5]
    wghtFact = [1.2, 1.0, 0.8, 0.5]

    # input_folder = input('Input File (Relative Path like Files/sign/sign_20_3): ')
    # input_folder = '../'+input_folder+'/'


    prefix = '/' + dataset_name + '_'
    p0 = int(input_folder.split('_')[1])
    nInc = int(input_folder.split('_')[2])
    num_of_files = nInc + 1
    print(p0, num_of_files)

    # outputFolder = input('summary output folder: ')
    # outputFolder = outputFolder + '/'
    parts = input_folder.split('/')
    lastpart = parts[len(parts) - 1]
    parts.remove(lastpart)
    outputFolder = '/'.join(parts)

    f_sumname = outputFolder + '/' + dataset_name + '_summary' + '.csv'

    title = 'sl,p0,nInc,' \
            'minsup,mu,wf,minWExSup,' \
            'time-n,time-i,time-p,' \
            'pat-n,pat-i,pat-p' \
            '\n'
    f_sum = ffopen(f_sumname, 'a',title)

    f_detname = input_folder + '/' + dataset_name + '_details' + '.csv'

    title = 'sl,p0,nInc,' \
            'minsup,mu,wf,' \
            'inc_no,' \
            'time-n,time-i,time-p,' \
            'pat-n,pat-i,pat-p' \
            '\n'
    f_det = ffopen(f_detname, 'a',title)

    f_sum.close()
    f_det.close()



    for th in threshold:
        for m in mu:
            for w in wghtFact:
                print('_____________',th, m, w)
                f_sum = open(f_sumname,'a')
                f_det = open(f_detname,'a')

                UserDefined.min_sup = th
                Variable.mu = m
                UserDefined.wgt_factor = w

                times0 = []
                patterns0 = []
                times1 = []
                patterns1 = []
                times2 = []
                patterns2 = []
                final_minWExSup = ThresholdCalculation.get_wgt_exp_sup()

                # _______naive____________####################
                print('naive')

                previous_usdb = []
                previous_psdb = []
                Variable.size_of_dataset = 0

                for i in range(0, num_of_files):
                    # initialize file info
                    previous_time = time.time()
                    # f = ffopen(input_folder + '/result/hudaiBUTdorkar.txt','w')
                    # f.close()
                    FileInfo.initial_dataset = ffopen(input_folder + prefix + str(i) + '.txt', 'r')
                    FileInfo.fs = ffopen(input_folder + '/result/fs_naive' + str(i) + '.txt', 'w')
                    FileInfo.sfs = ffopen(input_folder + '/result/sfs_naive' + str(i) + '.txt', 'w')

                    # Dataset Preprocessing
                    PreProcess().doProcess()


                    WeightAssign.assign(ProgramVariable.itemList)
                    # WAM calculation && DataBase size update
                    WAMCalculation.upto_sum = 0
                    WAMCalculation.upto_wSum = 0
                    WAMCalculation.update_WAM()

                    Variable.size_of_dataset += len(ProgramVariable.uSDB)
                    ProgramVariable.uSDB += previous_usdb
                    ProgramVariable.pSDB += previous_psdb

                    root_node = UWSequence().douWSequence()
                    fssfs_trie = Trie(root_node)
                    fssfs_trie.update_trie(fssfs_trie.root_node)
                    fssfs_trie.trie_into_file(fssfs_trie.root_node, '')

                    FileInfo.fs.close()
                    FileInfo.sfs.close()

                    cnt = 0
                    f = open(input_folder + '/result/fs_naive' + str(i) + '.txt', 'r')
                    for line in f:
                        if line == '\n' or line.strip() == '':
                            break
                        cnt += 1
                    patterns0.append(cnt)
                    f.close()

                    end_time = time.time()
                    t = end_time - previous_time
                    times0.append(round(t,4))

                    previous_psdb = ProgramVariable.pSDB
                    previous_usdb = ProgramVariable.uSDB

                    # print(i,'done')
                final_minWExSup = ThresholdCalculation.get_wgt_exp_sup()
                print('baseline: ', round(final_minWExSup,3), round(sum(times0),4),patterns0[len(patterns0)-1])

                # ________uWSInc_________-###################
                print('uWSInc')

                initFile = prefix + '0.txt'

                fname = input_folder + initFile
                FileInfo.set_initial_file_info(fname, input_folder + '/result/uWSI_fs0.txt',
                                               input_folder + '/result/uWSI_sfs0.txt')

                previous_time = time.time()
                # preprocess the input file
                PreProcess().doProcess()
                # initialize the parameters
                WAMCalculation.upto_sum = 0
                WAMCalculation.upto_wSum = 0

                wgt_assign_obj = WeightAssign()
                wgt_assign_obj.assign(ProgramVariable.itemList)
                WAMCalculation.update_WAM()

                Variable.size_of_dataset = len(ProgramVariable.uSDB)
                fsfss_trie_root_node = UWSequence().douWSequence()
                fsfss_trie = Trie(fsfss_trie_root_node)
                fsfss_trie.update_trie(fsfss_trie.root_node)
                fsfss_trie.trie_into_file(fsfss_trie.root_node, '')

                FileInfo.sfs.close()
                FileInfo.fs.close()

                cur_time = time.time()
                t = cur_time - previous_time

                times1.append(round(t,4))

                # print('init done')

                cnt = 0
                f = open(input_folder + '/result/uWSI_fs0.txt', 'r')
                for line in f:
                    if line == '\n' or line.strip() == '':
                        break
                    cnt += 1
                patterns1.append(cnt)
                f.close()

                uwsinc = uWSInc(fsfss_trie, )

                for i in range(1, num_of_files):
                    FileInfo.fs = open(input_folder + '/result/uWSI_fs' + str(i) + '.txt', 'w')
                    FileInfo.sfs = open(input_folder + '/result/uWSI_sfs' + str(i) + '.txt', 'w')
                    fname = input_folder + prefix + str(i) + '.txt'

                    previous_time = time.time()

                    IncPreProcess(fname).preProcess()
                    wgt_assign_obj.assign(ProgramVariable.itemList)
                    WAMCalculation.update_WAM()

                    uwsinc.uWSIncMethod()

                    cur_time = time.time()
                    t = cur_time - previous_time
                    times1.append(round(t,4))

                    FileInfo.fs.close()
                    FileInfo.sfs.close()

                    cnt = 0
                    f = open(input_folder + '/result/uWSI_fs' + str(i) + '.txt', 'r')
                    for line in f:
                        if line == '\n' or line.strip() == '':
                            break
                        cnt += 1
                    patterns1.append(cnt)
                    f.close()

                    # print(i, 'done')

                print('uWSInc: ',round(ThresholdCalculation.get_wgt_exp_sup(),3), round(sum(times1),4), patterns1[len(patterns1) - 1])

                # uWSInc+##################
                print('uWSInc+')

                fname = input_folder + initFile
                FileInfo.set_initial_file_info(fname, input_folder + '/result/uWSIP_fs0.txt',
                                               input_folder + '/result/uWSIP_sfs0.txt')
                FileInfo.ls = open(input_folder + '/result/uWSIP_ls0.txt', 'w')

                previous_time = time.time()

                PreProcess().doProcess()

                # initialize the parameters
                WAMCalculation.upto_sum = 0
                WAMCalculation.upto_wSum = 0
                wgt_assign_obj = WeightAssign()
                wgt_assign_obj.assign(ProgramVariable.itemList)

                WAMCalculation.update_WAM()
                Variable.size_of_dataset = len(ProgramVariable.uSDB)

                fsfss_trie_root_node = UWSequence().douWSequence()
                fsfss_trie = Trie(fsfss_trie_root_node)
                fsfss_trie.update_trie(fsfss_trie.root_node)
                fsfss_trie.trie_into_file(fsfss_trie.root_node, '')

                cur_time = time.time()
                t = cur_time - previous_time
                ls_trie = Trie(TrieNode(False, None, None, 0.0, False))

                FileInfo.fs.close()
                FileInfo.sfs.close()
                FileInfo.ls.close()

                uwsincplus = uWSIncPlus(fsfss_trie, ls_trie)

                times2.append(round(t,4))

                cnt = 0
                f = open(input_folder + '/result/uWSIP_fs0.txt', 'r')
                for line in f:
                    if line == '\n' or line.strip() == '':
                        break
                    cnt += 1
                patterns2.append(cnt)
                f.close()

                for i in range(1, num_of_files):
                    fname = input_folder + prefix + str(i) + '.txt'
                    FileInfo.initial_dataset = open(fname, 'r')
                    FileInfo.fs = open(input_folder + '/result/uWSIP_fs' + str(i) + '.txt', 'w')
                    FileInfo.sfs = open(input_folder + '/result/uWSIP_sfs' + str(i) + '.txt', 'w')
                    FileInfo.ls = open(input_folder + '/result/uWSIP_ls' + str(i) + '.txt', 'w')

                    previous_time = time.time()
                    # FileInfo.initial_dataset = open(prefix, 'r')
                    PreProcess().doProcess()
                    wgt_assign_obj.assign(ProgramVariable.itemList)
                    # wgt_assign_obj.manual_assign()
                    WAMCalculation.update_WAM()
                    uwsincplus.uWSIncPlusMethod(UserDefined.min_sup * 2)

                    cur_time = time.time()
                    t = cur_time - previous_time
                    times2.append(round(t,4))

                    FileInfo.fs.close()
                    FileInfo.sfs.close()
                    FileInfo.ls.close()

                    cnt = 0
                    f = open(input_folder + '/result/uWSIP_fs' + str(i) + '.txt', 'r')
                    for line in f:
                        if line == '\n' or line.strip() == '':
                            break
                        cnt += 1
                    patterns2.append(cnt)
                    f.close()

                    # print(i, 'done')

                print('uWSInc+: ',round(ThresholdCalculation.get_wgt_exp_sup(),3), round(sum(times2),4), patterns2[len(patterns2) - 1])

                ##____data collection###########

                # buf = 'sl,p0,nInc,' \
                #       'minsup,mu,wf,' \
                #       'time-n,time-i,time-p,' \
                #       'pat-n,pat-i,pat-p' \
                #       '\n'

                data = ['-', p0, nInc, th, m, w,final_minWExSup, round(sum(times0),4), round(sum(times1),4), round(sum(times2),4),
                        patterns0[len(patterns0) - 1], patterns1[len(patterns1) - 1], patterns2[len(patterns2) - 1]]
                buffer = [str(d) for d in data]
                buf = ','.join(buffer) + '\n'
                f_sum.write(buf)

                # buf = 'sl,p0,nInc,' \
                #       'minsup,mu,wf,' \
                #       'inc_no' \
                #       'time-n,time-i,time-p,' \
                #       'pat-n,pat-i,pat-p' \
                #       '\n'

                data_common = ['-', p0, nInc, th, m, w]
                data = [str(d) for d in data_common]
                buffer = ','.join(data)+','
                for i in range(0, nInc + 1):
                    data_det = [i, times0[i], times1[i], times2[i], patterns0[i], patterns1[i], patterns2[i]]
                    data = [str(d) for d in data_det]
                    buf = ','.join(data) + '\n'
                    row = buffer+buf
                    f_det.write(row)

                f_sum.close()
                f_det.close()
