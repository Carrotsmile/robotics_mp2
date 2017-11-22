from spr import lineSegmentIntersect

a1, a2 = [-1, 0] , [1, 0]
b1, b2 = [0,  1] , [0, -1]

print('should be true')
print(lineSegmentIntersect(a1, a2, b1, b2))

c1, c2 = [2, 0], [4, 0]
print('should be false')
print(lineSegmentIntersect(a1, a2, c1, c2))
print(lineSegmentIntersect(a1, b1, a2, b2))
print(lineSegmentIntersect(b1, b2, c1, c2))

