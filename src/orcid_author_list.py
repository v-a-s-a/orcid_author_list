#!/usr/bin/env python
"""
Generating an author list based on a list of ORCIDs.

TODO:
    * Ordering authors correctly.
    * Matching affiliations based on disambiguated organization identifiers.

"""

import requests as req
import rtfunicode
import pycountry
import pdb
import argparse as arg


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


def remove_duplicates(li):
    my_set = set()
    res = []
    for e in li:
        if e not in my_set:
            res.append(e)
            my_set.add(e)
    return res


class Author:
    """
    An author on the publication list.
    """

    def __init__(self, orcid):
        """
        An author is uniquely identified by their ORCID.

        The orcid data base is hit for all relevant information.
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
        self.givenName = r.json().get('orcid-profile').get('orcid-bio').get('personal-details').get('given-names').get('value').title()
        self.familyName = r.json().get('orcid-profile').get('orcid-bio').get('personal-details').get('family-name').get('value').title()

        # parse email -- stored as None if email is not marked as primary or if email is not verified
        if r.json().get('orcid-profile').get('orcid-bio').get('contact-details'):
            emails = r.json().get('orcid-profile').get('orcid-bio').get('contact-details').get('email')
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
            print('Author has no recorded and publicly available information. Source: {0}'.format(r.json().get('orcid-profile').get('orcid-identifier').get('uri')))
            self.affiliations = None
        elif not r.json().get('orcid-profile').get('orcid-activities').get('affiliations'):
            print('Author has no recorded and publicly available affiliations. Source: {0}'.format(r.json().get('orcid-profile').get('orcid-identifier').get('uri')))
            self.affiliations = None
        else:
            affiliations = r.json()['orcid-profile']['orcid-activities']['affiliations']['affiliation']
            currentAffiliations = filter(lambda affiliation: affiliation.get('end-date') is None and affiliation.get('organization'), affiliations)
            self.affiliations = remove_duplicates([Affiliation(
                organization_name=value['organization']['name'],
                department=value['department-name'],
                organization_city=value['organization']['address']['city'],
                organization_region=value['organization']['address']['region'],
                organization_country=value['organization']['address']['country'],
                disambiguated_organization_identifier=None,
                disambiguation_source=None) for value in currentAffiliations])

    def __repr__(self):
        return '{first_name} {family_name}'.format(first_name=self.givenName, family_name=self.familyName)


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


def __main__():

    parser = arg.ArgumentParser()
    parser.add_argument('--input', action='store', dest='input_file',
                        help='File containing one ORCID per line.')
    parser.add_argument('--out', action='store', dest='output_file',
                        help='Output RTF file to write authors list to.')
    args = parser.parse_args()

    dat = [line for line in open(args.input_file)]

    # load authors from orcid db
    orcids = remove_duplicates([x.strip() for x in dat if x])
    authors = {orcid: Author(orcid) for orcid in orcids}

    # index unque affiliations based on author order in the orginal .csv file
    affiliations_index = dict()
    counter = 1
    for orcid in orcids:
        if authors[orcid].affiliations:
            affiliations = authors[orcid].affiliations
        else:
            continue
        for affiliation in affiliations:
            if not affiliations_index.get(affiliation):
                affiliations_index[affiliation] = counter
                affiliations_index[counter] = affiliation
                counter += 1

    # pdb.set_trace()

    with open(args.output_file, 'wb') as outFile:
        # rtf "header"
        out_bytes = b'{\\rtf1 \\utf-8 '

        # print author list: name and affilliation reference
        authors_with_affiliations = [authors[orcid]
                                     for orcid in orcids
                                     if authors[orcid].affiliations]
        author_affiliations = [author.affiliations
                               for author in authors_with_affiliations]
        formatted_affiliations_indices = ['{\\super ' + str(sorted([affiliations_index[affiliation] for affiliation in affiliations])).strip('[').strip(']') + '}' for affiliations in author_affiliations]
        encoded_affiliations_indicies = [x.encode('utf8') for x in formatted_affiliations_indices]

        encoded_authors = [str(author).encode('rtfunicode') for author in authors_with_affiliations]
        out_bytes += b', '.join([b''.join(x) for x in zip(encoded_authors, encoded_affiliations_indicies)])
        out_bytes += '\n\n'.encode('rtfunicode')

        # print affiliations
        encoded_affiliations = [str(affiliations_index[i + 1]).replace(' ,', '').encode('rtfunicode') for i in range(int(len(affiliations_index) / 2))]
        encoded_affiliation_index = ['{{\\super {0}}}'.format(i + 1).encode('utf8') for i in range(int(len(affiliations_index) / 2))]
        out_bytes += b''.join([b''.join(x) for x in zip(encoded_affiliation_index, encoded_affiliations)])

        # end rtf file
        out_bytes += b'}'

        outFile.write(out_bytes)


if __name__ == '__main__':
    __main__()
