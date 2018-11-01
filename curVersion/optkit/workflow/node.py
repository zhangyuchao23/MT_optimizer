'''
A class for the nodes on the workflow tree.
'''
class Node:
	def __init__(self, child=None, changedFlag=True):
		'''
		Attributes
		----------
		child : list of Node
			all children of the node
		changedFlag : bool
			whether this node has been changed
		'''
		self.child = child
		self.changedFlag = changedFlag
		self.validator_node()

	def validator_node(self):
		'''
		Check the validities of child and changedFlag of the node.

		Raises
		------
		TypeError
			When child is not of type Node.
			When changedFlag is not of type bool.
		'''
		try:
			if not self.child == None:
				for i in self.child:
					if not isinstance(i, Node):
						raise TypeError("Parameter child must be of type Node.")
			if not isinstance(self.changedFlag, bool):
				raise TypeError("Parameter changedFlag must be of type bool.")
		except Exception as e:
			raise e