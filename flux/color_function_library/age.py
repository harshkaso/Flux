import numpy as np

class Age:
    def __init__(self):
        self.name = 'Age'

    def get_colors(self, color_context, color_1, color_2, color_3, base_alpha):
        max_age = color_context.particles.max_age.value
        min_age = color_context.particles.min_age.value
        particle_age = color_context.particles.all_particles[4]
        age_range   = max_age-min_age
        age_normals = ((particle_age - min_age) / age_range)
        # red   = np.clip(np.asarray(np.add(color_1[0], np.multiply(age_normals, (color_2[0] - color_1[0]))), dtype=int), min=0,max=255)
        # green = np.clip(np.asarray(np.add(color_1[1], np.multiply(age_normals, (color_2[1] - color_1[1]))), dtype=int), min=0,max=255)
        # blue  = np.clip(np.asarray(np.add(color_1[2], np.multiply(age_normals, (color_2[2] - color_1[2]))), dtype=int), min=0,max=255)
        # alpha = np.repeat(base_alpha, red.size)
        # return red, green, blue, alpha

        # Create masks for the two segments
        mask1 = age_normals <= 0.5
        mask2 = age_normals > 0.5
        
        # Initialize arrays for the final colors
        red = np.empty_like(age_normals, dtype=int)
        green = np.empty_like(age_normals, dtype=int)
        blue = np.empty_like(age_normals, dtype=int)
        
        # Interpolate between color_1 and color_2 for the first segment
        age_normals1 = age_normals[mask1] * 2  # Normalize to [0, 1]
        red[mask1] = np.clip(color_1[0] + age_normals1 * (color_2[0] - color_1[0]), 0, 255).astype(int)
        green[mask1] = np.clip(color_1[1] + age_normals1 * (color_2[1] - color_1[1]), 0, 255).astype(int)
        blue[mask1] = np.clip(color_1[2] + age_normals1 * (color_2[2] - color_1[2]), 0, 255).astype(int)
        
        # Interpolate between color_2 and color_3 for the second segment
        age_normals2 = (age_normals[mask2] - 0.5) * 2  # Normalize to [0, 1]
        red[mask2] = np.clip(color_2[0] + age_normals2 * (color_3[0] - color_2[0]), 0, 255).astype(int)
        green[mask2] = np.clip(color_2[1] + age_normals2 * (color_3[1] - color_2[1]), 0, 255).astype(int)
        blue[mask2] = np.clip(color_2[2] + age_normals2 * (color_3[2] - color_2[2]), 0, 255).astype(int)
        
        # Create the alpha channel
        alpha = np.full_like(red, base_alpha)
        
        return red, green, blue, alpha