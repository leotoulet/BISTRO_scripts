# BISTRO SCENARIOS OPTIMIZATION

This repo contains scrits used to run experiements on pre-defined scenarios with BISTRO and to analyse the results.

Currently, the repo contains two plug-and-play scenarios: 

	* A cordon-style pricing policy that charges users a fixed amount each time they cross a predefined boundary (As currently in use in Oslo)

	* A mileage based toll policy that charges drivers a per-mile amount when they drive within a defined area.

## Installing BISTRO and setting up the optimizer 

This section gives step by step instructions on how to install BISTRO, Mongodb and the hyperopt package on a clean Ubuntu distro. In order to run a BISTRO optimization at correct speeds, we recommend using at least an AWS m5a.8xlarge instance, or equivalent. This should allow for a simulation rate of about 6 Samples/hour.

1. Clone BeamCompetition from [Gitlab](https://gitlab.aicrowd.com/uber/BeamCompetitions). This contains BISTRO's files and the Sioux Faux scenario.

2. Install python3 if not present, and python3-pip (`sudo apt update` and `sudo apt install python3-pip`)

3. Install hyperopt (without superuser!) : `pip3 install hyperopt`

4. Install mongodb by following [this](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/) tutorial.

5. Install the required python dependencies: `pip3 install docker untangle xmltodict pandas shapely pymongo`

6. Install docker: `sudo apt install docker.io`


Once all of the previous steps are completed, you should configure Beam:

1. Change the number of iterations used during optimization (Instruction TBA)

2. Unbreak Beam


## Running experiments

With BISTRO installed and configured, refer to each experiment's folder to get step by step instructions on how to run it. For all experiments, there are three generic steps:

1. Use the settings file to set the experiment parameters
2. Run (as super user) the file that corresponds to the desired scenario
3. Launch as many hyperopt workers as the system can run. These will run individual simulations and produce Samples.




## Analysing experiment results

Use Dashboard or my code?