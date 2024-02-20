import ast
import numpy as np
from scipy.spatial import ConvexHull, convex_hull_plot_2d



with open('lander.txt', 'r') as f:
    shapelist = ast.literal_eval(''.join(f.readlines()))

points = np.array([])
for s in shapelist:
    for p in s[1]:
        if points.shape[0] == 0:
            points = np.array(p)
        else:
            points = np.vstack((points,np.array(p)))

hull = ConvexHull(points)
print(points)
print('hull:',points[hull.vertices])
