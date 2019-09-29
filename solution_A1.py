# --------------------------
# Name: Jiayao Pang ID: 194174300
# CP460 (Fall 2019)
# Assignment 1
# --------------------------


import math
import string


# ---------------------------------
#       Given Functions          #
# ---------------------------------
# -----------------------------------------------------------
# Parameters:   fileName (string)
# Return:       contents (string)
# Description:  Utility function to read contents of a file
#               Can be used to read plaintext or ciphertext
# -----------------------------------------------------------
def file_to_text(fileName):
    inFile = open(fileName, 'r')
    contents = inFile.read()
    inFile.close()
    return contents


# -----------------------------------------------------------
# Parameters:   text (string)
#               filename (string)            
# Return:       none
# Description:  Utility function to write any given text to a file
#               If file already exist, previous content will be over-written
# -----------------------------------------------------------
def text_to_file(text, filename):
    outFile = open(filename, 'w')
    outFile.write(text)
    outFile.close()
    return


# -----------------------------------------------------------
# Parameters:   r: #rows (int)
#               c: #columns (int)
#               pad (str,int,double)
# Return:       empty matrix (2D List)
# Description:  Create an empty matrix of size r x c
#               All elements initialized to pad
#               Default row and column size is 2
# -----------------------------------------------------------
def new_matrix(r, c, pad):
    r = r if r >= 2 else 2
    c = c if c >= 2 else 2
    return [[pad] * c for i in range(r)]


# -----------------------------------------------------------
# Parameters:   marix (2D List)
# Return:       None
# Description:  prints a matrix each row in a separate line
#               Assumes given parameter is a valid matrix
# -----------------------------------------------------------
def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(matrix[i][j], end='\t')
        print()
    return


# -----------------------------------------------------------
# Parameters:   marix (2D List)
# Return:       text (string)
# Description:  convert a 2D list of characters to a string
#               left to right, then top to bottom
#               Assumes given matrix is a valid 2D character list
# -----------------------------------------------------------
def matrix_to_string(matrix):
    text = ""
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            text += matrix[i][j]
    return text


# --------------------------------------------------------------
# Parameters:   plaintext(string)
#               key (string)
# Return:       ciphertext (string)
# Description:  Encryption using Scytale Cipher
#               Key is the diameter, i.e. # rows
#               Assume infinte length rod (infinte #columns)
# --------------------------------------------------------------
def e_scytale(plaintext, key):
    # By definition, number of rows is key
    r = int(key)
    # number of columns is the length of ciphertext/# rows    
    c = int(math.ceil(len(plaintext) / key))
    # create an empty matrix for ciphertext rxc
    cipherMatrix = new_matrix(r, c, "")

    # fill matrix horizontally with characers, pad empty slots with -1
    counter = 0
    for i in range(r):
        for j in range(c):
            cipherMatrix[i][j] = plaintext[counter] if counter < len(plaintext) else -1
            counter += 1

    # convert matrix into a string (vertically)
    ciphertext = ""
    for i in range(c):
        for j in range(r):
            if cipherMatrix[j][i] != -1:
                ciphertext += cipherMatrix[j][i]
    return ciphertext


# ---------------------------------
#       Problem 1                #
# ---------------------------------

# ----------------------------------------------------
# Parameters:   ciphertext(string)
#               key (string)
# Return:       plaintext (string)
# Description:  Decryption using Scytale Cipher
#               Assumes key is a valid integer in string format             
# ---------------------------------------------------
def d_scytale(ciphertext, key):
    plaintext = ""
    # your code here
    # get the # of rows and columns
    r = int(key)
    c = int(math.ceil(len(ciphertext) / r))

    # calculate how many empty slots in the matrix
    empty = r * c - len(ciphertext)
    temp = c - empty % c
    sub = int(empty / c)

    # create an empty matrix
    cipherMatrix = new_matrix(r, c, "")

    # fill the matrix vertically with characters in ciphertext
    counter = 0
    for i in range(c):
        for j in range(r - sub):
            cipherMatrix[j][i] = ciphertext[counter] if counter < len(ciphertext) else -1
            counter += 1
            if i >= temp and j == r - 1:
                cipherMatrix[r - 1][i] = -1
                counter -= 1

    # convert the matrix to string
    for i in range(r):
        for j in range(c):
            if cipherMatrix[i][j] != -1:
                plaintext += cipherMatrix[i][j]

    # judge whether there are more than 1 empty slots in the last column of the matrix
    # if yes, then return ''
    empty_slots = 0
    for i in range(r):
        if cipherMatrix[i][c - 1] == -1 or cipherMatrix[i][c - 1] == '':
            empty_slots += 1
    if empty_slots > 1:
        return ''

    return plaintext


# ---------------------------------
#       Problem 2                #
# ---------------------------------

# -----------------------------------------------------------
# Parameters:   dictFile (string): filename
# Return:       list of words (list)
# Description:  Reads a given dictionary file
#               dictionary file is assumed to be formatted: each word in a separate line
#               Returns a list of strings, each pertaining to a dictionary word
# -----------------------------------------------------------
def load_dictionary(dictFile):
    dictList = []
    # your code here
    # open and read the dictionary file
    dict_file = open(dictFile, 'r', encoding='ISO-8859-15')
    file_content = str(dict_file.read())
    dict_file.close()

    # split the words read from the dictionary file to a word list
    dictList = file_content.split('\n')

    return dictList


# -------------------------------------------------------------------
# Parameters:   text (string)
# Return:       list of words (list)
# Description:  Reads a given text
#               Each word is saved as an element in a list. 
#               Returns a list of strings, each pertaining to a word in file
#               Gets rid of all punctuation at the start and at the end 
# -------------------------------------------------------------------
def text_to_words(text):
    wordList = []
    # your code here
    # replace every '\n' to a space
    # then split the text with more than or equal to 1 space
    text = text.replace('\n', ' ')
    text = ' '.join(text.split())
    wordList = text.split(' ')

    # delete the punctuations in front of or behind the word element
    for i in range(len(wordList)):
        wordList[i] = wordList[i].strip(string.punctuation)

    return wordList


# -----------------------------------------------------------
# Parameters:   text (string)
#               dictFile (string): dictionary file
# Return:       (#matches, #mismatches)
# Description:  Reads a given text, checks if each word appears in dictionary
#               Returns a tuple of number of matches and number of mismatches.
#               Words are compared in lowercase.
# -----------------------------------------------------------
def analyze_text(text, dictFile):
    matches = 0
    mismatches = 0
    # your code here
    # get the dictionary list and word list
    dictList = load_dictionary(dictFile)
    wordList = text_to_words(text)

    # compare every word in word list in lowercase to the dictionary list
    # to get the # of matches and mismatches
    for word in wordList:
        if word.lower() in dictList:
            matches += 1

    mismatches = len(wordList) - matches

    return (matches, mismatches)


# -----------------------------------------------------------
# Parameters:   text (string)
#               dictFile (string): dictionary file
#               threshold (float): number between 0 to 1
# Return:       True/False
# Description:  Check if a given file is a plaintext
#               If #matches/#words >= threshold --> True
#                   otherwise --> False
#               If invalid threshold given, default is 0.9
#               An empty string is assumed to be non-plaintext.
# -----------------------------------------------------------
def is_plaintext(text, dictFile, threshold):
    # your code here
    # check if there is an invalid threshold
    # if yes then set it to a default value
    if threshold < 0 or threshold > 1.00:
        threshold = 0.90
    # check if the text is empty
    if text == '':
        return False

    # get the # of matches and mismatches
    (match, mismatch) = analyze_text(text, dictFile)
    # calculate the percentage of matches and compare to the threshold
    if float(match / (match + mismatch)) >= threshold:
        return True

    return False


# ---------------------------------
#       Problem 3                #
# ---------------------------------

# ----------------------------------------------------
# Parameters:   cipherFile (string)
#               dictFile (string)
#               startKey (int)
#               endKey (int)
#               threshold (float)
# Return:       key (string)
# Description:  Apply brute-force to break scytale cipher
#               Valid key range: 2-100 (if invalid --> print error msg and return '')
#               Valid threshold: 0-1 (if invalid --> print error msg and return '')
#               If decryption is successful --> print plaintext and return key
#               If decrytpoin fails: print error msg and return ''
# ---------------------------------------------------
def cryptanalysis_scytale(cipherFile, dictFile, startKey, endKey, threshold):
    # your code here
    # invalid key or threshold check
    if threshold > 1.0 or threshold < 0:
        print("Invalid threshold value. Operation aborted!")
        return ''
    if startKey < 2 or startKey > 100 or endKey < 2 or endKey > 100:
        print("Invalid key range. Operation aborted!")
        return ''

    # get the ciphertext from the ciphertext file
    ciphertext = file_to_text(cipherFile)

    # try every key
    for i in range(startKey, endKey + 1):
        decode = d_scytale(ciphertext, i)
        if is_plaintext(decode, dictFile, threshold):
            print('Key found: ', i)
            print(decode)
            return i
        print('key ', i, ' failed')

    print('No key was found')
    return ''  # you may change this


# ---------------------------------
#       Problem 4                #
# ---------------------------------

# ----------------------------------------------------
# Parameters:   None
# Return:       polybius_square (string)
# Description:  Returns the following polybius square
#               as a sequential string:
#               [1] [2]  [3] [4] [5] [6] [7] [8]
#           [1]      !    "   #   $   %   &   '
#           [2]  (   )    *   +   '   -   .   /
#           [3]  0   1    2   3   4   5   6   7
#           [4]  8   9    :   ;   <   =   >   ?
#           [5]  @   A    B   C   D   E   F   G
#           [6]  H   I    J   K   L   M   N   O
#           [7]  P   Q    R   S   T   U   V   W
#           [8]  X   Y    Z   [   \   ]   ^   _
# ---------------------------------------------------
def get_polybius_square():
    polybius_square = ''
    # your code here
    # use the chr() function is easier
    for i in range(32, 96):
        polybius_square += chr(i)

    return polybius_square


# --------------------------------------------------------------
# Parameters:   plaintext(string)
#               key (none)
# Return:       ciphertext (string)
# Description:  Encryption using Polybius Square
# --------------------------------------------------------------
def e_polybius(plaintext, key):
    ciphertext = ''
    # your code here
    polybius_square = get_polybius_square()

    # encrypt every character except for '\n'
    for c in plaintext:
        if c is not '\n':
            for i in range(8):
                for j in range(8):
                    if polybius_square[i * 8 + j] == c.upper():
                        ciphertext += str(i + 1)
                        ciphertext += str(j + 1)
    return ciphertext


# ---------------------------------
#       Problem 5                #
# ---------------------------------

# -------------------------------------------------------
# Parameters:   ciphertext(string)
#               key (none)
# Return:       plaintext (string)
# Description:  Decryption using Polybius Square Cipher
#               Detects invalid ciphertext --> print error msg and return ''
#               Case 1: #of chars (other than \n) is not even
#               Case 2: the ciphertext contains non-numerical chars (except \n')
# -------------------------------------------------------
def d_polybius(ciphertext, key):
    plaintext = ''
    # your code here
    # invalid ciphertext check
    if '\n' in ciphertext:
        temp = str(ciphertext).replace('\n', '')
        if len(temp) % 2 != 0:
            print("Invalid ciphertext! Decryption Failed!")
            return ''
        if temp.isnumeric() is False:
            print("Invalid ciphertext! Decryption Failed!")
            return ''

    else:
        if len(ciphertext) % 2 != 0 or len(ciphertext) == 0:
            print("Invalid ciphertext! Decryption Failed!")
            return ''
        if ciphertext.isnumeric() is False:
            print("Invalid ciphertext! Decryption Failed!")
            return ''

    polybius_square = get_polybius_square()

    # decrypt the ciphertext
    counter = 0
    while counter < len(ciphertext):
        if ciphertext[counter] is '\n':
            plaintext += '\n'
            counter += 1
        else:
            r = int(ciphertext[counter]) - 1
            c = int(ciphertext[counter + 1]) - 1
            plaintext += polybius_square[r * 8 + c]
            counter += 2

    return plaintext
