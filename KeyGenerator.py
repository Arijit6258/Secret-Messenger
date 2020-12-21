'''
 step - 1 :
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
def generatePopulation(totalBits, populationSize):
    population = list()
    for count in range(populationSize):
        chromosome = generateSingleChromosome(totalBits)
        ## excluding same chromosome in population
        if(chromosome in population):
            continue
        population.append(chromosome)
    return population



'''
 step - 2 :
        Generate two offspring chromosomes from two parent chromosomes after crossover.
'''



def crossover(population, crossoverRate):
    ## calculate number of crossovers
    numberOfBits = len(population[0])
    numberOfKeys = len(population)
    numberOfCrossover = int((crossoverRate*numberOfBits*numberOfKeys)/100)

    ## doing k-point crossovers
    for i in range(numberOfCrossover):
        ## step1 - select two parent chromosomes
        parentIndex1 = random.randint(0, numberOfKeys-1)
        parentIndex2 = parentIndex1 ## making sure that index2 and index1 does not become same
        while(parentIndex1 == parentIndex2):
            parentIndex2 = random.randint(0, numberOfKeys-1)

        parentChromosome1 = population[parentIndex1]
        parentChromosome2 = population[parentIndex2]

        ## step2 - randomly selecting k value
        k = random.randint(1, 32)
        ## taking even value of k for ease of crossover algo
        if k%2 == 1:
            k += 1
        crossoverPoints = list()

        ## step3 - selecting random k crossover points
        while(len(crossoverPoints) != k):
            point = random.randint(0, len(parentChromosome1)-1)
            if point not in crossoverPoints: ## checking so that no two points are same
                crossoverPoints.append(point)

        ## sort crossoverPoints
        crossoverPoints.sort()

        ## step4 - creating offspring chromosomes by swaping chromosomal parts
        offspringChromosome1 = ""
        offspringChromosome2 = ""
        for i in range(0, k, 2):
            ## indexing to make two parts of the chromosome - index1 to index2 and index2 to index3
            index1 = 0
            if i != 0:
                index1 = crossoverPoints[i-1]+1
            index2 = crossoverPoints[i]+1
            index3 = crossoverPoints[i+1]+1

            ## keeping first part intacting
            offspringChromosome1 += parentChromosome1[index1:index2]
            offspringChromosome2 += parentChromosome2[index1:index2]

            ## interchanging second part
            offspringChromosome1 += parentChromosome2[index2:index3]
            offspringChromosome2 += parentChromosome1[index2:index3]

            ## adding last part
            if i == k-2:
                offspringChromosome1 += parentChromosome1[index3:]
                offspringChromosome2 += parentChromosome2[index3:]

        ## replace parent chromosomes with offspring chromosomes
        ##print(parentChromosome1, parentChromosome2, offspringChromosome1, offspringChromosome2, crossoverPoints)
        population[parentIndex1] = offspringChromosome1
        population[parentIndex2] = offspringChromosome2


def mutation(mutationRate, totalBits, population):
    ## calculate number of mutation operations that has to be done
    numberOfKeys = len(population)
    numberOfMutation = int((mutationRate*totalBits*numberOfKeys)/100)
    for i in range(numberOfMutation):
        ## select chromosome for mutation
        index = random.randint(0, numberOfKeys-1)
        chromosome = population[index]

        ## select position in chromosome for mutation
        position = random.randint(0, len(chromosome)-1)

        ## construct muted chromosome
        mutedChromosome = ""
        mutedChromosome += chromosome[0:position]

        ## toggle one bit
        if chromosome[position] == '1':
            mutedChromosome += '0'
        else:
            mutedChromosome += '1'

        mutedChromosome += chromosome[position+1:]

        ## replace actual chromosome with muted chromosome
        population[index] = mutedChromosome



''' MAIN ''' 

totalBits = 64
populationSize = 200
crossoverRate = 0.9
mutationRate = 0.2

population = generatePopulation(totalBits, populationSize)
crossover(population, crossoverRate)
mutation(mutationRate, totalBits, population)

