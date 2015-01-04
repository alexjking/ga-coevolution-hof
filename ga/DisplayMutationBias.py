import Population

import matplotlib.pyplot as plt
import numpy as np
import random

#displays a graph showing the mutation bias within two populations
class DisplayMutationBias:

	_population_size = 25

	def __init__(self):
		self._pop1 = Population.Population()
		self._pop2 = Population.Population()
		self._pop1.set_fitness_max()
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
	x = []
	y_pop1 = []
	y_pop2 = []


	for i in xrange(600):
		print i
		pop1, pop2 = bias.next_generation()

		# display average
		# x.append(i)
		# y_pop1.append(pop1.get_mean_fitness())
		# y_pop2.append(pop2.get_mean_fitness())

		# display whole sample
		for chromosome in pop1._pop:
			x.append(i)
			y_pop1.append(chromosome.get_fitness())
		for chromosome in pop2._pop:
			y_pop2.append(chromosome.get_fitness())

	plt.scatter(x, y_pop1, s=1, facecolor='red', lw=0)
	plt.scatter(x, y_pop2, s=1, facecolor='grey', lw=0)

	#generate y=50
	x_50 = [i for i in xrange(600)]
	y_50 = [50 for _ in xrange(600)]
	plt.scatter(x_50, y_50, s=1, facecolor='black', lw=1)

	plt.ylabel('Objective fitness')
	plt.xlabel('Generations')
	plt.axis([0, 600, 0, 100])
	plt.show()