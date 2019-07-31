from UtilityTechniques.ProbabilityWeightAssign import ProbabilityAssign


if __name__ == '__main__':
    where = '../sign/v0/sign_pp'
    read = '../sign/v0/sign_s_v0_p'
    probs = '../Files/probs.csv'
    for i in range(0, 13):
        fwhere = where+str(i)+'.txt'
        fread = read+str(i)+'.txt'
        ProbabilityAssign(fread, probs, fwhere).Assigning()
