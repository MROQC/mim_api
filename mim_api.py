"""
@summary: Utilised the MIMAssistant's Web API by Daniel Parvin
from MIM Software, Inc.
@author: Daniel Parvin and Neha Bhomia
"""

import sys
import json
import requests
import os


def ask_mim(nid, rule_input, list_input):
    """Launch an Assistant rule using the Web API.
    Get the bearer token, server address, and port from
    environment (or use values as defined). Get the Assistant's
    RPLs and rules.
    Run the selected rule on the selected RPL with the defined search
    parameters.
    """
    sources = (make_request('get', 'search-sources').json())
    # test
    for x, source in enumerate(sources):
        print(x, ":", source['patientListName'])
    rpls = list(filter(rpl_filter, sources))
    if not rpls:
        print('There are no RPLs to search. '
              'Configure an RPL and try again.')
        return
    rules = (make_request('get', 'rules').json())
    # test
    for x, rule in enumerate(rules):
        print(x, ":", rule['ruleName'])
    if not rules:
        print('There are no Assistant rules to run. '
              'Configure an Assistant rule and try again.')
        return

    rule_id = select_rule(rules, rule_input)
    selected_rpl = select_source(rpls, list_input)
    tag = 'PatientID'
    operator = 'IS'

    data = get_run_body(rule_id, selected_rpl, tag, operator, nid)
    post_response = make_request('post', 'run', data)


def make_request(method, path, data=None):
    """
    Handle the api communications from MIM.
    :param method:
    :param url:
    :param data:
    :param headers:
    :return:
    """
    headers = {'Authorization': f"Bearer {os.environ.get('token')}"}
    server_address = os.environ.get('server', 'localhost')
    port = os.environ.get('port', '17443')
    api_path = f'https://{server_address}:{port}/mim/api/v1/assistant/'
    url = api_path + path

    if method == 'post':
        res = requests.post(url, json=data, headers=headers, verify='./MIM_Software_Root_CA.cer')
    if method == 'get':
        res = requests.get(url, json=data, headers=headers, verify='./MIM_Software_Root_CA.cer')
    if res.status_code != 200:
        # raise Exception(res.raise_for_status())
        # test
        print("the code is not 200.something wrong with the request itself")
        print(res.status_code)
        raise Exception(res.json()['userFriendlyMessage'])
    return res


def get_mim_config_path():
    """Get MIM's default configuration folder, depending on OS."""
    mim_config_path = ('C:/ProgramData/MIM/web_api/'
                       if sys.platform.startswith('win')
                       else '/Library/Application Support/MIM/web_api/')
    return mim_config_path


def rpl_filter(source):
    """Determine whether a source has a type of "RPL" or not."""
    source_type = source.get('type', 'other')
    if source_type.casefold() == 'RPL'.casefold():
        return True
    else:
        return False


def select_rule(rules, rule_input):
    """Return the rule ID of the selected rule."""
    for x, rule in enumerate(rules):
        if rule['ruleName'] == rule_input:
            rule_number = x
            return rules[rule_number]['ruleId']


def select_source(sources, list_input):
    """Return a source list by number."""
    for x, source in enumerate(sources):
        if source['patientListName'] == list_input:
            source_number = x
            return sources[source_number]


def get_run_body(rule_id, rpl, tag, operator, value):
    """Generate the body of the HTTPS POST "run" endpoint."""
    return {
        'parameters': {
            'initialSeries': {
                'seriesFilter': {
                    '@type': 'SeriesFilterGroup',
                    'condition': 'OR',
                    'filters': [
                        {
                            '@type': 'SeriesFilter',
                            'tag': tag,
                            'operator': operator,
                            'value': value
                        }
                    ]
                },
                'dataLocationIdentifier': rpl
            }
        },
        'ruleId': rule_id
    }

