<template>
<div>
  {{ info }}
</div>
</template>

<script>
import axios from "axios";

export default{

  data () {
    return {
      info: null
    }
  },
  mounted () {
    axios
      .get('http://167.99.243.10:5000/stats/delay/S8/de%3A09188%3A5410/de%3A09188%3A5400')
      .then(response => (this.info = response))
  }
}
</script>