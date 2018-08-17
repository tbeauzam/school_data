#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
import json

class SchoolData:
    """ An object representation of a school based on the associated CSV

    This object should not be used directly, as it is strongly
    tied to SchoolDataFetcher. It is however possible to print it.
	
    Attributes:
        See the Readme.txt to see the attributes
    
    """

    
    # Constant listing all attributes names

    _ATTRIBUTE_LIST = ['code_etablissement', 'appellation_officielle', 'denomination_principale', 'patronyme_uai',
                       'secteur_public_prive', 'adresse', 'lieu_dit', 'boite_postale', 'code_postal',
                       'localite_d_acheminement', 'commune', 'coordonnee_x', 'coordonnee_y', 'epsg', 'latitude',
                       'longitude', 'qualite_d_appariement', 'localisation', 'code_nature', 'nature',
                       'code_etat_etablissement', 'etat_etablissement', 'code_departement', 'code_region',
                       'code_academie', 'code_commune', 'departement', 'region', 'academie', 'position', 'telephone']

    
    # Builtins

    def __init__(self, data):
        """Init. data is a dict where keys are field names of the csv"""

        self.code_etablissement = data['Code établissement']
        self.appellation_officielle = data['Appellation officielle']
        self.denomination_principale = data['Dénomination principale']
        self.patronyme_uai = data['Patronyme uai']
        self.secteur_public_prive = data['Secteur Public/Privé']
        self.adresse = data['Adresse']
        self.lieu_dit = data['Lieu dit']
        self.boite_postale = data['Boite postale']
        self.code_postal = data['Code postal']
        self.localite_d_acheminement = data['Localite d\'acheminement']
        self.commune = data['Commune']
        self.coordonnee_x = data['Coordonnee X']
        self.coordonnee_y = data['Coordonnee Y']
        self.epsg = data['EPSG']
        self.latitude = data['Latitude']
        self.longitude = data['Longitude']
        self.qualite_d_appariement = data['Qualité d\'appariement']
        self.localisation = data['Localisation']
        self.code_nature = data['Code nature']
        self.nature = data['Nature']
        self.code_etat_etablissement = data['Code état établissement']
        self.etat_etablissement = data['Etat établissement']
        self.code_departement = data['Code département']
        self.code_region = data['Code région']
        self.code_academie = data['Code académie']
        self.code_commune = data['Code commune']
        self.departement = data['Département']
        self.region = data['Région']
        self.academie = data['Académie']
        self.position = data['Position']
        self.telephone = data['Téléphone']


    def __repr__(self):
        """Displays a basic list of all attributes on the form 'key: value'"""

        rep = "School data:\n"
        att_list = ["%s: %s" % (att, getattr(self, att)) for att in self._ATTRIBUTE_LIST]
        rep += '\n'.join(att_list)
        return rep.encode('utf-8')


    def __str__(self):
        """Displays attributes using the better_format method, and indentation"""
        return json.dumps(self.better_format(), indent=4, ensure_ascii=False).encode('utf-8')
        

    # Public

    def better_format(self):
        """Povides a more organized format for readability.
        
        Attributes are spread across three groups:
        - info: information about school name and organization
        - localisation: everything about the adress in term of region, town, etc.
        - donnees_geographiques: geolocalisation of the school

        - code_etablissement: ID of the school. It is kept in the main scope
        of the data structure for convenience.

        """

        info = { "appellation_officielle" : self.appellation_officielle,
                "denomination_principale" : self.denomination_principale,
                "patronyme_uai" : self.patronyme_uai,
                "secteur_public_prive" : self.secteur_public_prive,
                "code_nature" : self.code_nature,
                "nature" : self.nature,
                "code_etat_etablissement" : self.code_etat_etablissement,
                "etat_etablissement" : self.etat_etablissement,
                "code_academie" : self.code_academie,
                "academie" : self.academie,
                "telephone" : self.telephone }

        localisation = { "localisation" : self.localisation,
                "adresse" : self.adresse,
                "qualite_d_appariement" : self.qualite_d_appariement,
                "region" : self.region,
                "code_region" : self.code_region,
                "departement" : self.departement,
                "code_departement" : self.code_departement,
                "commune" : self.commune,
                "code_commune" : self.code_commune,
                "lieu_dit" : self.lieu_dit,
                "boite_postale" : self.boite_postale,
                "code_postal" : self.code_postal,
                "localite_d_acheminement" : self.localite_d_acheminement }

        geographic_data = { "coordonnee_x" : self.coordonnee_x,
                "coordonnee_y" : self.coordonnee_y,
                "latitude" : self.latitude,
                "longitude" : self.longitude,
                "position" : self.position,
                "epsg" : self.epsg }

        data = { "code_etablissement" : self.code_etablissement, 
                "info" : info,
                "localisation" : localisation,
                "donnees_geo" : geographic_data }

        return data
