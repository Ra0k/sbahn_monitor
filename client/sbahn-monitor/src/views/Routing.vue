<template>
<!-- comment 
 -->
<div>
  <multiselect v-model="stationName1" :options="stationsList" placeholder="From..."></multiselect>
  <multiselect v-model="stationName2" :options="stationsList" placeholder="To..."></multiselect>


  <p> Name1:  {{ stationName1 }}  </p>
  <p> {{ stationId1 }}  </p>

  <p> Name2: {{ stationName2 }}  </p>
  <p> {{ stationId2 }}  </p>




  <p> {{ info2.data }}  </p>
  <p> {{ info.data }}  </p>
  
  

</div>
</template>

<script>
import axios from "axios";
import Multiselect from 'vue-multiselect';

var stationIdFrom = 'de%3A09177%3A3270'
var stationIdTo = 'de%3A09162%3A910'




var query = 'http://167.99.243.10:5000/route/from/'+stationIdFrom +'/to/' + stationIdTo
var queryStations = 'http://167.99.243.10:5000/stations'

var stationIds =[ "de:09162:1910", "de:09177:3280", "de:09174:6950", "de:09174:6910", "de:09162:1710", "de:09177:3270", "de:09184:2260", "de:09174:6870", "de:09184:2550", "de:09175:4010", "de:09162:910", "de:09179:6200", "de:09184:2540", "de:09174:6800", "de:09174:6850", "de:09162:700", "de:09184:2340", "de:09162:8", "de:09184:2250", "de:09184:2570", "de:09175:4070", "de:09178:2650", "de:09175:4030", "de:09179:6180", "de:09162:710", "de:09177:3290", "de:09174:6920", "de:09179:6120", "de:09184:2300", "de:09162:310",
 "de:09162:1120", "de:09188:5470", "de:09184:2110", "de:09162:320", "de:09178:2860", "de:09178:3240", "de:09162:1740", "de:09178:2680", "de:09184:2330", "de:09179:6190", "de:09188:5430", "de:09188:5350", "de:09181:502", "de:09179:6250", "de:09179:6130", "de:09162:1110", "de:09188:5360", "de:09175:4050", "de:09175:4060", "de:09179:6220", "de:09184:2130", "de:09184:2280", "de:09184:2500", "de:09175:3950", "de:09184:2590", "de:09179:6100", "de:09184:2140", "de:09162:7",
 "de:09178:2850", "de:09162:1130", "de:09179:6240", "de:09162:6", "de:09174:6810", "de:09162:1150", "de:09184:2120", "de:09188:5410", "de:09162:31", "de:09184:2220", "de:09184:2560", "de:09182:43227", "de:09184:2240", "de:09184:2530", "de:09173:4750", "de:09162:3", "de:09184:2040", "de:09162:720", "de:09174:1920", "de:09162:1", "de:09175:4040", "de:09174:6930", "de:09182:43677", "de:09162:9", "de:09162:1800", "de:09162:1700", "de:09162:900", "de:09184:2580", "de:09162:1810", "de:09184:2020", "de:09179:6140", "de:09179:6150",
  "de:09179:6160", "de:09162:2", "de:09174:6900", "de:09175:3970", "de:09162:1300", "de:09162:300", "de:09162:1730", "de:09184:2200", "de:09178:2660", "de:09188:5370", "de:09162:1010", "de:09174:6890", "de:09162:1900", "de:09184:2000", "de:09179:6110", "de:09162:5", "de:09177:3250", "de:09182:43342", "de:09184:2210", "de:09162:10", "de:09184:2270", "de:09162:1000", "de:09174:6840", "de:09184:2600", "de:09175:3960", "de:09188:5460", "de:09179:6170", "de:09184:2520",
  "de:09178:2670", "de:09162:800", "de:09162:4", "de:09174:6820", "de:09184:2350", "de:09174:6880", "de:09179:6210", "de:09188:5400", "de:09162:1310", "de:09162:1320", "de:09177:3260", "de:09162:1100", "de:09188:5450", "de:09188:5490", "de:09188:5390", "de:09188:5420", "de:09184:2320", "de:09162:920", "de:09188:5480", "de:09179:6230", "de:09184:2030", "de:09184:2310", "de:09162:1930", "de:09184:2010", "de:09175:4000", "de:09174:6830", "de:09162:1720", "de:09188:5380", "de:09173:4760", "de:09184:2230","de:09175:4020" ]

var stationNames= [ "Allach", "Altenerding", "Altomünster", "Arnbach", "Aubing", "Aufhausen", "Aying", "Bachern", "Baierbrunn", "Baldham", "Berg am Laim", "Buchenau", "Buchenhain", "Dachau", "Dachau Stadt", "Daglfing", "Deisenhofen", "Donnersbergerbrücke", "Dürrnhaar", "Ebenhausen-Schäftlarn", "Ebersberg", "Eching", "Eglharting", "Eichenau", "Englschalking", "Erding", "Erdweg", "Esting", "Fasanenpark", "Fasanerie", "Fasangarten", "Feldafing", "Feldkirchen", "Feldmoching", "Flughafen Besucherpark", "Flughafen München",
 "Freiham", "Freising", "Furth", "Fürstenfeldbruck", "Gauting", "Geisenbrunn", "Geltendorf", "Germering-Unterpfaffenhofen", "Gernlinden", "Giesing", "Gilching-Argelsried", "Grafing", "Grafing Stadt", "Grafrath", "Gronsdorf", "Großhelfendorf", "Großhesselohe Isartalbahnhof", "Grub", "Gräfelfing", "Gröbenzell", "Haar", "Hackerbrücke", "Hallbergmoos", "Harras", "Harthaus", "Hauptbahnhof", "Hebertshausen", "Heimeranplatz", "Heimstetten", "Herrsching", "Hirschgarten", "Hohenbrunn",
 "Hohenschäftlarn", "Holzkirchen", "Höhenkirchen-Siegertsbrunn", "Höllriegelskreuth", "Icking", "Isartor", "Ismaning", "Johanneskirchen", "Karlsfeld", "Karlsplatz", "Kirchseeon", "Kleinberghofen", "Kreuzstraße", "Laim", "Langwied", "Leienfelsstraße", "Leuchtenbergring", "Lochham", "Lochhausen", "Lohhof", "Maisach", "Malching", "Mammendorf", "Marienplatz", "Markt Indersdorf", "Markt Schwaben", "Mittersendling", "Moosach", "Neuaubing", "Neubiberg", "Neufahrn", "Neugilching", "Neuperlach Süd", "Niederroth",
  "Obermenzing", "Oberschleißheim", "Olching", "Ostbahnhof München", "Ottenhofen", "Otterfing", "Ottobrunn", "Pasing", "Peiß", "Perlach", "Petershausen", "Planegg", "Poing", "Possenhofen", "Puchheim", "Pullach", "Pulling", "Riem", "Rosenheimer Platz", "Röhrmoos", "Sauerlach", "Schwabhausen", "Schöngeising", "Seefeld-Hechendorf", "Siemenswerke", "Solln", "St. Koloman", "St.-Martin-Straße", "Starnberg", "Starnberg Nord", "Steinebach", "Stockdorf", "Taufkirchen", "Trudering", "Tutzing", "Türkenfeld",
  "Unterföhring", "Unterhaching", "Untermenzing", "Unterschleißheim", "Vaterstetten", "Vierkirchen-Esterhofen", "Westkreuz", "Weßling", "Wolfratshausen", "Wächterhof", "Zorneding"]

console.log(query)



export default{
  components:{Multiselect,
},
  data () {
    return {

      stationName1: '',
      stationName2: null,
      stationId1: '',
      stationId2: '',
      info: null,
      info2: null,
      stationIdFrom: stationIdFrom,
      stationIdTo: stationIdTo,
      stations: null,
      staionsList: [],
      stationIds: [], 
      id: 0,
    }
  },
  mounted () {
    axios.get(query)
      .then(response => (this.info2 = response))
    axios.get(queryStations)
      .then(response => (this.info = response))
 
  },

  created() {
    axios.get(queryStations, {})
      .then((response) => { this.stationsList = response.data.map(x => x.station_name) })
  
  },

  watch: {

       stationName1: function(value) {
         this.stationName1 = value
         this.stationId1 = encodeURIComponent(stationIds[stationNames.indexOf(value)])
       },
       stationName2: function(value) {
         this.stationName2 = value
         this.stationId2 = encodeURIComponent(stationIds[stationNames.indexOf(value)])
       },
       

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