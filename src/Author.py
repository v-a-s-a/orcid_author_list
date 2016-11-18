#!/usr/bin/env python

import requests as req
from Affiliation import Affiliation
from utilities import remove_duplicates


class Author:
    """
    An author on the publication list.
    """

    def __init__(self, orcid, affiliations_checker):
        """
        An author is uniquely identified by their ORCID. All author information
        is drawn from the ORCID database.
        """
        self.orcid = orcid

        # hit orcid for the author profile
        try:
            r = req.get(
                'http://pub.orcid.org/v1.2_rc7/{0}/orcid-profile'.format(orcid),
                headers={'Accept': 'application/orcid+json'})
            r.raise_for_status()
        except req.ConnectionError:
            print("Failed to connect to ORCID database.")

        # parse names
        self.givenName = r.json()['orcid-profile']['orcid-bio']['personal-details']['given-names']['value'].title()
        self.familyName = r.json()['orcid-profile']['orcid-bio']['personal-details']['family-name']['value'].title()

        # parse email -- stored as None if email is not marked as primary or if email is not verified
        if r.json().get('orcid-profile').get('orcid-bio').get('contact-details'):
            emails = r.json()['orcid-profile']['orcid-bio']['contact-details']['email']
            primaryEmails = [x for x in emails if (x.get('primary') is True and x.get('verified'))]
            otherEmails = [x for x in emails if (x.get('primary') is False and x.get('verified'))]
            if primaryEmails:
                self.email = primaryEmails[0]
            elif otherEmails:
                self.email = otherEmails
            else:
                self.email = None
        else:
                self.email = None

        # parse affiliations
        if not r.json().get('orcid-profile').get('orcid-activities'):
            print('Author has no recorded and publicly available information. Source: {0}'.format(r.json()['orcid-profile']['orcid-identifier']['uri']))
            self.affiliations = None
        elif not r.json().get('orcid-profile').get('orcid-activities').get('affiliations'):
            print('Author has no recorded and publicly available affiliations. Source: {0}'.format(r.json().get('orcid-profile').get('orcid-identifier').get('uri')))
            self.affiliations = None
        else:
            affiliations_data = r.json()['orcid-profile']['orcid-activities']['affiliations']['affiliation']
            current_affiliations = filter(lambda affiliation: affiliation.get('end-date') is None and affiliation.get('organization'), affiliations_data)
            affiliations = [Affiliation(
                institution_name=value['organization']['name'],
                department=value['department-name'],
                city=value['organization']['address']['city'],
                region=value['organization']['address']['region'],
                country=value['organization']['address']['country'],
                disambiguated_id=None,
                disambiguation_source=None) for value in current_affiliations]

            # check against the canonical affiliations
            self.affiliations = remove_duplicates([affiliations_checker.validate(x) for x in affiliations])

    def __repr__(self):
        return '{first_name} {family_name}'.format(first_name=self.givenName, family_name=self.familyName)
