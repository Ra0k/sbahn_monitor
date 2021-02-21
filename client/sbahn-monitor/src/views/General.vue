<template>

  <div>
      <apexchart width="500" type="bar" :options="options" :series="series"></apexchart>
      <apexchart width="500" type="line" :options="options" :series="series"></apexchart>

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
      all: [],
      ndelayed: [],
      pdelayed: [],
      avg_delay: [],
      max_delay: [], 
      hour_data: [],
      options: {
        chart: {
          id: 'vuechart-example'
        },
        xaxis: {
          categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
        }
      },
      series: [{
        name: 'series-1',
        data: [30, 40, 45, 50, 49, 60, 70, 91]
      }]
    }
  },

  async created() {
    const { data } = await axios.get(
      "http://127.0.0.1:8000/stats/delay/all/current_week/grouped/hourly"
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



    console.log(data);
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
