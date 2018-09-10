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

    with_phone = list()
    for item in result:
        if item.telephone != "":
            with_phone.append(item)

    a.generate_json_file(with_phone, "schools_with_phone.json")
    a.generate_json_file(result, "all_schools.json")

    print("Finished with success!")

if __name__ == "__main__":
    main()

