# -*- coding: utf-8 -*-
# Python3
# Author: Nguyen Canh Toan
# Email: canhtoannguyen60@gmail.com
# This program gets ranks of apps on Google Play Store from apptweak.com, and
# store them in folder data/ggplay/ranking.csv. The detailed information on
# which apps are scraped, and how the information on apptweak.com is selected
# are in the file index.yaml.
# Thanks for your effort to maintain this code, have fun, HAPPY CODING then!
# I am sorry if my coding style is not appropriate to PEP8.
# Back then I am still a newbie in this area.


import datetime
import urllib.request
import urllib.error
import urllib.parse
import json
import csv
import codecs
import lxml
from lxml import html
import yaml


def reverse_date_isoformat(date):
    """
    Params:
        date (datetime.date): the given date.

    Returns:
        (string): dd-mm-yyyy - the reverse format of standard date isoformat.

    >>> import datetime
    >>> reverse_date_isoformat(datetime.date(2016,11,1))
    '01-11-2016'
    """
    list_date_params = date.isoformat().split('-')
    return '-'.join(list_date_params[::-1])


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


def request(url):
    req = urllib.request.urlopen(url)
    # process handle exception
    response = req.read()
    return response


def get_top_apps(response):
    """
    Params:
        response (string): HTML response of ranking page.

    Returns:
        top_charts (list of string): list of name of top applications.
    """
    tree = lxml.html.fromstring(response)
    top_apps = []
    for it in range(1, 201):
        xpath = xpath = '/html/body/div[1]/main/div/div[2]/div[1]/ul/li[{}]/a/div/h5/text()'
        xpath = xpath.format(it)
        # print tree.xpath(xpath)
        app_name = tree.xpath(xpath)[0]
        top_apps.append(app_name)

    return top_apps


def get_apps_rank(top_apps, apps_list):
    """
    Params:
        top_apps (list_of_string): HTML response of ranking page.

    Returns:
        apps_rank (dictionary{string:int}): rank of apps in given date,
        "0" if apps are not in the table.
    """
    def get_viber_pos():
        pos = 0
        for memb in top_apps:
            pos += 1
            if 'Viber' in memb:
                return pos

        return 0

    apps_rank = {}
    for app in apps_list:
        apps_rank[app] = 0  # initialize as 0, meaning not in the top apps.
        if app in top_apps:
            # print app
            apps_rank[app] = top_apps.index(app) + 1
        elif 'Viber' in app: # special treatment for this on-the-change Viber
            apps_rank[app] = get_viber_pos()

    return apps_rank


def get_ranking(params):
    # index_file = index.yaml
    apps_list = params['apps_list']
    today = datetime.date.today() - datetime.timedelta(days=1)
    # today = reverse_date_isoformat(today)
    # yesterday = reverse_date_isoformat(yesterday)
    # print params
    # print url
    resp = request(params['src_domain'])
    top_apps = get_top_apps(resp)
    apps_rank_today = get_apps_rank(top_apps, apps_list)
    return apps_rank_today


def log_to_output(apps_rank_today, rank_params):

    stream = open(rank_params['dir'] + rank_params['ranking_file'], "a")
    writer = csv.writer(stream)

    today = datetime.date.today() - datetime.timedelta(days=1)

    res = [today.__format__("%m-%d-%Y")]
    for app_name in rank_params['apps_list']:
        print(app_name, apps_rank_today)
        res.append(apps_rank_today[app_name])

    writer.writerow(res)
    stream.close()


def process_ranking(index_file):
    rank_params = get_params(index_file)['rank']
    apps_rank_today = get_ranking(rank_params)
    # msg = get_message_data(rank_params)
    # print msg, apps_rank_today
    log_to_output(apps_rank_today, rank_params)


print("Program start!\n")
print("Get ranks of apps\n")
process_ranking('index_ggplay.yaml')
print("Finish sucessfully!\n")

# Uncomment to enable doctest
# if __name__ == "__main__":
#   import doctest
#   doctest.testmod()
# run('index.yaml')
