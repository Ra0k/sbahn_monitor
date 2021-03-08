<template>

  <div>
      <!-- <apexchart width="500" type="bar" :options="options_bar" :series="series_bar"></apexchart> -->
      <multiselect v-model="line" :options="linesList" placeholder="Pick a line..." label="line_name" track-by="line_name"></multiselect>
      <!-- <multiselect v-model="station2" :options="staionsList" placeholder="Pick a station..." label="station_name" track-by="station_name"></multiselect> -->

      <apexchart width="500" type="line" :options="options_line" :series="series_line"></apexchart>
      <apexchart type="heatmap" height="350" :options="chartOptions" :series="series"></apexchart>
  </div>
   
</template>

<script>
import axios from "axios";
import Navbar from '../components/Navbar';
import VueApexCharts from 'vue-apexcharts'


export default {
  name: "General",
  components: {
    Navbar,
    VueApexCharts

  },
  

  data: function() {
    return {
      line: null,
      all: [],
      ndelayed: [],
      pdelayed: [],
      avg_delay: [],
      max_delay: [], 
      hour_data: [],
      options_line: null,
      series_line: null,
      options_bar: null,
      series_bar: null,
      chartOptions: {
        dataLabels: {
          enabled: false
        },
        colors: ["#008FFB"],
        xaxis: {
          type: 'category',
        },
        title: {
          text: 'HeatMap Chart (Single color)'
        },
      },
      linesList: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S20'],
      series: [{
          name: 'Metric1',
          data: this.generateData(20, {
            min: 0,
            max: 90
          })
        },
        {
          name: 'Metric2',
          data: this.generateData(20, {
            min: 0,
            max: 90
          })
        },
        {
          name: 'Metric3',
          data: this.generateData(20, {
            min: 0,
            max: 90
          })
        },
        {
          name: 'Metric4',
          data: this.generateData(20, {
            min: 0,
            max: 90
          })
        },
        {
          name: 'Metric5',
          data: this.generateData(20, {
            min: 0,
            max: 90
          })
        },
        {
          name: 'Metric6',
          data: this.generateData(20, {
            min: 0,
            max: 90
          })
        },
        {
          name: 'Metric7',
          data: this.generateData(20, {
            min: 0,
            max: 90
          })
        },
        {
          name: 'Metric8',
          data: this.generateData(20, {
            min: 0,
            max: 90
          })
        },
        {
          name: 'Metric9',
          data: this.generateData(20, {
            min: 0,
            max: 90
          })
        }
      ],
    }
  },

  methods: {
    generateData(count, yrange) {
      var i = 0;
      var series = [];
      while (i < count) {
        var x = (i + 1).toString();
        var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
        series.push({
          x: x,
          y: y
        });
        i++;
      }
      return series;
    }
  },

  async created() {
    const { data } = await axios.get(
      "http://167.99.243.10:5000/stats/delay/all/current_week/grouped/hourly"
    );

    var i = 0;
    while (data[i]) {
      this.all.push({i, total:data[i]["#all"]});
      this.ndelayed.push({i, total:data[i]["#delayed"]});
      this.pdelayed.push({i, total:data[i]["%delayed"]});
      this.avg_delay.push({i, total:data[i]["avg_delay"]});
      this.max_delay.push({i, total:data[i]["max_delay"]});
      i = i + 1;
    }


    this.hour_data = {
      labels: [ "Delayed", "All" ], 
      backgroundColors: ["#E55381", "#74A57F"],
      borderColors: ["#190B28", "#077187"],
      pointBorderColors:["#190B28", "#0E1428"],
      pointBackgroundColors:["#E55381", "#AFD6AC"],
      i:      this.all.map(d => d.i), 
      total:[ this.ndelayed.map(d => d.total), 
              this.all.map(d => d.total), 
              this.pdelayed.map(d => d.total), 
              this.avg_delay.map(d => d.total), 
              this.max_delay.map(d => d.total) ]
              };

    this.options_line = {
        chart: {
          id: 'vuechart-example'
        },
        xaxis: {
          categories: this.hour_data.i
        }
      };
    
    this.series_line = [{
        name: 'series-1',
        data: this.hour_data.total[0]
      }]

    
    this.options_bar = {
        chart: {
          id: 'vuechart-example'
        },
        xaxis: {
          categories: this.hour_data.i
        }
      };
    
    this.series_bar = [{
        name: 'series-1',
        data: this.hour_data.total[1]
      }]


    console.log(this.hour_data.total[0]);
  }
}
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Quicksand');

html, body {
  font-family: 'Quicksand', sans-serif;
} 


* {
  box-sizing: border-box;
}
body {
  font-family: 'Quicksand', sans-serif;
}
header {
  font-family: 'Quicksand', sans-serif;
  width: 100vw;
  background-color: rgb(163, 163, 163);
  padding: 15px;
  text-align: center;
}
</style>
