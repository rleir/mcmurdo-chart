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
// var formButton = d3.select("#a-button").onclick( function(d){
// d3.event.preventDefault();}); this would replace the following 3 lines

document.getElementById("a-button").addEventListener("click", function(event){
    event.preventDefault()
});

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

    // update the selector
    var e = document.getElementById('year-select');
    if(e) e.value = year;
    
//    formSelect.value = year;
//    .property('checked', false)
    loadData(year);
});

formSelect.on("change", function() {
    var year = this.value;
//    formSelect.value = year;
    loadData(year);
});

// the initial load
loadData(formSelect.node().value);

//locate main svg element
var svgDoc = d3.select("#chart svg");

function ready (err, data) {
    // create initial radial-barcharts
    svgDoc
        .selectAll("g")
        .data(positions)
        .enter()
        .append("g")
        .classed('radial-parent', true) // 1
        .attr("transform",function(d,i){
            var chart = radialBarChart()
                .barHeight(60)
                .reverseLayerOrder(true)
                .barColors([
                    '#EEB945', // Capi  /Yellow
                    '#E67323', // Aphe  /orange
                    '#B66199', // Gala  /mauve
                    '#9392CB', // Spio  /purple
                    '#76D9FA', // Noto  /blue
                    '#ce4b46', // Ophr  /ochre
                    '#aa79c1', // Phil  /purple
                    '#9ab661'  // Edwa  /green
                ])  
                .domain([0,30])
                .tickValues([5,10,15,20,25])
                .tickCircleValues([1,2,3,4,5,6,7,8,9,10]);
            positions[i].chart = chart;
            d3.select(this)
                .datum(eval("data." + d.placeName))
                .call(chart);
            return "translate(" + d.x + " " + d.y + ")"
        });

    // update existing radial-barcharts
    // zzzz first time, this is overwriting
    svgDoc
        .selectAll("g.radial-parent")
        .data(positions)
        .each(function(p, i) {
            d3.select(this)
                .datum(eval("data." + p.placeName)) 
                .call(p.chart);
        });
}
    
function loadData(year) {
    var filename = 'data/chart_by_mapsite_' + year + '.json'
    d3.json(filename, ready);
}
