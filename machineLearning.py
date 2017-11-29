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

#yes or no
attributeValue = []


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
	return ingredient
	#return bestGain


# data = test set (cuisine)
def entropy(data, target_attr):
	val_freq = {}
	data_entropy = 0.0

	#calculate frequency of each of the values in target attribute Value
	#yes/no for ingredients, 20 different cuisine
	#target_attr is cuisine and target_attr is ingredient
	if (target_attr == 'cuisine'):
		for dish in data:
			if (dish.get('cuisine') in val_freq):
				val_freq[ dish.get('cuisine') ] += 1.0
			else:
				val_freq[ dish.get('cuisine') ] = 1.0
	else:
		for dish in data:
			hasIngredient = False
			if target_attr in dish.get('ingredients'):
				hasIngredient = True

			if (hasIngredient in val_freq):
				val_freq[ hasIngredient ] += 1.0
			else:
				val_freq[ hasIngredient ] = 1.0

	#calculate entropty of data for target attribute, using S = Sum every attr value (p log p)
	for freq in val_freq.values():
		data_entropy += (-freq/len(data)) * math.log(freq/len(data), 2)

	return data_entropy


def gain(data, attr, target_attr):
	#caculates info gain (reduction in entropy) by splitting data on chosen attribute (attr)
	val_freq = {}
	subset_entropy = 0.0

	#calculate frequency of each values in attribute
	if (attr == 'cuisine'):
		for dish in data:
			if (dish.get('cuisine') in val_freq):
				val_freq[ dish.get('cuisine') ] += 1.0
			else:
				val_freq[ dish.get('cuisine') ] = 1.0
	else:
		for dish in data:
			hasIngredient = False
			if attr in dish.get('ingredients'):
				hasIngredient = True
			if (hasIngredient in val_freq):
				val_freq[ hasIngredient ] += 1.0
			else:
				val_freq[ hasIngredient ] = 1.0

	#calculate sum of entropy for each suset of dishes
	for val in val_freq.keys():
		val_prob = val_freq[val]/sum(val_freq.values())
		data_subset = [dish for dish in data if (dish.get('cuisine') == val or attr in dish.get('ingredients') == val)]
		subset_entropy += val_prob * entropy(data_subset,target_attr)

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
		return vals[0]
	else:
		#choose next best attribute
		best = selectFeature(data, attributes, target_attr)
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
		feature = selectFeature(currentNode)
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
	subset1 = training[0:100]
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

	#print( selectFeature(training, ingredients, 'cuisine') )
	print(buildDecisionTree(subset1, ingredients, "cuisine"))

if __name__ == "__main__":
	main()
