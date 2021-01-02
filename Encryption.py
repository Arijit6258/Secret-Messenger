## Import all the required libraries
import random

''' 
    Step 1 - DNA Sequencing
        DNA sequencing is the process of determining the sequence of nucleotide bases (As, Ts, Cs, and Gs) in a piece of DNA.
'''

def dnaSequencing():
    nucleotide_bases = ['A', 'T', 'C', 'G']
    nucleotide_encoding_table = dict()

    ## There are total 256 or 4^4 characters available
    ## We have to encode all the characters uniquely

    ## Characters list - 
    ## index represents ASCII value of characters
    ## characters[index] represented if the character is encoded or not
    ## characters[index] = 0 -> not encoded
    ## characters[index] = 1 -> encoded
    characters = list()
    for i in range(256): 
        characters.append(0)

    ## Generating all possible sequnences of nucleotide base of length 4
    ## It will make total possible sequences = 256
    for nucleotide_base1 in nucleotide_bases:
        for nucleotide_base2 in nucleotide_bases:
            for nucleotide_base3 in nucleotide_bases:
                for nucleotide_base4 in nucleotide_bases:
                    sequence = nucleotide_base1 + nucleotide_base2 + nucleotide_base3 + nucleotide_base4
                    ## Assign a character randomly choosen
                    index = random.randint(0, 255)
                    while characters[index] == 1:
                        index = random.randint(0, 255)
                    
                    ## Insert the character with ascii value = index in the dictionary
                    nucleotide_encoding_table[sequence] = chr(index)
                    ## Mark the character as visited
                    characters[index] = 1

    #print(len(nucleotide_encoding_table))
    #print(nucleotide_encoding_table)
    
    ## Format of encoding table is - sequence : character 
    ## But required format for encoding is character : sequence

    final_encoding_table = dict()
    for sequence in nucleotide_encoding_table:
        character = nucleotide_encoding_table[sequence]
        final_encoding_table[character] = sequence

    return final_encoding_table 

print(dnaSequencing())