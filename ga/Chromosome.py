#!/usr/bin/python

import random
import math

#Chromosome represented as a scalar value
class Chromosome:

	_max_value = 100
	_skills = []

	def __init__(self, dimensions, value=0):
		self._skills = []
		if 100 % dimensions == 0:
			skill_length = self._max_value / dimensions
			for i in xrange(dimensions):
				self._skills.append([value for _ in xrange(skill_length)])
		else:
			raise Exception("Invalid number of dimensions for genome")
		

	# return objective fitness of this chromosome
	def get_fitness(self):
		fitness_sum = 0
		for skill in self._skills:
			fitness_sum += reduce(lambda x,y: x+y, skill)
		return fitness_sum

	# return the fitness for a particular skill
	def get_skill_fitness(self, index):
		return reduce(lambda x,y: x+y, self._skills[index])

	# return whether self has a higher fitness than another chromosome
	def score(self, b):
		# find skill with maximum difference
		max_skill_difference = -1
		max_skill_index = -1
		for index in xrange(len(self._skills)):
			self_fitness = self.get_skill_fitness(index)
			b_fitness = b.get_skill_fitness(index)
			difference = abs(self_fitness - b_fitness)
			if difference > max_skill_difference:
				max_skill_difference = difference
				max_skill_index = index

		# compare the two chromosomes skills with the highest diff to see who wins
		if self.get_skill_fitness(max_skill_index) > b.get_skill_fitness(max_skill_index):
			return 1
		else:
			return 0

	def mutate(self):
		for index, skill in enumerate(self._skills):
			new_skill = []
			for value in skill:
				if random.random() <= 0.005:
					new_skill.append(random.choice([0,1]))
				else:
					new_skill.append(value)
			self._skills[index] = new_skill

	def print_string(self):
		print self._skills

	def set_fitness_max(self):
		dimensions = len(self._skills)
		self._skills = []
		if 100 % dimensions == 0:
			skill_length = self._max_value / dimensions
			for i in xrange(dimensions):
				self._skills.append([1 for _ in xrange(skill_length)])
		else:
			raise Exception("Invalid number of dimensions for genome")



class IntransitiveSuperiorityChromosome(Chromosome):

	def score(self, b):
		# find skill with lowest difference
		min_skill_difference = self._max_value #init to a large value
		min_skill_index = -1
		for index in xrange(len(self._skills)):
			self_fitness = self.get_skill_fitness(index)
			b_fitness = b.get_skill_fitness(index)
			difference = abs(self_fitness - b_fitness)
			if difference < min_skill_difference:
				min_skill_difference = difference
				min_skill_index = index

		# compare the two chromosomes skills with the lowest diff to see who wins
		if self.get_skill_fitness(min_skill_index) > b.get_skill_fitness(min_skill_index):
			return 1
		else:
			return 0



if __name__ == '__main__':
	chromosome = Chromosome(10)
	chromosome2 = Chromosome(10)

	chromosome.mutate()
	chromosome.mutate()
	chromosome.mutate()
	chromosome.mutate()
	chromosome.mutate()
	chromosome.mutate()
	chromosome.mutate()
	chromosome.mutate()

	chromosome.print_string()
	chromosome2.print_string()
	print chromosome.get_fitness()
	print chromosome2.get_fitness()

	print chromosome.score(chromosome2)

