import numpy as np
from config import UIDimensions, UITypes
from types import SimpleNamespace

class Vortex:
    def __init__(self):
        self.name = 'Vortex'
        self.attractors = None
        self.rotations = None
        self.args = SimpleNamespace( 
            points = SimpleNamespace( 
                label = 'Points',
                value = 3,
                min_value = 1,
                max_value = 10,
                type =  UITypes.SLIDER_INT,
                callback = self._spawn_attractors
            )
        )
        self._spawn_attractors(self.args.points.value)
        self.init_flowfield()


    def init_flowfield(self):
        self.spawn_coordinates = np.ones((UIDimensions.flowfield_height, UIDimensions.flowfield_width), dtype=bool)


    def _spawn_attractors(self, points):
        self.attractors = (np.random.rand(points, 2) * (UIDimensions.flowfield_width, UIDimensions.flowfield_height)).astype(np.int32)
        self.rotations = np.random.choice([np.pi / 2, -np.pi / 2], size=(points))
    
    def get_angles(self, particles: np.ndarray, frame_count):
        # # Vectors towards the attractor points
        dx = np.asarray(self.attractors[:, 0, np.newaxis] - particles[0], dtype=np.float32)  # Shape: (A, P)
        dy = np.asarray(self.attractors[:, 1, np.newaxis] - particles[1], dtype=np.float32)  # Shape: (A, P)
        
        # # Compute angles directly from dx/dy components
        # angles = np.arctan2(dy, dx) + self.rotations[:, np.newaxis]
        
        # # Calculate weights using vectorized operations
        # distances_sq = dx**2 + dy**2
        # inv_dist = np.sqrt(distances_sq)
        # weights = np.divide(1.0, inv_dist, where=inv_dist > 1e-8, out=np.zeros_like(inv_dist))
        
        # # Compute trigonometric components using single pass
        # sin_vals = np.sin(angles, out=dx)  # Reuse dx memory
        # cos_vals = np.cos(angles, out=dy)  # Reuse dy memory
        
        # # Sum using broadcasting instead of einsum
        # f_sin = (sin_vals * weights).sum(axis=0)
        # f_cos = (cos_vals * weights).sum(axis=0)
        
        # # Fast normalization using fused multiply-add
        # norm = np.sqrt(f_sin**2 + f_cos**2)
        # # np.maximum(norm, 1e-8, out=norm)
        
        # return f_cos/norm, f_sin/norm
        # Calculate the vectors from particles to attractors
        # dx = self.attractors[:, 0, np.newaxis] - particles[0]  # Shape: (A, P)
        # dy = self.attractors[:, 1, np.newaxis] - particles[1]  # Shape: (A, P)
        
        # Calculate distances to each attractor
        distances_sq = dx**2 + dy**2
        inv_dist = np.sqrt(distances_sq)
        weights = np.divide(1.0, inv_dist, where=inv_dist > 1e-8, out=np.zeros_like(inv_dist))
        
        # Normalize weights
        weights_sum = weights.sum(axis=0)
        normalized_weights = weights / weights_sum
        
        # Compute angles directly from dx/dy components
        angles = np.arctan2(dy, dx) + self.rotations[:, np.newaxis]
        
        # Compute weighted average of sine and cosine components
        sin_vals = np.sin(angles)
        cos_vals = np.cos(angles)
        
        weighted_sin = (sin_vals * normalized_weights).sum(axis=0)
        weighted_cos = (cos_vals * normalized_weights).sum(axis=0)
        
        # Compute final angles
        final_angles = np.arctan2(weighted_sin, weighted_cos)
        
        return final_angles