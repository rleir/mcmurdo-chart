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
all_years = [ '1988', '1990', '1991', '1992', '1993', '1997', '1998', '2002', '2003', '2004', '2007', '2008', '2009', '2010', '2011', '2012', '2014']

def chart_by_mapsite(year):
    input_file = 'data/all_sites_' + year + '.csv'

    output_file = 'data/chart_by_mapsite_' + year + '.json'
    all_data   = {}
    all_sites = [ "CinderCones",
                  "WinterQuartersInner",
                  "WinterQuartersMiddle",
                  "WinterQuartersOuter",
                  "Outfall",
                  "OutfallA",
                  "OutfallB",
		  "Transition",
                  "Road",
		  "JettyN",
		  "JettyS",
		  "Armitage"]

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

    years_with_complete_data=['1988', '2002', '2003', '2004', '2007', '2008', '2009', '2010', '2011']

#    for year in years_with_complete_data:
    for year in all_years:
        chart_by_mapsite(year)
