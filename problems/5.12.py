# spbt.py backtracking parser
# Grammar:
#    <S> -> 'a'<S>
#    <S> -> 'a' 'a'
# Test:
#    aa -> ok
#    aaa -> ok 
#    aaaa -> ok
#    a -> bad 
#    ab -> bad 
#    nil -> bad 
# Hint:
#    This grammar requires a lookahaed in the token stream

import sys   # needed to access command line arg

#global variables
tokenindex = -1
curchar = ''

def main():
   parser()      # call the parser

def parser():
   advance()   # prime curchar with first character
   if S():
      print("String in language")
   else:
      print("String not in language")

def S():
   global curchar
   if not consume('a'): return False
   if not consume('a'): return False
   while curchar == 'a':
      advance()
   return curchar == ''

def advance():
   global tokenindex, curchar
   tokenindex += 1    # move tokenindex to next token
   # check for null string or end of string
   if len(sys.argv) < 2 or tokenindex >= len(sys.argv[1]):
      curchar = ''    # signal the end by returning ''
   else:
      curchar = sys.argv[1][tokenindex]

def consume(expected):
   global curchar
   if expected == curchar:
      advance()
      return True
   else:
      return False

main()
