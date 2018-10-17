
# AIChE 2018 -- Hands-On with Molecular Simulation -- Managing Data Spaces, Performing MD, and Analyzing Trajectories with Signac, HOOMD-Blue, and Freud


## About

This is the software code used for demonstration during the tutorial on signac, HOOMD-Blue, and freud as part of the *Hands-On with Molecular Simulation* at the Annual Meeting of the American institute for Chemical Engineers (AIChE) in 2018.

## Authors

  * Joshua A. Anderson
  * Carl S. Adorf
  * Vyas Ramasubramani
  * Sharon C. Glotzer

## Installation

This demonstration is executed as a Jupyter notebook and requires a few Python packages as dependency.
These dependencies are listed in the `requirements.txt` file.

First, clone this repository

    ~ $ git clone https://bitbucket.org/glotzer/aiche-2018-hoomd-signac-freud.git

### With conda

We recommend to use conda to install all required software.
Make sure to add the conda-forge channel to your .condarc channel (with highest priority), then execute:

    ~/aiche-2018-hoomd-signac-freud $ conda install --file requirements.txt

Note: You might need to install the `nb_conda_kernels` package if the Jupyter notebook does not recognize the correct Python kernel.

### With pip


    ~/aiche-2018-hoomd-signac-freud $ pip install -r requirements.txt

## Usage

To start the demo, execute

    ~/aiche-2018-hoomd-signac-freud $ jupyter notebook analysis.ipynb
