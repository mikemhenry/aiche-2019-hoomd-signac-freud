import hoomd
import hoomd.hpmc
import numpy
import math
hoomd.context.initialize('--mode=cpu')

# parameters
n = 5        # number of vertices
seed = 1     # RNG seed


def get_area(vertices):
    """Compute area of polygon."""
    n = len(vertices)
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += abs(vertices[i][0] * vertices[j][1]-vertices[j][0] * vertices[i][1])
    return a / 2.0


def get_vertices(n):
    """Compute vertices of a regular n-gon."""
    theta = numpy.linspace(0, 2*math.pi, num=n, endpoint=False)
    return 0.5 * numpy.array([numpy.cos(theta), numpy.sin(theta)]).T


# derived parameters
vertices = get_vertices(n)
poly_area = get_area(vertices)

# compute box parameters
m = 20
phi = 0.6   # packing fraction (for initial config and move size tuning)
cell_area = 2 * poly_area / phi
a = math.sqrt(cell_area / math.sqrt(3))

# initialize system
hoomd.init.create_lattice(unitcell=hoomd.lattice.hex(a=a), n=[m, int(m/math.sqrt(3))])
mc = hoomd.hpmc.integrate.convex_polygon(d=0.2, a=0.2, seed=seed)
mc.shape_param.set('A', vertices=vertices)

# write out generated file
d = hoomd.dump.gsd("init.gsd", period=1, group=hoomd.group.all(), overwrite=True)
d.dump_state(mc)
d.write_restart()
