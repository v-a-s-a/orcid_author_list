#!/usr/bin/env python

import pycountry


class Affiliation:
    """
    An author's affiliation.
    """

    def __init__(self, department, organization_name, organization_city,
                 organization_region, organization_country,
                 disambiguated_organization_identifier, disambiguation_source):
        """
        Parse the JSON 'affiliations' field from the ORCID response.
        """
        self.department = department
        self.organization_name = organization_name
        self.organization_city = organization_city
        self.organization_region = organization_region
        self.organization_country = organization_country
        self.disambiguated_organization_identifier = disambiguated_organization_identifier
        self.disambiguation_source = disambiguation_source

        if self.department is None:
            self.department = ''

        if self.organization_region is None:
            self.organization_region = ''

    def __eq__(self, other):
        """
        This is a hierarchical match. First, attempt to match on disambiguated
        IDs. If this fails, attempt to match on organization name and address.
        If this fails, look up in the matching dictionary.
        """
        if self.disambiguated_organization_identifier and self.disambiguation_source and other.disambiguated_organization_identifier and other. disambiguation_source:
            _equal = self.disambiguated_organization_identifier == other.disambiguated_organization_identifier and self.disambiguation_source == other.disambiguation_source
        elif self.organization_name and self.organization_address and other.organization_name and other.organization_address:
            _equal = self.organization_name == other.organization_name and self.organization_address == other.organization_address
        elif _corrected_affiliations.get(self.organization_name):
            _equal = _corrected_affiliations.get(self.organization_name) == other.organization_name
        elif _corrected_affiliations.get(other.organization_name):
            _equal = _corrected_affiliations.get(other.organization_name) == self.organization_name
        elif _corrected_affiliations.get(other.organization_name) and _corrected_affiliations.get(self.organization_name):
            _equal = _corrected_affiliations.get(other.organization_name) == _corrected_affiliations.get(self.organization_name)
        else:
            _equal = False

        return _equal

    def __repr__(self):
        proper_country = pycountry.countries.get(
            alpha_2=self.organization_country).name

        return '{dept} {name}, {city}, {region}, {country}. '.format(
            dept=self.department, name=self.organization_name,
            city=self.organization_city, region=self.organization_region,
            country=proper_country)

    def __hash__(self):
        if self.disambiguated_organization_identifier and self.disambiguation_source:
            _hashString = '{0} {1}'.format(self.disambiguated_organization_identifier, self.disambiguation_source)
        elif _corrected_affiliations.get(self.organization_name):
            _hashString = str(_corrected_affiliations.get(self.organization_name))
        else:
            _hashString = str(self)

        return hash(_hashString)


# This global dictionary will store all corrections of observed affiliation
# names that DO NOT have disambiguated IDs in the ORCID databse.
_corrected_affiliations = {
    'Decode genetics / Amgen':
        Affiliation(
            organization_name='deCODE genetics / Amgen',
            department=None,
            organization_city='Reykjavik',
            organization_region=None,
            organization_country='IS',
            disambiguated_organization_identifier=None,
            disambiguation_source=None)
}