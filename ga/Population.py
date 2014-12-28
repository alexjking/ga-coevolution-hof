#!/usr/bin/python

import Chromosome
import random

class Population:

	_pop = []
	_population_size = 25
	_sample_size = 15

	def __init__(self, chromosome_value):
		self._pop = [Chromosome.Chromosome(chromosome_value) for _ in xrange(self._population_size)]

	def print_pop(self):
		print [chromosome.get_fitness() for chromosome in self._pop]

	def mutate(self):
		for chromosome in self._pop:
			chromosome.mutate()

	def get_sample(self):
		return random.sample(self._pop, self._sample_size)
