<template>
   <div>

    <div class="card">
			<div class="card-header">Pick a line and station to see specific statistics</div>
			<div class="card-body">
				<multiselect v-model="line" :options="linesList" placeholder="Pick a line..." ></multiselect>
        <multiselect v-model="station" :options="stationsList" placeholder="Pick a station..." label="station_name" track-by="station_name"></multiselect>
      </div>
      <div class="row">
         <div class="col-sm-6">
            <div class="card">
               <div class="card-header">How many trains were delayed this year on sertain day time?</div>
               <div class="card-body">
                  <apexchart type="bar" :options="options_bar" :series="series_bar"></apexchart>
               </div>
            </div>
         </div>
         <div class="col-sm-6">
            <div class="card">
               <div class="card-header">Current week delay percentage heatmap for line {{this.line}}</div>
               <div class="card-body">
                  <apexchart type="heatmap" height="350" :options="chartOptions" :series="seriesHeatMap"></apexchart>
               </div>
            </div>
         </div>
      </div>
    <p></p>

    <div class="row">
        
         <div class="col-sm-6">
            <div class="card mb-3">
               <div class="card-header">Average delay (mins) on {{this.station["station_name"]}} during this week</div>
               <div class="card-body">
                  <apexchart type="line" height="350" :options="options_line" :series="series_line"></apexchart>
               </div>
            </div>
         </div>
         <div class="col-sm-6">
            <div class="card border-info mb-3" style="max-width: 18rem;">
               <div class="card-header">Real-time delay on {{this.station["station_name"]}}</div>
               <div class="card-body">
                  <h5 class="card-title">{{this.delayNow}} mins</h5>
               </div>
            </div>
         </div>

		</div>
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
            station: '[Choose the line!]',
            delayNow: 0,
            card_bg: 'bg-success',
            queryGetStations: '',
            queryDelayNow: '',


            all: [],
            ndelayed: [],
            pdelayed: [],
            avg_delay: [],
            max_delay: [],
            hour_data: [],
            options_bar: null,
            series_bar: null,

            station_all: [],
            station_ndelayed: [],
            station_pdelayed: [],
            station_avg_delay: [],
            station_max_delay: [],
            station_week_data: [],
            options_line: null,
            series_line: null,

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


        // console.log(this.hour_data.total[0]);
    },


    watch: {
        line: function() {
            this.queryGetStations = 'http://167.99.243.10:5000/line/' + this.line + '/stations'

        },

        station: function() {
            this.queryDelayNow = 'http://167.99.243.10:5000/stats/delay/station/' + encodeURIComponent(this.station['station_id']) + "/current_week/grouped/daily"


        },

        queryDelayNow: async function() {

            var response = await axios.get(this.queryDelayNow)
            this.delayNow = response['data']['2021-03-09'][0]['avg_delay'].toPrecision(2)

            var delayWeek = response['data']
            var dates_for_week = ['2021-03-03', '2021-03-04', '2021-03-05', '2021-03-06', '2021-03-07', '2021-03-08', '2021-03-09']

            var i = 0;
        while (dates_for_week[i]) {
            this.station_all.push({
                i: dates_for_week[i],
                total: delayWeek[dates_for_week[i]][0]["#all"]
            });
            this.station_ndelayed.push({
                i: dates_for_week[i],
                total: delayWeek[dates_for_week[i]][0]["#delayed"]
            });
            this.station_pdelayed.push({
                i: dates_for_week[i],
                total: delayWeek[dates_for_week[i]][0]["%delayed"]
            });
            this.station_avg_delay.push({
                i: dates_for_week[i],
                total: delayWeek[dates_for_week[i]][0]["avg_delay"].toPrecision(2)
            });
            this.station_max_delay.push({
                i: dates_for_week[i],
                total: delayWeek[dates_for_week[i]][0]["max_delay"]
            });
            i = i + 1;
        }

        this.station_week_data = {
            labels: ["Delayed", "All"],
            backgroundColors: ["#E55381", "#74A57F"],
            borderColors: ["#190B28", "#077187"],
            pointBorderColors: ["#190B28", "#0E1428"],
            pointBackgroundColors: ["#E55381", "#AFD6AC"],
            i: this.station_all.map(d => d.i),
            total: [this.station_ndelayed.map(d => d.total),
                this.station_all.map(d => d.total),
                this.station_pdelayed.map(d => d.total),
                this.station_avg_delay.map(d => d.total),
                this.station_max_delay.map(d => d.total)
            ]
        };

         this.options_line = {
            chart: {
                id: 'vuechart-example'
            },
            colors: ['#66DA26'],
            xaxis: {
                categories: this.station_week_data.i
            }
        };

        this.series_line = [{
            name: 'series-1',
            data: this.station_week_data.total[3]
        }]
        console.log(this.options_line)

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

            console.log(orderedStations[1][0])

            for (i = 1; i < orderedStations.length + 1; i++) {

                this.queryGetGroupedForStation = 'http://167.99.243.10:5000/stats/delay/station/' + encodeURIComponent(orderedStations[i][1]) + "/current_week/grouped/daily"

                //  console.log(this.queryGetGroupedForStation)
                var response = await axios.get(this.queryGetGroupedForStation)
                var stationName = orderedStations[i][0]
                var delaysArray = []
                var heatMapStats_ = response.data
                Object.keys(heatMapStats_).forEach(function(key) {
                    delaysArray.push(heatMapStats_[key][0]["%delayed"])
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
  position: relative;
  margin: auto;
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
