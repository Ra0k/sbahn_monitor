<template>
    <div>
        <multiselect v-model="selectedStation" :options="stationsList" placeholder="Station"/>
        <multiselect v-model="selectedClaim" :options="claims" placeholder="Claim"/>
        <form>
            <button :disabled="stationAndClaimFilled" v-on:click="submitClaim">Submit </button>
        </form>
        <p>
            {{this.claimsMap}}
        </p>
    </div>
</template>

<script>
import axios from "axios";
import Multiselect from 'vue-multiselect';


export default{
    components:{
        Multiselect,
    },
    data() {
        return {
            stationsList: [],
            stationsMap: [],
            selectedStation: '',
            claims: [],
            claimsMap: [],
            selectedClaim: '',
            disableButton: true

        }
    },
    mounted() {
        axios.get('http://167.99.243.10:5000/claims')
            .then(response => (this.claims =  response.data.map(function(a) { return a.text}) ))
            .then(response => (this.claimsToMap(response.data)))
        axios.get('http://167.99.243.10:5000/stations')
            .then(response => (this.stationsList =  response.data.map(function(a) { return a.station_name}) ))
            .then(response => (stationsToMap(response.data)))
    },
    created(){

    },
    // computed values which will be automatically recalculated on updates
    computed: {
        stationAndClaimFilled() {
            if (this.selectedStation != '' && this.selectedClaim != ''){
                return false
            }else{
                return true
            }
        }
    },
    //methods which can be used in things like event handlers
    methods: {
        claimsToMap: function(r) {
            for (claim in r){
                this.claimsMap.set(claim.text, claim.id)
            } 
        },
        stationsToMap: function(r) {
            for (station in r){
                this.stationsMap.set(station.station_name, station.station_id)
            } 
        },
        submitClaim: function(event) {
            var stationId = this.stationsMap.get(this.selectedStation)
            var claimId = this.claimsMap.get(this.selectedClaim)
            axios.post('http://167.99.243.10:5000/reports/station/'+stationId+'/'+claimId)
        }
    }
}
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
