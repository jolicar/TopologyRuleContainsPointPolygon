# encoding: utf-8

import gvsig
import sys

from gvsig import geom
from gvsig import uselib #para cargar plugins, scripting no tiene cargados todos los plugins
uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from org.gvsig.expressionevaluator import GeometryExpressionEvaluatorLocator, ExpressionEvaluatorLocator
from org.gvsig.topology.lib.api import TopologyLocator
from org.gvsig.topology.lib.spi import AbstractTopologyRule
from org.gvsig.fmap.geom import GeometryLocator

from deletePolygonAction import DeletePolygonAction
from createPointAction import CreatePointAction

class ContainsPointPolygonRule(AbstractTopologyRule):


  def __init__(self, plan, factory, tolerance, dataSet1, dataSet2):
      AbstractTopologyRule.__init__(self, plan, factory, tolerance, dataSet1, dataSet2)
      self.addAction(DeletePolygonAction())
      self.addAction(CreatePointAction())

      self.expression = ExpressionEvaluatorLocator.getManager().createExpression()
      self.expressionBuilder = GeometryExpressionEvaluatorLocator.getManager().createExpressionBuilder()
      self.geomName=None


  def contains(self, polygon1, dataSet2): 
    if dataSet2.getSpatialIndex() != None:
      for featureReference in dataSet2.query(polygon1): # change query for getFeaturesThatEnvelopeIntersectsWith
        feature2 = featureReference.getFeature()
        point2 = feature2.getDefaultGeometry()
        proj2=point2.getProjection()
        point2 = point2.force2D()
        point2.setProjection(proj2)
        if polygon1.contains(point2):
          return  True
      return False

    if self.geomName==None:
      store2 = dataSet2.getFeatureStore()
      self.geomName = store2.getDefaultFeatureType().getDefaultGeometryAttributeName()

    self.expression.setPhrase(
      self.expressionBuilder.ifnull(
        self.expressionBuilder.geometry(polygon1),
        self.expressionBuilder.constant(False),
        self.expressionBuilder.ST_Contains(
          self.expressionBuilder.geometry(polygon1),
          self.expressionBuilder.ST_Force2D(self.expressionBuilder.column(self.geomName))
        )
      ).toString()
    )
    if dataSet2.findFirst(self.expression) != None:
      return True
    return False


  def intersectsWithBuffer(self, polygon1, dataSet2): 
    buffer1 = polygon1.buffer(self.getTolerance())
    
    if dataSet2.getSpatialIndex() != None:
      for featureReference in dataSet2.query(buffer1): # change query for getFeaturesThatEnvelopeIntersectsWith
        feature2 = featureReference.getFeature()
        point2 = feature2.getDefaultGeometry()
        proj2=point2.getProjection()
        point2 = point2.force2D()
        point2.setProjection(proj2)
        if buffer1.intersects(point2):
          return  True
      return False

    if self.geomName==None:
      store2 = dataSet2.getFeatureStore()
      self.geomName = store2.getDefaultFeatureType().getDefaultGeometryAttributeName()

    self.expression.setPhrase(
      self.expressionBuilder.ifnull(
        self.expressionBuilder.geometry(buffer1),
        self.expressionBuilder.constant(False),
        self.expressionBuilder.ST_Intersects(
          self.expressionBuilder.ST_Force2D(self.expressionBuilder.column(self.geomName)),
          self.expressionBuilder.geometry(buffer1) 
        )
      ).toString()
    )

    if dataSet2.findFirst(self.expression) != None:
      return True
    return False

  def execute(self, taskStatus, report):
      dataSet1 = self.getDataSet1()
      dataSet2 = self.getDataSet2()
      
      store1=dataSet1.getFeatureStore()
      store2=dataSet2.getFeatureStore()

      if store1.getSRSDefaultGeometry()==store2.getSRSDefaultGeometry():
        self.execute(self, taskStatus, report)
      else:
        msgbox("Can't execute rule. The two datasets cant have a different projection")
        pass

  
  def check(self, taskStatus, report, feature1): #feature1=polygon
    try:
      polygon1 = feature1.getDefaultGeometry()
      tolerance = self.getTolerance()
      dataSet2 = self.getDataSet2()
      geometryType1 = polygon1.getGeometryType()
      
      geomManager = GeometryLocator.getGeometryManager()
      subtype = geom.D2

      mustConvert2D=(not geometryType1.getSubType() == geom.D2)

      if tolerance==0:
        operation=self.contains
      else:
        operation=self.intersectsWithBuffer
        
      if geomManager.isSubtype(geom.POLYGON,geometryType1.getType()):
        if mustConvert2D:
          proj=polygon1.getProjection()
          polygon1=polygon1.force2D()
          polygon1.setProjection(proj)

        if not operation(polygon1, dataSet2):
          report.addLine(self,
            self.getDataSet1(),
            self.getDataSet2(),
            polygon1,
            polygon1,
            feature1.getReference(),
            None,
            -1,
            -1,
            False,
            "The polygon dont have any internal point.",
            ""
          )

      elif geomManager.isSubtype(geom.MULTIPOLYGON,geometryType1.getType()):
        proj=polygon1.getProjection()
        if mustConvert2D:
          polygon1=polygon1.force2D()
          polygon1.setProjection(proj)
        if not operation(polygon1, dataSet2):
          report.addLine(self,
            self.getDataSet1(),
            self.getDataSet2(),
            multipolygon,
            multipolygon,
            feature1.getReference(), 
            None,
            -1,
            -1,
            False,
            "The multipolygon dont have any internal point.",
            ""
        )

      else:
        report.addLine(self,
          self.getDataSet1(),
          self.getDataSet2(),
          point1,
          point1,
          feature1.getReference(),
          None,
          -1,
          -1,
          False,
          "Unsupported geometry type.",
          ""
      )

    except:
      ex = sys.exc_info()[1]
      gvsig.logger("Can't execute rule. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)


def main(*args):
    pass