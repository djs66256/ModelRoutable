#!/usr/bin/python
# -*- coding: UTF-8 -*-

from iostream import *
from ast import *
import os

class rewriter:
  pass

class ObjcRewriter (rewriter):
  def __init__(self, name, path, ast):
    self.name = name
    self.path = path
    self.moduleAST = ast

    hpath = os.path.join(path, name + '.h')
    mpath = os.path.join(path, name + '.m')
    self.hstream = foutstream(hpath)
    self.mstream = foutstream(mpath)

  def rewrite(self):
    self.__doRewriteHFile()
    self.__doRewriteMFile()

  def __doRewriteHFile(self):
    self.hstream.write('\n#import <UIKit/UIKit.h>\n\n')
    self.__doRewriteHFileEnum()
    self.__doRewriteHFileModel()
    self.__doRewriteHFileRoutable()

  def __doRewriteHFileEnum(self):
    for enum in self.moduleAST.getEnums():
      self.hstream.write('typedef NS_ENUM(NSInteger, ').write(enum.name)
      self.hstream.write(') {\n')
      first = True
      for tp in enum.data:
        if not first:
          self.hstream.write('\n')
        else:
          first = False
        self.hstream.write('  ').write(tp[0]).write(' = ').write(tp[1]).write(',')
      self.hstream.write('\n};\n\n')

  def __doRewriteHFileModel(self):
    pass

  def __isEnumType(self, type):
    for enum in self.moduleAST.getEnums():
      if enum.name == type:
        return True
    return False

  ObjcTypeMap = {
    'String': 'NSString',
    'int': 'NSInteger',
    'bool': 'BOOL'
  }

  def __mapObjcType(self, type):
    o = ObjcRewriter.ObjcTypeMap.get(type) or type
    return o
  

  '''

   - (void)openVideoDetailWithParams:(void(^)(id<NMVideoDetailViewControllerInParamsBuilder> builder))builder
                              finish:(void(^)(id<NMVideoDetailViewControllerOutParams> result, NSError *error))finish;
  '''
  def __doRewriteHFileRoutable(self):
    for routable in self.moduleAST.getRoutables():
      inparamsBuilder = routable.get('class') + 'InParamsBuilder'
      outparams = routable.get('class') + 'OutParams'

      self.__doRewriteHfileInParams(inparamsBuilder, routable.get('in'))
      self.__doRewriteHfileOutParams(outparams, routable.get('out'))

    # router
    self.hstream.write('@interface Navigator (').write(self.name).write(')\n')
    for routable in self.moduleAST.getRoutables():
      inparamsBuilder = routable.get('class') + 'InParamsBuilder'
      outparams = routable.get('class') + 'OutParams'
      self.hstream.write('- (void)open').write(routable.name).write('WithParams:(void(^)(id<').write(inparamsBuilder).write('> builder))builder finish:(void(^)(id<').write(outparams).write('> result, NSError *error))finish;\n')
    self.hstream.write('@end\n\n')

  '''
  @protocol NMVideoDetailViewControllerInParamsBuilder <NSObject>
  @property (nonatomic, copy) id<NMVideoDetailViewControllerInParamsBuilder>(^mvId)(NSString *mvId);
  @end
  '''
  def __doRewriteHfileInParams(self, name, ast):
    self.hstream.write('@protocol ').write(name).write(' <NSObject>\n')
    for p in ast.properties:
      if p.isBaseType() or p.type.startswith('id') or self.__isEnumType(p.type):
        self.hstream.write('@property (nonatomic, copy) id<').write(name).write('>(^').write(p.name).write(')(').write(self.__mapObjcType(p.type)).write(' ').write(p.name).write(');\n')
      else:
        self.hstream.write('@property (nonatomic, copy) id<').write(name).write('>(^').write(p.name).write(')(').write(self.__mapObjcType(p.type)).write(' *').write(p.name).write(');\n')
    self.hstream.write('@end\n\n')

  '''
  @protocol NMVideoDetailViewControllerOutParams <NSObject>
  @property (nonatomic, strong) NSString *mvId;
  @end
  '''
  def __doRewriteHfileOutParams(self, name, ast):
    self.hstream.write('@protocol ').write(name).write(' <NSObject>\n')
    for p in ast.properties:
      if p.isBaseType() or self.__isEnumType(p.type):
        self.hstream.write('@property (nonatomic, assign) ').write(self.__mapObjcType(p.type)).write(' ').write(p.name).write(';\n')
      else:
        self.hstream.write('@property (nonatomic, strong) ').write(self.__mapObjcType(p.type))
        if p.type.startswith('id'):
          self.hstream.write(' *')
        else:
          self.hstream.write(' ')
        self.hstream.write(p.name).write(';\n')
    self.hstream.write('@end\n\n')

  def __doRewriteMFile(self):
    self.__doRewriteMFileModel()
    self.__doRewriteMFileRoutable()

  def __doRewriteMFileModel(self):
    pass

  def __doRewriteMFileRoutable(self):
    pass