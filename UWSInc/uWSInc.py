from DynamicPortion.Trie import Trie
from Utility.Parameters import Parameters
from uWseq.uWSequence import uWSequence


class uWSInc():
    uWSeq = None
    wfile = '../weight.txt'
    candtfile = '../candidate.txt'
    fsFileName = '../intialFS.txt'
    sfsFileName = '../intialSFS.txt'
    finalFSfile = '../FSFromuWSInc.txt'
    intSDBfile = '../signDB2'
    preSDBfile = '../preProcessed.txt'
    apSDBfile = '../appendedSDB.txt'
    finalSFSfile = '../SFSFromuWSInc.txt'

    fssfsTrie = None

    def __init__(self):
        self.fssfsTrie = Trie(self.finalFSfile, self.finalSFSfile, self.apSDBfile)
        self.uWSeq = uWSequence(Parameters.min_sup, Parameters.minExpWeight,
                                self.wfile, self.candtfile, self.fsFileName, self.sfsFileName,
                                self.intSDBfile, self.preSDBfile)
        self.uWSeq.douWSequence()
        self.uWSeq.fsFile.close()
        self.uWSeq.sfsFile.close()
        self.uWSeq.candidateFile.close()
        Parameters.dbSize = len(self.uWSeq.uSDB)

        seqfile = open(self.fsFileName, 'r')
        for seqtuple in seqfile:
            seq, support = seqtuple.split(' ')
            self.fssfsTrie.insertion(self.fssfsTrie.rootNode, seq, 0, support)

        seqfile = open(self.sfsFileName, 'r')
        for seqtuple in seqfile:
            seq, support = seqtuple.split(' ')
            self.fssfsTrie.insertion(self.fssfsTrie.rootNode, seq, 0, support)
        pass

    def uWSIncMethod(self, apDBname):
        supportThreshold = Parameters.semiBoundary()
        self.fssfsTrie.supportDP.setReadfile(apDBname)
        self.fssfsTrie.traverseTrie(self.fssfsTrie.rootNode, [], supportThreshold)
        Parameters.dbSize += self.fssfsTrie.supportDP.curDBSize

        self.fssfsTrie.updateTrie(self.fssfsTrie.rootNode)
        self.fssfsTrie.trieIntoFile(self.fssfsTrie.rootNode, '')
        self.fssfsTrie.FSwhereToWrite.write('\n')
        self.fssfsTrie.SFSwhereToWrite.write('\n')

        return

