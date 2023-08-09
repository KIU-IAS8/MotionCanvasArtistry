from tools.display_functions import LiveCapture
from visualization.objects.sphere import Sphere
from visualization.visualize import Picture

# lc = LiveCapture()
# lc.display_sobel_filter_gradient_magnitude()

picture = Picture()

s1 = Sphere(start_color=(0.0, 1.0, 0.0), end_color=(0.0, 1.0, 0.0))
s2 = Sphere(radius=0.3, position=(0.5, 0.5, 0.0))

picture.visualize(spheres=[s1, s2])
