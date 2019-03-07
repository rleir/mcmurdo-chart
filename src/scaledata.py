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

years_with_complete_data=['1988', '2002', '2003', '2004', '2007', '2008', '2009', '2010', '2011']

all_years = [ '1988', '1990', '1991', '1992', '1993', '1997', '1998', '2002', '2003', '2004', '2007', '2008', '2009', '2010', '2011', '2012', '2014']
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
site_names = {
    "Cinder Cones - 13250 m": "CinderCones",
     "WQI   ":              "WinterQuartersInner",
     "WQM   ":              "WinterQuartersMiddle",
     "WQO   ":              "WinterQuartersOuter",
     "Outfall - 0 m":              "Outfall",
     "OA   ":              "OutfallA",
     "OB   ":              "OutfallB",
     "T   ":              "Transition",
     "R   ":              "Road",
     "JN   ":              "JettyN",
     "JS   ":              "JettyS",
     "CA: 1000 m":              "Armitage"}
#     CA: 1000 m
site_keys = list(site_names.keys())
species_keys = list(featured_species.keys())

all_data   = {}
for year in all_years:
    all_data[year] = {}

    for site_key in site_keys:
        site = site_names[site_key]
        all_data[year][site] = []
        all_data[year][site].append({})
        all_data[year][site][0]["data"]={}
        for species in species_keys:
            abbr = featured_species[species]
            all_data[year][site][0]["data"][abbr]=-10.0


def readfiles():

    for file in input_files:
        path = "data/"+file
        # read xls, find avg sheet
        wb = open_workbook(path)
        for sheet in wb.sheets():
            shname = sheet.name
            if shname.endswith("final averages"):
                coltoyear=[]           # zzz needs saving somewhere
                site = ""
                for row in range(sheet.nrows):
                    if row == 0:
                        site_key = sheet.cell(0,0).value
                        site = site_names[site_key]
                    if row == 1:
                        coltoyear = readheader(sheet,row)
                    else:
                        for col in range(sheet.ncols):
                            if col == 0:
                                species = sheet.cell(row,col).value
                                if species not in featured_species:
                                    continue
                                else:
                                    for datacol in range(sheet.ncols):
                                        if datacol > 0 and datacol%2 == 1:
                                            print(coltoyear,datacol)
                                            year = coltoyear[datacol]
                                            abbr = featured_species[species]
                                            print(year,site,abbr,row,datacol)
                                            all_data[year][site][0]["data"][abbr] = sheet.cell(row,datacol).value

#for i in range(sheet.ncols):
# print sheet.cell_type(1,i),sheet.cell_value(1,i)

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
                
    print(coltoyear)
    return coltoyear


ROW_LIMIT = 8

if __name__ == "__main__":
    # execute only if run as a script
    readfiles()
    


