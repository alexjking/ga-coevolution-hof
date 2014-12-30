import Population
import random
import matplotlib.pyplot as plt
import numpy as np

class Coevolution:


	def __init__(self):
		self._pop1 = Population.Population(0)
		self._pop2 = Population.Population(0)

	def next_generation(self):
		
		pop1_sample = self._pop1.get_sample()
		pop2_sample = self._pop2.get_sample()

		pop1_copy = self._pop1.coevolve(pop2_sample)
		pop2_copy = self._pop2.coevolve(pop1_sample)

		return pop1_copy, pop2_copy

if __name__ == '__main__':
	coev = Coevolution()
	x = []
	y1 = []
	y2 = []

	# coevolve two populations, recording data
	for generation in xrange(600):
		print  "-----{}-----".format(generation)

		#get next generation of both populations
		pop1, pop2 = coev.next_generation()

		#add to current population info to graph
		for chromosome in pop1._pop:
			x.append(generation)
			y1.append(chromosome.get_fitness())
		for chromosome in pop2._pop:
			y2.append(chromosome.get_fitness())

	# generate scatter graph
	plt.scatter(x, y1, s=1, facecolor='red', lw=0)
	plt.scatter(x, y2, s=1, facecolor='grey', lw=0)
	plt.ylabel('Objective fitness')
	plt.xlabel('Generations')
	plt.scatter([i for i in xrange(600)], [50 for _ in xrange(600)], s=1, facecolor='black', lw=1)
	plt.scatter([i for i in xrange(600)], [100 for _ in xrange(600)], s=1, facecolor='black', lw=1)
	plt.axis([0, 600, 0, 110])
	plt.show()





