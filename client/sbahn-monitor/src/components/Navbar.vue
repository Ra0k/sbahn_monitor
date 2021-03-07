<template>

    
<nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #808080;">
  <a class="navbar-brand" href="/">
    <img src="../assets/logo.png" width="40" height="40" class="d-inline-block" alt="">
    S-BAHN MONITOR
  </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link" href="/">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item active">
        <a class="nav-link" href="#/stats/">Statistics</a>
      </li>
      <li class="nav-item active">
        <a class="nav-link" href="#/alerts/">Alerts</a>
      </li>
      
    </ul>
  </div>
</nav>

</template>

<script>
import Dropdown from './Dropdown';
export default {
  name: 'navbar',
  components: {
    Dropdown
  },
  data () {
    return {

    }
  }
}
</script>

<style src="bootstrap/dist/css/bootstrap.min.css"> 
/* nav {
  display: flex;
  align-items: center;
  justify-content: center;
} */
/* nav .menu-item {
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
} */
</style>