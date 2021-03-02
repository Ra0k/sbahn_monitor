<template>
  <div id="app">
    <app-header />
    <dropdown-selector />
    <router-view/>
    <graph-cards />
    <app-footer />
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import DropdownSelector from '@/components/DropdownSelector.vue'
import GraphCards from './components/GraphCards.vue'

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
    DropdownSelector,
    GraphCards
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
