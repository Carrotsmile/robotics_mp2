from spr import lineSegmentIntersect
from spr import areVisible

a1, a2 = [-1, 0] , [1, 0]
b1, b2 = [0,  1] , [0, -1]

print('should be true')
print(lineSegmentIntersect(a1, a2, b1, b2))

c1, c2 = [2, 0], [4, 0]
print('should be false')
print(lineSegmentIntersect(a1, a2, c1, c2))
print(lineSegmentIntersect(a1, b1, a2, b2))
print(lineSegmentIntersect(b1, b2, c1, c2))


print("start of areVisible tests...")
a1, a2, a3, a4 = [1, 1], [-1, 1], [-1, -1], [1, -1]
poly1 = [a1, a2, a3, a4]
v1 = [0, 2]
v2 = [0, -2]
v3 = [10, 0]
v4 = [-10, 0]

m1 = [1.1, 0]
m2 = [-1.1, 0]
polygons = [poly1]


print("should be false")
print(areVisible(v1, v2, polygons))
print(areVisible(v1, m1, polygons))
print(areVisible(v2, m2, polygons))

print("should be true")
print(areVisible(v1, v3, polygons))
print(areVisible(v2, v3, polygons))
print(areVisible(v1, v4, polygons))
print(areVisible(v2, v4, polygons))
