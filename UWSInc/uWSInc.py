from Parameters.ProgramVariable import ProgramVariable
from Parameters.Variable import Variable
from Parameters.FileInfo import FileInfo


class uWSInc():

    def __init__(self, trie):
        self.fssfsTrie = trie
        pass

    def uWSIncMethod(self):
        Variable.size_of_dataset += len(ProgramVariable.uSDB)
        print(Variable.size_of_dataset, ' at uWSIncMethod..')
        for i in range(0, len(ProgramVariable.uSDB)):
            self.fssfsTrie.update_support(self.fssfsTrie.root_node, None, 0.0, i)
        self.fssfsTrie.traverse_trie(self.fssfsTrie.root_node)
        self.fssfsTrie.update_trie(self.fssfsTrie.root_node)
        self.fssfsTrie.trie_into_file(self.fssfsTrie.root_node, '')
        FileInfo.fs.write('\n \n')
        FileInfo.sfs.write('\n \n')
        return

