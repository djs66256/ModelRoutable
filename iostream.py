#!/usr/bin/python
# -*- coding: UTF-8 -*-

class stream:
  pass

class instream (stream):
  def readChar(self):
    pass

  def readLine(self):
    pass

class finstream (instream):
  def __init__(self, path):
    self.path = path
    self.file = open(path, 'r')

  def __del__(self):
    self.file.close()

  def readChar(self):
    return self.file.read(1)

  def readLine(self):
    return self.file.readline()

class outstream (stream):
  def write(self, s):
    pass
  def writeLine(self, s):
    pass

class foutstream (outstream):
  def __init__(self, path):
    self.path = path
    self.file = open(path, 'w')

  def write(self, s):
    self.file.write(s)
    return self

  def writeLine(self, s):
    self.file.writeline(s)
    return self