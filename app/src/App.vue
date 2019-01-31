<template lang="pug">
#app
  textarea(v-model="lyrics"
           placeholder="edit me")
  .controls
    button(@click="fillData") Run
    button(@click="reset") Reset
  Graph(:chart-data="datacollection" :options="options")
  .lyrics
    Sentence(v-for="(sentence, si) in parsedData.sentences"
            :key="si"
            :sentence="sentence"
            @morphemeActive="onActive"
            @sentenceActive="onActive")
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
      selectedContent: null,
      options: {
        scale: {
          pointLabels: {
              fontColor: ["#C39A11", "#AFCA1A", "#67B841", "#2F7DC2", "#1D267C", "#8D4597", "#871C21", "#DD6B0D"],
          },
        },
      }
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
        labels: ["Joy", "Trust", "Fear", "Suprise", "Sadness", "Disgust", "Anger", "Anticipation"],
        datasets: [{
          label: this.content.label || "data",
          data: this.content.score
        }]
      }
    }
  },
  methods: {
    async fillData () {
      this.rawData = (await axios.post("http://localhost:8000", this.lyrics)).data
    },
    onActive (score, midasi) {
      this.selectedContent = {
        score: score,
        label: midasi
      }
    },
    reset () {
      this.selectedContent = null}
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
.lyrics
  height: 20rem
  overflow: scroll
</style>
