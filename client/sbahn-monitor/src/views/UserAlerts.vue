<template>
    <div>
        <b-card title="Select a station for more detailed information or to submit a report">
            <multiselect v-model="selectedStation" :options="stations" placeholder="Select station" :allow-empty="true"/>
            <multiselect v-model="selectedClaim" :options="claims" placeholder="Select issue" :allow-empty="true"/>
            <form>
                <b-button :disabled="stationAndClaimFilled" v-on:click="submitClaim">Submit </b-button>
            </form>
            <b-card :style="{display: (selectedStation != '' && selectedStation != null) ? 'contents' : 'none'}" :title='selectStationTitle'>
                <div :style="{display: noIssues ? 'contents' : 'none'}">
                    <b-button variant='success'>No Issues Reported</b-button>
                </div>
                <div :style="{display: someIssues ? 'contents' : 'none'}" >
                    <b-button variant='danger'>Warning! Issues Reported</b-button>
                </div>
                <b-table :items="selectedStationReports" :fields="stationFields" visiblity:inherit>
                </b-table>
            </b-card>
        </b-card>
        <b-card title='Recently Reported Issues:'>
            <b-table hover striped :items="visibleReports" :fields="generalReportsFields">
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
            <b-button v-on:click="incrementVisibleReports" :disabled="disableShowMore">Show More</b-button>
        </b-card>
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
            nGeneralReports: 5,
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
            ],
            nSubmissions: 0
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

        const resp = await axios.get('http://167.99.243.10:5000/reports')
        var grdata = resp.data
        for (var key in grdata){
            var tmp = grdata[key]
            tmp['period'] = tmp['period'].substring(11, 16)
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
        selectStationTitle(){
            return 'Reported Issues at: '+this.selectedStation+' (in last hour)'
        },
        visibleReports(){
            if (this.generalReports == null){
                return []
            }else{
                return this.generalReports.slice(0, this.nGeneralReports)
            }
        },
        disableShowMore(){
            if (this.generalReports == null){
                return true
            }else{
                this.nGeneralReports == this.generalReports.length
            }
        },
        noIssues(){
            var nIssues = 0
            for (var cat in this.selectedStationReports) {
                nIssues += this.selectedStationReports[cat].report_num
            }
            if (this.selectedStation != '' && this.selectedStation != null && nIssues == 0){
                console.log('true')
                return true
            }else{
                return false
            }
        },
        someIssues(){
            var nIssues = 0
            for (var cat in this.selectedStationReports) {
                nIssues += this.selectedStationReports[cat].report_num
            }
            if (this.selectedStation != '' && this.selectedStation != null && nIssues > 0){
                console.log('true')
                return true
            }else{
                return false
            }
        }
    },
    watch: {
        nSubmissions: async function () {
            const resp = await axios.get('http://167.99.243.10:5000/reports')
            var grdata = resp.data
            this.generalReports = []
            for (var key in grdata){
                this.generalReports.push(grdata[key])
            }
        }
    },
    asyncComputed: {
        selectedStationReports: async function(){
            if (this.selectedStation != '' && this.selectedStation != null && this.nSubmissions >= 0){
                var stationId = encodeURIComponent(this.selectedStationId)
                console.log('http://167.99.243.10:5000/reports/station/'+stationId)
                var resp = await axios.get('http://167.99.243.10:5000/reports/station/'+stationId)
                var stationReports = resp.data
                var latestReports = stationReports[Object.keys(stationReports)[0]]      
            }else{
                var latestReports = []
            }
            return latestReports
        },

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
            this.nSubmissions += 1
        },
        incrementVisibleReports: function(){
            var n = this.generalReports.length          
            this.nGeneralReports = Math.min(this.nGeneralReports + 5, n)
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
