# -*- coding: utf-8 -*-
import requests
import json
import sys
import csv

metaflag = 'content'
article_database = []
article = []
article_text = ''

def write_csv(data, filename):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ['author', 'pub', 'title', 'url', 'date', 'text']
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

def read_text_file(filename):
    filedata = [line.rstrip('\n') for line in open(filename, 'r')]
    return filedata


def convert_date_to_unix(exceldate):
    datelist = exceldate.split('/')
    unixdate = ''
    unixdate += datelist[2]
    unixdate += '-'
    if len(datelist[0]) == 2:
        unixdate += datelist[0]
    else:
        unixdate += '0'
        unixdate += datelist[0]
    unixdate += '-'
    if len(datelist[1]) == 2:
        unixdate += datelist[1]
    else:
        unixdate += '0'
        unixdate += datelist[1]
    return unixdate

dooo_text = read_text_file('no_scrape.txt')

for line in dooo_text:
    if line != '':
        if metaflag == 'metadata':
            if '=====' not in line:
                article.append(line.split(',')[0])
                article.append(line.split(',')[1])
                article.append(line.split(',')[2])
                article.append(line.split(',')[3])
                article.append(convert_date_to_unix(line.split(',')[4]))
            else:
                metaflag = 'content'
        else:
            if '=====' not in line:
                article_text += line
                article_text += ' '
            else:
                article.append(article_text)
                print(article)
                article_database.append(article)
                metaflag = 'metadata'
                article = []
                article_text = ''

write_csv(article_database, 'dooo_no_scrape.csv')
