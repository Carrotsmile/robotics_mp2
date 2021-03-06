import sys
import numpy as np
import itertools as it
import heapq
import visualize
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

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
'''
test if line segments intersect with each other 
by solving system of equation for two seperate parametric
equations
'''
def lineSegmentIntersect(a1, a2, b1, b2):
    A1, A2, B1, B2 = np.array(a1), np.array(a2), np.array(b1), np.array(b2)
    return intersect(A1, A2, B1, B2)
    

'''
Returns True if the two vertices are visible to each other,
else it returns false
'''
def areVisible(v1, v2, otherPolygons):
    for polygon in otherPolygons:
        for p1, p2 in zip(polygon, polygon[1:] + [polygon[0]]):
            #print((v1, v2, p1, p2))
            if lineSegmentIntersect(v1, v2, p2, p1) and p1 != v1 and v2 != p2 and p1 != v2 and p2 != v1:
                return False
            #if lineSegmentIntersect(v1, v2, p2, p1) != lineSegmentIntersect(v1, v2, p1, p2):
                #return False
    return True

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
            #print(polygon[i-1])
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

    #creates all pairs of polygons
    polypairs = list(it.combinations(polygons, 2))
    for poly1, poly2 in polypairs:
        pointpairs = list(it.product(poly1, poly2))
        #otherpolies = filter(lambda poly: poly != poly1 and poly != poly2, polygons)
        otherpolies = polygons
        for p1, p2 in pointpairs:
            #check if p1 and p2 are reflex
            i1 = revVertexMap.get(tuple(p1))
            i2 = revVertexMap.get(tuple(p2))
            v = areVisible(p1, p2, otherpolies)
            bi = areBitangent(p1, p2, poly1, poly2)
            if v and bi and (i1 != None) and (i2 != None):
                dis = distance(p1, p2)
                if(adjacencyListMap.get(i1) == None):
                    adjacencyListMap[i1] = []
                adjacencyListMap[i1].append([i2, dis])
                if(adjacencyListMap.get(i2) == None):
                    adjacencyListMap[i2] = []
                adjacencyListMap[i2].append([i1, dis])
    for poly in polygons:
        ppairs = list(it.combinations(poly, 2))
        for p1, p2 in ppairs:
            v = areVisible(p1, p2, [poly])
            bi = areBitangent(p1, p2, poly, poly)
            if v and bi:
                i1 = revVertexMap.get(tuple(p1))
                i2 = revVertexMap.get(tuple(p2))
                dis = distance(p1, p2)
                if(adjacencyListMap.get(i1) == None):
                    adjacencyListMap[i1] = []
                adjacencyListMap[i1].append([i2, dis])
                if(adjacencyListMap.get(i2) == None):
                    adjacencyListMap[i2] = []
                adjacencyListMap[i2].append([i1, dis])
    # Your vertexMap should look like
    # {1: [5.2,6.7], 2: [9.2,2.3], ... }
    #
    # and your adjacencyListMap should look like
    # {1: [[2, 5.95], [3, 4.72]], 2: [[1, 5.95], [5,3.52]], ... }
    #
    # The vertex labels used here should start from 1
    
    return vertexMap, adjacencyListMap

'''
Special bitangent, where only one of the points neighbors are looked at
because the other point is a goal/start location
'''
def specBitangent(s1, v1, poly1):
    i1 = poly1.index(v1)
    left = poly1[i1-1]
    right = poly1[(i1+1)%len(poly1)]
    a, b = isReflexive(s1, v1, left), isReflexive(s1, v1, right)
    return a == b

'''
Perform uniform cost search 
'''
def uniformCostSearch(adjListMap, start, goal):

    #essentially just translated from the psuedocode on wikipedia
    path = []
    pathLength = 0
    
    gScore = dict()
    #fScore = dict()
    cameFrom = dict()
    openSet = dict()
    openHeap = []
    closedSet = dict()

    gScore[start] = 0
    t = (gScore[start], start)
    heapq.heappush(openHeap, t)
    openSet[start] = t

    while(len(openHeap) > 0):
        expNode = heapq.heappop(openHeap)
        if expNode[1] == goal:
            #trace through cameFrom to find the path
            result_path = []
            currNode = goal
            while cameFrom.get(currNode) != None:
                result_path.append(currNode)
                currNode = cameFrom.get(currNode)
            result_path.append(start)
            result_path = result_path[::-1]
            len_results = 0
            for p1, p2 in zip(result_path[:len(result_path) -1], result_path[1:]):
                a = adjListMap.get(p1)
                for edge in a:
                    if edge[0] == p2:
                        len_results += edge[1]
                        break
            return result_path, len_results
        #print expNode
        lip = adjListMap.get(expNode[1])
        if lip == None:
            lip = []
        for neighbor in lip:
            print neighbor
            if closedSet.get(neighbor[0]) != None:
                continue
            t_gScore = gScore[expNode[1]] + neighbor[1]
            if gScore.get(neighbor[0]) != None and gScore.get(neighbor[0]) <= t_gScore:
                continue

            cameFrom[neighbor[0]] = expNode[1] #test
            gScore[neighbor[0]] = t_gScore

            temp = (gScore[neighbor[0]], neighbor[0])
            if openSet.get(neighbor[0]) == None:
                openSet[neighbor[0]] = temp
                heapq.heappush(openHeap, temp)
            else:
                r = openSet[neighbor[0]]
                r_i = openHeap.index(r)
                openHeap[r_i] = temp
                openSet[neighbor[0]] = temp
                heapq.heapify(openHeap)
    #return empty list for no path found
    return [], 0
    # Your code goes here. As the result, the function should
    # return a list of vertex labels, e.g.
    #
    # path = [23, 15, 9, ..., 37]
    #
    # in which 23 would be the label for the start and 37 the
    # label for the goal.

'''
Agument roadmap to include start and goal
'''
def updateRoadmap(polygons, vertexMap, adjListMap, x1, y1, x2, y2):
    updatedALMap = adjListMap.copy() #copy instead because we are returning upated map
    startLabel = 0
    goalLabel = -1
    start = [x1, y1]
    goal = [x2, y2]

    #this is supposed to be for making it convient to pass the right polygons as arguments
    polyMap = dict()
    for polygon in polygons:
        for i in vertexMap:
            v = vertexMap.get(i)
            if v in polygon:
                polyMap[i] = polygon
    #creates edge between start and goal if they are visible
    if areVisible(start, goal, polygons):
        if updatedALMap.get(startLabel) == None:
            updatedALMap[startLabel] = []
        if updatedALMap.get(goalLabel) == None:
            updatedALMap[goalLabel] = []
        updatedALMap[startLabel].append([goalLabel, distance(start,goal)])
        updatedALMap[goalLabel].append([startLabel, distance(start,goal)])
    for i in vertexMap:
        v = vertexMap.get(i)
        f_poly = polyMap[i]
        #other_polygons = filter(lambda x: x != f_poly, polygons)
        other_polygons = polygons
        bi_start, vis_start = specBitangent(start, v, polyMap[i]), areVisible(start, v, other_polygons)
        bi_goal, vis_goal = specBitangent(goal, v, polyMap[i]), areVisible(goal, v, other_polygons)
        if bi_start and vis_start:
            #add connection from start to v
            if updatedALMap.get(startLabel) == None:
                updatedALMap[startLabel] = []
            start_dist = distance(start, v)
            updatedALMap[startLabel].append([i, start_dist])
            if updatedALMap.get(i) == None:
                updatedALMap[i] = []
            updatedALMap[i].append([startLabel, start_dist])
            
        if bi_goal and vis_goal:
            #add connection from goal to v
            if updatedALMap.get(goalLabel) == None:
                updatedALMap[goalLabel] = []
            goal_dist = distance(goal, v)
            updatedALMap[goalLabel].append([i, goal_dist])
            if updatedALMap.get(i) == None:
                updatedALMap[i] = []
            updatedALMap[i].append([goalLabel, goal_dist])

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
    
    visualize.drawEverything(polygons, updatedALMap, vertexMap, path, [x1, y1], [x2, y2])
    # Extra visualization elements goes here
