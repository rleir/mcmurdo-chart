#!/usr/bin/env python3
"""
Handy utility to reformat some data for use in a d3js chart.
  read 12 xls files
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
import glob
from xlrd import open_workbook

input_files = [ "Cape Armitage 1988-2014.xls",
                "Cinder Cones 1988-2014.xls",
                "Outfall 1988-2014.xls"]

featured_species= {
    "Capitella perarmata": "Capi",
    "Aphelochaeta sp": "Aphe", 
    "Galathowenia scotiae": "Gala",
    "Spiophanes tcherniai": "Spio",
    "Nototanais dimorphus": "Noto",
    "Ophryotrocha notialis SUM": "Ophr",
    "Philomedes spp.": "Phil",
    "Edwardsia meridionalis": "Edwa"
    }

# years_with_complete_data=['1988', '2002', '2003', '2004', '2007', '2008', '2009', '2010', '2011']

all_years = [ '1988', '1990', '1991', '1992', '1993', '1997', '1998', '2002', '2003', '2004', '2007', '2008', '2009', '2010', '2011', '2012', '2014']

site_names = {
    "Cinder Cones - 13250 m":              "CinderCones",
    "Winter Quarters Bay Inner -330 m":    "WinterQuartersInner",
    "Winter Quarters Bay Middle -200 m":   "WinterQuartersMiddle",
    "Winter Quarters Bay Outer -170 m":    "WinterQuartersOuter",
    "Outfall - 0 m":                       "Outfall",
    "Outfall South A 115 m":               "OutfallA",
    "Outfall South B 166 m":               "OutfallB",
    "Transition 250 m":                    "Transition",
    "Road 290 m":                          "Road",
    "Jetty North 420 m":                   "JettyN",
    "Jetty South 434 m":                   "JettyS",
    "CA: 1000 m":                          "Armitage"}
all_sites = list(site_names.values())
site_keys = list(site_names.keys())
species_keys = list(featured_species.keys())

all_data   = {}


def initData():
    for year in all_years:
        all_data[year] = {}

        for site_key in site_keys:
            site = site_names[site_key]
            all_data[year][site] = []
            all_data[year][site].append({})
            all_data[year][site][0]["data"   ]={}
            all_data[year][site][0]["average"]={}
            for species in species_keys:
                abbr = featured_species[species]
                all_data[year][site][0]["data"][abbr]=0
                all_data[year][site][0]["average"][abbr]=-10


def readFiles():

    input_files = glob.glob('data/*.xls')
    for path in input_files:
        # read xls, find avg sheet
        wb = open_workbook(path)
        final_av_s_found = 0
        for sheet in wb.sheets():
            shname = sheet.name
            if shname.endswith("final averages"):
                final_av_s_found = 1
                coltoyear=[]           # zzz needs saving somewhere
                site = ""
                for row in range(sheet.nrows):
                    if row == 0:
                        site_key = sheet.cell(0,0).value
                        # is this an expected value?
                        if not site_key in site_names :
                            print("unexpected site name " + site_key + " in " + path)
                        site = site_names[site_key]
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
                                        if datacol > 0 and datacol%2 == 1:
                                            year = coltoyear[datacol]
                                            all_data[year][site][0]["average"][abbr] = sheet.cell(row,datacol).value
        if final_av_s_found == 0 :
            print("final averages sheet not found in " + path)

                                            
def scaleData():
    max_average   = {}
    running_count = {}
    for species_key in species_keys:
        max_average  [species_key] = 0
        running_count[species_key] = 0

    # find the max average for each species
    for year in all_years:
        for site_key in site_keys:
            site = site_names[site_key]
            for species_key in species_keys:
                abbr = featured_species[species_key]
                replicates_average = all_data[year][site][0]["average"][abbr]
                if  max_average[  species_key] < replicates_average :
                    max_average[  species_key] = replicates_average
                    running_count[species_key] += 1

    for species_key in species_keys:
        if max_average[species_key] <= 0 :
            print("error, running count 0 " + species_key)
        if running_count[species_key] <= 0 :
            print("error, running count 0 " + species_key)
 
    # scale all the data in the range 0 to 100 where 100 represents the max average 
    for year in all_years:
        for site_key in site_keys:
            site = site_names[site_key]
            for species_key in species_keys:
                abbr = featured_species[species_key]
                replicates_average = all_data[year][site][0]["average"][abbr]
                max_avg = max_average[  species_key]

                display = -10.0
                if replicates_average > -10 :
                    #display = replicates_average*100 / (max_avg+0.00001)
                    display = replicates_average*100 / max_avg
                all_data[year][site][0]["data"][abbr] = display

def writeFiles():
    for year in all_years:
        # write output
        output_file = "all_sites_" + str(year) + ".csv"

        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ["organism","abbr"] + all_sites 
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for species_key in species_keys:
                abbr = featured_species[ species_key]
                row_data = {'organism': species_key, 'abbr': abbr}
                for site in all_sites:
                    row_data[site] =        all_data[year][site][0]["data"][abbr] 
                writer.writerow(row_data)

def readheader(sheet,row):
    coltoyear=[]
    for col in range(sheet.ncols):
        colheader = sheet.cell(row,col).value
        if col == 0:
            coltoyear.append(0) 
        else:
            if colheader.endswith("-ave"):
                if col%2 == 0:
                    print("error, ave in col "+str(col))
                year = colheader[-6:-4]
                if int(year) > 80:
                    year = "19"+year
                else:
                    year = "20"+year
                coltoyear.append(year)
            else:
                if col%2 == 1:
                    print("error, no ave in col "+str(col))
                coltoyear.append(0) 
                
    return coltoyear


ROW_LIMIT = 8

if __name__ == "__main__":
    # execute only if run as a script

    initData()
    readFiles()
    scaleData()
    writeFiles()
    


