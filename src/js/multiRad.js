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

//locate main svg element
var svgDoc = d3.select("#chart svg");

function ready (err, data) {
//zzz    console.log(data);
    //create basic radbars
    svgDoc
	.append("g").selectAll("g")
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
		.datum(eval("data." + d.name)) // i specifies the location
		.call(chart);
            return "translate(" + d.x + " " + d.y + ")"
	});
}
    
d3.json('data/chart_by_mapsite_2011.json', ready);

