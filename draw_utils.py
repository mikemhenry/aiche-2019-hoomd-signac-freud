import numpy as np
from matplotlib import collections, patches, cm, pyplot as plt
import math
import geometry


def quat2ang(quats):
    """Convert quaternions to angles."""
    return np.mod(2*np.arctan2(quats[:, 3], quats[:, 0]), 2*np.pi)


def draw_config(fig, ax, box, pos, angles, psi, nverts):
    ax.set_xlim((-box.Lx/2, box.Lx/2))
    ax.set_ylim((-box.Ly/2, box.Ly/2))
    verts = geometry.get_vertices(nverts)

    cmap = cm.get_cmap('hsv')

    for i, p in enumerate(pos):
        # Rotate polygon
        mat = np.array([
            [np.cos(angles[i]), np.sin(angles[i])],
            [-np.sin(angles[i]), np.cos(angles[i])]])
        coords = verts.dot(mat)
        ax.add_patch(patches.Polygon(
            xy=p[:2]+coords, facecolor=cmap((np.angle(psi[i])+math.pi)/(2*math.pi)), linewidth=0))


def draw_pmft(fig, ax, pmft, nverts):
    im = ax.contourf(pmft.X, pmft.Y, pmft.PMFT)
    cb = fig.colorbar(im, ax=ax)
    cb.set_label("$k_b T$", fontsize=12)
    ax.add_patch(patches.Polygon(xy=geometry.get_vertices(nverts)))


def draw_voronoi(fig, ax, box, cells):
    """Draw voronoi tesselation"""
    cols = [len(cell) for cell in cells]
    cmap = cm.get_cmap('Set1', np.unique(cols).size)
    bounds = np.array(range(min(cols), max(cols)+2))
    patches = [plt.Polygon(cell[:, :2]) for cell in cells]

    patch_collection = collections.PatchCollection(patches, edgecolors='black')
    patch_collection.set_array(np.array(cols))
    patch_collection.set_clim(bounds[0], bounds[-1])
    patch_collection.set_cmap(cmap)

    ax.add_collection(patch_collection)
    ax.set_xlim((-box.Lx/2, box.Lx/2))
    ax.set_ylim((-box.Ly/2, box.Ly/2))

    cb = fig.colorbar(patch_collection, ax=ax, ticks=bounds, boundaries=bounds)
    cb.set_ticks(cb.formatter.locs + 0.5)
    cb.set_ticklabels((cb.formatter.locs - 0.5).astype('int'))
    cb.set_label("Number of sides", fontsize=12)
