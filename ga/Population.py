#!/usr/bin/python

import Chromosome
import random
from copy import deepcopy
import numpy as np
import math

class Population:

	_pop = []
	_population_size = 25
	_sample_size = 1

	_individual_dimensions = 1

	def __init__(self, intransitive_superiority):
		self._intransitive_superiority = intransitive_superiority
		if intransitive_superiority:
			self._pop = [Chromosome.IntransitiveSuperiorityChromosome(self._individual_dimensions) for _ in xrange(self._population_size)]	
		else:
			self._pop = [Chromosome.Chromosome(self._individual_dimensions) for _ in xrange(self._population_size)]	

	# set population fitness to max (for testing)
	def set_fitness_max(self):
		if intransitive_superiority:
			self._pop = [Chromosome.IntransitiveSuperiorityChromosome(self._individual_dimensions, value=1) for _ in xrange(self._population_size)]	
		else:
			self._pop = [Chromosome.Chromosome(self._individual_dimensions, value=1) for _ in xrange(self._population_size)]

	def print_pop(self):
		print [chromosome.get_fitness() for chromosome in self._pop]

	def mutate(self):
		for chromosome in self._pop:
			chromosome.mutate()

	def get_sample(self):
		return random.sample(self._pop, self._sample_size)

	def get_mean_fitness(self):
		return reduce(lambda x,y: x+y, [chromosome.get_fitness() for chromosome in self._pop])/len(self._pop)

	def get_roulette_wheel(self, sample):
		roulette_wheel = []

		subj_fitness_list = []
		subj_fitness_sum = 0.0
		subj_fitness_list.append(0.0)
		for individual in self._pop:
			subj_fitness = self._get_subj_fitness(individual, sample)
			subj_fitness_list.append(subj_fitness)
			subj_fitness_sum += subj_fitness

		# store list so that it can be used to calculate the mean subj fitness
		self.subj_fitness_list = subj_fitness_list

		if subj_fitness_sum > 0:
			subj_fitness_probability_list = []
			current_sum = 0.0
			for i, individual in enumerate(self._pop):
				temp = subj_fitness_list[i] / subj_fitness_sum
				probability = current_sum + temp
				subj_fitness_probability_list.append(probability)
				current_sum = probability

			subj_fitness_probability_list.append(1.0)
			return subj_fitness_probability_list
		else:
			#subj fitness sum is zero therefore all have lost and are equal
			subj_fitness_probability_list = []
			increment = 1.0 / len(self._pop) 
			current_sum = 0.0
			for i in xrange(len(self._pop)):
				 subj_fitness_probability_list.append(current_sum)
				 current_sum += increment
			subj_fitness_probability_list.append(1.0)
			return subj_fitness_probability_list



	def set_individual(self, index, individual):
		self._pop[index] = individual

	# coevolve this population a single generation using a sample from another population
	def coevolve(self, sample):
		#generate fitness roulette wheel
		roulette_wheel = self.get_roulette_wheel(sample)

		evolved_pop = Population(self._intransitive_superiority)

		#loop through every individual
		new_population_list = []

		for index, individual in enumerate(self._pop):
			individual_copy = deepcopy(individual)

			selection = self.select_individual(roulette_wheel)
			selection.mutate()

			evolved_pop.set_individual(index, selection)


		self._pop = evolved_pop._pop
		return self



	# roulette wheel selection
	def select_individual(self, roulette_wheel):

		random_choice = random.random()
		for index in xrange(len(self._pop)):
			roulette_value = roulette_wheel[index]
			if random_choice >= roulette_value and random_choice < roulette_wheel[index+1]:
				return deepcopy(self._pop[index])

		print "error"
		print random_choice


	def _get_subj_fitness(self, individual, sample):
		subj_score_list = [individual.score(ind2) for ind2 in sample]
		fitness = np.mean(subj_score_list)
		return fitness

	# return the average subjective score for the last coevolution
	def get_subjective_average(self):
		if self.subj_fitness_list is not None:
			new_list = [subj_fit/float(self._sample_size) for subj_fit in self.subj_fitness_list]
			return np.mean(self.subj_fitness_list)
		else:
			return -1.0

	def get_subjective_list(self):
		if self.subj_fitness_list is not None:
			return self.subj_fitness_list
		else:
			return [-1.0 for _ in xrange(self._population_size)]



	
