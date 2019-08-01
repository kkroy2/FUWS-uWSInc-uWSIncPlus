from UtilityTechniques.ProbabilityWeightAssign import ProbabilityAssign, checkCSV


if __name__ == '__main__':
    where = '../LEVIATHAN/v0/LEVIATHAN_v0_pp'
    read = '../LEVIATHAN/v0/LEVIATHAN_v0_p'
    probs = '../Files/probs.csv'
    for i in range(0, 11):
        fwhere = where+str(i)+'.txt'
        fread = read+str(i)+'.txt'

        ProbabilityAssign(fread, probs, fwhere).Assigning()
    # checkCSV.file = open('../Files/probs.csv', 'r')
    # checkCSV.run()
