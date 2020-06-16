# encoding: utf-8

import gvsig
import sys

from org.gvsig.topology.lib.spi import AbstractTopologyRuleAction

class DeletePolygonAction(AbstractTopologyRuleAction):
    
    def __init__(self):
        AbstractTopologyRuleAction.__init__(
            self,
      "containsPointPolygon",
            "DeletePolygonAction",
            "Delete Polygon Action",
            "The delete action removes polygon features for cases when Contains Point Topology Rule it is false. The rule evaluates all the polygons. If each polygon have at least one point inside, the rule returns True. The points has to fall within the polygon's area, not on the boundary or out of it."
        )
    
    def execute(self, rule, line, parameters):
        try:
            dataSet = rule.getDataSet1()
            dataSet.delete(line.getFeature1())
        except:
            ex = sys.exc_info()[1]
            gvsig.logger("Can't execute action. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass