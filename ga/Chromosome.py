#!/usr/bin/python

import random
import math

#Chromosome represented as a scalar value
class Chromosome:

	_max_value = 100

	def __init__(self, value):
		if value is not None:
			self.value = value
		else:
			self.value = 0

	# return objective fitness of this chromosome
	def get_fitness(self):
		return self.value

	def mutate(self):
		#convert current value to a bit string
		bit_string_value = list("")
		bit_string_value += [1 for _ in xrange(self.value)]
		bit_string_value += [0 for _ in xrange(self._max_value - self.value)]

		#mutate the bit string
		for i in xrange(self._max_value): 
			if random.random() <= 0.005:
				#bit_string_value[i] = random.choice([0,1])
				if bit_string_value[i] == 1:
					bit_string_value[i] = 0
				else:
					bit_string_value[i] = 1

		#recalculate the value/fitness
		sum = reduce(lambda x,y: x+y, bit_string_value)
		self.value = sum


if __name__ == '__main__':
	chromosome = Chromosome()
	chromosome.value = 0
	print chromosome.get_fitness()
	chromosome.mutate()
