#!/usr/bin/env python
import argparse

import signac


def main(args):
    project = signac.init_project("polygon-fluid-solid-transition")

    for n in args.num_vertices:
        for betaP in args.betaP:
            for seed in range(args.replicas):
                job = project.open_job(dict(n=n, betaP=betaP, seed=seed))
                job.doc.setdefault('steps', 20000)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'num_vertices', type=int, nargs='+',
        help="Specify the number of vertices to initialize jobs for.")
    parser.add_argument(
        '--betaP', type=float, nargs='+', default=13.2,
        help="Specify the pressures to initialize jobs for.")
    parser.add_argument(
        '--replicas', type=int, default=3,
        help="Specify the number of replicas per state point.")
    args = parser.parse_args()
    main(args)
