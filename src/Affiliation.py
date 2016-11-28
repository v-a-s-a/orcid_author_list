#!/usr/bin/env python

import pycountry


class Affiliation:
    """
    An author's affiliation.
    """

    def __init__(self, department='', institution_name='', city='',
                 region='', country='',
                 disambiguated_id='', disambiguation_source='',
                 postal_code=''):
        self.department = self.munge_field(department)
        self.institution_name = self.munge_field(institution_name)
        self.city = self.munge_field(city)
        self.region = self.munge_field(region)
        self.country = self.munge_field(country)
        self.disambiguated_id = self.munge_field(disambiguated_id)
        self.disambiguation_source = self.munge_field(disambiguation_source)
        self.postal_code = self.munge_field(postal_code)

    def __eq__(self, other):
        """
        This is a critical method.

        We compare based on:
            disambiguated-id
            disambiguated-id-source
            department-name
            institution-name
            institution-city
            institution-region
            institution-country
        """

        return (
            self.disambiguated_id == other.disambiguated_id and
            self.disambiguation_source == other.disambiguation_source and
            self.institution_name == other.institution_name and
            self.department == other.department and
            self.city == other.city and
            self.region == other.region and
            self.country == other.country and
            self.postal_code == other.postal_code
        )

    def __repr__(self):
        proper_country = pycountry.countries.get(
            alpha_2=self.country).name

        return '{dept} {name}, {city}, {region}, {country} {postal_code}.'.format(
            dept=self.department, name=self.institution_name,
            city=self.city, region=self.region,
            country=proper_country, postal_code=self.postal_code)

    def __hash__(self):
        _hash_string = ' '.join([self.disambiguated_id,
                                 self.disambiguation_source,
                                 self.institution_name,
                                 self.department,
                                 self.city,
                                 self.region,
                                 self.country,
                                 self.postal_code])

        return hash(_hash_string)
