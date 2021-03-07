<template>
    <div>
        <multiselect v-model="selectedStation" :options="stations" placeholder="Select station" :allow-empty="true"/>
        <multiselect v-model="selectedClaim" :options="claims" placeholder="Select issue" :allow-empty="true"/>
        <form>
            <button :disabled="stationAndClaimFilled" v-on:click="submitClaim">Submit </button>
        </form>
        <b-card :style="{display: (selectedStation != '' && selectedStation != null) ? 'contents' : 'none'}">
                <b-table :items="selectedStationReports" :fields="stationFields" visiblity:inherit>
                </b-table>
        </b-card>
        <!-- <b-table hover striped :items="generalReports" :fields="generalReportsFields" :style="{visibility: selectedStation == '' ? 'visible' : 'hidden'}"> -->
        <b-table hover striped :items="generalReports" :fields="generalReportsFields">
            <template #cell(show_details)="row">
                <b-button size="sm" @click="row.toggleDetails" class="mr-2" :disabled="row.item['#reports'] == 0">
                {{ row.detailsShowing ? 'Hide' : 'Show'}} Details
                </b-button>
            </template>

            <template #row-details="row">
                <b-card>
                    <b-table :items="row.item.stations" :fields="generalReportsFieldsDetails">
                    </b-table>
                    <!-- <b-button size="sm" @click="row.toggleDetails">Hide Details</b-button> -->
                </b-card>
            </template>
        </b-table>
    </div>
</template>

<script>
import axios from "axios";
import Multiselect from 'vue-multiselect';
import { BTable, BButton, BCard } from 'bootstrap-vue'

export default{
    name: "AlertsInterface",
    components:{
        Multiselect,
        'b-table' : BTable,
        'b-button' : BButton,
        'b-card': BCard
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
            generalReportsFields: [
                {key: 'period', label: 'Timestamp'}, 
                {key: '#reports', label: 'Number of Reported Issues'}, 
                {key: 'show_details', label: ''}
            ],
            generalReportsFieldsDetails: [
                {key: 'station_name', label: 'Station'}, 
                {key: 'report_num', label: 'Number of Reported Issues'}
            ],
            stationReports: [],
            stationFields: [
                {key: 'claim_text', label: 'Issue'},
                {key: 'report_num', label: 'Number of Reported Issues'}
            ]

        }
    },
    async created() {
        const claimsResponse = await axios.get('http://167.99.243.10:5000/claims')
        this.claimsData = claimsResponse.data
        this.claims = this.claimsData.map(function(a) { return a.text})

        var cdata = this.claimsData
        for (var index in cdata){
            this.claimsMap[cdata[index]['text']]= cdata[index]['claim_id']
        }

        const stationsResponse = await axios.get('http://167.99.243.10:5000/stations')
        this.stationsData = stationsResponse.data
        this.stations = this.stationsData.map(function (a) {return a.station_name})
        
        var sdata = this.stationsData
        for (var sindex in sdata){
            this.stationsMap[sdata[sindex]['station_name']] = sdata[sindex]['station_id']
        }

        const generalReports = await axios.get('http://167.99.243.10:5000/reports')
        var grdata = generalReports.data
        for (var key in grdata){
            this.generalReports.push(grdata[key])
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
        },
    },
    asyncComputed: {
        selectedStationReports: async function(){
            if (this.selectedStation != '' && this.selectedStation != null){
                var stationId = encodeURIComponent(this.selectedStationId)
                console.log('http://167.99.243.10:5000/reports/station/'+stationId)
                var resp = await axios.get('http://167.99.243.10:5000/reports/station/'+stationId)
                var stationReports = resp.data
                var latestReports = stationReports[Object.keys(stationReports)[0]]      
            }else{
                var latestReports = []
            }
            return latestReports
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
