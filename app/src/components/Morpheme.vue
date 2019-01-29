<template lang="pug">
span.morpheme(:style="active ? 'active' : ''"
              @click="$emit('active', morpheme.score, morpheme.midasi)")
  | {{ morpheme.midasi }}
</template>

<script>
export default {
  props: {
    morpheme: {
      type: Object
    },
    active: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="sass">
.morpheme
  display: inline-block
.morpheme:hover
  background: #cce5ff
</style>
