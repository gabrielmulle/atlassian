"""
Pyhton script
"""

import csv
import sys
import os.path
from os import path
import fileinput

def findreplace(filename, output,swap):
    # reading the file to be modified 
    text = open(filename, "r")

    # open CSV file with old & new values to find and replace
    with open(swap, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        find = 0
        replace = 1

    #interate through each row in CSV
        line = 1
        for row in csv_reader:
            try:
                #join() method combines all contents of file to be modified and forms as a string 
                text = ''.join([i for i in text])  
                
                # find and replace content based on CSV mapping
                print('replacing instances of {} with {}'.format(row[find], row[replace]))
                text = text.replace(row[find],row[replace]) 
                
                # output file to be written to
                # this is a copy of the original with replaced strings 
                x = open(output,"w") 
                
                # all the replaced text is written in the output file 
                x.writelines(text) 
                x.close()
                line += 1
            except IndexError:
                print('\\nERROR: List index out of range on line ' + str(line) + '. There is likely a row without a column value. Please verify the find,replace mapping CSV')
                sys.exit(1)

def main():
    try:
        filename = sys.argv[1]      #take 1st output from command line as filename
        swap = sys.argv[2]          #take 2nd output from command line as findAndReplace mapping
    except:
        print ('\\nPlease enter the csv filename in the following format: python3 findreplace.py originalFile.csv findAndReplaceMapping.csv')
        sys.exit(1)     #exit program if no arguments present
    if (path.exists(filename)):     #check if file is in same directory
        output = 'output_test.csv'
        print('\\nOriginal file:', filename)
        print('Mapping file:', swap)
        findreplace(filename, output,swap)

        print('\\nOutput file: ', output, '\\n')
    else:
        print("Could not find the file " + filename + ". Make sure you're in the same directory.\\n")
        exit
if __name__ == '__main__':
    main()
