'use strict';

var formSelect = d3.select("#year-select");
var formButton = d3.select("#a-button");
// var formButton = d3.select("#a-button").onclick( function(d){
// d3.event.preventDefault();}); this would replace the following 3 lines

document.getElementById("a-button").addEventListener("click", function(event){
    event.preventDefault()
});

var positions;

// load some json files, and wait for them to be loaded
queue()
    .defer(d3.json, "data/positions.json")
    .defer(d3.json, "data/allyears.json")
    .await(analyze);

function analyze( error, apositions, all_years) {
    if(error) { console.log(error); }

    positions = apositions;

    // add options to the selector for all years
    var min = 0,
        max = all_years.length - 1,
        select = formSelect.node();

    for (var i = min; i<=max; i++){
        var opt = document.createElement('option');
        var year = all_years[i];
        opt.value = year;
        opt.innerHTML = year;
        select.appendChild(opt);
    }

    formButton.on("click", function() {
        var year = formSelect.node().value;

        //find next in year array
        // note that this algo does not scale
        var x=0,
            ay_len = all_years.length;
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
    
        loadData(year);
    });

    formSelect.on("change", function() {
        var year = this.value;
        loadData(year);
    });

    // the initial load
    loadData(formSelect.node().value);
}
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
                    'rgb(94, 119, 220)', // Capi
                    'rgb(145, 193, 228)', // Aphe
                    'rgb(255, 208, 189)', // Gala
                    'rgb(247, 105, 123)', // Spio
                    'rgb(119, 157, 224)', // Noto
                    'rgb(181, 229, 229)', // Ophr
                    'rgb(255, 158, 155)', // Phil
                    'rgb(207, 73, 105)'  // Edwa
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
