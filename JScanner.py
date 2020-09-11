#!/usr/bin/python3
from re import search
from requests import get
from termcolor import colored
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from jsbeautifier import beautify
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor

from lib.Functions import starter
from lib.PathFunctions import PathFunction
from lib.Globals import *

FPathApp = PathFunction()

parser = ArgumentParser(description=colored('Javascript Scanner', color='yellow'), epilog=colored("Enjoy bug hunting", color='yellow'))
parser.add_argument('-w', '--wordlist', type=str, help='Absolute path of wordlist')
parser.add_argument('-oD', '--output-directory', type=str, help="Output directory")
parser.add_argument('-d', '--domain', type=str, help="Domain name")
parser.add_argument('-t', '--threads', type=int, help="Number of threads")
parser.add_argument('-b', '--banner', action="store_true", help="Print banner and exit")
argv = parser.parse_args()

starter(argv)

def scan_js(url: str) -> bool:
    global output_file
    urlparser = urlparse(url)
    if search(".*\.js$", urlparser.path):
        try:
            jsurl = FPathApp.slasher(FPathApp.urler(urlparser.netloc)) + FPathApp.payloader(urlparser.path)
            print(f"{ColorObj.information} Trying to get data from {colored(jsurl, color='cyan')}")
            output_file.write("{:<40} <--- URL\n".format(jsurl))
            jsreq = get(jsurl)
            jstext = str(beautify(jsreq.text)).split('\n')
            for jsline in jstext:
                for dom_source in dom_sources_regex:
                    if search(dom_source, jsline):
                        print(f"{ColorObj.good} Found sensitive data: {colored(jsline, color='cyan')}")
                        output_file.write("{:<40} <--- From regex {}\n".format(jsline.strip(' '), dom_source))
                for dom_sink in dom_sinks_regex:
                    if search(dom_sink, jsline):
                        print(f"{ColorObj.good} Found sensitive data: {colored(jsline, color='cyan')}")
                        output_file.write("{:<40} <--- From regex {}\n".format(jsline.strip(' '), dom_sink))
            return True
        except Exception as E:
            print(f"{ColorObj.bad} Exception {E},{E.__class__},{E.__class__} occured")
            return False
    if not search(".*\.js$", urlparser.path):
        jsurl = FPathApp.slasher(FPathApp.urler(urlparser.netloc)) + FPathApp.payloader(urlparser.path)
        print(f"{ColorObj.information} Trying to get data from {colored(jsurl, color='cyan')}")
        output_file.write("{:<40} <--- URL\n".format(jsurl))
        jsreq = get(jsurl)
        jsx = BeautifulSoup(jsreq.text, 'html.parser')
        jssoup = jsx.find_all("script")
        for jscript in jssoup:
            if jscript != None:
                jstext = str(beautify(jscript.string)).split('\n')
                for jsline in jstext:
                    for dom_source in dom_sources_regex:
                        if search(dom_source, jsline):
                            print(f"{ColorObj.good} Found sensitive data: {colored(jsline, color='cyan')}")
                            output_file.write("{:<40} <--- From regex {}\n".format(jsline, dom_source))
                    for dom_sink in dom_sinks_regex:
                        if search(dom_sink, jsline):
                            print(f"{ColorObj.good} Found sensitive data: {colored(jsline, color='cyan')}")
                            output_file.write("{:<40} <--- From regex {}\n".format(jsline, dom_sink))

def main():
    global output_file
    if not argv.wordlist or not argv.output_directory or not argv.domain:
        print(f"{ColorObj.bad} Use --help")
        exit(0)
    input_wordlist = [line.rstrip('\n') for line in open(argv.wordlist)]
    output_file = open(FPathApp.slasher(argv.output_directory) + argv.domain + '.jscan', 'a')
    
    with ThreadPoolExecutor(max_workers=argv.threads) as mapper:
        mapper.map(scan_js, input_wordlist)

main()
