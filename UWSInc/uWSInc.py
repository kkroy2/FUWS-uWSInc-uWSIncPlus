from Parameters.ProgramVariable import ProgramVariable


class uWSInc():

    def __init__(self, trie):
        self.fssfsTrie = trie
        pass

    def uWSIncMethod(self):
        for i in range(0, len(ProgramVariable.uSDB)):
            self.fssfsTrie.update_support(self.fssfsTrie.root_node, None, 0.0, 0, i)
        self.fssfsTrie.traverse_trie(self.fssfsTrie.root_node)
        self.fssfsTrie.update_trie(self.fssfsTrie.root_node)
        self.fssfsTrie.trie_into_file(self.fssfsTrie.root_node, '')
        return

