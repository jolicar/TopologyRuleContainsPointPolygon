# encoding: utf-8

import gvsig
import sys

from org.gvsig.topology.lib.spi import AbstractTopologyRuleAction
from org.gvsig.fmap.geom import GeometryLocator

class DeletePolygonAction(AbstractTopologyRuleAction):
    
    def __init__(self):
        AbstractTopologyRuleAction.__init__(
            self,
      "containsPointPolygon",
            "Create Point Action",
            "Create Point Action",
            " This action creates a new aleatory internal point feature on the wrong polygon feature. The behavior of the create action in multigeometries is simple. If the multipolygon don't have at lest one point on his geometry, the fixed action create a new aleatory internal point feature on his first geometry."
        )
    
    def execute(self, rule, line, parameters):
      geomManager = GeometryLocator.getGeometryManager()
      try:
        dataSet1 = rule.getDataSet1()
        dataSet2 = rule.getDataSet2()
  
        store1=dataSet1.getFeatureStore()
        store2=dataSet2.getFeatureStore()
  
        proj=store1.getDefaultFeatureType().getProjection()
        subtype=store1.getDefaultFeatureType().getSubType()
  
        if geomManager.isSubtype(geom.MULTIPOLYGON,store1.getDefaultFeatureType().getType()):
          polygon=line.getFeature1().getPrimitiveAt(0)

        polygon=line.getFeature1()
        newPoint = geomManager.createPoint(polygon.getInteriorPoint().getX(),polygon.getInteriorPoint().getY(), subtype)
        newPoint.setProjection(proj)

        store2.insert(newPoint)

      except:
        ex = sys.exc_info()[1]
        gvsig.logger("Can't execute action. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass