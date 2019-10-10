<template>
  <div>
    avgRating: {{ average }}<br/>
  </div>
</template>

<script>
export default {
  props: {
    votes: {
      type: Array,
      required: true
    }
  },
  computed: {
    average: function () {
      if (this.votes.length > 0)
        return this.votes.map(v => v.rating).reduce((l, r) => l + r) / this.votes.length

      return 0.0
    }
  }
}
</script>
