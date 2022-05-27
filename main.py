"""
@summary: Launching MIM Assistant rule using the Assistant's Web API.
This script will read in a csv file (system argument)
with the nid, the workflow name, and the patient list in MIM,
(the inputs prompted for in the web api)
and will launch the workflow for it.
Logging is used for errors and output to console.
@organization: MROQC
@author: Neha Bhomia
@Last Updated: 5/11/2022
"""

import csv
import mim_api
import logging
import sys

# file path for the csv file with nids workflows and patient lists
file_path = str(sys.argv[1])


def read_params(csv_file):
    """
    :param csv_file: input file in csv format, containing columns nid, workflow name, patient list
    :return: dictionary with key as a counter and value as a list of nid, workflow name and patient list
    """
    csv_dict = dict()
    with open(csv_file, mode='r') as inp:
        reader = csv.reader(inp)
        csv_dict = {row[0]: [row[1], row[2]] for row in reader}
    return csv_dict


def run_workflow(csv_dict):
    """
    This function takes a dictionary of nids with workflow name and patient list and uses the
    functions in the MIM assistant python API to runs the specified workflows on those nids.
    :param csv_dict: a dictionary with key as a counter and value as list of nid, workflow name and patient list
    :return: runs workflows. output successful or count of errors with error log.
    """
    for dict_key in csv_dict.keys():
        nid = dict_key
        rule_input = csv_dict[dict_key][0]
        list_input = csv_dict[dict_key][1]
        try:
            mim_api.ask_mim(nid, rule_input, list_input)
            logging.info(f"The code ran on nid: {nid}")
        except Exception as e:
            logging.error("%s - Error occurred in row: %s", e, (dict_key, csv_dict[dict_key][0], csv_dict[dict_key][1]))
    return logging.info("workflows over")


if __name__ == '__main__':
    run_workflow(read_params(file_path))
