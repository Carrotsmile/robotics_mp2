import sys
import numpy as np
from math import sqrt
'''
Report reflexive vertices
'''
#http://planning.cs.uiuc.edu/node271.html#fig:bitangentcomp
def findReflexiveVertices(polygons):
    vertices=[]
    
    # Your code goes here
    # You should return a list of (x,y) values as lists, i.e.
    # vertices = [[x1,y1],[x2,y2],...]
    for polygon in polygons:
        for i in range(len(polygon)):
            left = np.array(polygon[i-1])
            mid = np.array(polygon[i])
            right = np.array(polygon[(i + 1) % len(polygon)])

            det = np.linalg.det(np.array([left-mid, right-mid]))
            if det > 0:
                vertices.append(polygon[i])
    return vertices

'''
Euclidean Distance between vertices
'''
def distance(v1, v2):
    a = (v1[0] - v2[0]) ** 2
    b = (v1[1] - v2[1]) ** 2
    return sqrt(a + b)

'''
find if three vertices are reflective
'''
def isReflexive(left, mid, right):
    a = np.array(left)
    b = np.array(mid)
    c = np.array(right)
    det = np.linalg.det(np.array([a-b, c-b]))
    return det < 0

'''
given two vertices and their corresponding polygons,
are the two vertices bitangent?
'''
def areBitangent(v1, v2, poly1, poly2):
    # (f(p1, p2, p5) xor f(p3, p2, p5)) or (f(p4, p5, p2) xor f(p6, p5, p2))
    # left1 -> p1, mid1 -> p2, right1 -> p3
    # left2 -> p4, mid2 -> p5, right2 -> p6

    #get indices of vertices being analyzed
    mid1_index, mid2_index = poly1.index(v1), poly2.index(v2)

    #get the physical vertices themselves
    left1, left2 = poly1[mid1_index-1], poly2[mid2_index-1]
    mid1, mid2   = poly1[mid1_index], poly2[mid2_index]
    right1, right2 = poly1[(mid1_index + 1) % len(poly1)], poly2[(mid2_index + 1) % len(poly2)]

    f = isReflexive
    return not ((f(left1, mid1, mid2) != f(right1, mid1, mid2)) or (f(left2, mid2, mid1) != f(right2, mid2, mid1)))
    
'''
Compute the roadmap graph
'''
def computeSPRoadmap(polygons, reflexVertices):

    vertexMap = dict()
    revVertexMap = dict()
    reflexMap = dict()
    adjacencyListMap = dict()
    
    #create dictionaries for convience
    for i in range(1, len(reflexVertices) + 1):
        vertexMap[i] = reflexVertices[i-1]
        reflexMap[tuple(reflexVertices[i-1])] = reflexVertices[i-1]
        revVertexMap[tuple(reflexVertices[i-1])] = i

    #this is just to get the 'easy' edges around the polygons
    for polygon in polygons:
        for i in range(len(polygon)):
            print(polygon[i-1])
            left = reflexMap.get(tuple(polygon[i - 1]))
            right = reflexMap.get(tuple(polygon[(i+1) % len(polygon)]))
            mid = reflexMap.get(tuple(polygon[i]))
            if left != None and mid != None:
                #add left to adjacencyListMap
                a, b = revVertexMap.get(tuple(mid)), revVertexMap.get(tuple(left))
                adj = adjacencyListMap.get(a)
                if adj == None:
                    adjacencyListMap[a] = []
                adjacencyListMap[a].append([b, distance(mid, left)])
            if right != None and mid != None:
                #add right to adjacencyListMap
                a, b = revVertexMap.get(tuple(mid)), revVertexMap.get(tuple(right))
                adj = adjacencyListMap.get(a)
                if adj == None:
                    adjacencyListMap[a] = []
                adjacencyListMap[a].append([b, distance(mid, right)])

    
    # Your code goes here
    # You should check for each pair of vertices whether the
    # edge between them should belong to the shortest path
    # roadmap. 
    #
    # Your vertexMap should look like
    # {1: [5.2,6.7], 2: [9.2,2.3], ... }
    #
    # and your adjacencyListMap should look like
    # {1: [[2, 5.95], [3, 4.72]], 2: [[1, 5.95], [5,3.52]], ... }
    #
    # The vertex labels used here should start from 1
    
    return vertexMap, adjacencyListMap

'''
Perform uniform cost search 
'''
def uniformCostSearch(adjListMap, start, goal):
    path = []
    pathLength = 0
    
    # Your code goes here. As the result, the function should
    # return a list of vertex labels, e.g.
    #
    # path = [23, 15, 9, ..., 37]
    #
    # in which 23 would be the label for the start and 37 the
    # label for the goal.
    
    return path, pathLength

'''
Agument roadmap to include start and goal
'''
def updateRoadmap(polygons, vertexMap, adjListMap, x1, y1, x2, y2):
    updatedALMap = dict()
    startLabel = 0
    goalLabel = -1

    # Your code goes here. Note that for convenience, we 
    # let start and goal have vertex labels 0 and -1,
    # respectively. Make sure you use these as your labels
    # for the start and goal vertices in the shortest path
    # roadmap. Note that what you do here is similar to
    # when you construct the roadmap. 
    
    return startLabel, goalLabel, updatedALMap

if __name__ == "__main__":
    
    # Retrive file name for input data
    if(len(sys.argv) < 6):
        print "Five arguments required: python spr.py [env-file] [x1] [y1] [x2] [y2]"
        exit()
    
    filename = sys.argv[1]
    x1 = float(sys.argv[2])
    y1 = float(sys.argv[3])
    x2 = float(sys.argv[4])
    y2 = float(sys.argv[5])

    # Read data and parse polygons
    lines = [line.rstrip('\n') for line in open(filename)]
    polygons = []
    for line in range(0, len(lines)):
        xys = lines[line].split(';')
        polygon = []
        for p in range(0, len(xys)):
            polygon.append(map(float, xys[p].split(',')))
        polygons.append(polygon)

    # Print out the data
    print "Pologonal obstacles:"
    for p in range(0, len(polygons)):
        print str(polygons[p])
    print ""

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
    

    # Extra visualization elements goes here
