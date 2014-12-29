import Population
import random
import matplotlib.pyplot as plt
import numpy as np

class Coevolution:


	def __init__(self):
		self._pop1 = Population.Population(0)
		self._pop2 = Population.Population(0)
		self._pop1.mutate()
		self._pop1.mutate()
		self._pop2.mutate()
		self._pop2.mutate()

	def next_generation(self):
		#generate proportionate fitness

		# find sample of pops which are better than average of the other pop
		#self._pop1.get_roulette_wheel()



		x = []
		y1 = []
		y2 = []

		#evolve pop1
		for generation in xrange(600):

			pop1_sample = self._pop1.get_sample()
			pop2_sample = self._pop2.get_sample()

			print  "-----{}-----".format(generation)
			pop1_copy = self._pop1.coevolve(pop2_sample)
			pop2_copy = self._pop2.coevolve(pop1_sample)

			for chromosome in pop1_copy._pop:
				x.append(generation)
				y1.append(chromosome.get_fitness())

			for chromosome in pop2_copy._pop:
				y2.append(chromosome.get_fitness())

			self._pop1.print_pop()
			self._pop2.print_pop()

		plt.scatter(x, y1, s=1, facecolor='red', lw=0)
		plt.scatter(x, y2, s=1, facecolor='grey', lw=0)
		plt.ylabel('Objective fitness')
		plt.xlabel('Generations')
		plt.scatter([i for i in xrange(600)], [50 for _ in xrange(600)], s=1, facecolor='black', lw=1)
		plt.scatter([i for i in xrange(600)], [100 for _ in xrange(600)], s=1, facecolor='black', lw=1)
		plt.axis([0, 600, 0, 110])
		plt.show()


if __name__ == '__main__':
	coev = Coevolution()
	coev.next_generation()





