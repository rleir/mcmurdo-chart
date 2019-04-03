# mcmurdo-chart
An experiment in radial bar charts using the d3js toolkit (see http://d3js.org ).

Based on Peter Cook's
 https://github.com/prcweb/d3-radialbar
 removed .append('svg') l42

The positions being charted must be specified in data/positions.json in this format:

[   {"x": 95, "y":275,  "placeName": "TR",   "fullName": "Turtle Rock -13250 m"},
        {"x":250, "y":430,  "placeName": "CCN",  "fullName": "Cinder Cones -5000 m"},
    ...

The position x,y values are chosen manually at the moment.

The years being charted must be specified in data/allyears.json in this format:

    [   "1988",
        "1990",
    ....

The input data is expected to be in a single xlsx spreadsheet of any name located in the data directory:

    $ ls data/*.xlsx
    data/inputSomeData.xlsx

This spreadsheet must have a header row with header cells each containing a 2 digit year and a position indicator corresponding to a placeName field in positions.json, followed by '-ave'. The 2 digit year must appear in allyears.json. For example, a header cell might be 'TR08-ave' above a column of 2008 data for the position at Turtle Rock.

The first column must contain species names. Not all species will get charted; the species which are charted are those listed in featuredSpecies.json. The header row must contain a first cell of 'Species'.

The data cells in the body of the of the spreadsheet are considered to be 'averages' because each site was sampled in several positions a few metres apart, and the samples are averaged to produce the value in the cell. 

The last column must contain a maximum average value for the species. The header row must contain a cell above the average data with the cell value 'MAX'.



Format the data:

    $ python scaledata.py

View the visualisation at URL
http://localhost/index.html
