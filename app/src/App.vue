<template lang="pug">
#app
  textarea(v-model="lyrics"
           placeholder="edit me")
  button(@click="fillData") Run
  Graph(:chart-data="datacollection")
  .lyrics
    Sentence(v-for="(sentence, si) in parsedData.sentences"
            :key="si"
            :sentence="sentence")
</template>

<script>
import Graph from './components/Graph.vue'
import Sentence from './components/Sentence.vue'
import axios from 'axios'

export default {
  name: 'app',
  components: {
    Graph,
    Sentence
  },
  data () {
    return {
      lyrics: "",
      rawData: null,
      defaultData: {score: [0, 0, 0, 0, 0, 0, 0, 0], sentences: [], lyrics: ""},
      selectedContent: null
    }
  },
  computed: {
    parsedData () {
      return JSON.parse(this.rawData) || this.defaultData
    },
    content () {
      return this.selectedContent || this.parsedData
    },
    datacollection () {
      return {
        labels: ["Joy", "Sadness", "Trust", "Disgust", "Fear", "Anger", "Suprise", "Anticipation"],
        datasets: [{
          label: "data",
          data: this.content.score
        }]
      }
    }
  },
  methods: {
    async fillData () {
      this.rawData = (await axios.post("http://localhost:8000", this.lyrics)).data
    },
  }
}
</script>

<style lang="sass">
#app
  font-family: 'Avenir', Helvetica, Arial, sans-seri
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  text-align: center
  display: flex
  flex-direction: column
  align-items: center
  color: #2c3e50
  margin-top: 60px
.small
  max-width: 300px
  margin:  150px auto
</style>
