import numpy as np
import matplotlib.pyplot as plt

def lorenz_attractor(x, y, z, sigma=10, rho=28, beta=8/3):
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return dx, dy, dz

# Parameters
sigma = 10
rho = 28
beta = 8/3
dt = 0.01
num_steps = 10000

# Number of trajectories and initial conditions
num_trajectories = 10
initial_conditions = np.random.randn(num_trajectories, 3) * 10

# Arrays to store trajectories
x_traj = np.zeros((num_trajectories, num_steps))
y_traj = np.zeros((num_trajectories, num_steps))

# Compute trajectories for each initial condition
for i in range(num_trajectories):
    x, y, z = initial_conditions[i]
    for step in range(num_steps):
        dx, dy, dz = lorenz_attractor(x, y, z, sigma, rho, beta)
        x += dx * dt
        y += dy * dt
        z += dz * dt
        x_traj[i, step] = x
        y_traj[i, step] = y

# Plot all trajectories in 2D
plt.figure(figsize=(8, 6))
for i in range(num_trajectories):
    plt.plot(x_traj[i], y_traj[i], alpha=0.7, linewidth=0.7)
plt.title('Lorenz Attractor (2D Projection)')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.show()
