

        // Width and height
        var w =300;
        var h = w;
        var pad = {left:90, top:40, right:50, bottom:70}
        var innerpad = 5
        
        var totalh = h + pad.top + pad.bottom
        var totalw = w + pad.left + pad.right

         
        var svg = d3.select("#anks")
                    .append("svg:svg")
                    .attr("width", totalw)
                    .attr("height", totalh);

        // Panel for dot plot.
        var dotplot = svg.append("g")
                    .attr("id", "dotplot")
                    .attr("transform", "translate(" + pad.left +  "," + pad.top +  ")")
                    
        // Scales

        var xScale = d3.scale.linear()
            //.domain([d3.min(top_acts, function(d){return d[1];}), d3.max(top_acts, function(d){return d[1];})])
            .domain([3,10])
            .range([20,w-20])
            .clamp(true);

        var yScale = d3.scale.ordinal()
            .domain(top_mols)
            .rangeBands([20,h], .1);

        // Background
        dotplot.append("rect")
             .attr("height", h)
             .attr("width", w)
             .attr("fill", d3.rgb(200, 200, 200))
             .attr("stroke", "black")
             .attr("stroke-width", 1)
             .attr("pointer-events", "none");


        // Axis labels
        dotplot.append("text")
               .attr("id", "xaxis")
               .attr("class", "axes")
               .attr("x", w/2)
               .attr("y", h+pad.bottom*0.7)
               .text("pIC50")
               .attr("dominant-baseline", "middle")
               .attr("text-anchor", "middle")
               .attr("fill", "slateblue");
        dotplot.append("text")
               .attr("id", "yaxis")
               .attr("class", "axes")
               .attr("x", -pad.left*0.8)
               .attr("y", h/2)
               .text("molregno")
               .attr("dominant-baseline", "middle")
               .attr("text-anchor", "middle")
               .attr("transform","rotate(270, " + -pad.left*0.9 + "," + h/2 +")")
               .attr("fill", "slateblue");

        // Axis scales
        var xticks = xScale.ticks(5);
        var yticks = top_mols;

        dotplot.selectAll("empty")
               .data(xticks)
               .enter()
               .append("text")
               .attr("class", "axes")
               .text(function(d){
                            return d3.format(".2f")(d);})
               .attr("x", function(d){
                                 return xScale(d);
                                 })
               .attr("y", h+pad.bottom*0.3)
               .attr("dominant-baseline", "middle")
               .attr("text-anchor", "middle");

        dotplot.selectAll("empty")
               .data(yticks)
               .enter()
               .append("text")
               .attr("class", "axes")
               .text(function(d){
                                return d;
                                })
               .attr("x", -pad.left*0.05)
               .attr("y", function(d){ 
                                    return yScale(d);
                                    })
               .attr("dominant-baseline", "middle")
               .attr("text-anchor", "end");

        dotplot.selectAll("empty")
               .data(xticks)
               .enter()
               .append("line")
               .attr("class", "axes")
               .attr("x1", function(d){
                                    return xScale(d);
                                    })
               .attr("x2", function(d){
                                    return xScale(d);
                                    })
               .attr("y1", 0)
               .attr("y2", h)
               .attr("stroke", "white")
               .attr("stroke-width", 1);

        dotplot.selectAll("empty")
               .data(yticks)
               .enter()
               .append("line")
               .attr("class", "axes")
               .attr("y1", function(d){
                                    return yScale(d);
                                    })
               .attr("y2", function(d){
                                    return yScale(d);
                                    })
               .attr("x1", 0)
               .attr("x2", w)
               .attr("stroke", "white")
               .attr("stroke-width", 1);
        // Add dots.  
        dotplot.selectAll("empty")
                .data(top_acts)
                .enter()
                .append("svg:circle")
                .attr("class", "circle tooltip")
                .attr("title", function(d){ return "<img src='https://www.ebi.ac.uk/chembldb/compound/displayimage_large/"+ d[0] + "' style='height:130px; width:130px;' />" + "<br>" + d[4] + "<br>assay id:"+ "<a href=https://www.ebi.ac.uk/chembldb/assay/inspect/"+ d[5] + ">"+ d[5] + "</a>" + "<br>protein id:"+ "<a href=https://www.ebi.ac.uk/chembldb/target/inspect/"+ d[6] + ">"+ d[6] + "</a>"+ "<br>Compound id:"+ "<a href=https://www.ebi.ac.uk/chembldb/compound/inspect/"+ d[7] + ">"+ d[7] + "</a>";})
                .attr("cy", function(d) {
                            return yScale(d[0])+ Math.floor(Math.random()*13) - 6;
                            })
                .attr("cx", function(d) {
                                return xScale(d[1]);
                                })
                .attr("r", 3)
                .attr("stroke", "black")
                .attr("stroke-width", 1)
                .attr("fill", "red")
                .on("mouseover", function(d){
                   d3.select(this)
                    .attr("stroke", "white")
                    })
                .on("mouseout", function(d){
                    d3.select(this).attr("stroke","black")
                    });
