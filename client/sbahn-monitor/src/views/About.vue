<template>
  <div class="container">
  <!--
  <nav>
    <Dropdown title="Lines" :items="lines" />
    <Dropdown title="Stations" :items="stations_drop" />
    <Dropdown title="Time period" :items="times" />

    
      <Dropdown title="Stations" :items="stations" />
      </nav>
    <h2>{{current.title}}</h2>
    <div class="row mt-5" v-if="this.all.length > 0">
      <div class="col">
        <h2 class="text">Number of all trains hourly - Daglfing as default</h2>

      </div>
    </div>
-->
  
    <apexchart width="380" type="donut" :options="options" :series="series"></apexchart>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import Dropdown from '../components/Dropdown';
import VueApexCharts from 'vue-apexcharts'

export default {
  name: "General",
  components: {
    Dropdown, 
    VueApexCharts


  },

  data: function() {
    return {
      options: {},
      series: [44, 55, 41, 17, 15]
    }
  },

 /*
  
  data() {
    return {
      all: [],
      ndelayed: [],
      ndelayedChartColors: {
        borderColor: "#077187",
        pointBorderColor: "#0E1428",
        pointBackgroundColor: "#AFD6AC",
        backgroundColor: "#74A57F"
      },
      allColors: {
        borderColor: "#190B28",
        pointBorderColor: "#190B28",
        pointBackgroundColor: "#E55381",
        backgroundColor: "#E55381"
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
        xAxes: [{
          stacked: true,
        }],
        yAxes: [{
          stacked: true,
        }]
        },
        legend: {
        display: false,
        },
      },
      pdelayed: [],
      avg_delay: [],
      max_delay: [], 
      hour_data: [], 
      lines: [
        {
          title: 'S8',
          link: '#'
        }
      ],
      stations: [],
      // stations: ["Herrsching", "Steinebach", "Neugilching", 
      //           "Geisenbrunn", "Harthaus", "Neuaubing", 
      //           "Pasing", "Hirschgarten", "Hackerbrücke", 
      //           "Karlsplatz", "Isartor", "Ostbahnhof München", 
      //           "Daglfing", "Johanneskirchen", "Ismaning", "Flughafen Besucherpark" ], 
      stations_drop: [
        // {
        //   title: 'Herrsching',
        //   link: '#'
        // }, 
        // {
        //   title: 'Steinebach',
        //   link: '#'
        // }, 
        // {
        //   title: 'Daglfing',
        //   link: '#'
        // }, 
      ],
      times:[
        {
          title: 'hour',
          link: '#'
        }, 
        {
          title: 'week',
          link: '#'
        }, 
        {
          title: 'month',
          link: '#'
        }
      ],
      current: {
        title:"", 
        time_period:""
        }
    };
    watch: {

    }
  },

  async created() {
    const { data } = await axios.get(
      "http://127.0.0.1:8000/line/S8/stations"
    );

    var i = 0;
    while (data[data["name"]][i]) {
      this.stations_drop.push({title:data[data["name"]][i]["station_name"], link:"/general"});      
      i = i + 1;
    }

    // if(this.current.title != "" & this.current.time_period != ""){
    // const { data } = await axios.get(
    //   "http://127.0.0.1:8000/stats/delay/stations/current_week/grouped/hourly"
    // );
    // }


    // while(this.current.title == ""){
      
    // }
    // while(this.current.time_period == ""){}

    // this.current.time_period = "hourly"
    // this.current.title = "Daglfing"
    // var i = 0;
    // while (data[i]) {
    //   var j = 0;
    //   while (data[i][j]){
    //     if(data[i][j]["station_name"] == "Daglfing"){
    //       this.all.push({i, total:data[i][j]["#all"]});
    //       this.ndelayed.push({i, total:data[i][j]["#delayed"]});
    //       this.pdelayed.push({i, total:data[i][j]["%delayed"]});
    //       this.avg_delay.push({i, total:data[i][j]["avg_delay"]});
    //       this.max_delay.push({i, total:data[i][j]["max_delay"]});
    //       }
    //     j = j + 1;
    //   }
    //   i = i + 1;
    // }

    // this.hour_data = {
    //   labels: [ "Delayed", "All" ], 
    //   backgroundColors: ["#E55381", "#74A57F"],
    //   borderColors: ["#190B28", "#077187"],
    //   pointBorderColors:["#190B28", "#0E1428"],
    //   pointBackgroundColors:["#E55381", "#AFD6AC"],
    //   i:      this.all.map(d => d.i), 
    //   total:[ this.ndelayed.map(d => d.total), 
    //           this.all.map(d => d.total), 
    //           this.pdelayed.map(d => d.total), 
    //           this.avg_delay.map(d => d.total), 
    //           this.max_delay.map(d => d.total) ]
    //           };

    console.log(data);
    // console.log(this.max_delay);
    // console.log(this.avg_delay);
    // console.log(data);
  }
  
  */


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
nav {
  display: flex;
  align-items: center;
  justify-content: center;
}
nav .menu-item {
  color: #FFF;
  padding: 10px 20px;
  position: relative;
  text-align: center;
  border-bottom: 3px solid transparent;
  display: flex;
  transition: 0.4s;
}
nav .menu-item.active,
nav .menu-item:hover {
  background-color: #444;
  border-bottom-color: #FF5858;
}
nav .menu-item a {
  color: inherit;
  text-decoration: none;
}
</style>