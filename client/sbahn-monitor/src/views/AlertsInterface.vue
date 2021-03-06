<template>
    <div>
        <multiselect v-model="selectedStation" :options="stations" placeholder="Station"/>
        <multiselect v-model="selectedClaim" :options="claims" placeholder="Claim"/>
        <form>
            <button :disabled="stationAndClaimFilled" v-on:click="submitClaim">Submit </button>
        </form>
        <p>
        </p>
    </div>
</template>

<script>
import axios from "axios";
import Multiselect from 'vue-multiselect';


export default{
    name: "AlertsInterface",
    components:{
        Multiselect,
    },
    data() {
        return {
            stations: [],
            stationsMap: [],
            stationsData: [],
            selectedStation: '',
            claims: [],
            claimsData: [],
            claimsMap: [],
            selectedClaim: '',
            disableButton: true,

        }
    },
    async created() {
        const claimsResponse = await axios.get('http://167.99.243.10:5000/claims')
        this.claimsData = claimsResponse.data
        this.claims = this.claimsData.map(function(a) { return a.text})

        var cdata = this.claimsData
        var index 
        for (index in cdata){
            this.claimsMap[cdata[index]['text']]= cdata[index]['id']
        }

        const stationsResponse = await axios.get('http://167.99.243.10:5000/stations')
        this.stationsData = stationsResponse.data
        this.stations = this.stationsData.map(function (a) {return a.station_name})
        
        var sdata = this.stationsData
        for (index in sdata){
            this.stationsMap[sdata[index]['station_name']] = sdata[index]['station_id']
        }

    },
    // computed values which will be automatically recalculated on updates
    computed: {
        stationAndClaimFilled: function() {
            if (this.selectedStation != '' && this.selectedClaim != ''){
                return false
            }else{
                return true
            }
        },
        selectedStationId: function(){
            return this.stationsMap[this.selectedStation]
        },
        selectedClaimId: function() {
            return this.claimsMap[this.selectedClaim]
        }

    },
    //methods which can be used in things like event handlers
    methods: {
        submitClaim: function(event) {
            var stationId = this.selectedStationId
            var claimId = this.selectedClaimId
            console.log(this.selectedStationId, claimId)
            //var claimId = this.genClaimsMap()[this.selectedClaim]
            //console.log(this.selectedStation, this.selectedClaim)
            //console.log(this.stationsMap, this.claimsMap)
            //console.log('http://167.99.243.10:5000/reports/station/'+stationId+'/'+claimId)
            //axios.post('http://167.99.243.10:5000/reports/station/'+stationId+'/'+claimId)
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
