import tkinter as tk
from tkinter import filedialog
import numpy as np
import plotly.graph_objs as go
from methods import concave_hull, alpha_shape, delaunay_boundary, compute_alpha

# Function to upload and process the file
def upload_and_process(method):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return

    # Load the points from the file
    points = np.loadtxt(file_path)

    # Select method based on user input
    if method == "Concave Hull":
        points_2d = points[:, :2]
        boundary_indices = concave_hull(points_2d)
        boundary_points = points[boundary_indices]
    elif method == "Alpha Shape":
        alpha = compute_alpha(points)
        boundary_indices = alpha_shape(points, alpha)
        boundary_points = points[boundary_indices]
    elif method == "Delaunay Boundary":
        boundary_indices = delaunay_boundary(points)
        boundary_points = points[boundary_indices]
    else:
        return

    # Visualize the results
    visualize_points(points, boundary_points)

# Function to visualize points with Plotly
def visualize_points(points, boundary_points):
    fig = go.Figure()

    # Non-boundary points
    non_boundary_points = np.array([p for p in points if p not in boundary_points])
    fig.add_trace(go.Scatter3d(
        x=non_boundary_points[:, 0],
        y=non_boundary_points[:, 1],
        z=non_boundary_points[:, 2],
        mode='markers',
        marker=dict(size=3, color='blue'),
        name='Non-Boundary Points'
    ))

    # Boundary points
    fig.add_trace(go.Scatter3d(
        x=boundary_points[:, 0],
        y=boundary_points[:, 1],
        z=boundary_points[:, 2],
        mode='markers',
        marker=dict(size=5, color='red'),
        name='Boundary Points'
    ))

    fig.update_layout(
        title="3D Visualization of Selected Method",
        scene=dict(
            xaxis_title="X-axis",
            yaxis_title="Y-axis",
            zaxis_title="Z-axis",
        )
    )
    fig.show()

# GUI using Tkinter
def main():
    root = tk.Tk()
    root.title("3D Building Boundary Detection")

    # Upload button
    upload_button = tk.Button(root, text="Upload and Process File", command=lambda: upload_and_process(method_var.get()))
    upload_button.pack(pady=20)

    # Dropdown menu to select method
    method_var = tk.StringVar(root)
    method_var.set("Select Method")
    method_menu = tk.OptionMenu(root, method_var, "Concave Hull", "Alpha Shape", "Delaunay Boundary")
    method_menu.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
