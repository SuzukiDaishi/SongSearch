import { createApp } from 'vue'

createApp({
  data() {
    return {
      tracks: [],
      tracksSelect: [],
      chords: ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
      searchId: null
    }
  },
  async mounted() {
    let data = await fetch('data_wav.json')
    this.tracks = await data.json()
    this.tracksSelect = JSON.parse(JSON.stringify(this.tracks))
  },
  methods: {
    sortHist(e) {
      this.searchId = e.target.value
      this.tracks.sort((a, b) => {
        let ad = this.modeSlideDistance(
          this.tracksSelect[e.target.value].mode_hist, 
          a.mode_hist
        )
        let bd = this.modeSlideDistance(
          this.tracksSelect[e.target.value].mode_hist, 
          b.mode_hist
        )
        return ad - bd 
      })
    },
    modeSlideDistance(hist1, hist2) {
      let h1 = hist1.map(v=>v/Math.max(...hist1))
      let h2 = hist2.map(v=>v/Math.max(...hist2))
      let r = Infinity
      for (let x=0; x<12; x++) {
        h1 = [
          h1[(x+0)%12], h1[(x+1)%12], h1[(x+2)%12], h1[(x+3)%12], 
          h1[(x+4)%12], h1[(x+5)%12], h1[(x+6)%12], h1[(x+7)%12],
          h1[(x+8)%12], h1[(x+9)%12], h1[(x+10)%12], h1[(x+11)%12]
        ]
        let s = 0
        for (let i=0; i<12; i++) s += Math.pow(h1[i] - h2[i], 2)
        r = Math.min(s, r)
      }
      return r
    }
  }
}).mount('#app')