# AI - Homework 4
# Machine Learning
# Katharine Xie, Monica Kuo


import json
import math
import sys
sys.setrecursionlimit(10000)


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

	def print(self):
		exampleNumbers = []
		for i in range(0, len(self.examples)):
			exampleNumbers.append(self.examples[i]["id"])
		print(exampleNumbers)
		# at leaf of tree
		if(self.category != None):
			print(self.category)
		# at inner node of tree, reursively print child nodes
		if(self.yesNode != None):
			self.yesNode.print()
		if(self.noNode != None):
			self.noNode.print()

#yes or no
attributeValue = []


# build the decision tree
def buildTree(currentNode, ingredients):

	# get current node examples
	examples = currentNode.examples
	'''
	print()
	for example in examples:
		print(example["id"])
	'''

	# if all examples are in the same result category,
	# mark node in the tree with that category and exit out of recursion
	# category = cuisine
	sameCuisine = sameCategory(examples)
	if(sameCuisine):
		category = examples[0]["cuisine"]
		currentNode.setCategory(category)

	else:
		# Pick Feature that best splits Examples into different result categories
		# feature = ingredient
		feature = selectFeature(examples, ingredients, "cuisine")
		currentNode.setFeature(feature)

		# split examples into yes and no sublists based on feature
		yes = []
		no = []
		for example in examples:
			if(feature in example['ingredients']):
				yes.append(example)
			else:
				no.append(example)

		if(yes!=[]):
			# create nodes for yes sublist
			yesNode = Node(yes)
			# add node to decision tree
			currentNode.setYesNode(yesNode)
			# recurse on node
			buildTree(yesNode, ingredients)

		if(no!=[]):
			# create nodes for no sublist
			noNode = Node(no)
			# add node to decision tree
			currentNode.setNoNode(noNode)
			# recurse on node
			buildTree(noNode, ingredients)

	return currentNode


# test the decision tree
def testTree(rootNode, examples):
	numberIncorrect = 0
	for example in examples:
		# traverse decision tree using features in example
		# stop when node.category != None
		currentNode = rootNode
		testCategory = None
		while(True):
			# category reached
			if(currentNode.category!=None):
				testCategory = currentNode.category
				break
			# no category determined, traverse tree
			feature = currentNode.feature
			if(feature in example["ingredients"]):
				currentNode = currentNode.yesNode
			else:
				currentNode = currentNode.noNode

		# compare resulting cuisine with actual cuisine
		# if(!correct): numberIncorrect+=1
		trueCategory = example["cuisine"]
		if(testCategory!=trueCategory):
			numberIncorrect += 1

	return numberIncorrect


# find the best feature to split the examples based on
# best feature will be the ingredient that achieves the most even split
def selectFeature(data, attrList, target_attr):
	#cycle through each attribute and calculates info gain
	#choose best gain
	bestGain = sys.float_info.min
	bestIngredient = ''
	for ingredient in attrList:
		infoGain = gain(data, ingredient, target_attr)
		if infoGain > bestGain:
			bestGain = infoGain
			bestIngredient = ingredient
	return bestIngredient
	#return bestGain


# data = test set (cuisine)
def entropy(data, target_attr):
	val_freq = {}
	data_entropy = 0.0

	#calculate frequency of each of the values in target attribute Value
	#yes/no for ingredients, 20 different cuisine
	#target_attr is cuisine and target_attr is ingredient
	#if (target_attr == 'cuisine'):
	for dish in data:
		if (dish.get('cuisine') in val_freq):
			val_freq[ dish.get('cuisine') ] += 1.0
		else:
			val_freq[ dish.get('cuisine') ] = 1.0
	#print(val_freq)

	#calculate entropty of data for target attribute, using S = Sum every attr value (p log p)
	for freq in val_freq.values():
		if freq == 0:
			continue
		data_entropy += (-1.0*freq/len(data)) * math.log(1.0*freq/len(data), 2)
	return data_entropy


def gain(data, attr, target_attr):
	#caculates info gain (reduction in entropy) by splitting data on chosen attribute (attr)
	val_freq = {}
	subset_entropy = 0.0

	#calculate frequency of each values in attribute
	for dish in data:
		hasIngredient = False
		if attr in dish.get('ingredients'):
			hasIngredient = True
		#print(hasIngredient)
		#print(attr)
		if (hasIngredient in val_freq):
			val_freq[ hasIngredient ] += 1.0
		else:
			val_freq[ hasIngredient ] = 1.0

	#calculate sum of entropy for each subset of dishes
	for val in val_freq.keys():
		#|Sv|/|S|
		val_prob = 1.0*val_freq[val]/(1.0*sum(val_freq.values()))
		#sublist of recipes with or without ingredient
		data_subset = [dish for dish in data if ((attr in dish.get('ingredients')) == val)]
		subset_entropy += val_prob * entropy(data_subset,target_attr)

	#print(attr + " %f" %subset_entropy)
	#print(attr + " %f" %(entropy(data, target_attr) - subset_entropy))
	return (entropy(data, target_attr) - subset_entropy)



# returns whether or not all examples are of the same category
def sameCategory(examples):
	category = examples[0]["cuisine"]
	for example in examples:
		if(not category == example["cuisine"]):
			return False
	return True

def get_values(data, attr):
	#cycles through each dish in data and return list of values for attribute
	val_freq = {}
	data_entropy = 0.0

	for dish in data:
		hasIngredient = False
		if attr in dish.get('ingredients'):
			hasIngredient = True
		if (hasIngredient in val_freq):
			val_freq[ hasIngredient ] += 1.0
		else:
			val_freq[ hasIngredient ] = 1.0
	return val_freq.keys()


def get_examples(data, best, val):
	#returns list of dishes in data set that have val for the best attribute
	dishResult = []
	for dish in data:
		hasIngredient = False
		if best in dish.get('ingredients'):
			hasIngredient = True
		if hasIngredient == val:
			dishResult.append(dish)
	return dishResult


def buildDecisionTree(data, attributes, target_attr):
	#returns new decision tree based on the exmaples given
	data = data [:]
	#values of the cuisine
	vals = [dish.get('cuisine') for dish in data]
	default = {} #Node with Italian as value ?????????????????

	#if there's no example set or if the ingredients list is empty
	if not data or (len(attributes)-1) <= 0:
		return default
	#if all dish are same cuisine then return that classification
	elif vals.count(vals[0]) == len(vals):
		#print(vals[0])
		return vals[0]
	else:
		#choose next best attribute
		best = selectFeature(data, attributes, target_attr)
		#print(best)
		#create new tree/node with best attribute and empty dictionary
		tree = {best:{}}
		#create new decision tree/sub node for each value in best attributes
		#for val in get_values(data, best):
		subtreeTrue = buildDecisionTree(
			get_examples(data, best, True),
			[a for a in attributes if a != best],
			target_attr
		)

		#add new subtree to empty dictionary in our new tree/nodes
		tree[best][True] = subtreeTrue

		subtreeFalse = buildDecisionTree(
			get_examples(data, best, False),
			[a for a in attributes if a != best],
			target_attr
		)

		#add new subtree to empty dictionary in our new tree/nodes
		tree[best][False] = subtreeFalse
	return tree


def main():
	# import ingredients
	ingredients = []
	ingredientsFile = open('ingredients.txt', 'r')
	for i in range(0, 2398):
		ingredients.append(ingredientsFile.readline().strip()[1:-1])

	# import training set
	# split training set into 6 subsets (to use k-Fold cross validation on)
	subset1 = []
	subset2 = []
	subset3 = []
	subset4 = []
	subset5 = []
	subset6 = []
	trainingFile = open('training.json', 'r')
	for i in range(0, 1794):
		if(i%6 == 0):
			subset1.append(json.loads(trainingFile.readline().strip()))
		elif(i%6 == 1):
			subset2.append(json.loads(trainingFile.readline().strip()))
		elif(i%6 == 2):
			subset3.append(json.loads(trainingFile.readline().strip()))
		elif(i%6 == 3):
			subset4.append(json.loads(trainingFile.readline().strip()))
		elif(i%6 == 4):
			subset5.append(json.loads(trainingFile.readline().strip()))
		elif(i%6 == 5):
			subset6.append(json.loads(trainingFile.readline().strip()))


	# k-Fold cross validation
	# train algorithm on 5 training subsets
	# test algorithm on remaining i subset

	# test on subset1
	trainingSubset = subset2 + subset3 + subset4 + subset5 + subset6
	testingSubset = subset1
	# build tree
	rootNode = Node(trainingSubset)
	decisionTree = buildTree(rootNode, ingredients) # uncomment this to build tree
	# decisionTree.print()
	# test tree
	numberIncorrect = testTree(rootNode, testingSubset)
	# calculate percent incorrect
	percentIncorrect = numberIncorrect/299 * 100
	print(percentIncorrect)

	# test on subset2
	trainingSubset = subset1 + subset3 + subset4 + subset5 + subset6
	testingSubset = subset2
	# build tree
	rootNode = Node(trainingSubset)
	decisionTree = buildTree(rootNode, ingredients) # uncomment this to build tree
	# decisionTree.print()
	# test tree
	numberIncorrect = testTree(rootNode, testingSubset)
	# calculate percent incorrect
	percentIncorrect = numberIncorrect/299 * 100
	print(percentIncorrect)

	# test on subset3
	trainingSubset = subset1 + subset2 + subset4 + subset5 + subset6
	testingSubset = subset3
	# build tree
	rootNode = Node(trainingSubset)
	decisionTree = buildTree(rootNode, ingredients) # uncomment this to build tree
	# decisionTree.print()
	# test tree
	numberIncorrect = testTree(rootNode, testingSubset)
	# calculate percent incorrect
	percentIncorrect = numberIncorrect/299 * 100
	print(percentIncorrect)

	# test on subset4
	trainingSubset = subset1 + subset2 + subset3 + subset5 + subset6
	testingSubset = subset4
	# build tree
	rootNode = Node(trainingSubset)
	decisionTree = buildTree(rootNode, ingredients) # uncomment this to build tree
	# decisionTree.print()
	# test tree
	numberIncorrect = testTree(rootNode, testingSubset)
	# calculate percent incorrect
	percentIncorrect = numberIncorrect/299 * 100
	print(percentIncorrect)

	# test on subset5
	trainingSubset = subset1 + subset2 + subset3 + subset4 + subset6
	testingSubset = subset5
	# build tree
	rootNode = Node(trainingSubset)
	decisionTree = buildTree(rootNode, ingredients) # uncomment this to build tree
	# decisionTree.print()
	# test tree
	numberIncorrect = testTree(rootNode, testingSubset)
	# calculate percent incorrect
	percentIncorrect = numberIncorrect/299 * 100
	print(percentIncorrect)

	# test on subset6
	trainingSubset = subset1 + subset2 + subset3 + subset4 + subset5
	testingSubset = subset6
	# build tree
	rootNode = Node(trainingSubset)
	decisionTree = buildTree(rootNode, ingredients) # uncomment this to build tree
	# decisionTree.print()
	# test tree
	numberIncorrect = testTree(rootNode, testingSubset)
	# calculate percent incorrect
	percentIncorrect = numberIncorrect/299 * 100
	print(percentIncorrect)


	#print( selectFeature(training, ingredients, 'cuisine') )
	#buildDecisionTree(trainingSubset, ingredients, "cuisine")
	#entropy(trainingSubset, "cuisine")
	#ingredients2 = ["salt"]
	#selectFeature(trainingSubset, ingredients, "cuisine")

if __name__ == "__main__":
	main()
