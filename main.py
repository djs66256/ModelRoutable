#!/usr/bin/python
# -*- coding: UTF-8 -*-

from iostream import *
from scanner import *
from parser import *
from rewriter import *

print('=================== BEGIN ===================')

instream = finstream('module.model')

# print instream.readChar()
# print instream.readChar()
# print instream.readChar()
# print instream.readChar()

sc = scanner(instream)

p = parser(sc)

p.parse()

rewriter = ObjcRewriter('NMVideoModule', '.', p.getModuleAST())
rewriter.rewrite()

# for i in range(0, 10):
#   print sc.getNextToken()

# while sc.getNextToken():
#   print sc.getCurToken().type

print('=================== END ===================')