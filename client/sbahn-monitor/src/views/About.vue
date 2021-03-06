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