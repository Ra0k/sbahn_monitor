<template>
   <div>

    <div class="card">
			<div class="card-header">Pick a line and station to see specific statistics</div>
			<div class="card-body">
				<multiselect v-model="line" :options="linesList" placeholder="Pick a line..." ></multiselect>
        <multiselect v-model="station" :options="stationsList" placeholder="Pick a station..." label="station_name" track-by="station_name"></multiselect>
      </div>
		</div>
      <div class="row">
         <div class="col-sm-6">
            <div class="card">
               <div class="card-header">Trains delayed by hour</div>
               <div class="card-body">
                  <apexchart type="bar" :options="options_line" :series="series_line"></apexchart>
               </div>
            </div>
         </div>
         <div class="col-sm-6">
            <div class="card">
               <div class="card-header">Percentage of trains delayed for line {{this.line}} over last week</div>
               <div class="card-body">
                  <apexchart type="heatmap" height="350" :options="chartOptions" :series="seriesHeatMap"></apexchart>
               </div>
            </div>
         </div>
<!--          <div class="col-sm-6">
            <div class="card text-white bg-warning mb-3" style="max-width: 18rem;">
               <div class="card-header">Real-time delay on {{this.station["station_name"]}}</div>
               <div class="card-body">
                  <h5 class="card-title">Warning card title</h5>
                  <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
               </div>
            </div>
         </div> -->
      </div>
      <!-- <apexchart type="heatmap" h
         eight="350" :options="chartOptions" :series="series"></apexchart> -->
   </div>
</template>

<script>
import axios from "axios";
import Navbar from '../components/Navbar';
import VueApexCharts from 'vue-apexcharts'
import Multiselect from 'vue-multiselect';
import VueSpeedometer from "vue-speedometer";
var moment = require('moment');

export default {
    name: "General",
    components: {
        Navbar,
        VueApexCharts,
        Multiselect,
        VueSpeedometer
    },

    data: function() {
        return {
            line: '[Choose the line!]',
            station: '',
            queryGetStations: '',
            all: [],
            ndelayed: [],
            pdelayed: [],
            avg_delay: [],
            max_delay: [],
            hour_data: [],
            options_line: null,
            series_line: null,
            options_bar: null,
            series_bar: null,
            chartOptions: {
                dataLabels: {
                    enabled: false
                },
                colors: ["#fb3b00"],
                xaxis: {
                    type: 'category',
                },
            },
            linesList: ['S1', 'S2', 'S3', 'S4', 'S6', 'S7', 'S8', 'S20'],
            stationsList: [],
            seriesHeatMap: []
  
        }
    },

    methods: {
        generateData(count, yrange) {
            var i = 0;
            var series = [];
            while (i < count) {
                var x = (i + 1).toString();
                var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
                series.push({
                    x: x,
                    y: y
                });
                i++;
            }
            return series;
        }
    },

    async created() {
        const {
            data
        } = await axios.get(
            "http://167.99.243.10:5000/stats/delay/all/this_year/grouped/hourly"
        );

        var i = 0;
        while (data[i]) {
            this.all.push({
                i,
                total: data[i]["#all"]
            });
            this.ndelayed.push({
                i,
                total: data[i]["#delayed"]
            });
            this.pdelayed.push({
                i,
                total: data[i]["%delayed"]
            });
            this.avg_delay.push({
                i,
                total: data[i]["avg_delay"]
            });
            this.max_delay.push({
                i,
                total: data[i]["max_delay"]
            });
            i = i + 1;
        }


        this.hour_data = {
            labels: ["Delayed", "All"],
            backgroundColors: ["#E55381", "#74A57F"],
            borderColors: ["#190B28", "#077187"],
            pointBorderColors: ["#190B28", "#0E1428"],
            pointBackgroundColors: ["#E55381", "#AFD6AC"],
            i: this.all.map(d => d.i),
            total: [this.ndelayed.map(d => d.total),
                this.all.map(d => d.total),
                this.pdelayed.map(d => d.total),
                this.avg_delay.map(d => d.total),
                this.max_delay.map(d => d.total)
            ]
        };

        this.options_line = {
            chart: {
                id: 'vuechart-example'
            },
            xaxis: {
                categories: this.hour_data.i,
                title: {text: 'Hour of Day'},

            },
            tooltip: {
                formatter: function(val, opts) {
                    return val + "..."
                }
            },
            dataLabels: {enabled: false}

        };

        this.series_line = [{
            name: 'Delays',
            data: this.hour_data.total[0]
        }]


        this.options_bar = {
            chart: {
                id: 'vuechart-example'
            },
            xaxis: {
                categories: this.hour_data.i
            }
        };

        this.series_bar = [{
            name: 'series-1',
            data: this.hour_data.total[1]
        }]


    },


    watch: {
        line: function() {
            this.queryGetStations = 'http://167.99.243.10:5000/line/' + this.line + '/stations'

        },

        station: function() {
            this.queryStats = 'http://167.99.243.10:5000/stats/delay/station/' + encodeURIComponent(this.station['station_id']) + "/current_week/grouped/weekly"

        },

        queryGetStations: async function() {

            var response = await axios.get(this.queryGetStations)
            this.seriesHeatMap = [];
            this.stationsList = response['data'][response['data']['tracks'][0]]

            var i;
            var orderedStations = [];
            for (i = 0; i < this.stationsList.length; i++) {
                var station_name = this.stationsList[i]['station_name']
                var station_id = this.stationsList[i]['station_id']
                orderedStations[this.stationsList[i]['order']] = [station_name, station_id]
            }


            for (i = 1; i < orderedStations.length + 1; i++) {

                this.queryGetGroupedForStation = 'http://167.99.243.10:5000/stats/delay/station/' + encodeURIComponent(orderedStations[i][1]) + "/current_week/grouped/daily"

                var response = await axios.get(this.queryGetGroupedForStation)
                var stationName = orderedStations[i][0]
                var delaysArray = []
                var heatMapStats_ = response.data
                Object.keys(heatMapStats_).forEach(function(key) {
                    delaysArray.push({x:moment(key).format('dddd'), y:heatMapStats_[key][0]["%delayed"]})
                })
                
                this.seriesHeatMap.push({
                    name: stationName,
                    data: delaysArray
                })

            }

        },
    }

}
</script>


<style src="bootstrap/dist/css/bootstrap.min.css">

  
@import url('https://fonts.googleapis.com/css?family=Quicksand');
html, body {
	font-family: 'Quicksand', sans-serif;
	height: 100%;
}

div.card {
	height: 100%;
}

#left-col {
	height: 100%;
}

#right-col {
	display: flex;
	flex-direction: column;
	height: 100%;
}

#right-card-container {
	flex: 1;
}

#right-card-content {
	height: 100%;
	width: 100%;
	background: red;
}

#right-bottom-element {
	background: blue;
	display: inline-block;
	height: 100px;
	width: 100%;
}

* {
	box-sizing: border-box;
}

body {
	font-family: 'Quicksand', sans-serif;
}

header {
	font-family: 'Quicksand', sans-serif;
	width: 100vw;
	background-color: rgb(163, 163, 163);
	padding: 15px;
	text-align: center;
}
</style>
