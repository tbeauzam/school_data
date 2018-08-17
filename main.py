#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from SchoolDataFetcher import SchoolDataFetcher
from SchoolData import SchoolData

def main():

    print("\nBeginning of the script.\n")

    a = SchoolDataFetcher()
    result = a.scrap_resources()
    a.generate_json_file(result)

if __name__ == "__main__":
    main()

