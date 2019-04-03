#!/usr/bin/env python3
"""Handy utility to reformat some data for use in a d3js chart."""

__author__ = "Richard Leir"
__copyright__ = "Copyright 2018, Richard Leir"
__credits__ = ["Kathy Conlan", "Mike Bostock"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Richard Leir"
__email__ = "rleir at leirtech ddot com"
__status__ = "Production"

import csv
import json
import copy

ROW_LIMIT = 8

def chart_by_mapsite(year):
    all_sites = [ ]
    positions = [ ]
    with open("data/positions.json") as json_file:
        positions= json.load( json_file)
    for position in positions:
        all_sites.append(position['placeName'])

    input_file = 'data/all_sites_' + year + '.csv'

    output_file = 'data/chart_by_mapsite_' + year + '.json'
    all_data   = {}

    # foreach site
    #   foreach organism
    #     is there a site avgcountscal? add it to data
    for site in all_sites:
        # read input
        with open(input_file, newline='') as csvfile:
            input_data = csv.DictReader(csvfile)
            radial_data = {}
            iter=0
            for row in input_data:
                # OrderedDict([('organism', 'Capitella perarmata'), ('CinderCones', '0.000'), ('Outfall', '17.118'), ('Armitage', '0.000')])
                iter += 1
                if iter > ROW_LIMIT :
                    break
                keys = list(row.keys())
                organism_name = row['abbr']
                if site in keys:
                    radial_data[organism_name]=row[site]
                else:
                    radial_data[organism_name]=0.0

            site_data = []
            site_data_inner = {}
            site_data_inner["data"] = radial_data
            site_data.append( site_data_inner )
            all_data[site] = copy.deepcopy(site_data)        

    # write output
    with open(output_file, "w") as fp:
        json.dump(all_data , fp) 


if __name__ == "__main__":
    # execute only if run as a script

    all_years = [ ]
    with open("data/allyears.json") as json_file:
        all_years= json.load( json_file)
        
    for year in all_years:
        chart_by_mapsite(year)
