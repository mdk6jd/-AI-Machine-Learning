# AI - Homework 4
# Machine Learning
# Kathy Xie, Monica Kuo

import json

# node class
class Node:
	def __init__(self, examples):
		# list of examples
		self.examples = examples 
		# feature (ingredient)
		self.feature = None
		# category (cuisine)
		self.category = None
		# yes and no pointers
		self.yesNode = None
		self.noNode = None

	def setFeature(self, feature):
		self.feature = feature

	def setCategory(self, category):
		self.category = category

	def setYesNode(self, node):
		self.yesNode = node

	def setNoNode(self, node):
		self.noNode = node

#yes or no
attributeValue = []

# TODO ----------
# find the best feature to split the examples based on 
# best feature will be the ingredient that achieves the most even split
def SelectFeature(examples):
	pass
	# create a dict where all the keys are the ingredients and all the values
	# are counts of the occurrences of each ingredient in all of the examples.

	# ingredient that has count closest to len(examples)/2 will be best ingredient
	# return this ingredient

# TODO ----------
def information_gain(examples, attribute, entropy):
    gain = entropy
    for value in attributeValue:
    	pass

# returns whether or not all examples are of the same category
def sameCategory(examples):
	category = examples[0]["cuisine"]
	for example in examples:
		if(not category == example["cuisine"]):
			return False
	return True


# build the decision tree
def buildTree(rootNode):
	queue = [rootNode]
	while(queue!=[]):

		# get current node
		currentNode = queue.pop(0)
		examples = currentNode.examples

		# if all examples are in the same result category,
		# mark node in the tree with that category and continue to next loop
		# category = cuisine 
		sameCuisine = sameCategory(examples)
		if(sameCuisine):
			category = examples[0]["cuisine"]
			currentNode.setCategory(category)
			continue

		# Pick Feature that best splits Examples into different result categories
		# feature = ingredient
		feature = SelectFeature(currentNode)
		currentNode.setFeature(feature)
		# split examples into yes and no sublists based on feature
		yes = []
		no = []
		for example in examples:
			if(feature in example['ingredients']):
				yes.append(example)
			else:
				no.append(example)
		# create nodes for yes and no sublists
		yesNode = Node(yes)
		noNode = Node(no)
		# add nodes to decision tree 
		currentNode.setYesNode(yes)
		currentNode.setNoNode(no)
		# add nodes to queue
		queue.append(yesNode)
		queue.append(noNode)

# TODO ----------
# test the decision tree
def testTree(rootNode, examples):
	numberIncorrect = 0
	for example in examples:
		# traverse decision tree using features in example
		# stop when node.category != None

		# compare resulting cuisine with actual cuisine
		# if(!correct): numberIncorrect+=1
		pass
	return numberIncorrect


def main():
	# import ingredients
	ingredients = []
	ingredientsFile = open('ingredients.txt', 'r')
	for i in range(0, 2398):
		ingredients.append(ingredientsFile.readline().strip()[1:-1])

	# import training set
	training = []
	trainingFile = open('training.json', 'r')
	for i in range(0, 1794):
		training.append(json.loads(trainingFile.readline().strip()))

	# split training set into 6 subsets (to use k-Fold cross validation on)
	subset1 = training[0:299]
	subset2 = training[299:598]
	subset3 = training[598:897]
	subset4 = training[897:1196]
	subset5 = training[1196:1495]
	subset6 = training[1495:1795]

	# k-Fold cross validation
	# train algorithm on 5 training subsets
	# test algorithm on remaining i subset

	# test on subset1
	trainingSubset = subset2 + subset3 + subset4 + subset5 + subset6
	testingSubset = subset1
	# build tree
	rootNode = Node(trainingSubset)
	# decisionTree = buildTree(rootNode) # uncomment this to build tree
	# test tree
	numberIncorrect = testTree(rootNode, testingSubset)
	# calculate percent incorrect
	# percentIncorrect = numberIncorrect/299 * 100

	# repeat above code k-1 times 

if __name__ == "__main__":
	main()