# AI - Homework 4
# Machine Learning
# Kathy Xie, Monica Kuo

import json

# node class
class Node:
	def __init__(self, examples):
		# list of examples
		self.examples = examples 
		# classifying feature
		self.feature = None
		# yes and no pointers
		self.yesNode = None
		self.noNode = None

	def setFeature(self, feature):
		self.feature = feature

	def setYesNode(self, node):
		self.yesNode = node

	def setNoNode(self, node):
		self.noNode = node

#yes or no
attributeValue = []

def SelectFeature(rootNode):
	pass

    #feature = pick best feature
    # Pick Feature that best splits Examples into different result categories

    #value of yes or no
    #for value in feature:
    # for item in testVal:
        #if item has the ingrediant
            #put them into a list or set
        #else
            #put them into another set
        #if the cuisine is the same
            #MARK IT???????????????
        #else:
            #SelectFeature(list)

	# For each Value of Feature
		# Find Subset S of Examples such that Feature == Value
		# If all examples in S are in same result category
			# Mark relevant node in the tree with that category
		# Else
			# Call SelectFeature(S)


def information_gain(examples, attribute, entropy):
    gain = entropy
    for value in attributeValue:
    	pass

# build the decision tree
def buildTree(rootNode):
	SelectFeature(rootNode)

# test the decision tree
def testTree(rootNode, examples):
	numberIncorrect = 0
	for example in examples:
		# traverse decision tree using features in example 
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
	decisionTree = buildTree(rootNode)
	# test tree
	numberIncorrect = testTree(rootNode, testingSubset)
	# calculate percent incorrect
	# percentIncorrect = numberIncorrect/299 * 100

if __name__ == "__main__":
	main()