<template lang="pug">
p.sentence
  Morpheme(v-for="(morpheme, mi) in sentence.morphemes"
           @acvite="onActive"
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
  methods: {
    onActive (score, midasi) {
      this.$emit("morphemeActive", score, midasi)
    }
  }
}
</script>
