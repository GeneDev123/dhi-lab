import { createApp } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
// import axios from 'https://cdn.jsdelivr.net/npm/vue-axios@3.5.2/dist/vue-axios.esm.min.js';

export default function createVueApp() {
  return createApp({
    data() {
      return {
        items: [],
      }
    },
    mounted() {
      console.log("VueJs running");
      console.log("Todo: Connect to the django API");
      // axios.get('/api/items/')
      //   .then(response => {
      //     this.items = response.data;
      //   })
      //   .catch(error => {
      //     console.error('Error fetching items:', error);
      //   });
    }
  });
}