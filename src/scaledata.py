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

featured_species= [
    "Capitella perarmata",
    "Aphelochaeta sp", 
    "Galathowenia scotiae",
    "Spiophanes tcherniai",
    "Nototanais dimorphus",
    "Ophryotrocha notialis SUM",
    "Philomedes spp.",
    "Edwardsia meridionalis"]

def readfiles():
    for file in input_files:
        path = "data/"+file
        # read xls, find avg sheet

        wb = open_workbook(path)
        for sheet in wb.sheets():
            shname = sheet.name
            if shname.endswith("final averages"):
                coltoyear=[] 
                for row in range(sheet.nrows):
                    if row == 1:
                        coltoyear = readheader(sheet,row)
                    elif row > 1:  # skip row 0
                        values = []
                        for col in range(sheet.ncols):
                            if col == 0:
                                species = sheet.cell(row,col).value
                                if species in featured_species:
                                    print(sheet.cell(row,col).value)
                        #                        values.append(sheet.cell(row,col).value)
#                        print(sheet.cell(row,col))
#                    print (','.join(values))
                print()

#text:'CA14-ave'
#text:'CA14-se'
#text:'Laternula elliptica'
#number:1.5
#number:0.7637626158259734
#number:0.8333333333333334

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
                year = colheader[-6:-4]
                if int(year) > 80:
                    year = "19"+year
                else:
                    year = "20"+year
                coltoyear.append(year)
            else:
                coltoyear.append(0) 
                
    print(coltoyear)
    return coltoyear


ROW_LIMIT = 8

if __name__ == "__main__":
    # execute only if run as a script
    readfiles()
    


