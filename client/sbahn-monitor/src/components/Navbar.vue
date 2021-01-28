<template>
  <nav>
    <div class="menu-item">
      <router-link to="/general">Charts Demo</router-link>
    </div>
    <div class="menu-item">
      <router-link to="/about">Another Chart</router-link>
    </div>
    <div class="menu-item">
      <router-link to="/heatmap">Heatmap Chart</router-link>
    </div>
    <div class="menu-item">
      <router-link to="/Stats_Routing">StatsRouting</router-link>
    </div>
    <div class="menu-item">
      <router-link to="/Routing">Routing</router-link>
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
      lines: [
        {
          title: 'S4',
          link: '#'
        },
        {
          title: 'S4',
          link:'#'
        },
        {
          title: 'S8',
          link: '#'
        }
      ],
      stations: [
        {
          title: 'TODO',
          link: '#'
        },
        {
          title: 'TODO',
          link:'#'
        },
        {
          title: 'TODO',
          link: '#'
        }
      ]
    }
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