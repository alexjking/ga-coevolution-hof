import random

class HallOfFame:

	hof_sample_size = 5

	def __init__(self):
		self.hof = []

	def print_hof(self):
		print "hof"
		if self._hof is not None:
			print [individual.get_fitness() for individual in self._hof]

	def update(self, individual):
		self.hof.append(individual)

	def get_sample(self):
		if self.hof_sample_size > len(self.hof):
			random_hof_sample = random.sample(self.hof, len(self.hof))
		else:
			random_hof_sample = random.sample(self.hof, self.hof_sample_size)
		return random_hof_sample

	# returns a true or false value whether this individual won against a sample from this hof
	def compete_against_hof(self, individual):
		for champion in self.get_sample():
			if individual.score(champion) == 0:
				return False
		return True # if individual has won against all selected champions


