# h1shell.py hybrid interpreter
# test: $ python3 problems/p1008.py problems/p1008.in
import sys, time   # sys needed to access cmd line args and sys.exit()

class Token:
   def __init__(self, line, column, category, lexeme):
      self.line = line         # source program line number of the token
      self.column = column     # source program column in which token starts
      self.category = category # category of the token
      self.lexeme = lexeme     # token in string form

# global variables 
trace = False      # controls token trace
grade = False      # set to True to create output to be graded

postfix = []       # problem 10.8 data structure
stack = []

source = ''        # receives entire source program
sourceindex = 0    # index into the source code in source
line = 0           # current line number 
column = 0         # current column number
tokenslist = []    # list of tokens created by the tokenizer
tokenindex = -1    # index of current token in tokens
token = None       # current token
prevchar = '\n'    # '\n' in prevchar signals start of new line
blankline = True

co_names = []      # holds variable names
co_consts = []     # constants constants in binary form
co_code = []       # holds bytecode

# token categories that can start statements

# constants that represent token categories
EOF           = 0      # end of file
PRINT         = 1      # 'print' keyword
UNSIGNEDINT   = 2      # unsigned integer
NAME          = 3      # identifier that is not a keyword
ASSIGNOP      = 4      # '=' assignment operator
LEFTPAREN     = 5      # '('
RIGHTPAREN    = 6      # ')'
PLUS          = 7      # '+'
MINUS         = 8      # '-'
TIMES         = 9      # '*'
NEWLINE       = 10     # end of line
ERROR         = 11     # if not any of the above, then error

# displayable names for each token category
catnames = ['EOF', 'print', 'UNSIGNEDINT', 'NAME', 'ASSIGNOP',
            'LEFTPAREN', 'RIGHTPAREN', 'PLUS', 'MINUS',
            'TIMES', 'NEWLINE','ERROR']

# keywords and their token categories}
keywords = {'print': PRINT}

# one and two-character tokens and their token categories
smalltokens = {'=':ASSIGNOP, '(':LEFTPAREN, ')':RIGHTPAREN,
               '+':PLUS, '-':MINUS, '*':TIMES, '\n':NEWLINE, '':EOF}

# bytecode opcodes
UNARY_NEGATIVE    = 11      # hex 0B
BINARY_MULTIPLY   = 20      # hex 14
BINARY_ADD        = 23      # hex 17
PRINT_ITEM        = 71      # hex 47
PRINT_NEWLINE     = 72      # hex 48
STORE_NAME        = 90      # hex 5A
LOAD_CONST        = 100     # hex 64
LOAD_NAME         = 101     # hex 65

#################
# main function #
#################
def main():
   global source

   if len(sys.argv) == 2:
      try:
         infile = open(sys.argv[1], 'r')
         source = infile.read()   # read source code
      except IOError:
         print('Cannot read input file ' + sys.argv[1])
         sys.exit(1)
   else:
      print('Wrong number of command line arguments')
      print('Format: python h1.py <infile>')
      sys.exit(1)

   if source[-1] != '\n':
      source = source + '\n'

   if grade:
      print(time.strftime('%c') + '%34s' % 'YOUR NAME HERE')
      print('Interpreter = ' + sys.argv[0])
      print('Input file  = ' + sys.argv[1])

   if trace:
      print('------------------------------------------- Token trace')
      print('Line  Col Category       Lexeme\n')


   try:
      tokenizer() # tokenize source code in source
      parser()    # parse and compile

   # on an error, display an error message
   # token is the token object on which the error was detected
   except RuntimeError as emsg: 
      # output slash n in place of newline
      lexeme = token.lexeme.replace('\n', '\\n')
      print('\nError on '+ "'" + lexeme + "'" + ' line ' +
         str(token.line) + ' column ' + str(token.column))
      print(emsg)         # message from RuntimeError object
      sys.exit(1)

   if trace:
      print('------------------------------------------- Tables')
      print('co_names  = ', co_names)
      print('co_consts = ', co_consts)
      print('co_code   = ', co_code)

   if grade or trace:
      print('------------------------------------------- Program output')
   interpreter()  # interpret bytecode in co_code

####################
# tokenizer        #
####################
def tokenizer():
   global token
   curchar = ' '                       # prime curchar with space

   while True:
      # skip whitespace but not newlines
      while curchar != '\n' and curchar.isspace():
         curchar = getchar() # get next char from source program

      # construct and initialize token
      token = Token(line, column, None, '')  

      if curchar.isdigit():            # start of unsigned int?
         token.category = UNSIGNEDINT  # save category of token
         while True:
            token.lexeme += curchar    # append curchar to lexeme
            curchar = getchar()        # get next character
            if not curchar.isdigit():  # break if not a digit
               break

      elif curchar.isalpha() or curchar == '_':   # start of name?
         while True:
            token.lexeme += curchar    # append curchar to lexeme
            curchar = getchar()        # get next character
            # break if not letter, '_', or digit
            if not (curchar.isalnum() or curchar == '_'):
               break

         # determine if lexeme is a keyword or name of variable
         if token.lexeme in keywords:
            token.category = keywords[token.lexeme]
         else:
            token.category = NAME

      elif curchar in smalltokens:
         token.category = smalltokens[curchar]      # get category
         token.lexeme = curchar
         curchar = getchar()       # move to first char after the token

      else:                         
         token.category = ERROR    # invalid token 
         token.lexeme = curchar    # save lexeme
         raise RuntimeError('Invalid token')
      
      tokenslist.append(token)     # append token to tokens list
      if trace:                    # display token if trace is True
         print("%3s %4s  %-14s %s" % (str(token.line), 
            str(token.column), catnames[token.category], token.lexeme))

      if token.category == EOF:    # finished tokenizing?
         break

# getchar() gets next char from source and adjusts line and column
def getchar():
   global sourceindex, column, line, prevchar, blankline

   # check if starting a new line
   if prevchar == '\n':    # '\n' signals start of a new line
      line += 1            # increment line number                             
      column = 0           # reset column number
      blankline = True     # initialize blankline

   if sourceindex >= len(source):  # at end of source code?
      column = 1                   # set EOF column to 1
      prevchar = ''                # save current char for next call
      return ''                    # null str signals end of source

   c = source[sourceindex] # get next char in the source program
   sourceindex += 1        # increment sourceindex to next character
   column += 1             # increment column number
   if not c.isspace():     # if c not whitespace then line not blank
      blankline = False    # indicate line not blank
   prevchar = c            # save current character

   # if at end of blank line, return space in place of '\n'
   if c == '\n' and blankline:
      return ' '
   else:
      return c             # return character to tokenizer()

####################
# parser functions #
####################
# advances to the next token in the list tokens
def advance():
   global token, tokenindex 
   tokenindex += 1
   if tokenindex >= len(tokenslist):
      raise RuntimeError('Unexpected end of file')
   token = tokenslist[tokenindex]

# advances if current token is the expected token
def consume(expectedcat):
   if (token.category == expectedcat):
      advance()
   else:
     raise RuntimeError('Expecting ' + catnames[expectedcat])

# top level function of parser
#
# To handle MINUS, after each push to the postfix list, check if the top of
# stack is MINUS.  If so, pop the MINUS and add it to the postfix list.
def parser():
   leftparen_symbol = list(smalltokens.keys())[list(smalltokens.values()).index(LEFTPAREN)]
   for token in tokenslist:
      if token.category in (PLUS, TIMES, ASSIGNOP, PRINT):
         if len(stack) > 0:
            peek = stack[-1]
            # deal with + and * precedence
            if token.category == PLUS and peek.category == TIMES:
               postfix.append(stack.pop())
         stack.append(token)
      elif token.category in (MINUS,):
         stack.append(token)
      elif token.category in (NEWLINE, EOF):
         while len(stack) > 0:
            postfix.append(stack.pop())
      elif token.category in (NAME, UNSIGNEDINT):
         postfix.append(token)
         if len(stack) > 0: 
            peek = stack[-1]
            if peek.category == MINUS:
               peek = stack.pop()
               postfix.append(peek)
      elif token.category in (LEFTPAREN,):
         stack.append(token)
      elif token.category in (RIGHTPAREN,):
         while len(stack) > 0:
            token = stack.pop()
            lexeme = token.lexeme
            if lexeme == leftparen_symbol:
               if len(stack) > 0: 
                  peek = stack[-1]
                  if peek.category == MINUS:
                     peek = stack.pop()
                     postfix.append(peek)
               break
            postfix.append(token) 
      else:
         raise RuntimeError('Parsing error: unexpected token ', token.lexeme)
   while len(stack) > 0:
      postfix.append(stack.pop())

def program():
   while token.category in [NAME, PRINT]:
      stmt()

def stmt():
   simplestmt()
   consume(NEWLINE)

def simplestmt():
   if token.category == NAME:
      assignmentstmt()
   elif token.category == PRINT:    
      printstmt() 
   else:
      raise RuntimeError('Expecting statement')

def assignmentstmt():
   if token.lexeme in co_names:
      index = co_names.index(token.lexeme)
   else:
      index = len(co_names)
      co_names.append(token.lexeme)
   advance()
   consume(ASSIGNOP)
   expr()
   co_code.append(STORE_NAME)
   co_code.append(index)

def printstmt():
   advance()
   consume(LEFTPAREN)
   expr()
   co_code.append(PRINT_ITEM)
   co_code.append(PRINT_NEWLINE)
   consume(RIGHTPAREN)

def expr():   
   term()
   while token.category == PLUS:
      advance()
      term()
      co_code.append(BINARY_ADD)

def term():
   global sign
   sign = 1
   factor()
   while token.category == TIMES:
      advance()
      sign = 1
      factor()
      co_code.append(BINARY_MULTIPLY)

def factor():
   global sign 
   if token.category == PLUS:
      advance()
      factor()
   elif token.category == MINUS:
      sign = -sign
      advance()
      factor()
   elif token.category == UNSIGNEDINT:
      v = sign * int(token.lexeme)
      if v in co_consts:
         index = co_consts.index(v)
      else:
         index = len(co_consts)
         co_consts.append(v)
      co_code.append(LOAD_CONST)
      co_code.append(index) 
      advance()
   elif token.category == NAME:
      if token.lexeme in co_names:
         index = co_names.index(token.lexeme)
      else:
         raise RuntimeError('Name ' + token.lexeme + ' is not defined')
      co_code.append(LOAD_NAME)
      co_code.append(index)
      if sign == -1:
         co_code.append(UNARY_NEGATIVE)
      advance()
   elif token.category == LEFTPAREN:
      advance()
      savesign = sign
      expr()
      if savesign == -1:
         co_code.append(UNARY_NEGATIVE)
      consume(RIGHTPAREN)
   else:
      raise RuntimeError('Expecting factor')

########################
# bytecode interpreter #
########################
def interpreter():
   stack = []
   symbol = {}
   lvar = False

   for token in postfix:
      # print("interpreting token:", token.lexeme)
      if token.category == PRINT:
         v = stack.pop()
         if isinstance(v, str): v = symbol[v]
         print(v)
      elif token.category == UNSIGNEDINT:
         v = int(token.lexeme)
         stack.append(v)
      elif token.category == NAME:
         stack.append(token.lexeme)
      elif token.category == ASSIGNOP:
         v = stack.pop()
         s = stack.pop()
         symbol[s] = v
      elif token.category == PLUS:
         b = stack.pop()
         a = stack.pop()
         if isinstance(b, str): b = symbol[b]
         if isinstance(a, str): a = symbol[a]
         stack.append(a+b)
      elif token.category == MINUS:
         v = stack.pop()
         if isinstance(v, str): v = symbol[v]
         stack.append(-v)
      elif token.category == TIMES:
         b = stack.pop()
         a = stack.pop()
         if isinstance(b, str): b = symbol[b]
         if isinstance(a, str): a = symbol[a]
         stack.append(a*b)
      else:
         raise RuntimeError('interpreting error: unexpected token ', token.lexeme)

####################
# start of program #
####################
main()
if grade:
   # display interpreter's source code
   print('------------------------------------------- ' + sys.argv[0])
   print(open(sys.argv[0]).read())
