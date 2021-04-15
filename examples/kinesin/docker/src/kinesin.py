#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pandas
import argparse

from simularium_models_util.kinesin import KinesinSimulation
from simularium_models_util.visualization import KinesinVisualization


def main():
    parser = argparse.ArgumentParser(
        description="Runs and visualizes a ReaDDy kinesin simulation"
    )
    parser.add_argument(
        "params_path", help="the file path of an excel file with parameters")
    parser.add_argument(
        "data_column", help="the column index for the parameter set to use")
    parser.add_argument(
        "model_name", help="prefix for output file names", nargs='?', default="")
    args = parser.parse_args()
    parameters = pandas.read_excel(
        args.params_path, sheet_name="kinesin", usecols=[0, int(args.data_column)])
    parameters.set_index('name', inplace=True)
    parameters.transpose()
    run_name = list(parameters)[0]
    parameters = parameters[run_name]
    if not os.path.exists("outputs/"):
        os.mkdir("outputs/")
    parameters["name"] = "outputs/" + args.model_name + "_" + run_name
    kinesin_simulation = KinesinSimulation(parameters, True, True)
    kinesin_simulation.add_microtubule()
    kinesin_simulation.add_kinesin()
    kinesin_simulation.simulation.run(
        int(parameters["total_steps"]), parameters["timestep"])
    KinesinVisualization.visualize_kinesin(
        "{}.h5".format(parameters["name"]), parameters["box_size"], [])
    sys.exit(0)


if __name__ == '__main__':
    main()