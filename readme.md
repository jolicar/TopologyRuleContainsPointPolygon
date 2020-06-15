# Contains Point Topology Rule
![TopologyRuleContainsPointPolygon]()
* **Rule type:** *Polygon rule*
* **Primary dataset:** Polygon dataset (2D, 2DM, 3D and 3DM) (*Multygeometry allowed*)
* **Secundary dataset:** Point dataset (2D, 2DM, 3D and 3DM) (*Multygeometry allowed*)
* **Brief description:** The rule evaluates all the polygons. If each polygon have at least one point inside, the rule returns *True*. The points has to fall within the polygon's area, not on the boundary or out of it. The red polygons does the rule false. In 2DM, 3D and 3DM formats, the Z coordinate or M coordinate are ignored.

***NOTE 1:** If the Tolerance equals zero, the rule does as above. If the tolerance is greater than zero, the point are transformed into "polygon". If one point of this new polygon are inside of dataset 1 polygon, the rule return True.*

***NOTE 2:** The behavior of the rule in multigeometries is simple. For Multipolygons, if one of their geometries has at least one point inside, the rule returns True. For Multipoints, if one of these geometries are inside of polygon's area, the rule returns True.*

* **Potential fixes actions:** 
  - **Delete** The delete action removes polygon features for cases when *Contains Point* Topology Rule it is false.
  - **Create feature** This action creates a new point feature at the centroid of the  wrong polygon feature.

***NOTE 3:** The behavior of the create action in multigeometries is simple. If the multipolygon don't have at lest one point on his gemetry, the fixed action create a new point feature on his first geometry centroid.*

#### [*Back to GSoC2020 Project Wiki*](https://github.com/jolicar/GSoC2020/wiki/GSoC2020-New-rules-for-the-Topology-Framework-in-gvSIG-Desktop)