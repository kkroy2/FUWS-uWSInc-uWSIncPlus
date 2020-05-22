from UtilityTechniques.ProbabilityWeightAssign import ProbabilityAssign, checkCSV


if __name__ == '__main__':
    prefix_all = '../Files/Probability'
    file = ['prob_5_05.csv', 'prob_5_1.csv', 'prob_5_125.csv', 'prob_5_15.csv', 'prob_5_25.csv']
    read = prefix_all+'/OnlineRetail.txt'
    where = prefix_all+'/'
    for fname in file:
        probs = prefix_all+'/'+fname
        PA = ProbabilityAssign()
        PA.probsFile = open(probs, 'r')

        fwhere = where+'OnlineRetail_'+fname[:len(fname)-4]+'_sp'+'.txt'
        fread = read
        PA.whereToWrite = open(fwhere, 'w')
        PA.dataFile = open(fread, 'r')
        PA.Assigning()
