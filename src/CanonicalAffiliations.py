#!/usr/bin/env

from Affiliation import Affiliation


class CanonicalAffiliations:
    # This global dictionary will store all corrections of observed affiliation
    # names that DO NOT have disambiguated IDs in the ORCID databse.
    def __init__(self):

        self._corrected_affiliations = {
            Affiliation(
                institution_name='Decode genetics / Amgen',
                department=None,
                city='Reykjavik',
                region=None,
                country='IS',
                disambiguated_id=None,
                disambiguation_source=None): Affiliation(
                    institution_name='deCODE Genetics / Amgen',
                    department=None,
                    city='Reykjavik',
                    region=None,
                    country='IS',
                    disambiguated_id='58209',
                    disambiguation_source='RINGGOLD'),
            Affiliation(
                institution_name='23andMe',
                department='Research',
                city='Mountain View',
                region='CA',
                country='US',
                disambiguated_id='90645',
                disambiguation_source='RINGGOLD'): Affiliation(
                    institution_name='23andMe, Inc.',
                    department='Research',
                    city='Mountain View',
                    region='CA',
                    country='US',
                    disambiguated_id='90645',
                    disambiguation_source='RINGGOLD'),
            Affiliation(
                institution_name='23andMe',
                department=None,
                city='Mountain View',
                region='CA',
                country='USA',
                disambiguated_id='90645',
                    disambiguation_source='RINGGOLD'): Affiliation(
                    institution_name='23andMe, Inc.',
                    department=None,
                    city='Mountain View',
                    region='CA',
                    country='US',
                    disambiguated_id='90645',
                    disambiguation_source='RINGGOLD'),
            Affiliation(
                institution_name='Virginia Commonwealth University',
                department='Virginia Institute of Psychiatric & Behavioral Genetics',
                city='Richmond',
                region='VA',
                country='US',
                disambiguated_id='6889',
                disambiguation_source='RINGGOLD'): Affiliation(
                    institution_name='Virginia Commonwealth University',
                    department='Virginia Institute for Psychiatric and Behavioral Genetics',
                    city='Richmond',
                    region='VA',
                    country='US',
                    disambiguated_id='6889',
                    disambiguation_source='RINGGOLD')
        }

        self._best_guess_departments = {
            Affiliation(
                institution_name='23andMe, Inc.',
                department=None,
                city='Mountain View',
                region='CA',
                country='US',
                disambiguated_id='90645',
                disambiguation_source='RINGGOLD'): Affiliation(
                    institution_name='23andMe, Inc.',
                    department='Research',
                    city='Mountain View',
                    region='CA',
                    country='US',
                    disambiguated_id='90645',
                    disambiguation_source='RINGGOLD'),
            Affiliation(
                institution_name='Kaiser Permanente Northern California',
                department=None,
                city='Oakland',
                region='CA',
                country='US',
                disambiguated_id='214681',
                disambiguation_source='RINGGOLD'): Affiliation(
                    institution_name='Kaiser Permanente Northern California',
                    department='Division of Research',
                    city='Oakland',
                    region='CA',
                    country='US',
                    disambiguated_id='214681',
                    disambiguation_source='RINGGOLD')

        }

    def validate(self, affiliation):
        """
        Take an Affiliation object and check it against the dictionary of edits.

        If there is a match, return the stored, canonical representation.
        """
        correction = self._corrected_affiliations.get(affiliation)
        if correction:
            return correction
        else:
            return affiliation

    def guess_department(self, affiliation):
        """
        Take a guess for the department for a given affiliation.
        """
        correction = self._best_guess_departments.get(affiliation)
        if correction:
            return correction
        else:
            return affiliation


