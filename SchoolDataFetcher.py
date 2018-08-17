#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
from SchoolData import SchoolData
import requests
import os.path
import urllib2
import codecs
import json
import sys
import csv
import re


class SchoolDataFetcher:
    """This object handles the scrappping and parsing of the two data sources.
    It is also in charge of merging the data and generating the final json file.

    As it is self-sustainable (urls are hard-coded in), 'scrap_resources' method
    can be used directly.
    """

    # Constants

    _FILENAME = "data.csv"
    _EXPECTED_FIELD_LIST = ['Code établissement', 'Appellation officielle', 'Dénomination principale',
                'Patronyme uai', 'Secteur Public/Privé', 'Adresse', 'Lieu dit', 'Boite postale', 'Code postal',
                "Localite d'acheminement", 'Commune', 'Coordonnee X', 'Coordonnee Y', 'EPSG', 'Latitude', 'Longitude',
                "Qualité d'appariement", 'Localisation', 'Code nature', 'Nature',
                'Code état établissement', 'Etat établissement',
                'Code département', 'Code région', 'Code académie', 'Code commune',
                'Département', 'Région', 'Académie', 'Position', 'Téléphone']


    # Public

    def scrap_resources(self):
        """The most important method. Returns a list of SchoolData objects.
        
        If proceeds in a few steps:

        1. Checks if the named csv file is in the current directory. If not,
        it downloads it.

        2. Scraps data from the second data source and generate a list
        of dictionnaries containing phone numbers of all schools from that source.

        3. Reads the csv file. The first line are the field names, and is used
        to generate all dictionnaries sent to instantiate a SchoolData object.
        The merging of data is done during this step.

        """

        print("Checking if file '" + self._FILENAME + "' exists.")
        if os.path.isfile(self._FILENAME):
            print("File already existing. Trying to use it...")
        else:
            print("File not found. Downloading...")
            self._download_csv()
            print("Done.")
        
        print("Getting creteil data now:")
        creteil_school_list = self._scrap_creteil()
        print("Number of Val-de-Marne schools found: " + str(len(creteil_school_list)))

        school_list = list()
        with open(self._FILENAME, "rb") as csv_file:
            print("Opened '" + self._FILENAME + "' data file.")
            reader = csv.reader(csv_file, delimiter=u";".encode('utf-8'))

            print("Processing csv...:")
            i = 0
            field_list = list()
            for line in reader:
                if i:
                    values = [item.decode('utf-8') for item in line]
                    values.append("")
                    entry = dict(zip(field_list, values))
                    tmp = entry.get("Code postal")
                    if tmp[:2] != "94":
                        pass
                    else:
                        entry = self._get_telephone(entry, creteil_school_list)
                    new = SchoolData(entry)
                    school_list.append(new)
                    i += 1
                else:
                    field_list = [item.decode('utf-8') for item in line]
                    field_list.append("Téléphone")
                    self._check_and_format_field_list(field_list)
                    i += 1

        print("Processed " + str(len(school_list)) + " lines.\n")
        return school_list


    def generate_json_file(self, data):
        """Takes a list of SchoolData objects and dumps it into a .json file.
        Best used with a list produced by 'scrap_resources' method.
        """

        print("Creating json file from school list...:")
        json_list = list()
        for item in data:
            json_list.append(item.better_format())
        with codecs.open("schools_list.json", "ab", "utf-8") as f:
            f.write(json.dumps(json_list, ensure_ascii=False))


    # Private

    def _get_telephone(self, entry, other):
        """Checks the current line of CSV. If data matches with something
        in 'other', telephone from 'other' is added to 'entry'.

        Attributes:
        entry: dictionnary made with the current line of the csv file
        other: list of dicts containing schools data from Creteil academy
        """

        tmp = entry['Dénomination principale']
        if (tmp.find("LYCEE")) != -1:
            patronyme = entry['Patronyme uai']
            nature = re.sub(" (D ENSIGNEMENT|ENSEIGNT)", "", entry['Nature'])
            for item in other:
                if item['nom'].find(patronyme) != -1 and item['type'] == nature:
                    entry['Téléphone'] = item['telephone']
                    break
        return entry


    def _download_csv(self):
        """Scraps the first data source website to get the most recent csv file,
        and downloads it.
        
        It is worthy to note that if a new file with different field naming is put
        online, the file won't work as the program expects a precise list of fields.
        """

        target_url = "https://www.data.gouv.fr/fr/datasets/adresse-et-geolocalisation-des-etablissements-denseignement-du-premier-et-second-degres/"
        print("Scrapping file from website: " + target_url + ". Looking for the most recent version...")

        response = urllib2.urlopen(target_url)
        page = response.read()
        pattern = re.compile(r"<a.*?href=\"(.*?)\".*?>Consultez les dern.*?<\/a>")
        latest_page_url = re.search(pattern, page).group(1)

        response = urllib2.urlopen(latest_page_url)
        page = response.read().decode('utf-8')
        page = page.replace("\n", " ")
        pattern = re.compile(r"<article.*?class=\"card.*?CSV format export.*?(<a .*?Télécharger<\/a>).*?<\/article>")
        dl_url = re.search(pattern, page).group(1)
        dl_url = re.sub("(.*?href=\"|\" .*)", "", dl_url)
        
        print("Found. Expect a ~1 minute download...")
        response = urllib2.urlopen(dl_url)
        received = response.read()
        with open("./data.csv", "wb") as f:
            f.write(received)
        print(self._FILENAME + " saved with success!")


    def _scrap_creteil(self):
        """Scraps the second data source website, and generate a list of dicts
        containing some info on the scrapped schools.
        Basically, it scraps the towns of Val-de-Marne, and makes a POST request
        on each one to get the data needed.

        This is where the phone number is found.
        """

        target_url = "http://www.ia94.ac-creteil.fr/infogen/etablissements/lycees.htm"
        print("Scrapping data from website: " + target_url + ". Expect 10 - 15 seconds...")

        response = urllib2.urlopen(target_url)
        page = response.read().decode('iso-8859-1').replace("\n", "")
        pattern = re.compile("div id=\"afficheur\">(<form.*>.*<\/form>)")
        cities_form = pattern.search(page)
        cities_form = cities_form.group(1)
        tmp = re.finditer(r"<option.*?\"(.*?)\">(.*?)<\/option>", cities_form)

        i = 0
        cities_list = list()
        creteil_school_list = list()
        for item in tmp:
            if i:
                payload = {"Ville" : item.group(1)}
                r = requests.post(target_url, data=payload)
                tmp = self._extract_table(r.content.decode('iso-8859-1'))
                for school in tmp:
                    creteil_school_list.append(school)
                print("Done: " + item.group(2))
            i += 1
        return creteil_school_list


    def _extract_table(self, data):
        """Reads the table from the website containing all the schools data.
        A basic dict is filled for each school and added to the list.
        Returns a list of dicts (all schools on the current page).

        Attributes:
        data: a string containing the raw code of the HTML page that need to be scrapped
        """

        data = data.replace("\n", "")
        pattern = re.compile("div id=\"afficheur\">.*?<h3>(.*?)<\/h3>.*?(<table>.*?<\/table>)")
        table = pattern.search(data)
        head, table = table.group(1), table.group(2)
        code_postal = head.split()[0].strip()
        ville = head.replace(code_postal, "").strip()
        table = table.replace("&nbsp;", " ")

        school_list = list()
        for item in table.split("<tr>")[1:]:
            school = {}
            item = re.sub(r"<.*?>", "|", item)
            item = re.sub(r"\|+ ?\|+", "|", item)
            item = item.split("|")
            nature = item[1].strip()
            nature = nature.replace("é", "e")
            nature = nature.replace("è", "e")
            nature = re.sub("[^a-zA-Z]", " ", nature).upper()
            nature = re.sub(" *LYCEE *(DES METIERS)? *", "", nature)
            school["nom"] = item[2].strip()
            school["type"] = "LYCEE " + nature
            school["ville"] = ville
            school["code_postal"] = code_postal
            school["adresse"] = item[3].strip()
            school["telephone"] = item[4].split(":")[1].strip()
            school_list.append(school)
        return school_list


    def _check_and_format_field_list(self, data):
        """Checks if the first line of CSV (data) matches expected fields.
        If not, program ends.
        """

        diff = list(set(data) - set(self._EXPECTED_FIELD_LIST))
        if diff:
            sys.exit("Error: mismatching fields: " + ', '.join(diff)
                     + "\nExpected: " + ', '.join(self._EXPECTED_FIELD_LIST))
