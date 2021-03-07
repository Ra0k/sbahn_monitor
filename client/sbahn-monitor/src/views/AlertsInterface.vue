<template>
    <div>
        <multiselect v-model="selectedStation" :options="stations" placeholder="Station"/>
        <multiselect v-model="selectedClaim" :options="claims" placeholder="Claim"/>
        <form>
            <button :disabled="stationAndClaimFilled" v-on:click="submitClaim">Submit </button>
        </form>
        <b-table hover :items="generalReports" ></b-table>
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
            generalReports: [],
            stationReports: []

        }
    },
    async created() {
        const claimsResponse = await axios.get('http://167.99.243.10:5000/claims')
        this.claimsData = claimsResponse.data
        this.claims = this.claimsData.map(function(a) { return a.text})

        var cdata = this.claimsData
        var index 
        for (index in cdata){
            this.claimsMap[cdata[index]['text']]= cdata[index]['claim_id']
        }

        const stationsResponse = await axios.get('http://167.99.243.10:5000/stations')
        this.stationsData = stationsResponse.data
        this.stations = this.stationsData.map(function (a) {return a.station_name})
        
        var sdata = this.stationsData
        var sindex
        for (sindex in sdata){
            this.stationsMap[sdata[sindex]['station_name']] = sdata[sindex]['station_id']
        }

        const generalReports = await axios.get('http://167.99.243.10:5000/reports')
        this.generalReports = generalReports.data
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
        submitClaim: async function(event) {
            var stationId = encodeURIComponent(this.selectedStationId)
            var claimId = encodeURIComponent(this.selectedClaimId)
            console.log('http://167.99.243.10:5000/reports/station/'+stationId+'/'+claimId)
            var resp = await axios.post('http://167.99.243.10:5000/reports/station/'+stationId+'/'+claimId)
            if (resp.status == 200) {
                alert('Successfully submitted claim')
            }else{
                alert('Please try again')
            }
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
