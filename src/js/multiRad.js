'use strict';

var positions = [{"x":150, "y":550, "name": "CinderCones"},
		 {"x":300, "y":150, "name": "WinterQuartersInner"},
		 {"x":310, "y":250, "name": "WinterQuartersMiddle"},
		 {"x":310, "y":310, "name": "WinterQuartersOuter"},
		 {"x":440, "y":410, "name": "Outfall"},
		 {"x":500, "y":450, "name": "OutfallA"},
		 {"x":500, "y":450, "name": "OutfallB"},
		 {"x":520, "y":450, "name": "Transition"},
		 {"x":650, "y":490, "name": "Road"},
		 {"x":700, "y":500, "name": "JettyN"},
		 {"x":800, "y":560, "name": "JettyS"},
		 {"x":870, "y":580, "name": "Armitage"}
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

function ready (err, yearData) {
//zzz    console.log(yearData);
    //create basic radbars
    //	    d3.select(this)
    svgDoc
	.selectAll("g")
	.data(positions)
	.enter()
	.append("g")
	.attr("transform",function(positns,i){
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
		.datum(eval("yearData." + positns.name)) // i specifies the location
		.call(chart);
	    return "translate(" + positns.x + " " + positns.y + ")"
	});
}
    
function loadData(year) {
    console.log("loadv  "+year);
    var filename = 'data/chart_by_mapsite_' + year + '.json'
    d3.json(filename, ready);
}
