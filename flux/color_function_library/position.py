import numpy as np

class Position:
    def __init__(self):
        self.name = 'Position'

    def get_colors(self, color_context, color_1, color_2, color_3, base_alpha):
        x = color_context.particles.all_particles[0]
        y = color_context.particles.all_particles[1]
        flowfield_width  = color_context.flowfield.width 
        flowfield_height = color_context.flowfield.height
        x_normals = np.divide(x, flowfield_width)
        y_normals = np.divide(y, flowfield_height)
        # red   = np.clip(np.asarray(np.add(color_1[0], np.multiply(x_normals, (color_2[0] - color_1[0]))), dtype=int), min=0,max=255)
        # green = np.clip(np.asarray(np.add(color_1[1], np.multiply(y_normals, (color_2[1] - color_1[1]))), dtype=int), min=0,max=255)
        # blue  = np.clip(np.asarray(np.add(color_1[2], np.multiply(np.multiply(np.add(x_normals, y_normals), (color_2[2] - color_1[2])),0.5)), dtype=int), min=0,max=255)
        # alpha = np.repeat(base_alpha, red.size)
        # return red, green, blue, alpha

        # Combine x and y normals to create a single normalized value
        combined_normals = (x_normals + y_normals) / 2
        
        # Create masks for the two segments
        mask1 = combined_normals <= 0.5
        mask2 = combined_normals > 0.5
        
        # Initialize arrays for the final colors
        red = np.empty_like(combined_normals, dtype=int)
        green = np.empty_like(combined_normals, dtype=int)
        blue = np.empty_like(combined_normals, dtype=int)
        
        # Interpolate between color_1 and color_2 for the first segment
        combined_normals1 = combined_normals[mask1] * 2  # Normalize to [0, 1]
        red[mask1] = np.clip(color_1[0] + combined_normals1 * (color_2[0] - color_1[0]), 0, 255).astype(int)
        green[mask1] = np.clip(color_1[1] + combined_normals1 * (color_2[1] - color_1[1]), 0, 255).astype(int)
        blue[mask1] = np.clip(color_1[2] + combined_normals1 * (color_2[2] - color_1[2]), 0, 255).astype(int)
        
        # Interpolate between color_2 and color_3 for the second segment
        combined_normals2 = (combined_normals[mask2] - 0.5) * 2  # Normalize to [0, 1]
        red[mask2] = np.clip(color_2[0] + combined_normals2 * (color_3[0] - color_2[0]), 0, 255).astype(int)
        green[mask2] = np.clip(color_2[1] + combined_normals2 * (color_3[1] - color_2[1]), 0, 255).astype(int)
        blue[mask2] = np.clip(color_2[2] + combined_normals2 * (color_3[2] - color_2[2]), 0, 255).astype(int)
        
        # Create the alpha channel
        alpha = np.full_like(red, base_alpha)
        
        return red, green, blue, alpha