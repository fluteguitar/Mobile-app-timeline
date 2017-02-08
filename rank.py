#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import urllib.request, urllib.error, urllib.parse
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


def generate_ranking_url(path, store_name, country_code, category):
    """
    Params:
        store_name (string): ios/google-play-store
        country_code (tring): code name of the country
        category: category of applications.
    Returns:
        (string): 

    >>> generate_ranking_url("ios", "vn", "overall")
    'https://www.apptweak.com/app-ranking-charts-top-400/vn/ios/all?size=200'
    >>> generate_ranking_url("google-play-store", "vn", "COMMUNICATION")
    'https://www.apptweak.com/ranking-charts-top-400/vn/google-play-store/COMMUNICATION?size=200'
    """
    return "https://www.apptweak.com/{}/{}/{}/{}?size=200".format(path, country_code, store_name, category)


def request(url):
    """
    Params:
        url (string): Retrieve the top charts from Google Play Store with the 42matters Top Google Play 
        Charts API for a specific date and in more than 55 countries.

    Returns:
        (string): Top charts applications and their detailed information.

    """
    request = urllib.request.urlopen(url)
    #process handle exception
    
    response = request.read()
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
    for it in range(1,201):
        xpath = xpath = '/html/body/div[1]/main/div/div[2]/div[1]/ul/li[{}]/a/div/h5/text()'
        xpath = xpath.format(it)
        # print tree.xpath(xpath)
        app_name = tree.xpath(xpath)[0]
        top_apps.append(app_name)

    return top_apps



def get_apps_rank(top_apps,apps_list):
    """
    Params:
        top_apps (list_of_string): HTML response of ranking page.

    Returns:
        apps_rank (dictionary{string:int}): rank of apps in given date, 
        "-1" if apps are not in the table.
    """
    
    apps_rank = {}
    for app in apps_list:
        apps_rank[app] = -1 #initialize as -1, meaning not in the top apps.
        if app in top_apps:
            #print app
            apps_rank[app] = top_apps.index(app) + 1

    return apps_rank



def get_ranking(params):
    # index_file = index.yaml
    apps_list = params['apps_list']
    today = datetime.date.today() - datetime.timedelta(days = 1)

    # today = reverse_date_isoformat(today)
    # yesterday = reverse_date_isoformat(yesterday)
    #print params
    url = generate_ranking_url(params["path"], params["store_name"], params["country_code"], params["category"])
    #print url
    resp = request(url)
    top_apps = get_top_apps(resp)
    apps_rank_today = get_apps_rank(top_apps, apps_list)
    return apps_rank_today


def get_message_data(params):
    file_inp = params['dir'] + params['message_file']
    stream = open(file_inp, "r")
    reader = csv.reader(stream)
    next(reader, None)
    dic = {}
    for row in reader:
        if len(row) >= 2:
            dic[row[0]] = row[1]
    key_set = sorted(list(dic.keys()), reverse = True)
    # print key_set
    date = key_set[0]
    return dic[date]

def log_to_output(apps_rank_today,params):

    stream = open(params['dir'] + params['ranking_file'], "a")
    writer = csv.writer(stream)
    
    today = datetime.date.today() - datetime.timedelta(days = 1)

    res = [today.__format__("%m/%d/%Y")]
    for app_name in params['apps_list']:
        print(app_name, apps_rank_today)
        res.append(apps_rank_today[app_name])

    writer.writerow(res)
    stream.close()


def process_ranking(index_file):
    params = get_params(index_file)['rank']
    apps_rank_today = get_ranking(params)
    # msg = get_message_data(params)
    # print msg, apps_rank_today
    log_to_output(apps_rank_today, params)


print("Program start!\n")
print("Get ranks of apps\n")
process_ranking('index.yaml')
print("Finish sucessfully!\n")

# Uncomment to enable doctest
# if __name__ == "__main__":
#   import doctest
#   doctest.testmod()
#run('index.yaml')