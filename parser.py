#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ast import *
from scanner import *

class parser:
  def __init__(self, scanner):
    self.scanner = scanner
    self.curToken = self.scanner.getNextToken()
    self.rootAst = ModuleAST()

  def getModuleAST(self):
    return self.rootAst

  def parse(self):
    self.__doParse()

  def __consumeToken(self):
    self.curToken = self.scanner.getNextToken()

  def __logError(self):
    print('Error :' + str(self.curToken))

  def __logAST(self, ast):
    print(ast)

  def __doParse(self):
    while (self.curToken):
      tok = self.curToken
      if tok.type == Token.Enum:
        self.__doParseEnum()
      elif tok.type == Token.Model:
        self.__doParseModel()
      elif tok.type == Token.Routable:
        self.__doParseRoutable()
      elif tok.type == Token.Comment:
        pass
      else:
        self.__logError()
        break

  def __doParseEnum(self):
    self.__consumeToken()
    enum = EnumAST()
    if self.curToken.type == Token.Identifier:
      enum.setName(self.curToken.getValue())
      self.__consumeToken()
      if (self.curToken.type == Token.LBrace):
        self.__consumeToken()
        prop = self.__doParseProperty()
        while prop:
          enum.addNameAndValue(prop.name, prop.type)
          if self.curToken.type == Token.RBrace:
            # complete
            self.rootAst.addEnum(enum)
            self.__logAST(enum)
            self.__consumeToken()
            return enum
          else:
            prop = self.__doParseProperty()
    # Error
    self.__logError()

  def __doParseProperty(self):
    name = None
    ptype = None
    optional = True
    if self.curToken.type == Token.Identifier:
      name = self.curToken.getValue()
      self.__consumeToken()
    else :
      self.__logError()
      return None

    if self.curToken.type == Token.Colon:
      self.__consumeToken()
      if self.curToken.type == Token.Identifier:
        ptype = self.curToken.getValue()
        self.__consumeToken()
        if self.curToken.type == Token.Required:
          optional = False
          self.__consumeToken()
        return PropertyAST(name, ptype, optional)
    self.__logError()
    return None

  def __doParseModelContent(self, model):
    if self.curToken.type == Token.LBrace:
      self.__consumeToken()
      prop = self.__doParseProperty()
      while prop:
        model.addProperty(prop)
        if self.curToken.type == Token.RBrace:
          self.__consumeToken()
          return model
        prop = self.__doParseProperty()
    return None

  def __doParseModel(self):
    self.__consumeToken()
    name = None
    if self.curToken.type == Token.Identifier:
      name = self.curToken.getValue()
      self.__consumeToken()
      model = self.__doParseModelContent(ModelAST(name))
      if model:
        self.__logAST(model)
        self.rootAst.addModel(model)
        return model
    self.__logError()
    return None

  def __doParseRoutableContent(self, routable):
    if self.curToken.type == Token.LBrace:
      self.__consumeToken()
      while True:
        if self.curToken.type == Token.Identifier:
          name = self.curToken.getValue()
          self.__consumeToken()
          if self.curToken.type == Token.Colon:
            self.__consumeToken()
            if self.curToken.type == Token.Identifier:
              value = self.curToken.getValue()
              routable.set(name, value)
              self.__consumeToken()
              continue
            elif self.curToken.type == Token.LBrace:
              model = self.__doParseModelContent(ModelAST(''))
              if model:
                routable.set(name, model)
                continue
        elif self.curToken.type == Token.RBrace:
          self.__consumeToken()
          return routable
        self.__logError()
        return None
        

  def __doParseRoutable(self):
    self.__consumeToken()
    name = None
    if self.curToken.type == Token.Identifier:
      name = self.curToken.getValue()
      self.__consumeToken()
      routable = self.__doParseRoutableContent(RoutableAST(name))
      if routable:
        self.rootAst.addRoutable(routable)
        self.__logAST(routable)
        return routable
    self.__logError()
    return None
