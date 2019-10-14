# BISTRO_scripts

This repository contains scripts used for the visualization and interpretation of Hyperopt outputs of the BISTRO framework.

*Summary of files:*

	* Sample.py : contains an abstract class of a sample point of TPE and utilities to create that point. The class contains inputs, scores, directory locations...

	* collect_inputs.py : contains utilities that gather all input data of a Sample. Used internally by the Sample class, not meant to be used outside of it.

	* collect_outputs.py : contains utilities that gather all input data of a Sample. Used internally by the Sample class, not meant to be used outside of it.

	* bus_fares_analysis.py : contains functions that take a list of samples and create analysis graphs of KPIS and other metrics as a function of bus fares

	* 4Dinputviz.py: contains first shots at 4D visualization