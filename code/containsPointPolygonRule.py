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
      for featureReference in polygon1.query(dataSet2): # change query for getFeaturesThatEnvelopeIntersectsWith
        feature2 = featureReference.getFeature()
        point2 = feature2.getDefaultGeometry()
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
          self.expressionBuilder.column(self.geomName) 
        )
      ).toString()
    )
    if dataSet2.findFirst(self.expression) != None:
      return True
    return False


  def intersectsWithBuffer(self, polygon1, dataSet2): 
    store2 = dataSet2.getFeatureStore()
    features2=store2.getFeatures()
    for point2 in features2:
      point2 = point2.buffer(self.getTolerance())

    if dataSet2.getSpatialIndex() != None:
      for featureReference in polygon1.query(dataSet2): # change query for getFeaturesThatEnvelopeIntersectsWith
        feature2 = featureReference.getFeature()
        polygon2 = feature2.getDefaultGeometry()
        if polygon1.intersects(polygon2):
          return  True
      return False

    if self.geomName==None:
      self.geomName = store2.getDefaultFeatureType().getDefaultGeometryAttributeName()

    self.expression.setPhrase(
      self.expressionBuilder.ifnull(
        self.expressionBuilder.geometry(polygon1),
        self.expressionBuilder.constant(False),
        self.expressionBuilder.ST_Intersects(
          self.expressionBuilder.column(self.geomName),
          self.expressionBuilder.geometry(polygon1) 
        )
      ).toString()
    )

    if dataSet2.findFirst(self.expression) != None:
      return True
    return False


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
          for point1 in polygon1:
            point1 = geomManager.createPoint(point1.getX(),point1.getY(), subtype)
            point1.setProjection(proj)
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
        if mustConvert2D:
          multipolygon=geomManager.createMultiPolygon(subtype)
          proj=polygon1.getProjection()
          multipolygon.setProjection(proj)
          for polygon in polygon1:
            for point in polygon:
              point = geomManager.createPoint(point.getX(),point.getY(), subtype)
              point.setProjection(proj)
            multipolygon.addPolygon(polygon)
        else:
          multipolygon=polygon1
        if not operation(multipolygon, dataSet2):
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