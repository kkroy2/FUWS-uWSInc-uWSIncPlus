from UtilityTechniques.ProbabilityWeightAssign import ProbabilityAssign, checkCSV


if __name__ == '__main__':
    prefix_all = '../FIFA/v3/FIFA_v3_p'

    read = prefix_all
    where = prefix_all+'p'
    probs = '../Files/probs.csv'
    PA = ProbabilityAssign()
    PA.probsFile = open(probs, 'r')
    for i in range(0, 5):
        fwhere = where+str(i)+'.txt'
        fread = read+str(i)+'.txt'
        PA.whereToWrite = open(fwhere, 'w')
        PA.dataFile = open(fread, 'r')
        PA.Assigning()

    # PA.dataFile = open(read, 'r')
    # PA.whereToWrite = open(where, 'w')
    # PA.Assigning()

    # checkCSV.file = open('../Files/probs.csv', 'r')
    # checkCSV.run()
