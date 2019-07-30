
class uWSIncPlus():
    uWSeq = None
    intSDBfile = None
    preSDBfile = None
    wfile = None
    candtfile = None
    fsFileName = None
    sfsFileName = None
    finalFSfile = None
    bufferFile = None
    apSDBfile = None
    apPreSDBfile = None
    lsSDBfile = None
    fssfsTrie = None
    lsTrie = None

    def __init__(self):
        # print('this function is not calling why man')
        self.intSDBfile = '../signDB2'
        self.preSDBfile = '../preProcessed.txt'

        self.wfile = '../weight.txt'

        self.candtfile = '../candidate.txt'
        self.fsFileName = '../intialFS.txt'
        self.sfsFileName = '../intialSFS.txt'

        self.finalFSfile = '../fsFromuWSIncPlus.txt'
        self.finalSFSfile = '../sfsFromuWSIncPlus.txt'
        self.bufferFile = '../WSIncPlusbuffer.txt'

        self.apSDBfile = '../appendedSDB.txt'
        self.apPreSDBfile = '../apPreProcessedSDB.txt'

        self.apcandtfile = '../apcandidate.txt'
        self.apFSfile = '../apFS.txt'
        self.apSFSfile = '../apSFS.txt'

        self.fssfsTrie = Trie(self.finalFSfile, self.finalSFSfile, self.apSDBfile)
        self.lsTrie = Trie(self.bufferFile, self.bufferFile, self.apSDBfile)
        self.fssfsTrie.setlsTrie(self.lsTrie)

        self.uWSeq = uWSequence(Parameters.min_sup, Parameters.minExpWeight, self.wfile,
                                self.candtfile, self.fsFileName, self.sfsFileName,
                                self.intSDBfile, self.preSDBfile)

        self.uWSeq.douWSequence()

        Parameters.dbSize = len(self.uWSeq.uSDB)

        self.uWSeq.fsFile.close()
        self.uWSeq.sfsFile.close()
        self.uWSeq.candidateFile.close()

        seqfile = open(self.fsFileName, 'r')

        for seqTuple in seqfile:
            seq, support = seqTuple.split(' ')
            self.fssfsTrie.insertion(self.fssfsTrie.rootNode, seq, 0, support)

        seqfile = open(self.sfsFileName, 'r')

        for seqTuple in seqfile:
            seq, support = seqTuple.split(' ')
            self.fssfsTrie.insertion(self.fssfsTrie.rootNode, seq, 0, support)

        # self.fssfsTrie.printFSSFS(self.fssfsTrie.rootNode, '')

        lsfile = open(self.bufferFile, 'r')

        for lsTuple in lsfile:
            ls, support = lsTuple.split(' ')
            self.lsTrie.insertion(self.lsTrie.rootNode, ls, 0, support)

        return

    def uWSIncPlusMethod(self, apDBname):
        self.apSDBfile = apDBname
        self.uWSeq = uWSequence(Parameters.min_sup, Parameters.minExpWeight, self.wfile,
                                self.apcandtfile, self.apFSfile, self.apSFSfile,
                                self.apSDBfile, self.apPreSDBfile)
        self.uWSeq.douWSequence()
        self.uWSeq.fsFile.close()
        self.uWSeq.sfsFile.close()
        self.uWSeq.candidateFile.close()

        lsSeqfile = open(self.apFSfile, 'r')
        for lsSeqTuple in lsSeqfile:
            lsSeq, support = lsSeqTuple.split(' ')
            support = float(support)
            support += self.lsTrie.searchSupport(self.lsTrie.rootNode, lsSeq, 0)
            self.fssfsTrie.updateWithInsertion(self.fssfsTrie.rootNode, lsSeq, 0, support)

        lsSeqfile = open(self.apSFSfile, 'r')
        for lsSeqTuple in lsSeqfile:
            lsSeq, support = lsSeqTuple.split(' ')
            support = float(support)
            support += self.lsTrie.searchSupport(self.lsTrie.rootNode, lsSeq, 0)
            self.fssfsTrie.updateWithInsertion(self.fssfsTrie.rootNode, lsSeq, 0, support)

        self.fssfsTrie.supportDP.setReadfile(apDBname)
        self.fssfsTrie.traverseTrie(self.fssfsTrie.rootNode, [], Parameters.semiBoundary())
        Parameters.dbSize += self.fssfsTrie.supportDP.curDBSize

        self.fssfsTrie.lsTrie.rootNode.descendants = dict()
        self.fssfsTrie.updateWithlsTrieBuild(self.fssfsTrie.rootNode, [])
        self.fssfsTrie.updateTrie(self.fssfsTrie.rootNode)

        self.fssfsTrie.trieIntoFile(self.fssfsTrie.rootNode, '')
        self.fssfsTrie.FSwhereToWrite.write('\n')
        self.fssfsTrie.SFSwhereToWrite.write('\n')

        self.lsTrie.trieIntoFilePS(self.lsTrie.rootNode, '')
        self.lsTrie.FSwhereToWrite.write('\n')

        return

