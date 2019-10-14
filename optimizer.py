import logging
import os
import shutil
import sys
import uuid
from timeit import default_timer as timer

import pandas as pd

sys.path.append(os.path.abspath("../../"))
# print(sys.path)
import convert_to_input
from hyperopt import STATUS_OK

TMV = "Congestion: total vehicle miles traveled"
AVG_DELAY = "Congestion: average vehicle delay per passenger trip"
WORK_BURDEN = "Equity: average travel cost burden - work"
BUS_CROWDING = "Level of service: average bus crowding experienced"
COSTS_BENEFITS = "Level of service: costs and benefits"

SUBMISSION = "Submission Score"


DOCKER_IMAGE = "beammodel/beam-competition:0.0.3-SNAPSHOT"
CMD_TEMPLATE = "--scenario {0} --sample-size {1} --iters {2}"
SCENARIO_NAME = "sioux_faux"
SCORES_PATH = ("competition", "submissionScores.csv")
DIR_DELIM = "-"

logger = logging.getLogger(__name__)


def abspath2(path):
    path = os.path.abspath(os.path.expanduser(path))
    return path


def only_subdir(path):
    subdir, = os.listdir(path)  # Validates only returned element
    path = os.path.join(path, subdir)
    return path


def read_scores(output_dir):
    """Read scores from output directory as .csv file.
    """
    output_dir = only_subdir(only_subdir(output_dir))
    df = pd.read_csv(os.path.join(output_dir, *SCORES_PATH), index_col="Component Name")
    scores = df["Weighted Score"] #DO NOT CHANGE THIS LINE !
    return scores

def objective(params):
    """Objective function for Calling the Simulator"""
    # Keep track of evals

    start = timer()

    input_suffix = uuid.uuid4()

    input_dir = os.path.abspath(f"./submission-inputs/{input_suffix}")
    if not os.path.isdir('./submission-inputs'):
        os.system("rm -f ./submission-inputs")
    if not os.path.exists('./submission-inputs'):
        os.system('mkdir ./submission-inputs')
    if not os.path.exists(input_dir):
        os.system(f'mkdir {input_dir}')
        os.system('chmod -R 777 ./submission-inputs')

    # Run simulator, return a score
    sample_size = "15k"
    n_sim_iters = 30
    docker_cmd = CMD_TEMPLATE.format(SCENARIO_NAME, sample_size, n_sim_iters)

    # Write params to input submission csv files
    convert_to_input.convert_to_input(params, input_dir)

    output_suffix = uuid.uuid4()
    output_dir = os.path.abspath(f"./output/{output_suffix}")

    cmd = f"docker run -it -v {output_dir}:/output -v {input_dir}:/submission-inputs {DOCKER_IMAGE} {docker_cmd}"
    cmd = cmd + " > log.txt"
    logger.info("!!! execute simulator cmd: %s" % cmd)
    print("Running system command : " + cmd)
    os.system(cmd)
    print("BISTRO finished")


    #Change score HERE
    scores = read_scores(output_dir)
    score = scores[SUBMISSION]
    score = float(score)
    print("SCORE :", score)

    output_dir = only_subdir(only_subdir(output_dir))
    shutil.copy(os.path.join(output_dir, *SCORES_PATH), input_dir)

    paths = (input_dir, output_dir)

    loss = score

    run_time = timer() - start

    print(loss)

    # Dictionary with information for evaluation
    return {'loss': loss, 'params': params, 
            'train_time': run_time, 'status': STATUS_OK, 'paths': paths}
