<template>
  <div :style="{ width: '49.5%', display: 'inline-block' }">

    <h6 v-if="total > 0" class="text-center text-muted pt-0 mb-3">
      {{ title }}<br>({{ total }})
    </h6>
    <h6 v-if="total === 0" class="text-center text-muted pt-1 mb-1">
      no data for<br> {{ title }}
    </h6>

  </div>
</template>

<script>
var d3 = require("d3");

export default {
  props: {
    title: String,
    graphData: Array,
    radius: { type: Number, default: 60 },
    padding: { type: Number, default: 1 },
    regions: Array,
  },
  mounted: function() {
    if (this.graphData !== undefined && this.total > 0) {
      InitChart(this); // Only init if we have some info
    }
  },
  computed: {
    total: function() {
      var total = 0;
      for (var i = 0; i < this.graphData.length; i++) {
        total += this.graphData[i].count;
      }
      return total
    }
  },
  methods: {
    colorclass: function(label) {
      if (this.regions == null) {
        return "gender-display gender-" + label.toLowerCase();
      } else {
        return "region-display region-" + label;
      }
    },
    nicelabel: function (label) {
      if (label == "Male") {
        return "Male identifying";
      } else if (label == "NM") {
        return "Non-cis male identifying";
      } else if (label == "Unknown") {
        return "Unspecified";
      } else {
        return this.regions[label -1].name;
      }
    },
    percentage: function(quantity) {
      return " (" + Math.round(quantity / this.total * 100) + "%)";
    }
  }
}


function InitChart(vueContext){

  // Female - Male - Other - Unknown

  var pie = d3.pie()
      .value(function(d) { return d.count; })
      .sort(null);

  var arc = d3.arc()
      .innerRadius(vueContext.radius - (vueContext.radius / 2))
      .outerRadius(vueContext.radius - vueContext.padding * 2);

  var svg = d3.select(vueContext.$el).insert("svg", ":first-child")
      .attr("width", (vueContext.radius * 2) + vueContext.padding + vueContext.padding)
      .attr("height", (vueContext.radius * 2) + vueContext.padding + vueContext.padding)
      .append("g")
      .attr("transform", "translate(" + (vueContext.radius + vueContext.padding) + "," + (vueContext.radius + vueContext.padding) + ")");

  var path = svg.selectAll("path")
      .data(pie(vueContext.graphData.reverse()))
    .enter().append("path")
      .attr("class", function(d, i) { return "hoverable " + vueContext.colorclass(vueContext.graphData[i].label); })
      .attr("d", arc)

  var tooltip = d3.select("body").append("div")
    .attr("class", "d3-tooltip tooltip")
    .style("opacity", 0);

  path.on('mouseover', function(d, i) {
    tooltip.html("<div class='tooltip-inner'>" +
      vueContext.graphData[i].count + " " +
      vueContext.percentage(vueContext.graphData[i].count) +
      "<br>" +
      vueContext.nicelabel(vueContext.graphData[i].label) +
      "</div>")
      .style("left", (d3.event.pageX) + "px")
      .style("top", (d3.event.pageY - 28) + "px")
      .style('opacity', 1)
    d3.select(this).style('opacity', 0.5);
  });

  path.on('mouseout', function(d) {
    tooltip.style('opacity', 0)
    d3.select(this).style('opacity', 1);
  });
}
</script>
