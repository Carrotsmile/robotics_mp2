import sys

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib import collections  as mc
import matplotlib.lines as mlines
import matplotlib.patches as patches
import numpy as np

'''
Set up matplotlib to create a plot with an empty square
'''
def setupPlot():
    fig = plt.figure(num=None, figsize=(5, 5), dpi=120, facecolor='w', edgecolor='k')
    plt.autoscale(False)
    plt.axis('off')
    ax = fig.add_subplot(1,1,1)
    ax.set_axis_off()
    ax.add_patch(patches.Rectangle(
        (0,0),   # (x,y)
        1,          # width
        1,          # height
        fill=False
        ))
    return fig, ax

'''
Make a patch for a single pology 
'''
def createPolygonPatch(polygon):
    verts = []
    codes= []
    for v in range(0, len(polygon)):
        xy = polygon[v]
        verts.append((xy[0]/10., xy[1]/10.))
        if v == 0:
            codes.append(Path.MOVETO)
        else:
            codes.append(Path.LINETO)
    verts.append(verts[0])
    codes.append(Path.CLOSEPOLY)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='gray', lw=1)

    return patch
    
'''
Make a patch for the robot
'''
def createPolygonPatchForRobot(polygon):
    verts = []
    codes= []
    for v in range(0, len(polygon)):
        xy = polygon[v]
        verts.append((xy[0]/10., xy[1]/10.))
        if v == 0:
            codes.append(Path.MOVETO)
        else:
            codes.append(Path.LINETO)
    verts.append(verts[0])
    codes.append(Path.CLOSEPOLY)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='gray', lw=1)

    return patch

'''
draw roadmap, drawing a line for each edge that is green
'''
def displayRoadMap(adjList, vertMap):
    lines = []
    for key in adjList:
        value_list = adjList.get(key)
        p1 = vertMap.get(key)
        for v in value_list:
            p2 = vertMap.get(v[0])
            if p1 != None and p2 != None:
                #lines += [tuple(map(lambda x: x/10., p1)), tuple(map(lambda x: x/10., p2)), 'g']
                lines += [(p1[0] /10, p2[0] /10), (p1[1] /10, p2[1]/10), 'g']
    return lines
'''
draw the path that the robot takes from start to goal, red
'''
def drawPathStartToGoal(path, vertMap, start, goal):
    superMap = vertMap.copy()
    superMap[0] = start
    superMap[-1] = goal
    lines = []
    pairs = zip(path[:len(path)-1], path[1:])
    for p1, p2 in pairs:
        point1 = superMap.get(p1)
        point2 = superMap.get(p2)
        lines += [(point1[0]/10, point2[0]/10), (point1[1]/10, point2[1]/10), 'r']
    return lines

def drawEverything(polygons, adjList, vertMap, path, start, goal):
    fig, ax = setupPlot()
    lin = displayRoadMap(adjList, vertMap)
    print lin
    plt.plot(*lin)
    pat = drawPathStartToGoal(path, vertMap, start, goal)
    plt.plot(*pat)
    for p in range(0, len(polygons)):
        patch = createPolygonPatch(polygons[p])
        ax.add_patch(patch)    
    plt.show()

'''
Render polygon obstacles  
'''
def drawPolygons(polygons):
    fig, ax = setupPlot()
    for p in range(0, len(polygons)):
        patch = createPolygonPatch(polygons[p])
        ax.add_patch(patch)    
    plt.show()

if __name__ == "__main__":
    
    # Retrive file name for input data
    if(len(sys.argv) < 2):
        print "Please provide inpu tfile: python visualize.py [env-file]"
        exit()
    
    filename = sys.argv[1]

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
    for p in range(0, len(polygons)):
        print str(polygons[p])

    # Draw the polygons
    drawPolygons(polygons)

    
