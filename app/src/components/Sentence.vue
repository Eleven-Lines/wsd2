<template lang="pug">
p.sentence(@click="$emit('sentenceActive', sentence.score, sentence.sentence)"
           :style="{'color': color}")
  Morpheme(v-for="(morpheme, mi) in sentence.morphemes"
           @active="onActive"
           :key="mi"
           :morpheme="morpheme")
</template>

<script>
import Morpheme from '@/components/Morpheme.vue'

export default {
  components: {
    Morpheme
  },
  props: {
    sentence: {
      type: Object
    }
  },
  computed: {
    color () {
      if (this.mostEmo == 0 && this.sentence.score[0] == 0) {
        return "#2c3e50"
      }
      return ["#C39A11",
              "#AFCA1A",
              "#67B841",
              "#2F7DC2",
              "#1D267C",
              "#8D4597",
              "#871C21",
              "#DD6B0D"][this.mostEmo]
    },
    mostEmo () {
      return this.sentence.score.reduce((acc, currentValue, currentIndex) => {
        return (this.sentence.score[acc] < currentValue) ? currentIndex : acc
      }, 0)
    }
  },
  methods: {
    onActive (score, midasi) {
      this.$emit("morphemeActive", score, midasi)
    }
  }
}
</script>
<style lang="sass">
.sentence:hover
  background: #eeeeee
</style>
