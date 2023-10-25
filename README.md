# gliders
Tools for analyzing and plotting glider data.

Authors: Lori Garzio (lgarzio@marine.rutgers.edu) and Laura Nazzaro (nazzaro@marine.rutgers.edu)

## Installation Instructions
Add the channel conda-forge to your .condarc. You can find out more about conda-forge from their website: https://conda-forge.org/

`conda config --add channels conda-forge`

Clone the gliders repository

`git clone https://github.com/lgarzio/gliders.git`

Change your current working directory to the location that you downloaded gliders. 

`cd /Users/garzio/Documents/repo/gliders/`

Create conda environment from the included environment.yml file:

`conda env create -f environment.yml`

Once the environment is done building, activate the environment:

`conda activate gliders`

Install the toolbox to the conda environment from the root directory of the gliders toolbox:

`pip install .`

The toolbox should now be installed to your conda environment.
