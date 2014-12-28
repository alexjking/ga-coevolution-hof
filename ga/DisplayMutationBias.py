import Population

import matplotlib.pyplot as plt
import numpy as np
import random

#displays a graph showing the mutation bias within two populations
class DisplayMutationBias:

	_population_size = 25

	def __init__(self):
		self._pop1 = Population.Population(0)
		self._pop2 = Population.Population(100)
		self.print_populations()

	def next_generation(self):
		self._pop1.mutate()
		self._pop2.mutate()

		return [self._pop1, self._pop2]

	def print_populations(self):
		self._pop1.print_pop()
		self._pop2.print_pop()



if __name__ == '__main__':
	bias = DisplayMutationBias()
	x1 = []
	y1 = []
	x2 = []
	y2 = []

	x3 = []
	y3 = []

	for i in xrange(600):
		pop1, pop2 = bias.next_generation()
		for chromosome in pop1.get_sample():
			x1.append(i)
			y1.append(chromosome.get_fitness())
		for chromosome in pop2.get_sample():
			x2.append(i)
			y2.append(chromosome.get_fitness())
		x3.append(i)
		y3.append(50)

	plt.scatter(
		x1,
		y1,
		s=1,
		facecolor='red',
		lw=0
	)
	plt.scatter(
		x2,
		y2,
		s=1,
		facecolor='grey',
		lw=0
	)
	plt.scatter(
		x3,
		y3,
		s=1,
		facecolor='black',
		lw=1
	)
	plt.ylabel('Objective fitness')
	plt.xlabel('Generations')
	plt.axis([0, 600, 0, 100])
	plt.show()
		#bias.print_populations()
