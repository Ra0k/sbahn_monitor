<template>
<!-- comment 
 -->
<div>
  <multiselect v-model="station1" :options="staionsList" placeholder="From..." label="station_name" track-by="station_name"></multiselect>
  <multiselect v-model="station2" :options="staionsList" placeholder="To..." label="station_name" track-by="station_name"></multiselect>
  
  
<!-- comment

<br>  <br>
<p>{{stats.data}}</p>
all routes:
<p>{{allroutes}}</p>
<br> <br>
routes containing only sbahns:
<br> <br>
<p>{{routes}}</p>
-->

<br> <br>

Connections:

 <li v-for="route in routes" :key="connections"> 
    {{ route.connections }}
  </li>


</div>
</template>


<script>
import axios from "axios";
import Multiselect from 'vue-multiselect';

//example stations
var stationIdFrom = 'de%3A09177%3A3270'
var stationIdTo = 'de%3A09162%3A910'

//var query= 'http://167.99.243.10:5000/route/from/de%3A09162%3A1910/to/de%3A09177%3A3280'

var query = 'http://167.99.243.10:5000/route/from/'+stationIdFrom +'/to/' + stationIdTo
var queryStations = 'http://167.99.243.10:5000/stations'


export default{
  components:{
    Multiselect,
},
  data () {
    return {
      query : query,
      queryStats:'empty queryStats',
      queryStart:'',
      station1: '',
      station2: '',
      info: null,
      info2: null,
      info3: null,
      stationIdFrom: stationIdFrom,
      stationIdTo: stationIdTo,
      stations: null,
      staionsList: [],
      stats: [],
      allroutes:[],
      routes:[],
      queryComplete: "",
      id: 0,
    }
  },


  mounted () {
  
    axios.get('http://167.99.243.10:5000/route/from/'+ stationIdFrom +'/to/' + stationIdTo)
      .then(response => (this.info2 = response))
    axios.get(queryStations)
      .then(response => (this.staionsList = response.data))
    axios.get(this.queryComplete)
      .then(response => (this.info3 = response))  
   // axios.get(queryStats)
   //  .then(response => (this.stats = response.data))
  },

  created() {
    // axios.get(queryStations, {})
    //   .then((response) => { this.stationsList = response.data.map(x => x.station_name) })
  
  },

  methods: {
    get: function(url) {alert(url)}

  },

  watch: {

       station1: function() {
         if (this.station1['station_id'] != null & this.station2['station_id'] != null) {
           this.queryComplete = 'http://167.99.243.10:5000/route/from/' + encodeURIComponent(this.station1['station_id']) + '/to/' + encodeURIComponent(this.station2['station_id'])
         }
        this.queryStats = 'http://167.99.243.10:5000/stats/delay/station/' + encodeURIComponent(this.station1['station_id']) + "/current_week/grouped/weekly"
       },
      
       station2: function() {
         if (this.station1['station_id'] != null & this.station2['station_id'] != null) {
           this.queryComplete = 'http://167.99.243.10:5000/route/from/' + encodeURIComponent(this.station1['station_id']) + '/to/' +encodeURIComponent(this.station2['station_id'])
         }
      },
      queryComplete: function() {
         axios.get(this.queryComplete).then(response => (this.info3 = response)) 

       },
       queryStats: function() {
         axios.get(this.queryStats).then(response => (this.stats = response))
      
      },
      
      info3: function(){
        this.allroutes=this.info3.data.routes
        this.routes=this.info3.data.routes.filter( x=> (x.connections.every(c=>c.product=="SBAHN")))
      }
}
}

/* 
.filter( (x)=> {return x.connections[product = "SBAHN"];  })
*/

</script>


<style src="vue-multiselect/dist/vue-multiselect.min.css">
   ul{
    overflow: scroll;
    height: 300px;
  }

  li{
    list-style: none;
    list-style-type: none;
  } 
</style>
