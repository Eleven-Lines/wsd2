<template lang="pug">
span.morpheme(:style="active ? 'active' : ''"
              @click="$emit('active', morpheme.score, morpheme.midasi)"
              v-tooltip="toolTipMessage")
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
  },
  computed: {
    toolTipMessage () {
      const score = this.morpheme.score.map(a => Math.round(a * 100) / 100)
      return ("Joy: " + score[0]  + ", "
              + "Tru:" + score[1] + ", "
              + "Fea:" + score[2] + ", "
              + "Sup:" + score[3] + ", "
              + "Sad:" + score[4] + ", "
              + "Dis:" + score[5] + ", "
              + "Ang:" + score[6] + ", "
              + "Ant:" + score[7]
      ) 
    }
  },
}
</script>

<style lang="scss">
.morpheme {
  display: inline-block;
}
.morpheme:hover {
  background: #dddddd;
}
.tooltip {
  display: block !important;
  z-index: 10000;

  .tooltip-inner {
    background: #aaaaaa;
    color: white;
    border-radius: 5px;
    padding: 5px 10px 4px;
    font-size: 0.8rem;
  }

  .tooltip-arrow {
    width: 0;
    height: 0;
    border-style: solid;
    position: absolute;
    margin: 5px;
    border-color: black;
    z-index: 1;
  }

  &[x-placement^="top"] {
    margin-bottom: 5px;

    .tooltip-arrow {
      border-width: 5px 5px 0 5px;
      border-left-color: transparent !important;
      border-right-color: transparent !important;
      border-bottom-color: transparent !important;
      bottom: -5px;
      left: calc(50% - 5px);
      margin-top: 0;
      margin-bottom: 0;
    }
  }

  &[x-placement^="bottom"] {
    margin-top: 5px;

    .tooltip-arrow {
      border-width: 0 5px 5px 5px;
      border-left-color: transparent !important;
      border-right-color: transparent !important;
      border-top-color: transparent !important;
      top: -5px;
      left: calc(50% - 5px);
      margin-top: 0;
      margin-bottom: 0;
    }
  }

  &[x-placement^="right"] {
    margin-left: 5px;

    .tooltip-arrow {
      border-width: 5px 5px 5px 0;
      border-left-color: transparent !important;
      border-top-color: transparent !important;
      border-bottom-color: transparent !important;
      left: -5px;
      top: calc(50% - 5px);
      margin-left: 0;
      margin-right: 0;
    }
  }

  &[x-placement^="left"] {
    margin-right: 5px;

    .tooltip-arrow {
      border-width: 5px 0 5px 5px;
      border-top-color: transparent !important;
      border-right-color: transparent !important;
      border-bottom-color: transparent !important;
      right: -5px;
      top: calc(50% - 5px);
      margin-left: 0;
      margin-right: 0;
    }
  }

  &.popover {
    $color: #f9f9f9;

    .popover-inner {
      background: $color;
      color: black;
      padding: 24px;
      border-radius: 5px;
      box-shadow: 0 5px 30px rgba(black, .1);
    }

    .popover-arrow {
      border-color: $color;
    }
  }

  &[aria-hidden='true'] {
    visibility: hidden;
    opacity: 0;
    transition: opacity .15s, visibility .15s;
  }

  &[aria-hidden='false'] {
    visibility: visible;
    opacity: 1;
    transition: opacity .15s;
  }
}
</style>
