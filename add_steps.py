#!/usr/bin/env python
import argparse
from signac import get_project


def add_steps(job, steps):
    print("Adding {} steps to job {}.".format(steps, job))
    job.doc.steps += steps


def main(args):
    project = get_project()
    jobs = [project.open_job(id=jid) for jid in args.jobid]
    for job in jobs:
        add_steps(job, args.steps)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Add time steps for the specified jobs.

\n\nFor example with: `$ signac find n 5 | xargs ./add_steps 10000` """)

    parser.add_argument(
        'steps',
        type=int,
        default=10000,
        help="Add number of sampling steps to specified jobs.")
    parser.add_argument(
        'jobid',
        type=str,
        nargs='+',
        help="The job id of jobs to add steps for.")
    args = parser.parse_args()
    main(args)
