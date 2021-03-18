import treelib

class Query:
    '''The Query class. Store the query parts and keywords as a tree'''
    def __init__(self, root, field_name):
        self.root = root
        self.field_name = field_name
        self.keyword_tree = None
        self.leaf_node_name = None
        self.node_count = 0
        self.initialize_tree()

    def initialize_tree(self):
        '''Initialize the keyword tree of this query object'''
        self.keyword_tree = treelib.Tree()

    def insert_tree_pair(self, inputs, index_leaf):
        '''Insert a pair of keywords into the tree. Useful for AND and OR
            :param inputs: the two keywords
            :param index_leaf: index of the keyword to be used as next parent'''
        node_names = []
        for i in range(len(inputs)):
            node_name = inputs[i] + str(self.node_count)
            self.node_count += 1
            node_names.append(node_name)

            self.keyword_tree.create_node(inputs[i], node_name, parent=self.leaf_node_name)

        self.leaf_node_name = node_names[index_leaf]

    def insert_tree_single(self, input_string):
        '''Insert a keywords or an operator into the tree.
            :param input_string: either a keyword or an operator'''
        node_name = input_string + str(self.node_count)
        self.keyword_tree.create_node(input_string, node_name, parent=self.leaf_node_name)
        self.leaf_node_name = node_name
        self.node_count += 1

    def show_keyword_tree(self):
        '''Print the keyword tree in a structural way'''
        self.keyword_tree.show()
