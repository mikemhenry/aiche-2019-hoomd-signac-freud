#!/usr/bin/env python
import argparse

import signac


def main(args):
    project = signac.init_project("polygon-fluid-solid-transition")

    for betaP in args.betaP:
        for seed in range(args.replicas):
            job = project.open_job(dict(n=args.num_vertices, betaP=betaP, seed=seed))
            job.doc.setdefault('steps', 20000)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'num_vertices', type=int,
        help="Specify the number of vertices to initialize jobs for.")
    parser.add_argument(
        '--betaP', type=float, nargs='+', default=[10.0, 13.2, 14.0],
        help="Specify the pressures to initialize jobs for.")
    parser.add_argument(
        '--replicas', type=int, default=3,
        help="Specify the number of replicas per state point.")
    args = parser.parse_args()
    main(args)
