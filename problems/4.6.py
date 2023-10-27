# sp.py parser
import sys   # needed to access command line arg

#global variables
tokenindex = -1
token = ''
buffer = ''

def main():
   try:
      load()
      parser()         # call the parser
   except RuntimeError as emsg:
      print(emsg)

def load():
   global buffer
   if len(sys.argv) >= 2:
      f = open(sys.argv[1], "r")
      buffer = f.read()
   print(buffer)

def advance():
   global tokenindex, token
   global buffer
   tokenindex += 1     # move tokenindex to next token
   # check for null string or end of string
   if tokenindex >= len(buffer):
      token = ''      # signal the end by returning null string
   else:
      token = buffer[tokenindex]

def consume(expected):
   if expected == token:
      advance()
   else:
      raise RuntimeError('Expecting ' + expected)

def parser():
   advance()   # prime token with first character
   S()         # call function for start symbol
   # test if end of input string
   if token != '': 
      print('Garbage following <S>-string')
   
def S():
   A()
   C()

def A():
   consume('a')
   consume('b')

def C():
   if token == 'c':
      # perform actions corresponding to production 3
      advance()
      C()
   elif token == 'd':
      # perform action corresponding to production 4
      advance()
   else:
      raise RuntimeError('Expecting c or d')

main()
