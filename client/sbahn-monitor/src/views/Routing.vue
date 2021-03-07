<template>

<div>
  <multiselect v-model="station1" :options="staionsList" placeholder="From..." label="station_name" track-by="station_name"> width='75%'</multiselect>
  <multiselect v-model="station2" :options="staionsList" placeholder="To..." label="station_name" track-by="station_name"></multiselect>

  <div v-if="tableArray[0]"  class="text-center text-danger my-2">
    <b-table :items="js" :fields="fields" striped responsive="sm" :tbody-transition-props="transProps">
      <template #cell(show_details)="row">
        <b-button size="sm" @click="row.toggleDetails" class="mr-2">
          {{ row.detailsShowing ? 'Hide' : 'Show'}} Details
        </b-button>
      </template>

      <template #row-details="row">
        <b-card>

          <b-row class="mb-2">
            <b-col sm="3" class="text-sm-right"><b>Arrival: </b></b-col>
            <b-col>{{ row.item.arrival }}</b-col>
          </b-row>

        </b-card>
      </template>
    </b-table>  
  </div>

</div>

</template>


<script>
import axios from "axios";
import Multiselect from 'vue-multiselect';
import { BTable } from 'bootstrap-vue'
// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'
//example stations
var stationIdFrom = 'de%3A09177%3A3270'
var stationIdTo = 'de%3A09162%3A910'

//var query= 'http://167.99.243.10:5000/route/from/de%3A09162%3A1910/to/de%3A09177%3A3280'

var query = 'http://167.99.243.10:5000/route/from/'+stationIdFrom +'/to/' + stationIdTo
var queryStations = 'http://167.99.243.10:5000/stations'


export default{
  components:{
    Multiselect,
    'b-table' : BTable
},
  data () {
    return {
      array: [],
      tableArray: [],
      arrival: [],
      arrivalPlatform: [],
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
      departures: [],
      departurePlatform:[],
      delay:Array(),
      fields: ['Departure Time','departure platform','delay','Change(s)','show_details'],
      tableitems:[]
    
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
        this.js=[]
        this.allroutes=[]
        this.routes=[]
        this.array=[]
        this.tableArray=[]
        this.allroutes=this.info3.data.routes
        this.routes=this.info3.data.routes.filter( x=> (x.connections.every(c=>c.product=="SBAHN")))
      
        var i=0
        while (this.routes[i]) {
          var j = this.routes[i].connections.length

          this.array=[]
          this.array.push(this.routes[i]["departure"])
          this.array.push(this.routes[i].connections[0]["departurePlatform"]) 
          this.array.push(this.routes[i].connections[0]["arrivalPlatform"])  
          this.array.push(this.routes[i].connections[0]["delay"])   

          if ( j <2) {
              this.array.push(this.routes[i].connections[0]["arrival"])
            } else {
              this.array.push(this.routes[i].connections[1]["arrival"])
            }
          this.array.push(j-1)
          this.array.push(this.routes[i].connections[0]["inner_stops"])
          this.tableArray.push(this.array)
      
          
          this.js = this.tableArray.map(function (value,key){
                  return{
                    "Departure Time":value[0].substring(11, 16),
                    "departure platform":value[1],
                    "arrival platform":value[2],
                    "delay":value[3],
                    "arrival":value[4].substring(11, 16),
                    "Change(s)":value[5],
                    "InnerStops":value[6]
                    }
                  })
          
          i = i + 1; }
        

      }


 

      

    }
}


</script>


<style src="bootstrap/dist/css/bootstrap.min.css"> */
 ul{
    overflow: scroll;
    height: 300px;
  }

  li{
    list-style: none;
    list-style-type: none;
  }

  .multiselect {
    width: 50%;
    justify-content: center;
    align-items: center;
    display: inline;
  }

</style>
