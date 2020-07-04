# encoding: utf-8

import gvsig
import sys

from gvsig import uselib
uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from org.gvsig.fmap.geom import Geometry
from org.gvsig.tools.util import ListBuilder
from org.gvsig.topology.lib.api import TopologyLocator
from org.gvsig.topology.lib.spi import AbstractTopologyRuleFactory, RuleResourceLoaderUtils

from java.io import File

from containsPointPolygonRule import ContainsPointPolygonRule

class ContainsPointPolygonRuleFactory(AbstractTopologyRuleFactory):
      
    def __init__(self):
        AbstractTopologyRuleFactory.__init__(
            self,
            "ContainsPointPolygon",
            "Contains Point Polygon Rule GSoC2020",
            "The rule evaluates all the polygons. If each polygon have at least one point inside, the rule returns True. The points has to fall within the polygon's area, not on the boundary or out of it. The red polygons does the rule false.\n NOTE 1: If the Tolerance equals zero, the rule does as above. If the tolerance is greater than zero, the point are transformed into polygon. If one point of this new polygon are inside of dataset 1 polygon, the rule return True. \n NOTE 2: The behavior of the rule in multigeometries is simple. For Multipolygons, if one of their geometries has at least one point inside, the rule returns True. For Multipoints, if one of these geometries are inside of polygon's area, the rule returns True.",
            ListBuilder().add(Geometry.TYPES.POLYGON).add(Geometry.TYPES.MULTIPOLYGON).asList(),
            ListBuilder().add(Geometry.TYPES.POINT).add(Geometry.TYPES.MULTIPOINT).asList()
        )

        pathName = gvsig.getResource(__file__,'ContainsPointPolygon.json')
        url = File(pathName).toURL()
        gvsig.logger(str(url))
        json = RuleResourceLoaderUtils.getRule(url)
        self.load_from_resource(url, json)
    
    def createRule(self, plan, dataSet1, dataSet2, tolerance):
        rule = ContainsPointPolygonRule(plan, self, tolerance, dataSet1, dataSet2)
        return rule

def selfRegister():
    try:
        manager = TopologyLocator.getTopologyManager()
        manager.addRuleFactories(ContainsPointPolygonRuleFactory())
    except:
        ex = sys.exc_info()[1]
        gvsig.logger("Can't register rule. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass