<template>
<div>
  
  <p> From StationId: {{stationIdFrom}} </p>  
  <p> To StationId: {{stationIdTo}}</p> 

  <p> Average duration for this trip in seconds: {{ info.data.avg_duration }}  </p>
  <p> Average delay in seconds: {{ info.data.avg_delay }}  </p>
  <p> Percentage delayed: {{ info.data.percen_delayed }}  </p>

</div>

</template>

<script>
import axios from "axios";

var stationIdFrom = 'de%3A09188%3A5410'
var stationIdTo = 'de%3A09188%3A5400'
var query = 'http://167.99.243.10:5000/stats/delay/S8/'+'de%3A09188%3A5410' +'/'+'de%3A09188%3A5400';


export default{

  data () {
    return {
      info: null,
      stationIdFrom: stationIdFrom,
      stationIdTo: stationIdTo
    }
  },
  mounted () {
    axios
      .get(query)
      .then(response => (this.info = response))
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