'''
 step - 1 :
        Generate population of P chromosomes. Here P is taken to be 100.
'''

## importing all the required libraries
import random
import math
import numpy as np

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
                    if chromosome[totalBits-pos] == '1':
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
    while len(population)  != populationSize:
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
    while numberOfCrossover != 0:
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
        numberOfCrossover -= 1

    return population


''' 
Step 3 - 
    Mutation of chromosomes.
'''

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

    return population



''' Step 4 - 
        Converge the population to fittest chromosomes with the help of Fitness Function.
        Here randomness is the crucial factor because we are generating key for encryption and decryption.
        So run test (a randomness test) is considered as fitness function.
'''

## Calculating Run test score for each chromosome
def runTest(chromosome, totalBits):
    ## number of run is count of consecutive groups of 1s and 0s
    numberOfRuns = 0
    for bitPos in range(totalBits-1, -1, -1):
        ## either changing of a group or last group
        if (bitPos == 0) or (chromosome[bitPos] != chromosome[bitPos-1]):
            numberOfRuns += 1
    
    return numberOfRuns


## calculating fitness of single chromosome
def fitnessOfSingleChromosome(chromosome, totalBits):
    mean = ((2*totalBits)-1)/3
    stdDeviation = math.sqrt(16*totalBits-29)/90
    numberOfRuns = runTest(chromosome, totalBits)
    return (numberOfRuns-mean)/stdDeviation


## calculating fitness of the entire population
def fitnessOfPopulation(population, totalBits, check = 0):
    fitnessList = list()
    for chromosome in population:
        fitnessScore = fitnessOfSingleChromosome(chromosome, totalBits)
        fitnessList.append(fitnessScore)
        if (check):
            print(chromosome, fitnessScore)

    return fitnessList


## Replacing least fit chromosomes by fittest chromosomes so that population becomes more fit
def replaceChromosome(population, fitnessList, populationSize):
    maxScore = max(fitnessList)
    minScore = min(fitnessList)
    fittestChromosomeList = list()
    ## taking all the fittest chromosome
    for index in range(populationSize):
        if fitnessList[index] == maxScore:
            fittestChromosomeList.append(population[index])

    for index in range(populationSize):
        if fitnessList[index] == minScore:
            ## randomly take a fittest chromosome
            randomIndex = random.randint(0, len(fittestChromosomeList)-1)
            fittestChromosome = fittestChromosomeList[randomIndex]
            population[index] = fittestChromosome

    return population



''' Step 5 - 
        Needleman- Wunsch (NW) Algorithm - Global sequence alignment algorithm to generate final key
'''

## Needleman- Wunsch (NW) Algorithm is implemented using Dynamic Programming
def getNWScore(chromosome1, chromosome2, totalBits):
    ## Create a 2D matrix
    NW_matrix = np.zeros((totalBits+1, totalBits+1))

    ## scores for different conditions
    matchScore = 1
    mismatchPenalty = -1
    gapPenalty = -1

    ''' Step1 - Initialization '''

    ## filling the first row
    for col in range(1, totalBits+1):
        NW_matrix[0][col] = NW_matrix[0][col-1]+gapPenalty

    ## filling the first col
    for row in range(1, totalBits+1):
        NW_matrix[row][0] = NW_matrix[row-1][0]+gapPenalty


    ''' Step2 - Matrix Filling '''

    for row in range(1, totalBits+1):
        for col in range(1, totalBits+1):
            ## value taken from left, up and gap penalty added
            leftValue = NW_matrix[row][col-1]+gapPenalty
            upValue = NW_matrix[row-1][col]+gapPenalty
            
            ## value taken from diagonal and match penalty or mismatch penalty added 
            diagonalValue = NW_matrix[row-1][col-1]

            if chromosome1[row-1] == chromosome2[col-1]:
                diagonalValue += matchScore
            else:
                diagonalValue += mismatchPenalty

            NW_matrix[row][col] = max(upValue, leftValue, diagonalValue)

    ## bottom-right corner of NW Matrix contains score for alignment of chromosome1 and chromosome2
    return NW_matrix[totalBits][totalBits]




## XOR Operation
def XOR(chromosome1, chromosome2, totalBits):
    '''
        XOR-
            0 0 | 0
            0 1 | 1
            1 0 | 1
            1 1 | 0

        Same Bit - 0
        Different Bit - 1
    '''

    XORedChromosome = ""
    for bitPos in range(totalBits):
        if chromosome1[bitPos] == chromosome2[bitPos]:
            XORedChromosome += '0'
        else:
            XORedChromosome += '1'
    
    return XORedChromosome



## Applying NW Algorithm in population
def applyNW(population, populationSize, totalBits):
    fitnessList = fitnessOfPopulation(population, totalBits)

    ## Find index of fittest chromosomes
    maxScore = max(fitnessList)
    fittestIndex = list()
    for index in range(populationSize):
        if fitnessList[index] == maxScore:
            fittestIndex.append(index)

    ## Randomly choose one of the fittest chromosomes
    fittestChromosome = population[fittestIndex[random.randint(0, len(fittestIndex)-1)]]

    ## Find NW scores for each chromosome in population
    NWScoreList = list()
    for chromosome in population:
        score = getNWScore(fittestChromosome, chromosome, totalBits)
        NWScoreList.append(score)
    
    ## Find chromosomes with lowest score
    minScore = min(NWScoreList)
    ## Chromosome with lowest score
    index1 = NWScoreList.index(minScore)
    chromosome1 = population[index]
    ## Chromosome with lowest score is popped out
    population.pop(index1)
    NWScoreList.pop(index1)
    ## Chromosome with second lowest score
    secondMinScore = min(NWScoreList)
    index2 = NWScoreList.index(secondMinScore)
    chromosome2 = population[index2]
    ## Chromosome with lowest score is popped out
    population.pop(index2)
    NWScoreList.pop(index2)


    ## doing xor operation between chromosomes with lowest NW Score
    XORedChromosome = XOR(chromosome1, chromosome2, totalBits)

    ## adding new Xored chromosome
    population.append(XORedChromosome)

    return population


''' MAIN ''' 


totalBits = 64
populationSize = 100
crossoverRate = 0.85
mutationRate = 0.2

population = generatePopulation(totalBits, populationSize)

minScore = -1

'''
    Repeat steps from 1 to 4 till we get most random chromosomes. 
    As we are getting chromosomes with negative fitness values 
    we repeated the above steps till we get positive fitness score 
    for all the chromosomes in population.
'''
while minScore <= 0:
    population = crossover(population, crossoverRate)
    population = mutation(mutationRate, totalBits, population)
    fitnessList = fitnessOfPopulation(population, totalBits)
    minScore = min(fitnessList)
    population = replaceChromosome(population, fitnessList, populationSize)
    minScore = min(fitnessList)


## Applying NW algorithm to get the final key.
while populationSize > 1:
    population = applyNW(population, populationSize, totalBits)
    populationSize -= 1

finalKey = population[0]

print(finalKey)