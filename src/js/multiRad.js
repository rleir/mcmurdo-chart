'use strict';

var dataArray1 = [30,35,45,55,70];
var dataArray2 = [50,55,45,35,20,25,25,40];
//globals
var dataIndex=1;
var xBuffer=50;
var yBuffer=150;

//locate main svg element
var svgDoc = d3.select("#chart svg");

function ready (err, data) {

    //create basic radbars
    svgDoc
	.append("g").selectAll("g")
	.data(eval("dataArray"+dataIndex))
	.enter()
	.append("g")
	.attr("transform",function(d,i){
	    var chart = radialBarChart()
		.barHeight(110)
		.translt( {top: 20, right: 20, bottom: 20, left: 60})
		.reverseLayerOrder(true)
		.barColors(['#EEB945', '#E67323'])  // Yellow/orange
		.domain([0,17])
		.tickValues([5,10,15])
		.tickCircleValues([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]);
	    d3.select(this)
		.datum(data)
		.call(chart);
            var spacing = 400/(eval("dataArray"+dataIndex).length);
	    var trsx = xBuffer+(i*spacing);
            return "translate(" + trsx + " 150)"
	});
}
    
d3.json('data/months.json', ready);

