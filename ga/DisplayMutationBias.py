import Chromosome

import matplotlib.pyplot as plt
import numpy as np

#displays a graph showing the mutation bias within two populations
class DisplayMutationBias:

	_population1 = []
	_population2 = []

	_population_size = 25

	def __init__(self):
		self._population1 = [Chromosome.Chromosome(0) for _ in xrange(self._population_size)];
		self._population2 = [Chromosome.Chromosome(100) for _ in xrange(self._population_size)];
		self.print_populations()

	def next_generation(self):
		for c in self._population1:
			c.mutate()
		for c in self._population2:
			c.mutate()

		return [self._population1, self._population2]

	def print_populations(self):
		print "population1"
		fitness_list_1 = [c.get_fitness() for c in self._population1]
		fitness_list_2 = [c.get_fitness() for c in self._population2]
		print fitness_list_1
		print fitness_list_2

if __name__ == '__main__':
	bias = DisplayMutationBias()
	x1 = []
	y1 = []
	x2 = []
	y2 = []
	for i in xrange(600):
		pop1, pop2 = bias.next_generation()
		for chromosome in pop1:
			x1.append(i)
			y1.append(chromosome.get_fitness())
		for chromosome in pop2:
			x2.append(i)
			y2.append(chromosome.get_fitness())

		print [c.get_fitness() for c in pop1]
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
	plt.axis([0, 600, 0, 100])
	plt.show()
		#bias.print_populations()
