'use strict';

var positions = [{"x":150, "y":550, "placeName": "CinderCones"},
                 {"x":300, "y":150, "placeName": "WinterQuartersInner"},
                 {"x":310, "y":250, "placeName": "WinterQuartersMiddle"},
                 {"x":310, "y":310, "placeName": "WinterQuartersOuter"},
                 {"x":440, "y":410, "placeName": "Outfall"},
                 {"x":500, "y":450, "placeName": "OutfallA"},
                 {"x":500, "y":450, "placeName": "OutfallB"},
                 {"x":520, "y":450, "placeName": "Transition"},
                 {"x":650, "y":490, "placeName": "Road"},
                 {"x":700, "y":500, "placeName": "JettyN"},
                 {"x":800, "y":560, "placeName": "JettyS"},
                 {"x":870, "y":580, "placeName": "Armitage"}
                ];
var formSelect = d3.select("#year-select");
var formButton = d3.select("#a-button");


formButton.on("click", function() {
    var year = formSelect.node().value;
    if(year == "1988"){
        year = "2002";
    } else if(year == "2002"){
        year = "2003";
    } else if(year == "2003"){
        year = "2004";
    } else if(year == "2004"){
        year = "2007";
    } else if(year == "2007"){
        year = "2008";
    } else if(year == "2008"){
        year = "2009";
    } else if(year == "2009"){
        year = "2010";
    } else if(year == "2010"){
        year = "2011";
    } else if(year == "2011"){
        year = "1988";
    }
    console.log("buttonv  "+year);

    // update the selector
    var e = document.getElementById('year-select');
    if(e) e.value = year;
    
//    formSelect.value = year;
//    .property('checked', false)
    loadData(year);
});

formSelect.on("change", function() {
    var year = this.value;
    console.log("selectv  "+year);
//    formSelect.value = year;
    loadData(year);
});

// the initial load
loadData(formSelect.node().value);

//locate main svg element
var svgDoc = d3.select("#chart svg");

function ready (err, data) {
//zzz    console.log(data);
    //create basic radbars
    // d3.select(this)
    svgDoc
        .selectAll("g")
        .data(positions)
        .enter()
        .append("g")
        .attr("transform",function(d,i){
            var chart = radialBarChart()
                .barHeight(60)
                .reverseLayerOrder(true)
                .barColors([
                    '#EEB945',
                    '#E67323',
                    '#B66199',
                    '#9392CB',
                    '#76D9FA'])  // Yellow/orange/mauve/purple/blue
                .domain([0,17])
                .tickValues([5,10])
                .tickCircleValues([1,2,3,4,5,6,7,8,9,10]);
            d3.select(this)
                .datum(eval("data." + d.placeName)) // i specifies the location
                .call(chart);
            return "translate(" + d.x + " " + d.y + ")"
    });
}
    
function loadData(year) {
    console.log("loadv  "+year);
    var filename = 'data/chart_by_mapsite_' + year + '.json'
    d3.json(filename, ready);
}
