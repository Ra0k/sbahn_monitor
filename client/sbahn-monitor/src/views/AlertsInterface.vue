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
            stationsData: [],
            selectedStation: '',
            claims: [],
            claimsData: [],
            claimsMap: [],
            selectedClaim: '',
            disableButton: true

        }
    },
    mounted() {
        axios.get('http://167.99.243.10:5000/claims')
            .then(response => (this.claimsData = response.data))

        this.claims = this.claimsData.map(function(a) { return a.text})
        this.claimsMap = this.claimsToMap(this.claimsData)

        axios.get('http://167.99.243.10:5000/stations')
            .then(response => (this.stationsData = response.data))
        
        this.stationsList =  this.stationsData.map(function(a) { return a.station_name})
        this.stationsMap = this.stationsToMap(this.stationsData)

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
            for (index in r){
                this.claimsMap[r[index]['text']]= r[index]['id']
            }
            this.claimsToMap = r 
        },
        stationsToMap: function(r) {
            for (index in r){
                this.stationsMap[r[index]['station_name']] = r[index]['station_id']
            } 
        },
        submitClaim: function(event) {
            var stationId = this.stationsMap[this.selectedStation]
            var claimId = this.claimsMap[this.selectedClaim]
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
