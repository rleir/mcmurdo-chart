'use strict';

var positions = [{"x":150, "y":550, "placeName": "CCN"},
                 {"x":300, "y":150, "placeName": "WQBI"},
                 {"x":310, "y":250, "placeName": "WQM"},
                 {"x":310, "y":310, "placeName": "WQBO"},
                 {"x":440, "y":410, "placeName": "Out"},
                 {"x":500, "y":450, "placeName": "OSA"},
                 {"x":520, "y":450, "placeName": "OSB"},
                 {"x":650, "y":490, "placeName": "Trans"},
                 {"x":700, "y":500, "placeName": "Road"},
                 {"x":800, "y":560, "placeName": "JetN"},
                 {"x":870, "y":580, "placeName": "JetS"},
                 {"x":1070,"y":780, "placeName": "CA"}
                ];
var formSelect = d3.select("#year-select");
var formButton = d3.select("#a-button");
// var formButton = d3.select("#a-button").onclick( function(d){
// d3.event.preventDefault();}); this would replace the following 3 lines

document.getElementById("a-button").addEventListener("click", function(event){
    event.preventDefault()
});

var all_years ;
d3.json( "data/allyears.json", function(err, data) {
    all_years = data;
});


formButton.on("click", function() {
    var year = formSelect.node().value;

    //find next in year array
    // note that this algo does not scale
    var x=0;
    var ay_len = all_years.length;
    while ( all_years[x] != year){
        x += 1;
        if(x >= ay_len || x > 100){
            return;
        }
    }
    //when end, restart
    if(x+1 >= ay_len){
        x=0
    } else {
        x=x+1
    }
    year = all_years[x];
    
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
