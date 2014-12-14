#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
# from datetime import datetime as dt
import json
import codecs
import click
import csv
from zenlog import log


URL = "http://www.parlamento.pt/RegistoInteresses/Paginas/RegistoInteressesMembros_XIX_Governo.aspx"

fieldnames = ["name", "post", "start_date", "end_date"]


def file_get_contents(file):
    return open(file).read()


def file_put_contents(file, contents, utf8=True):
    f = codecs.open(file, 'w+', 'utf-8')
    c = contents.decode('utf-8').replace('\r', '')
    f.write(c)
    f.close()


def getpage(url):
    return urllib.urlopen(url).read()


def process_page():
    posts = []
    soup = BeautifulSoup(getpage(URL), "lxml")
    table = soup.find("div", attrs={"class": "ConteudoTexto"}).find("table", attrs={"summary": ""})
    rows = table.findAll("tr")
    for row in rows:
        if row.find("td", attrs={"height": "15"}) or "Registo de" in row.text:
            # entrada vazia ou link de pdf
            continue
        name, post, start_date, end_date = row.findAll('td')
        if not name.text:
            continue
        posts.append({"name": name.text.strip(),
                      "post": post.text.strip(),
                      "start_date": start_date.text.strip(),
                      "end_date": end_date.text.strip()})

    return posts


def scrape(format, verbose=False, outfile='', indent=1):
    posts = process_page()
    log.info("Saving to file %s..." % outfile)
    if format == "json":
        fp = codecs.open(outfile, 'w+', 'utf-8')
        fp.write(json.dumps(posts, encoding='utf-8', ensure_ascii=False, indent=indent, sort_keys=True))
        fp.close()
    elif format == "csv":
        fp = open(outfile, 'w+')
        writer = csv.DictWriter(fp, delimiter=",", quoting=csv.QUOTE_NONNUMERIC, quotechar='"', fieldnames=fieldnames)
        writer.writeheader()
        for row in posts:
            row = {k: v.strip().encode('utf-8') if type(v) in (str, unicode) else v for k, v in row.items()}
            writer.writerow(row)

    log.info("Done.")


@click.command()
@click.option("-f", "--format", help="Output file format, can be csv (default) or json", default="csv")
@click.option("-v", "--verbose", is_flag=True, help="Print some helpful information when running")
@click.option("-o", "--outfile", type=click.Path(), help="Output file (default is interessesgov.csv)")
@click.option("-i", "--indent", type=int, help="Spaces for JSON indentation (default is 2)", default=2)
def main(format, verbose, outfile, indent):
    if not outfile and format == "csv":
        outfile = "interessesgov.csv"
    elif not outfile and format == "json":
        outfile = "interessesgov.json"

    scrape(format, verbose, outfile, indent)

if __name__ == "__main__":
    main()
