#! /usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Toan Nguyen - fluteguitar@github"
__liscense__ = "GPL"
__email__ = "canhtoannguyen60@gmail.com"
__maintainer__ = "Toan Nguyen"
__status__ = "Production"
import os
import datetime
import urllib.request
import urllib.error
import urllib.parse
import csv
import codecs
import lxml
from lxml import html
import yaml
def convert_to_datetime_date(date):
    """Convert date to datetime.date
    Params:
        date (str):  "January 22, 2017"
    Return:
        (datetime.date): datetime.date(2017,1,22)
    >>> convert_to_datetime_date("January 22, 2017")
    datetime.date(2017, 1, 22)
    """
    date = date.split()
    month_name = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December']
    month = month_name.index(date[0]) + 1
    date[1] = date[1][:-1]
    return datetime.date(year=int(date[2]), month=month, day=int(date[1]))
def start_request(url):
    request = urllib.request.urlopen(url)
    # process handle exception
    response = request.read()
    return response
def log_data(version, date, change_log, database):
    if os.path.exists(database):
        mode = 'a'
    else:
        mode = 'w'
    if change_log == '':
        change_log = 'Rand'
    fields = [
        'ggplay',
        date,
        '1',
        '1',
        '1',
        '1',
        'Version',
        'Rand',
        version,
        change_log]
    fields_name = [
        'Platform',
        'Date',
        'App ID',
        'App Name',
        'Publisher ID',
        'Publisher Name',
        'Update Type',
        'Previous Value',
        'New Value',
        'Notes']
    stream = open(database, mode)
    writer = csv.writer(stream)
    if mode == 'w':
        writer.writerow(fields_name)
    writer.writerow(fields)
def format_change_log(log):
    """Reformat application news log to desired form.
    """
    # print(log)
    detele_char = ["u'", 'u"', "'", '"', "<p>",
                   "<br>", "</p>", '[', ']', "</br>"]
    for char in detele_char:
        log = log.replace(char, "")
    f = codecs.open("temp.txt", "w", "utf-8")
    f.write(log)
    f.close()
    f = open("temp.txt", "r")
    log = ""
    for line in f:
        log = log + line
    f.close()
    #log = log.replace("\n", " ")
    unicode_logr = {
        "\xc2\xb7": "\n-",
        "\xe2\x80\xa2": "\n-",
        "\xe2\x80\x94": "\n-",
        '\xc3\xa2\xc2\x80\xc2\xa2': "-",
        '\xc3\xb0\xc2\x9f\xc2\x91\xc2\xbb': '',
        '\xc3\x82\xc2\xa0': ' ',
        '\xc3\xa2\xc2\x80\xc2\x94': ' ',
        '\xa0': ' '
    }
    # print log
    for key in list(unicode_logr.keys()):
        log = log.replace(key, unicode_logr[key])
    return log
def parse_response(resp, log_resp, start_date, database):
    """
    Get all the app update activity from start_date.
    """
    log_tree = lxml.html.fromstring(log_resp)
    date = log_tree.xpath(
        '//*[@id="body-content"]/div/div/div[1]/div[4]/div/div[2]/div[1]/div[2]/text()')[0]
    date = convert_to_datetime_date(date)
    if date < start_date:
        return
    change_log = "\n".join(log_tree.xpath(
        '//div[@class="recent-change"]/text()'))
    change_log = format_change_log(change_log)
    tree = lxml.html.fromstring(resp)
    version = tree.xpath(
        '/html/body/div[1]/main/div/div[1]/div/div[2]/div[3]/table//tr[2]/td[3]/text()')[0].split()[0]
    log_data(version, date, change_log, database)
def get_params(index_file):
    """
    Params:
        index_file (string): index file name.
    Returns:
        (dictionary): parameters and values.
    >>> params = get_params("index.yaml")
    >>> params['country']
    'VN'
    >>> params['list_name']
    'topselling_free'
    >>> params['cat_key']
    'APPLICATION'
    """
    stream = open(index_file, "r")
    params = yaml.load(stream)
    stream.close()
    return params
def scan_for_change(index_file):
    params = get_params(index_file)['change_logs']
    today = datetime.date.today()
    start_date = today - datetime.timedelta(params['range_of_query'])
    for app_info in list(params['apps_src_dest'].keys()):
        print("Running: " + app_info + "\n")
        versionlog_url = params['apps_src_dest'][app_info][0]
        version_url = params['apps_src_dest'][app_info][1]
        database = params['dir'] + params['apps_src_dest'][app_info][2]
        log_resp = start_request(versionlog_url)
        log_resp = log_resp.decode('utf-8')
        resp = start_request(version_url)
        resp = resp.decode('utf-8')
        parse_response(resp, log_resp, start_date, database)

print("Program {} starts!".format(__file__))
scan_for_change('index_ggplay.yaml')
print("Program {} finish successfully".format(__file__))
# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
