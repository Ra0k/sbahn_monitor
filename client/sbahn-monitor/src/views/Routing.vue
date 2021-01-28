<template>

<div>

  <multiselect v-model="value" :options="stationsList" placeholder="From..."></multiselect>
  <multiselect v-model="value" :options="options" placeholder="To..."></multiselect>


  <p> {{ options }}  </p>

  <p> {{ stationsList }}  </p>


  <p> From StationId: {{stationIdFrom}} </p>  
  <p> To StationId: {{stationIdTo}}</p> 


  <p> {{ info2.data }}  </p>
  <p> {{ info.data }}  </p>
  

</div>
</template>

<script>
import axios from "axios";
import Multiselect from 'vue-multiselect';

var stationIdFrom = 'de%3A09188%3A5410'
var stationIdTo = 'de%3A09188%3A5400'

var query = 'http://167.99.243.10:5000/route/from/'+stationIdFrom +'/to/' + stationIdTo
var queryStations = 'http://167.99.243.10:5000/stations'


export default{
  components:{Multiselect,
},
  data () {
    return {
      value: null,
      info: null,
      info2: null,
      stationIdFrom: stationIdFrom,
      stationIdTo: stationIdTo,
      options: ['list', 'of', 'options'],
      stations: null,
      staionsList: []
    }
  },
  mounted () {
    axios.get(query)
      .then(response => (this.info2 = response))

    axios.get(queryStations)
      .then(response => (this.info = response))
 
  },

  created() {
    axios.get(queryStations, {})
      .then((response) => { this.stationsList = response.data.map(x => x.station_name) })
  }
}
</script>


<style>
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