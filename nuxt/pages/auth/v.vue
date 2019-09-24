<template>
  <v-container fluid>
    <v-flex xs12>
      <v-layout align-center justify-center fill-height>
        <div>Verifying email... please wait</div>
        <div>DEBUG: key={{ $route.query.key }}</div>
      </v-layout>
    </v-flex>
  </v-container>
</template>

<script>
export default {
  layout: 'empty',
  created () { 
      
  }
}
</script>
