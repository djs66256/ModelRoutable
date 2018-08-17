#!/usr/bin/python
# -*- coding: UTF-8 -*-

class AST:
  pass



class PropertyAST (AST):
  BaseTypes = ['int', 'double', 'bool']

  def __init__(self, name, type, optional):
    self.name = name
    self.type = type
    self.optional = optional

  def isBaseType(self):
    return self.type in PropertyAST.BaseTypes

  def __str__(self):
    return self.type + ' ' + self.name + ';'

class ModelAST (AST):
  def __init__(self, name):
    self.name = name
    self.properties = []

  def addProperty(self, p):
    self.properties.append(p)

  def __str__(self):
    props = ''
    for p in self.properties:
      props += '  ' + str(p) + '\n'
    return 'class ' + self.name + '{\n' + props + '\n}'

class EnumAST (AST):
  def __init__(self):
    self.name = None
    self.data = []

  def addNameAndValue(self, name, value):
    self.data.append((name, value))
  
  def setName(self, name):
    self.name = name

  def __str__(self):
    enumprops = ''
    for tp in self.data:
      if enumprops:
        enumprops += '\n'
      enumprops += '  ' + tp[0] +' = ' + tp[1] + ';'

    return 'enum ' + self.name + ' {\n' + enumprops + '\n}'


class RoutableAST (AST):
  def __init__(self, name):
    self.name = name
    self.data = {}

  def set(self, key, value):
    self.data[key] = value
  
  def get(self, key):
    return self.data[key]


class ModuleAST (AST):
  def __init__(self):
    self.asts = []
    self.modelAsts = []
    self.enumAsts = []
    self.routableAsts = []

  def addModel(self, model):
    self.modelAsts.append(model)

  def getModels(self):
    return self.modelAsts

  def addEnum(self, enum):
    self.enumAsts.append(enum)

  def getEnums(self):
    return self.enumAsts

  def addRoutable(self, r):
    self.routableAsts.append(r)

  def getRoutables(self):
    return self.routableAsts
