#!/usr/bin/env

from Affiliation import Affiliation


class CanonicalAffiliations:
    # This global dictionary will store all corrections of observed affiliation
    # names that DO NOT have disambiguated IDs in the ORCID databse.
    _corrected_affiliations = {
        Affiliation(
            institution_name='Decode genetics / Amgen',
            department=None,
            city='Reykjavik',
            region=None,
            country='IS',
            disambiguated_id=None,
            disambiguation_source=None): Affiliation(
                institution_name='deCODE genetics / Amgen',
                department=None,
                city='Reykjavik',
                region=None,
                country='IS',
                disambiguated_id=None,
                disambiguation_source=None)
    }

    def __init__(self):
        pass

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



