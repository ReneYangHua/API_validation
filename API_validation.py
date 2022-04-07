"""
Author: Rene Yang
Email: yang.rene@outlook.com
Version: 1.0
Release Date: 2022-04-10
Programming language: python 3.8.x
Description: This script is used to do the validation check for the API message in the following link.
    https://api.tmsandbox.co.nz/v1/Categories/6327/Details.json?catalogue=false
    The Acceptance Criteria:
        • Name = "Carbon credits"
        • CanRelist = true
        • The Promotions element with Name = "Gallery" has a Description that contains the text
        "Good position in category".
Usage:
    1. edit "acceptance_criteria.json" with JSON format according to the acceptance criteria
    2. python3 API_validation.py
"""

import json
import re
import os
import logging
import time
import sys
from urllib import request


logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_path = '.' + os.sep + 'logs' + os.sep
if not os.path.isdir(log_path):
    try:
        os.mkdir(log_path)
    except OSError as e:
        print(e)
        print('ERROR 0-0: the logs folder(%s) does not exist and cannot be created.' % log_path)
        sys.exit(10)
file_handler = logging.FileHandler(log_path + time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + '.log',
                                   mode='w')
file_handler.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter_file = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(formatter_file)
logger.addHandler(file_handler)
formatter_console = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter_console)
logger.addHandler(console_handler)


def api_verification(url_path='https://api.tmsandbox.co.nz/v1/Categories/6327/Details.json?catalogue=false'):
    pass_fail_flag = 0
    api_content = {}
    if len(sys.argv) > 1:
        get_input = str(sys.argv[1])
        if re.search(r'https://\S+', get_input):
            url_path = get_input.strip()
    if not get_api_message(api_content, url_path):
        return pass_fail_flag
    logger.info('*' * 30)
    logger.info('Validation is started...')
    logger.info('*' * 30)
    error_list, success_list = acceptance_criteria_check(api_content)
    if error_list:
        logger.info('*' * 30)
        logger.info('The validation result is FAIL.')
        logger.info('*' * 30)
        logger.info('The details are as following...')
        if success_list:
            logger.info('The following part validation result is PASS.')
            for line in success_list:
                logger.info(' * ' + line)
        logger.info('The following part validation result is FAIL.')
        for line in error_list:
            logger.error(line)
    else:
        logger.info('*' * 30)
        logger.info('The validation result is PASS.')
        logger.info('*' * 30)
        logger.info('The details are as following.')
        for line in success_list:
            logger.info(' * ' + line)
    logger.info('*' * 30)
    logger.info('Validation is completed.')
    logger.info('*' * 30)
    return pass_fail_flag


def get_api_message(api_content, url_path):
    logger.info('*' * 30)
    logger.info('Get the API message from the Web link...')
    logger.info(url_path)
    logger.info('*' * 30)
    get_response = request.urlopen(url_path)
    get_page = get_response.read()
    get_page = get_page.decode("utf-8")
    try:
        json_temp = json.loads(get_page)
    except:
        logger.error('1-0: the format in the Web link(%s) does not match the JSON format.' % url_path)
        return 0
    api_content.update(json_temp)
    logger.info('*' * 30)
    logger.info('The API message is transferred to JSON object.')
    logger.info('*' * 30)
    return 1


def acceptance_criteria_check(api_content):
    success_list = []
    error_list = []
    criterion_file = 'acceptance_criteria.json'
    if os.path.isfile(criterion_file):
        acceptance_criteria = {}
        with open(criterion_file) as criterion_f:
            try:
                json_temp = json.load(criterion_f)
            except:
                message = '2-0: the format in the JSON file(%s) does not match the JSON format.' % criterion_file
                logger.error(message)
                error_list += [message]
        if error_list:
            return error_list, success_list
        else:
            acceptance_criteria.update(json_temp)
    else:
        message = 'Notes: The acceptance criteria json file(%s) does not exist, ' \
                  'so the default acceptance criteria will be configured.' % criterion_file
        logger.info(message)
        acceptance_criteria = {
            'Name': 'Carbon credits',
            'CanRelist': True,
            'Promotions': [
                {
                    'Name': "Gallery",
                    'Description': 'Good position in category'
                }]}
    for check_item in acceptance_criteria.keys():
        if check_item not in api_content:
            message = '2-1: the key(%s) is not detected in the API message.' % check_item
            error_list += [message]
            continue
        if type(acceptance_criteria[check_item]) is not list:
            if acceptance_criteria[check_item] != api_content[check_item]:
                message = '2-2: the value of the key(%s) is unexpected. Actual: %s, Target: %s)' \
                                % (str(check_item), str(api_content[check_item]), str(acceptance_criteria[check_item]))
                error_list += [message]
            else:
                message = '%s = %s' % (str(check_item), str(api_content[check_item]))
                success_list += [message]
        else:
            if type(api_content[check_item]) is not list:
                message = '2-3: the format type in the %s is unexpected.' % criterion_file
                error_list += [message]
                continue
            for list_item in acceptance_criteria[check_item]:
                detect_temp = {}
                detect_flag = 1
                target_item = ''
                for key_list_item in list_item.keys():
                    detect_temp[key_list_item] = 0
                    target_item += str(key_list_item) + ' = ' + str(list_item[key_list_item]) + ', '
                target_item = target_item[:-2]
                for sub_api_content in api_content[check_item]:
                    for key_list_item in list_item.keys():
                        if key_list_item not in sub_api_content:
                            break
                        elif sub_api_content[key_list_item] != list_item[key_list_item]:
                            if key_list_item == 'Description':
                                search_format = str(list_item[key_list_item]).strip().replace(' ', r'\s+')
                                if re.search(search_format, sub_api_content[key_list_item]):
                                    detect_temp[key_list_item] = 1
                            break
                        else:
                            detect_temp[key_list_item] = 1
                for key_temp in detect_temp.keys():
                    if detect_temp[key_temp] == 0:
                        detect_flag = 0
                if detect_flag:
                    message = 'The content(' + target_item + ') is detected.'
                    success_list += [message]
                else:
                    message = '2-4: the content(%s) is not matched.' % target_item
                    error_list += [message]
    return error_list, success_list


if __name__ == '__main__':
    api_verification()
