#Reference: Parts of the code idea was gotten from: https://justcryptography.com/playfair_cipher-implementation/

#Add filler character 'X' if there is a same letter pair
import string #import string library
import re #import regular expression library

def text_pair(text):

    text_pair = ''
    i = 0
    while i < len(text):
        pair = text[i]
        if i == len(text)- 1 or text[i] == text[i+1]:
            pair += 'X'
            i += 1
        else:
            pair += text[i+1]
            i += 2

        text_pair += pair

    return text_pair


def cipher_matrix(key):
    key = key.upper()
    n = 5
    m = 5
    matrix = [0] * n
    for x in range (n):
        matrix[x] = [0] * m
    
    letters = []
    row = 0
    col = 0
    #Create matrix with the key
    for letter in key:
        if letter not in letters:
            matrix[row][col] = letter
            letters.append(letter)
        else:
            continue
        if (col==4):
            col = 0
            row += 1
        else:
            col += 1
    
    #Complete the matrix with letters from A to Z
    alphabet = string.ascii_uppercase.replace('J', '')
    

    for letter in alphabet:
        #No letter repitition
        if letter not in letters: 
            letters.append(letter)

    #filling the matrix with the letters            
    index = 0
    for i in range(5):
        for j in range(5):
            matrix[i][j] = letters[index]
            index+=1
    return matrix

#Code to find position of a letter in the matrix

def indexOf(letter,matrix):
    for i in range(len(matrix)): #iterate through i in the length of the matrix

        try:
            index = matrix[i].index(letter)
            return (i,index)
        except:
            continue
        
#playfair_cipher cipher encryption

def playfair_cipher(key, text, clause):
    text_size = len(text) #size of text
    alphabet = string.ascii_uppercase #initiliase the variable alphabet to be referenced later
    inc = 1
    non_letter = '' #variable to keep track of removed non-letter characters from text
    non_letter_index = []
    if clause != 'encrypt': #If 'clause' is encrypt, encryption takes place. Otherwise, decryption is done
        inc = -1
    matrix = cipher_matrix(key)
    text = text.upper()
    #text = text.replace(' ', '').replace(',', '')
    for i in range(len(text)):
        if text[i] not in alphabet:
            non_letter_index.append(i)
            non_letter += text[i] 

    regex = re.compile('[^a-zA-Z]') #regular expression syntax
    text = regex.sub('', text) #Replace letter not in alphabet to ''
    text = text_pair(text)

    encrypted_text = ''

    #Implementation of Playfair shift rules
    for (l1, l2) in zip(text[0::2], text[1::2]):
        row1,col1 = indexOf(l1,matrix)
        row2,col2 = indexOf(l2,matrix)
        if row1==row2: #If the letters are in the same row in the matrix
            encrypted_text += matrix[row1][(col1+inc)%5] + matrix[row2][(col2+inc)%5]
        elif col1==col2: #If the letters are in the same column
            encrypted_text += matrix[(row1+inc)%5][col1] + matrix[(row2+inc)%5][col2]
        else: #If letters are in a separate row and column
            encrypted_text += matrix[row1][col2] + matrix[row2][col1]

    result = ''
    #joining encrypted_text with non_letter characaters, maintaning their index in the original text
    x = 0
    list1 = list(encrypted_text) 
    for i in non_letter_index:
        list1.insert(i, non_letter[x])
        x += 1
    result = "".join([str(i) for i in list1])
    return result

'''print ('Encrypting')
print (playfair_cipher('secret', 'mosque', 'encrypt'))
print ('Decrypting')
print ( playfair_cipher('MONARCHY', 'ONTSML', 'dec'))'''
