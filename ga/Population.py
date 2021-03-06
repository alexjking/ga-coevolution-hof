#!/usr/bin/python

import Chromosome
import random
from copy import deepcopy
import numpy as np
import math
import HallOfFame

class Population:

	_pop = []
	_population_size = 25
	_sample_size = 1

	_individual_dimensions = 1

	_hof_sample = 15

	def __init__(self, hof=False, hof_filter=False):
		self._pop = [Chromosome.Chromosome(self._individual_dimensions) for _ in xrange(self._population_size)]	
		if hof:
			self._hof = HallOfFame.HallOfFame()
			self._hof_filter = hof_filter
		else: 
			self._hof = None

	# set population fitness to max (for testing)
	def set_fitness_max(self):
		for individual in self._pop:
			individual.set_fitness_max()

	def print_pop(self):
		print [chromosome.get_fitness() for chromosome in self._pop]

	def mutate(self):
		for chromosome in self._pop:
			chromosome.mutate()

	def get_sample(self):
		return random.sample(self._pop, self._sample_size)

	def get_mean_fitness(self):
		return reduce(lambda x,y: x+y, [chromosome.get_fitness() for chromosome in self._pop])/len(self._pop)

	def get_roulette_wheel(self, opponent_population):
		roulette_wheel = []

		subj_fitness_list = []
		subj_fitness_sum = 0.0
		subj_fitness_list.append(0.0)
		for individual in self._pop:
			subj_fitness = self._get_subj_fitness(individual, opponent_population)
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
	def coevolve(self, opponent_population):
		#mutate the whole population
		self.mutate()
		#generate fitness roulette wheel
		roulette_wheel = self.get_roulette_wheel(opponent_population)

		evolved_pop = []
		new_population_list = []
		for index, individual in enumerate(self._pop):
			individual_copy = deepcopy(individual)
			selection = self.select_individual(roulette_wheel)
			evolved_pop.append(selection)
		self.update_hof()

		self._pop = evolved_pop
		return self

	# adds the best individual of the current population to the hof
	def update_hof(self):
		if self._hof is not None:
			best_individual = None
			highest_subj_score = -1.0
			# loop through the subj fitness list generated by the roulette wheel function to find best individual
			for index, subj_score in enumerate(self.subj_fitness_list):
				if index > 0: # the first entry is used for other purposes so we should ignore this one and  refer to pop using index-1
					if subj_score > highest_subj_score:
						highest_subj_score = subj_score
						best_individual = self._pop[index-1]

			self._hof.update(best_individual)
			#self.print_hof()


	# roulette wheel selection
	def select_individual(self, roulette_wheel):
		random_choice = random.random()
		for index in xrange(len(self._pop)):
			roulette_value = roulette_wheel[index]
			if random_choice >= roulette_value and random_choice < roulette_wheel[index+1]:
				return deepcopy(self._pop[index])
		print "error"
		print random_choice


	def _get_subj_fitness(self, individual, opponent_population):
		sample = opponent_population.get_sample()
		# calculate subj scores against sample
		subj_score_list = [individual.score(ind2) for ind2 in sample] 
		#calculate subj scores against hof and append to score list
		if self._hof is not None:
			if self._hof_filter:
				# return score of 0 if individual doesnt beat all opponents
				if opponent_population._hof.compete_against_hof(individual):
					return np.mean(subj_score_list)
				else:
					return 0.0 # failed to beat all opponent hof
			else:
				# add subj scores to our list of scores
				hof_sample = opponent_population._hof.get_sample()
				subj_hof_score_list = [individual.score(champion) for champion in hof_sample] # compete against a sample from hall of fame
				subj_score_list.extend(subj_hof_score_list) 
				return np.mean(subj_score_list)
		else:
			return np.mean(subj_score_list)

	# return the average subjective score for the last coevolution
	def get_subjective_average(self):
		# if self.subj_fitness_list is not None:
		# 	return np.mean(self.subj_fitness_list)
		# else:
		# 	return -1.0
		if self.subj_fitness_list is not None:
			modified_list = []
			for index, subj_fitness in enumerate(self.subj_fitness_list):
				if index > 0:
					modified_list.append(subj_fitness)
			return np.mean(modified_list)
		else:
			return -1.0

	def get_subjective_list(self):
		if self.subj_fitness_list is not None:
			return self.subj_fitness_list
		else:
			return [-1.0 for _ in xrange(self._population_size)]

class IntransitiveSuperiorityPopulation(Population):

	def __init__(self, hof=False, hof_filter=False):
		self._pop = [Chromosome.IntransitiveSuperiorityChromosome(self._individual_dimensions) for _ in xrange(self._population_size)]	
		if hof:
			self._hof = HallOfFame.HallOfFame()
			self._hof_filter = hof_filter
		else: 
			self._hof = None