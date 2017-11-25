from spr import *

p1 = [[1,1], [1,-1], [3, -1], [3, 1]]
p2 = [[-3,-1], [-1,-1], [-1, 1], [-3, 1]]
polygons = [p1[::-1], p2[::-1]]

x1, y1, x2, y2 = -3, -2, 3, 2
# Compute reflex vertices
reflexVertices = findReflexiveVertices(polygons)
print "Reflexive vertices:"
print str(reflexVertices)
print ""

# Compute the roadmap 
vertexMap, adjListMap = computeSPRoadmap(polygons, reflexVertices)
print "Vertex map:"
print str(vertexMap)
print ""
print "Base roadmap:"
print str(adjListMap)
print ""

# Update roadmap
start, goal, updatedALMap = updateRoadmap(polygons, vertexMap, adjListMap, x1, y1, x2, y2)
print "Updated roadmap:"
print str(updatedALMap)
print ""

# Search for a solution     
path, length = uniformCostSearch(updatedALMap, start, goal)
print "Final path:"
print str(path)
print "Final path length:" + str(length)