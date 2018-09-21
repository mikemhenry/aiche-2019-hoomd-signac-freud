import math
import numpy


def get_vertices(n):
    """Compute vertices of a regular n-gon."""
    theta = numpy.linspace(0, 2*math.pi, num=n, endpoint=False)
    return 0.5 * numpy.array([numpy.cos(theta), numpy.sin(theta)]).T


def compute_poly_area(vertices):
    """Compute area of polygon."""
    n = len(vertices)
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += abs(vertices[i][0] * vertices[j][1]-vertices[j][0] * vertices[i][1])
    return a / 2.0
