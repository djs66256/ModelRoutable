#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

class Token:
  Space = ' '
  Enter = '\n'
  LBrace = '{'
  RBrace = '}'
  Colon = ':'
  Required = '!'
  Enum = 'enum'
  Routable = 'routable'
  Model = 'model'
  Comment = '//'
  Identifier = 'Identifier'

  '''
  loc: (line, col, length)
  '''
  def __init__(self, type, loc):
    self.type = type
    self.loc = loc
    self.value = None

  def setValue(self, v):
    self.value = v

  def getValue(self):
    return self.value

  def getLine(self):
    return self.loc[0]

  def getCol(self):
    return self.loc[1]

  def getColLength(self):
    return self.loc[2]

  def __str__(self):
    return 'token: ' + self.type + ', location: ' + str(self.loc) + ', value: ' + str(self.value)

class scanner:

  def __init__(self, instream):
    self.instream = instream
    self.line = 0
    self.col = 0
    self.curToken = None
    self.done = False
    self.curChar = None
    self.nextChar = None
    self.wordsReg = r'[\w\d_/]'

  def __readChar(self):
    self.col += 1
    if (self.nextChar):
      self.curChar = self.nextChar
      self.nextChar = None
      return self.curChar

    ch = self.instream.readChar()
    # print('read:' + ch)
    self.curChar = ch
    return ch

  def __backChar(self):
    self.col -= 1
    self.nextChar = self.curChar

  def __readWord(self):
    ch = self.__readChar()
    word = ''
    while(re.match(self.wordsReg, ch)):
      word += ch
      ch = self.__readChar()
    self.__backChar()
    return word
  
  def __readToNextLine(self):
    pass

  def getCurToken(self):
    return self.curToken

  def getNextToken(self):
    self.curToken = None
    self.__doNextToken()
    return self.curToken

  def __doNextToken(self):
    while(True):
      ch = self.__readChar()
      if ch == ' ':
        continue
      elif ch == '\n' or ch == '\r':
        self.line += 1
        self.col = 0
      elif ch == Token.LBrace or ch == Token.RBrace or ch == Token.Colon or ch == Token.Required:
        self.curToken = Token(ch, (self.line, self.col - 1, 1))
        break
      else :
        col = self.col - 1
        identifier = ch + self.__readWord()
        # print('read word: ' + identifier)
        if identifier == Token.Enum or identifier == Token.Model or identifier == Token.Routable:
          self.curToken = Token(identifier, (self.line, col, self.col - col + 1))
        else:
          self.curToken = Token(Token.Identifier, (self.line, col, self.col - col + 1))
          self.curToken.setValue(identifier)
        break
    
  