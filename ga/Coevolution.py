import Population
import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import sys

class Coevolution:


	def __init__(self, hof, hof_filter=False, intransitive_superiority=False):
		if intransitive_superiority:
			self._pop1 = Population.IntransitiveSuperiorityPopulation(hof, hof_filter)
			self._pop2 = Population.IntransitiveSuperiorityPopulation(hof), hof_filter
		else:
			self._pop1 = Population.Population(hof, hof_filter)
			self._pop2 = Population.Population(hof, hof_filter)

	def next_generation(self):
		
		pop1_sample = self._pop1.get_sample()
		pop2_sample = self._pop2.get_sample()

		pop1_copy = self._pop1.coevolve(self._pop2)
		pop2_copy = self._pop2.coevolve(self._pop1)

		return pop1_copy, pop2_copy

if __name__ == '__main__':
	hof = False
	hof_filter = False

	if len(sys.argv)>1 and sys.argv[1] == "hof":
		hof = True
		if len(sys.argv)>2  and sys.argv[2] == "filter":
			hof_filter = True
	coev = Coevolution(hof=hof, hof_filter=hof_filter, intransitive_superiority=False)
	x = []
	y1 = []
	y2 = []

	y_pop1_subj = []
	y_pop1_subj_list = []
	y_pop2_subj = []

	# coevolve two populations, recording data
	for generation in xrange(600):
		print  "-----{}-----".format(generation)

		#get next generation of both populations
		pop1, pop2 = coev.next_generation()

		#get subjective averages
		y_pop1_subj.append(pop1.get_subjective_average())
		y_pop2_subj.append(pop2.get_subjective_average())

		#add to current population info to graph
		for chromosome in pop1._pop:
			x.append(generation)
			y1.append(chromosome.get_fitness())
		for chromosome in pop2._pop:
			y2.append(chromosome.get_fitness())

	# generate scatter graph

	f = plt.figure(1)

	gs = gridspec.GridSpec(3,1, height_ratios=[8,1,1])

	ax = plt.subplot(gs[0])
	#plt.subplot(311)
	plt.scatter(x, y1, s=1, facecolor='red', lw=0)
	plt.scatter(x, y2, s=1, facecolor='grey', lw=0)
	plt.ylabel('Objective fitness')
	#plt.xlabel('Generations')
	plt.scatter([i for i in xrange(600)], [50 for _ in xrange(600)], s=1, facecolor='black', lw=1)
	plt.scatter([i for i in xrange(600)], [100 for _ in xrange(600)], s=1, facecolor='black', lw=1)
	plt.axis([0,  600, 0, 100])
	ax.tick_params(labelbottom='off')

	ax2 = plt.subplot(gs[1])
	plt.axis([0, 600, 0, 1])
	plt.yticks([0,1])
	ax2.tick_params(labelbottom='off')
	plt.scatter(xrange(600), y_pop1_subj, s=8, facecolor='red', lw=0)

	ax3 = plt.subplot(gs[2])
	plt.axis([0, 600, 0, 1])
	plt.yticks([0,1])
	plt.xlabel('Generations')
	plt.scatter(xrange(600), y_pop2_subj, s=8, facecolor='grey', lw=0)

	f.text(0.025, 0.21, "Average subj. fitness", rotation="vertical", va="center")

	f.tight_layout()
	#f.subplots_adjust()

	plt.show()





