
from spr import areBitangent

a, b, c = [0, 1], [0, 0], [1, 0]
poly1 = [a,b,c]

d, e, f= [-1, -2], [-1, -1], [-2, -1]
poly2 = [d, e, f]

print("should not be bitangent")
print(areBitangent(b, e, poly1, poly2))

a, b, c, v = [0, 1], [0, 0], [1, 0], [1, 1]
poly1 = [a,b,c, v]

d, e, f, g= [-1, -2], [-1, -1], [-2, -1], [-2, -2]
poly2 = [d, e, f, g]

print("should not be bitangent")
print(areBitangent(b, e, poly1, poly2))
print("should be bitangent")
print(areBitangent(a, f, poly1, poly2))
