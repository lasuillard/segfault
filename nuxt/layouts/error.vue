<template>
  <v-app>
    <v-layout align-center justify-center>
      <v-card width="600px">
        <v-card-title>
          <h1 class="display-3">{{ error.statusCode }} Error</h1>
        </v-card-title>
        <v-card-text>
          <h2 class="subtitle-1">{{ error.message }}</h2>
          <h2 class="subtitle-1">URL을 확인 해 주세요!</h2>
        </v-card-text>
        <v-card-actions>
          <v-layout fill-height align-end justify-end>
          <v-btn :to="{ name: 'index' }" exact replace large text>
            메인페이지로 돌아가기
          </v-btn>
          </v-layout>
        </v-card-actions>
      </v-card>
    </v-layout>
  </v-app>
</template>

<script>
export default {
  layout: 'empty',
  props: {
    error: {
      type: Object,
      default: null
    }
  }
}
</script>
