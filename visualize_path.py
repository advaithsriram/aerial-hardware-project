import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from path_planningfirst_csv import read_setpoints_from_csv_entry_exit, adaptive_times, compute_poly_coefficients, poly_setpoint_extraction


CSV_PATH = "gates_info.csv"


# Load gate information from CSV
gates = pd.read_csv(CSV_PATH)

# Extract setpoints and yaw setpoints from gate info
starting_point = [0, 0, 0]
original_setpoints = read_setpoints_from_csv_entry_exit(CSV_PATH, offset=0.4)
setpoints = original_setpoints
setpoints.insert(0, starting_point)
setpoints.append(starting_point)


times = adaptive_times(setpoints, total_time=15)
yaw_setpoints = gates["theta"].values.tolist()
disc_steps = 50

# Compute polynomial coefficients and extract trajectory setpoints
poly_coeffs = compute_poly_coefficients(setpoints, times)
trajectory_setpoints, time_setpoints = poly_setpoint_extraction(poly_coeffs, yaw_setpoints, times, disc_steps)

# Extract trajectory points for plotting
trajectory_x = [p[0] for p in trajectory_setpoints]
trajectory_y = [p[1] for p in trajectory_setpoints]

# Plotting the gates in the X-Y plane
plt.figure(figsize=(8, 8))
plt.title("Gate Positions and Trajectory in X-Y Plane")
plt.xlabel("X")
plt.ylabel("Y")

# Plot gates as lines
for _, gate in gates.iterrows():
    x, y, size, theta = gate["x"], gate["y"], gate["size"], gate["theta"]
    # Calculate rectangle corners
    dx = size / 2 * np.cos(np.pi - theta)
    dy = size / 2 * np.sin(np.pi - theta)

    # Define rectangle corners for plotting
    gate_line = np.array([[x - dx, y - dy], [x + dx, y + dy]])

    # Plot the gate as a rectangle
    plt.plot(gate_line[:, 0], gate_line[:, 1], color="red", linewidth=2, alpha=0.6, label="Gate" if _ == 0 else "")


# Plot the trajectory on top of the gate positions (lighter and thinner)
plt.plot(trajectory_x, trajectory_y, color="blue", linewidth=1, alpha=0.3, label="Trajectory")

# Add gate centers (with larger markers for visibility)
plt.scatter(gates["x"], gates["y"], color="red", marker="o", s=30, label="Gate Center")


# Add original setpoints
original_setpoints = np.array(original_setpoints)
plt.scatter(original_setpoints[:, 0], original_setpoints[:, 1], color="limegreen", marker="d", s=50, label="Setpoints")

# Add the starting point (with a distinct color and larger size)
plt.scatter(starting_point[0], starting_point[1], color="magenta", marker="*", s=50, label="Starting Point")


# Adding legend and grid
plt.legend()
plt.grid(True)
plt.axis("equal")  # Keep aspect ratio equal for x and y
plt.show()
