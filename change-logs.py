#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
import urllib.request, urllib.error, urllib.parse
import csv
import json
import codecs
import lxml
from lxml import html
import yaml


def convert_to_datetime_date(date):
    """Convert date to datetime.date

    Params:
        date (logring):  "Nov 15 '16"
    Return:
        (datetime.date): datetime.date(2016,11,15)

    >>> convert_to_datetime_date("Nov 15 '16")
    datetime.date(2016, 11, 15)
    """
    date = date.split()
    month_name = ['January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'Augulog', 'September', 'October', 'November', 'December']
    month_name = [x[:3] for x in month_name]
    month = month_name.index(date[0]) + 1
    date[2] = date[2].replace("'", '20')
    return datetime.date(year = int(date[2]), month = month, day = int(date[1]))



def start_request(url):
    request = urllib.request.urlopen(url)
    #process handle exception    
    response = request.read()
    return response



def log_data(app, version, date, change_log, database):
    if os.path.exists(database):
        mode = 'a'
    else:
        mode = 'w'
    if change_log == '':
        change_log = 'Rand'
    fields = ['iOS', date, '1', app, '1', '1', 'Version', 'Rand', version,change_log]
    fields_name = ['Platform', 'Date', 'App ID', 'App Name', 'Publisher ID', 
    'Publisher Name', 'Update Type', 'Previous Value', 'New Value', 'Notes']

    stream = open(database, mode)
    writer = csv.writer(stream)
    if mode == 'w':
        writer.writerow(fields_name)
    writer.writerow(fields)



def format_change_log(log):
    """Reformat application news log to desired form.

    """
    #print(log)
    detele_char = ["u'", 'u"', "'", '"' , "<p>", "<br>", "</p>", '-', '[', ']', "</br>"]
    for char in detele_char:
        log = log.replace(char, "")
    
    f = codecs.open("temp.txt","w", "utf-8")
    f.write(log)
    f.close()

    f = open("temp.txt","r")
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
        '\xc3\xa2\xc2\x80\xc2\x94': ' '
    }

    #print log

    for key in list(unicode_logr.keys()):
        log = log.replace(key, unicode_logr[key])

    return log



def process_response(resp, start_date, database):
    """
    Get all the app update activity from start_date.
    """

    tree = lxml.html.fromstring(resp)
    app_name = tree.xpath('//*[@id="bsap_1291153"]/div[2]/div/div[1]/div[1]/div/h1/text()')[0]
    change_log = ""
    for st in tree.xpath('//*[@id="bsap_1291153"]/div[2]/div/div[1]/div[2]/p[2]/text()'):
        change_log = change_log + st
    change_log = format_change_log(change_log)

    version_set = tree.xpath('//*[@id="bsap_1291153"]/div[2]/div/div[2]/div[2]/div/ul/li')
    for element in version_set:
        version = element.xpath('b/text()')[0]
        version = version.split()[1]
        date =  element.xpath("span/text()")[0]    
        date = convert_to_datetime_date(date)
        if date >= start_date:
            log_data(app_name, version, date, change_log, database)

        #reset changelog
        change_log = ""



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
    
    database = params['database_name']

    today = datetime.date.today()
    
    start_date = today - datetime.timedelta(params['range_of_query'])

    for app_info in list(params['apps_src_dest'].keys()):
        print("Running: " + app_info + "\n")
        url = params['apps_src_dest'][app_info][0]
        database = params['dir'] + params['apps_src_dest'][app_info][1]
        resp = start_request(url)
        process_response(resp, start_date, database)

    print("Finish!!!!")

scan_for_change('index.yaml')


# if __name__ == "__main__":
#     import doctest
#     doctest.testmod()
