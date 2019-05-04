import ply.lex as lex


class Scanner(object):

  def find_tok_column(self, token):
      last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
      if last_cr < 0:
        last_cr = -1
      return token.lexpos - last_cr

  def build(self):
      self.lexer = lex.lex(object=self)

  def input(self, text):
      self.lexer.input(text)

  def token(self):
      return self.lexer.token()

  literals = "+-*/=(){}[]:',;"
  reserved = {
      'if'        : 'IF',
      'else'      : 'ELSE',
      'for'       : 'FOR',
      'while'     : 'WHILE',
      'break'     : 'BREAK',
      'continue'   : 'CONTINUE',
      'return'    : 'RETURN',
      'eye'       : 'EYE',
      'zeros'     : 'ZEROS',
      'ones'      : 'ONES',
      'print'     : 'PRINT',
  }

   # List of token names.   This is always required
  tokens = [
      # matrix binary operators
      'DOTADD',
      'DOTSUB',
      'DOTMUL',
      'DOTDIV',
      # assignment operators
      'ADDASSIGN',
      'SUBASSIGN',
      'MULASSIGN',
      'DIVASSIGN',
      'COMMENT',
      'LT',
      'GT',
      'LE',
      'GE',
      'NE',
      'EQ',
      'ID',
      'FLOATNUM',
      'INTNUM',
      'STRING',
  ]  + list(reserved.values())


  # Regular expression rules for simple tokens
  t_DOTADD    = r'.\+'
  t_DOTSUB    = r'.-'
  t_DOTMUL    = r'.\*'
  t_DOTDIV    = r'./'
  t_ADDASSIGN    = r'\+='
  t_SUBASSIGN    = r'-='
  t_MULASSIGN    = r'\*='
  t_DIVASSIGN    = r'/='
  t_LT        = r'<'
  t_GT        = r'>'
  t_LE        = r'<='
  t_GE        = r'>='
  t_NE        = r'!='
  t_EQ        = r'=='

  def t_COMMENT(self, t):
       r'\#.*'
       pass

  def t_ID(self, t):
      r'[a-zA-Z_]\w*'
      t.type = Scanner.reserved.get(t.value,'ID')    # Check for reserved words
      return t

  def t_FLOATNUM(self, t):
      r'(\d+\.\d+ | \.\d+ | \d+\.)(E\d+)?'
      t.value = float(t.value)    
      return t

  def t_INTNUM(self, t):
      r'\d+'
      t.value = int(t.value)    
      return t

  def t_STRING(self, t):
      r'".*"'
      return t

  # Define a rule so we can track line numbers
  def t_newline(self, t):
      r'\n+'
      t.lexer.lineno += len(t.value)

  # A string containing ignored characters (spaces and tabs)
  t_ignore  = ' \t'

  # Error handling rule
  def t_error(self, t):
      print("Illegal character '%s'" % t.value[0])
      t.lexer.skip(1)




  # literals = "{}()<>=;:,+-*/%&|^"


  # reserved = {
  #  'break'   : 'BREAK',
  #  'continue': 'CONTINUE',
  #  'if'      : 'IF',
  #  'else'    : 'ELSE',
  #  'print'   : 'PRINT',
  #  'repeat'  : 'REPEAT',
  #  'return'  : 'RETURN',
  #  'while'   : 'WHILE',
  #  'until'   : 'UNTIL',
  # }


  # tokens = [ "AND", "EQ", "FLOAT", "GE", "ID", "INTEGER", "LE", "NEQ", "OR",
  #            "SHL", "SHR", "STRING", "TYPE",  ] + list(reserved.values())
           

  # t_ignore = ' \t\f'

  # def t_newline(self,t):
  #     r'\n+'
  #     t.lexer.lineno += len(t.value)

  # def t_newline2(self,t):
  #     r'(\r\n)+'
  #     t.lexer.lineno += len(t.value) / 2

  # def t_error(self,t):
  #     print("Illegal character '{0}' ({1}) in line {2}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
  #     t.lexer.skip(1)

  # def t_LINE_COMMENT(self,t):
  #     r'\#.*'
  #     pass

  # def t_BLOCK_COMMENT(self,t):
  #     r'/\*(.|\n)*?\*/'
  #     t.lexer.lineno += t.value.count('\n')

  # def t_FLOAT(self,t):
  #     r"\d+(\.\d*)|\.\d+"
  #     return t

  # def t_INTEGER(self,t):
  #     r"\d+"
  #     return t
  
  # def t_STRING(self,t):
  #     r'\"([^\\\n]|(\\.))*?\"'
  #     return t

  # def t_IF(self,t):
  #     r"if"
  #     return t

  # def t_ELSE(self,t):
  #     r"else"
  #     return t

  # def t_WHILE(self,t):
  #     r"while"
  #     return t
  
  # def t_PRINT(self,t):
  #     r"print"
  #     return t

  # def t_REPEAT(self,t):
  #     r"repeat"
  #     return t

  # def t_UNTIL(self,t):
  #     r"until"
  #     return t

  # def t_BREAK(self,t):
  #     r"break"
  #     return t
  
  # def t_RETURN(self,t):
  #     r"return"
  #     return t


  # t_EQ = r"=="
  # t_NEQ = r"!="
  # t_LE = r"<="
  # t_GE = r">="
  # t_OR = r"\|\|"
  # t_AND = r"&&"
  # t_SHL = r"<<"
  # t_SHR = r">>"


  # def t_TYPE(self,t):
  #     r"\b(int|float|string)\b"
  #     return t
  
  # def t_ID(self,t):
  #     r"[a-zA-Z_]\w*"
  #     t.type = Scanner.reserved.get(t.value, 'ID')
  #     return t