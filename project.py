#!/usr/bin/env python
import hoomd
import hoomd.hpmc
import math
from flow import FlowProject

import geometry


class Project(FlowProject):
    pass


@Project.operation
@Project.post.isfile("init.gsd")
def setup(job):
    "Prepare simulation for this job."
    hoomd.context.initialize('--mode=cpu')

    # derived parameters
    vertices = geometry.get_vertices(job.sp.n)
    poly_area = job.doc.poly_area = geometry.compute_poly_area(vertices)

    # compute box parameters
    m = 20
    phi = 0.6   # packing fraction (for initial config and move size tuning)
    cell_area = 2 * poly_area / phi
    a = math.sqrt(cell_area / math.sqrt(3))

    # initialize system
    hoomd.init.create_lattice(unitcell=hoomd.lattice.hex(a=a), n=[m, int(m/math.sqrt(3))])
    mc = hoomd.hpmc.integrate.convex_polygon(d=0.2, a=0.2, seed=job.sp.seed)
    mc.shape_param.set('A', vertices=vertices)

    # write out generated file
    d = hoomd.dump.gsd(job.fn("init.gsd"), period=1, group=hoomd.group.all(), overwrite=True)
    d.dump_state(mc)
    d.write_restart()


@Project.label
def sampled(job):
    import gsd.hoomd
    if job.isfile('trajectory.gsd'):
        with gsd.hoomd.open(job.fn('trajectory.gsd')) as traj:
            return traj[-1].configuration.step >= job.doc.steps


@Project.operation
@Project.pre.after(setup)
@Project.post(sampled)
def sample(job):
    "Sample system for the specified number of steps."
    hoomd.context.initialize('--mode=cpu')

    with job:
        hoomd.init.read_gsd(filename='init.gsd', restart='restart.gsd')
        mc = hoomd.hpmc.integrate.convex_polygon(restore_state=True, seed=job.sp.seed)
        d = hoomd.dump.gsd("trajectory.gsd", period=500, group=hoomd.group.all())
        d.dump_state(mc)

        restart = hoomd.dump.gsd("restart.gsd", period=500, group=hoomd.group.all(), truncate=True)
        restart.dump_state(mc)

        hoomd.analyze.log(filename="log.dat", quantities=['volume'], period=100)
        boxmc = hoomd.hpmc.update.boxmc(mc, betaP=job.sp.betaP, seed=job.sp.seed)
        boxmc.ln_volume(delta=0.001, weight=1)

        hoomd.run_upto(job.doc.steps + 1)
        restart.write_restart()


@Project.label
def psi_computed(job):
    import numpy as np
    if job.isfile('order.npz'):
        psi = np.load(job.fn('order.npz'))
        return psi['steps'][-1] >= job.doc.steps


@Project.operation
@Project.pre.after(sample)
@Project.post(psi_computed)
def compute_psi(job):
    import freud
    import gsd.hoomd
    import numpy as np

    op_hex = freud.order.HexOrderParameter(rmax=1.2, k=6)

    with gsd.hoomd.open(job.fn('trajectory.gsd')) as trajectory:
        steps = list()
        psi = list()
        for frame in trajectory[1:]:
            box = frame.configuration.box[:2].tolist()
            steps.append(frame.configuration.step)
            psi.append(op_hex.compute(box, frame.particles.position).psi.copy())

    np.savez(job.fn('order.npz'), steps=steps, psi=psi)


if __name__ == '__main__':
    Project().main()
