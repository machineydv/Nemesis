import os
import re
import sys
import json
import requests
import argparse
import jsbeautifier
from bs4 import BeautifulSoup
from urllib.parse import urlparse

python_dir = os.path.dirname(os.path.abspath(__file__))
JSON_LIST = []
with open(str(python_dir+'/regexes.json')) as regex_file:
    regex_data = json.load(regex_file)
for JSON_ITEMS in regex_data.items():
    JSON_LIST.append(JSON_ITEMS[1])


def htmljscan(path, wordlist):
    f = open(path, 'w+')
    for each_lines in wordlist:
        parse = urlparse(each_lines)
        uscheme, uloc, upath = parse.scheme, parse.netloc, parse.path
        if not re.search(".*\.js$", upath):
            htmljsurl = uscheme+"://"+uloc+upath
            f.write(htmljsurl);f.write('\n')
            htmljsreq = requests.get(htmljsurl)
            htmljscont = htmljsreq.text
            htmljstext = BeautifulSoup(htmljscont, 'html.parser')
            htmljssoup = htmljstext.find_all("script")
            for htmljsscript in htmljssoup:
                if htmljsscript.string != None:
                    htmljsstring = htmljsscript.string
                    htmljsbeauty = jsbeautifier.beautify(htmljsstring)
                    htmljslines = htmljsbeauty.split('\n')
            for htmljsline in htmljslines:
                for JSON_REGEX in JSON_LIST:
                    if re.search(JSON_REGEX, htmljsline):
                        f.write(htmljsline);f.write('\n')
    f.close()


def main():
    parser = argparse.ArgumentParser(description='Parse JS content from HTML file and find weakness', epilog='Enjoy bug hunting')
    parser.add_argument('-i', '--input', type=str, help="Input file containing .html and .php files")
    parser.add_argument('-o', '--output', type=str, help="Output directory")
    parser.add_argument('-d', '--domain', type=str, help="Domain name")
    parser.add_argument('-iD', '--inputdirectory', type=str, help="Input wordlist directory")
    argv = parser.parse_args()
    if not argv.input or not argv.output or not argv.domain:
        print("Use -h")
        exit(0)
    else:
	if not argv.inputdirectory:
            input_wordlist = [line.rstrip('\n') for line in open(argv.input)]
        else:
            if argv.inputdirectory[-1] != '/':
                input_wordlist = [line.rstrip('\n') for line in open(str(argv.inputdirectory + '/' + argv.input))]
            else:
                input_wordlist = [line.rstrip('\n') for line in open(str(argv.inputdirectory + argv.input))]
        if argv.output[-1] != '/':
            path_to_write = argv.output + '/' + argv.domain + '.htmljscan'
        else:
            path_to_write = argv.output + argv.domain + '.htmljscan'
        htmljscan(path_to_write, input_wordlist)


main()
