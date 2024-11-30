import numpy as np
from scipy.spatial import ConvexHull, Delaunay, distance_matrix
from collections import defaultdict

# Concave Hull (Convex Hull approximation)
def concave_hull(points_2d):
    hull = ConvexHull(points_2d)
    return hull.vertices  # Returns indices of boundary points

# Alpha Shape (Concave boundary with alpha value)
def alpha_shape(points, alpha):
    tri = Delaunay(points)
    boundary_indices = []
    for simplex in tri.simplices:
        for edge in [[simplex[0], simplex[1]], [simplex[1], simplex[2]], [simplex[2], simplex[0]]]:
            edge.sort()
            if np.linalg.norm(points[edge[0]] - points[edge[1]]) < alpha:
                boundary_indices.extend(edge)
    return list(set(boundary_indices))

# Delaunay Boundary Detection
def delaunay_boundary(points):
    tri = Delaunay(points[:, :2])
    edge_triangle_count = defaultdict(int)
    for simplex in tri.simplices:
        for edge in [[simplex[0], simplex[1]], [simplex[1], simplex[2]], [simplex[2], simplex[0]]]:
            edge_triangle_count[tuple(sorted(edge))] += 1
    boundary_points = [edge[0] for edge, count in edge_triangle_count.items() if count == 1]
    boundary_points += [edge[1] for edge, count in edge_triangle_count.items() if count == 1]
    return list(set(boundary_points))

# Compute Alpha Value Dynamically
def compute_alpha(points):
    dist_matrix = distance_matrix(points, points)
    nearest_distances = np.partition(dist_matrix, 1, axis=1)[:, 1]
    avg_distance = np.mean(nearest_distances)
    return avg_distance * 1.5  # Adjust multiplier if needed
