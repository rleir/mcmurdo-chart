#!/usr/bin/env python3
"""
Handy utility to reformat some data for use in a d3js chart.
  read input xls data file
  find final averages sheet
  allow for different years
  find the rows we want
  write intermediate per-year csv files??
  get maxaverages, do scaling
  write the yearly jsons
"""

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
from xlrd import open_workbook # type: ignore
from importdata import chart_by_mapsite
from typing import Dict, List

# The input spreadsheet might contain more species than we want to display.
# Here is the way to indicate which species we want to display:
featured_species = {} # type: Dict[ str, str]

all_years = [ ] # type: List[ str]

# Site name keys below match the column headers in the input xlsx
site_keys = [] # type: List[ str]

species_keys = []

all_data   = {} # type: Dict
max_average   = {} # type: Dict

def initData() -> None:
    global all_years
    with open("data/allyears.json") as json_file:
        all_years= json.load( json_file)

    global featured_species
    global species_keys
    with open("data/featured_species.json") as json_file:
        featured_species = json.load( json_file)
    species_keys = list(featured_species.keys())

    positions = [ ] # type: List[ Dict[ str,str]]
    with open("data/positions.json") as json_file:
        positions= json.load( json_file)
    for position in positions:
        site_keys.append(position['placeName'])

    for year in all_years:
        all_data[year] = {}

        for site_key in site_keys:
            all_data[year][site_key] = []
            all_data[year][site_key].append({})
            all_data[year][site_key][0]["data"   ]={}
            all_data[year][site_key][0]["average"]={}
            for species in species_keys:
                abbr = featured_species[species]
                all_data[year][site_key][0]["data"][abbr]=0
                all_data[year][site_key][0]["average"][abbr]=-10


def readFiles() -> None:
        # read xls, find avg sheet
        path = "data/SpeciesCounts.xlsx"
        wb = open_workbook(path)
        final_av_s_found = 0
        for sheet in wb.sheets():
            shname = sheet.name
            if shname.endswith("ave"):
                final_av_s_found = 1
                coltoyear=[] # type: List[ str]
                maxcol = 0
                for row in range(sheet.nrows):
                    if row == 0:
                        for col in range(sheet.ncols):
                            if "MAX" == sheet.cell(row,col).value:
                                maxcol = col
                    elif row == 1:
                        coltoyear = readheader(sheet,row)
                    else:
                        for col in range(sheet.ncols):
                            if col == 0:
                                species = sheet.cell(row,col).value
                                if species not in featured_species:
                                    continue
                                else:
                                    abbr = featured_species[species]
                                    for datacol in range(sheet.ncols):
                                        colval = coltoyear[datacol]
                                        if maxcol == datacol:
                                            max_average[abbr]= sheet.cell(row,datacol).value
                                        
                                        if colval == "MAXAVG":
                                            max_average[abbr]= sheet.cell(row,datacol).value

                                        elif datacol > 0 and colval != "not ave col":
                                            year = coltoyear[datacol][-4:]
                                            site = coltoyear[datacol][:-4]
                                            all_data[year][site][0]["average"][abbr] = sheet.cell(row,datacol).value
        if final_av_s_found == 0 :
            print("final averages sheet not found in " + path)

def scaleData() -> None:
    running_count = {}
    check_max_average   = {}

    for species_key in species_keys:
        abbr = featured_species[species_key]
        check_max_average  [abbr] = 0
        running_count[abbr] = 0

    # find the max average for each species
    for year in all_years:
        for site_key in site_keys:
            for species_key in species_keys:
                abbr = featured_species[species_key]
                replicates_average = all_data[year][site_key][0]["average"][abbr]
                if  check_max_average[ abbr] < replicates_average :
                    check_max_average[  abbr] = replicates_average
                    running_count[abbr] += 1

    for species_key in species_keys:
        abbr = featured_species[species_key]
        if check_max_average[abbr] <= 0 :
            print("error, running count 0 " + abbr)
        if running_count[abbr] <= 0 :
            print("error, running count 0 " + abbr)
 
    # scale all the data in the range 0 to 100 where 100 represents the max average 
    for year in all_years:
        for site_key in site_keys:
            for species_key in species_keys:
                abbr = featured_species[species_key]
                replicates_average = all_data[year][site_key][0]["average"][abbr]

                if max_average[  abbr] != check_max_average[  abbr]:
                    print("max_avg="+ str(max_average[  abbr]) + " check_max=" + str(check_max_average[  abbr]) + " species=" + abbr)
                max_avg = check_max_average[  abbr]

                display = -10.0 # should be 0, but -10 is a flag saying 'no data'
                #display = 1.0 # should be 0, but 1 avoids a bug in the tweening
                if replicates_average > -10 :
                    #display = replicates_average*100 / (max_avg+0.00001)
                    display = replicates_average*100 / max_avg
                all_data[year][site_key][0]["data"][abbr] = display

def writeFiles() -> None:
    for year in all_years:
        # write output
        output_file = "data/all_sites_" + str(year) + ".csv"

        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ["organism","abbr"] + site_keys 
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for species_key in species_keys:
                abbr = featured_species[ species_key]
                row_data = {'organism': species_key, 'abbr': abbr}
                for site_key in site_keys:
                    row_data[site_key] =        all_data[year][site_key][0]["data"][abbr]
                writer.writerow(row_data)

def readheader(sheet,row) -> List[str]:
    coltoyear=[]
    for col in range(sheet.ncols):
        colheader = sheet.cell(row,col).value
        if colheader == "MAX":
            coltoyear.append("MAXAVG") 
        elif not colheader.endswith("-ave"):
            coltoyear.append("not ave col") 

        else:                
                siten =  colheader[:-6]
                year = colheader[-6:-4]
                if int(year) > 80:
                    year = "19"+year
                else:
                    year = "20"+year
                coltoyear.append(siten+year)
    return coltoyear



if __name__ == "__main__":
    # execute only if run as a script

    initData()
    readFiles()
    scaleData()
    writeFiles()

    for year in all_years:
        chart_by_mapsite(year)
    


