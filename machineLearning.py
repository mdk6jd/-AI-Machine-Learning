# AI - Homework 4
# Machine Learning
# Kathy Xie, Monica Kuo

import json

def SelectFeature(Examples):
	pass
	# Pick Feature that best splits Examples into different result categories
	# For each Value of Feature
		# Find Subset S of Examples such that Feature == Value
		# If all examples in S are in same result category
			# Mark relevant node in the tree with that category
		# Else
			# Call SelectFeature(S)

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
	for i in range(0, 6):
		# train algorithm on 5 training subsets

		# test algorithm on remaining i subset

if __name__ == "__main__":
	main()