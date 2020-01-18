import logging
import os
import shutil
import sys
import uuid
from timeit import default_timer as timer
import untangle
import xmltodict
import gzip
#from clear_iters import remove

import pandas as pd
import csv
sys.path.append(os.path.abspath("../../"))
sys.path.append("/home/ubuntu/BeamCompetitions/")
import convert_to_input
from hyperopt import STATUS_OK

trans_dict = {

    'Iteration':'Iteration',

    'Accessibility: number of secondary locations accessible by car within 15 minutes':'driveSecondaryAccessibility',
    'Accessibility: number of secondary locations accessible by transit within 15 minutes':'transitSecondaryAccessibility',
    'Accessibility: number of work locations accessible by car within 15 minutes':'driveWorkAccessibility',
    'Accessibility: number of work locations accessible by transit within 15 minutes':'transitWorkAccessibility',

    'Congestion: average vehicle delay per passenger trip':'averageVehicleDelayPerPassengerTrip',
    'Congestion: total vehicle miles traveled':'motorizedVehicleMilesTraveled_total',
    'Equity: average travel cost burden -  secondary':'averageTravelCostBurden_Secondary',
    'Equity: average travel cost burden - work':'averageTravelCostBurden_Work',
    'Level of service: average bus crowding experienced':'busCrowding',
    'Level of service: costs and benefits':'costBenefitAnalysis',

    'Sustainability: Total grams GHGe Emissions':'sustainability_GHG',
    'Sustainability: Total grams PM 2.5 Emitted':'sustainability_PM'
}

AVG_DELAY = "averageVehicleDelayPerPassengerTrip"
WORK_BURDEN = "averageTravelCostBurden_Work"
SECOND_BURDEN = "averageTravelCostBurden_Secondary"
BUS_CROWDING = "busCrowding"
COSTS_BENEFITS = "costBenefitAnalysis"
GHG = "sustainability_GHG"
TOLL_REVENUE = "TollRevenue"
SUBMISSION = "Submission Score"


DOCKER_IMAGE = "beammodel/beam-competition:0.0.3-SNAPSHOT"
CMD_TEMPLATE = "--scenario {0} --sample-size {1} --iters {2} --config {3}"
CONFIG_PATH = "/fixed-data/sioux_faux/sioux_faux-15k.conf"
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
    docker_cmd = CMD_TEMPLATE.format(SCENARIO_NAME, sample_size, n_sim_iters, CONFIG_PATH)

    # Write params to input submission csv files
    convert_to_input.convert_to_input(params, input_dir)

    output_suffix = uuid.uuid4()
    output_dir = os.path.abspath(f"./output/{output_suffix}")

    cmd = f"docker run -it -v {output_dir}:/output -v {input_dir}:/submission-inputs -v /home/ubuntu/BeamCompetitions/fixed-data:/fixed-data:rw {DOCKER_IMAGE} {docker_cmd}"
    cmd = cmd + " > log.txt"
    logger.info("!!! execute simulator cmd: %s" % cmd)
    print("Running system command : " + cmd)
    os.system(cmd)
    print("BISTRO finished")
    
    score = get_score(output_dir)
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


def get_score(output_dir):
    standards = load_standards()
    raw_scores = read_raw_scores(output_dir)
    return compute_weighted_scores(raw_scores, standards)


#KPI is hard coded for now
def compute_weighted_scores(raw_scores, standards):
    congestion, social, toll = 0, 0, 0

    #Congestion
    congestion += (raw_scores[AVG_DELAY] - standards[AVG_DELAY][0])/standards[AVG_DELAY][1]/3.0
    congestion += (raw_scores[GHG] - standards[GHG][0])/standards[GHG][1]/3.0
    congestion += (raw_scores[VMT] - standards[VMT][0])/standards[VMT][1]/3.0
    #Social
    social += (raw_scores[WORK_BURDEN] - standards[WORK_BURDEN][0])/standards[WORK_BURDEN][1]/2.0
    social += (raw_scores[SECOND_BURDEN] - standards[SECOND_BURDEN][0])/standards[SECOND_BURDEN][1]/2.0

    #Toll revenue
    toll_revenue = (raw_scores[TOLL_REVENUE] - standards[TOLL_REVENUE][0])/standards[TOLL_REVENUE][1]

    return 1.0*congestion/5.0 + 2.0*social/5.0 - 2.0*toll_revenue/5.0

def read_raw_scores(output_dir):
    path = only_subdir(only_subdir(output_dir))
    path = os.path.join(path, "competition/rawScores.csv")
    dic = {}

    #if not check_file_existence(tpe_dir):
    #    print("Problem retreiveing raw scores")

    with open(path) as csvfile:
        df = pd.read_csv(csvfile)
        kpi_names = list(df.columns)
        for name in kpi_names:
            dic[trans_dict[name]] = list(df[name])[-1]

    dic['TollRevenue'] = read_toll_revenue(output_dir)
    return dic


def read_toll_revenue(output_dir):
    output_dir = only_subdir(only_subdir(output_dir))
    f = gzip.open(os.path.join(output_dir,'outputEvents.xml.gz'), 'rb')
    print("Loading events")
    doc = xmltodict.parse(f.read())
    print("Parsing tolls paid")
    totalTolls = 0
    for event in doc['events']['event']:
        if '@tollPaid' in event.keys():
            totalTolls += float(event['@tollPaid'])

    return totalTolls
            
def load_standards(file = "/home/ubuntu/settingsFiles/standardizationParameters.csv"):
    dict_name = file
    params = {}
    with open(dict_name) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            params[row[0]] = (float(row[1]), float(row[2]))
    return params

