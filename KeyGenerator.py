

''' step - 1 :
        Generate population of P chromosomes. Here P is taken to be 200.
'''

## importing all the required libraries
import random

def generateSingleChromosome(totalBits):
    ## chromosome is of 64 bits. We take 64 length string
    chromosome = ""
    parityBits = []
    i = 1
    while i <= totalBits:
        parityBits.append(i)
        i *= 2

    for bitPos in range(totalBits, 0, -1):
        ## data bits
        if bitPos not in parityBits:
            chromosome += str(random.randint(0, 1))

        ## parity bits
        else:
            countOfSetBit = 0
            for pos in range(totalBits, bitPos, -1):
                if (pos&bitPos) != 0:
                    if chromosome[pos-bitPos-1] == '1':
                        countOfSetBit += 1
            
            ## for odd number of 1s parity bit = 1
            ## for even number of 1s parity bit = 0
            if (countOfSetBit%2) == 1:
                chromosome += '1'
            else:
                chromosome += '0'
            
    return chromosome


## generate population
population = list()
totalBits = 64
for count in range(200):
    chromosome = generateSingleChromosome(totalBits)
    ## excluding same chromosome in population
    if(chromosome in population):
        continue
    population.append(chromosome)

print((population[0]))
