'use strict';

var positions = [{"x":150, "y":550},
		 {"x":300, "y":150},
		 {"x":310, "y":250},
		 {"x":310, "y":310},
		 {"x":440, "y":410},
		 {"x":500, "y":450},
		 {"x":500, "y":450},
		 {"x":520, "y":450},
		 {"x":650, "y":490},
		 {"x":700, "y":500},
		 {"x":800, "y":560},
		 {"x":870, "y":580}
		];

//locate main svg element
var svgDoc = d3.select("#chart svg");

function ready (err, data) {

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
		.barColors(['#EEB945', '#E67323'])  // Yellow/orange
		.domain([0,17])
		.tickValues([5,10,15])
		.tickCircleValues([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]);
	    d3.select(this)
		.datum(data)
		.call(chart);
            return "translate(" + d.x + " " + d.y + ")"
	});
}
    
d3.json('data/months.json', ready);

