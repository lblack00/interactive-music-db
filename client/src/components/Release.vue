<template>
  <div class="container">
    <div class="row">
      <h1>{{ data.artist[0].artist_name }} - {{ data.release[0].title }}</h1>
      <p>Country: {{ data.release[0].country }}</p>
      <p>Released: {{ data.release[0].released }}</p>
      <p>Genre: {{ data.genre.map(entry => entry.genre).join(', ') }} </p>
      <p>Style: {{ data.style.map(entry => entry.style).join(', ') }}</p>
    </div>

    <br>

    <div class="row">
      <div class="col-sm-10">
        <h2>Tracklist</h2>
        <hr>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Duration</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(track, index) in data.tracks" :key="index">
              <td>{{ track.title }}</td>
              <td>{{ track.duration }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <br v-if="data.release[0].notes">

    <div class="row" v-if="data.release[0].notes">
      <h2>Notes</h2>
      <hr>
      <p><pre>{{ data.release[0].notes }}</pre></p>
    </div>

    <br>

    <div class="row" v-if="data.track_artist.length">
      <!-- todo: depending on if there are all null roles,
               credits shouldn't be shown (small hack above in v-if) -->
      <h2>Credits</h2>
      <hr>
      <!-- passing a .filter function to only show credits with non-null roles -->
      <p v-for="(credit, index) in data.track_artist.filter(x => x.role !== null)" :key="index">
        {{ credit.role }} - {{ credit.artist_name }}
      </p>
      <p v-for="(credit, index) in data.artist.filter(x => x.role !== null)" :key="index">
        {{ credit.role }} - {{ credit.artist_name }}
      </p>
    </div>

    <br v-if="data.company.length">

    <div class="row" v-if="data.company.length">
      <!-- todo: depending on if there are all null roles,
               credits shouldn't be shown (small hack above in v-if) -->
      <h2>Companies</h2>
      <hr>
      <!-- passing a .filter function to only show credits with non-null roles -->
      <p v-for="(company, index) in data.company.filter(x => x.company_name !== null)" :key="index">
        {{ company.entity_type_name }} - {{ company.company_name }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Release',
  data() {
    return {
      data: [],
    };
  },
  methods: {
    getRelease() {
      const path = 'http://localhost:5001/release/';
      axios.get(path, {params: {release_id: this.$route.params.release_id}})
        .then((res) => {
          this.data = res.data.payload;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.getRelease();
  },
};
</script>

<style scoped>
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f7f8fa;
  color: #333;
  line-height: 1.6;
  padding: 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.row {
  margin-bottom: 20px;
}

h1, h2 {
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 10px;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #1abc9c;
}

p {
  font-size: 1rem;
  color: #7f8c8d;
  margin-bottom: 8px;
}

.table {
  width: 100%;
  margin-top: 10px;
  border-collapse: collapse;
}

.table th, .table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ecf0f1;
}

.table th {
  background-color: #ecf0f1;
  font-size: 1.1rem;
  color: #34495e;
}

.table tbody tr:hover {
  background-color: #ecf0f1;
  cursor: pointer;
}

h2 {
  font-size: 1.8rem;
  color: #16a085;
  border-bottom: 2px solid #16a085;
  padding-bottom: 5px;
}

p {
  font-size: 1.1rem;
  color: #34495e;
  margin-top: 8px;
}

pre {
  background-color: #f4f6f8;
  padding: 15px;
  border-radius: 5px;
  font-family: 'Courier New', monospace;
  font-size: 1rem;
  color: #7f8c8d;
}

.credit-list p {
  font-size: 1rem;
  color: #34495e;
}

.credit-list p:nth-child(even) {
  color: #16a085;
}

.company-list p {
  font-size: 1rem;
  color: #34495e;
}

@media (max-width: 768px) {
  .container {
    padding: 15px;
  }

  h1 {
    font-size: 1.8rem;
  }

  h2 {
    font-size: 1.5rem;
  }

  .table th, .table td {
    padding: 8px;
  }

  p {
    font-size: 0.9rem;
  }

  pre {
    font-size: 0.9rem;
    padding: 12px;
  }
}
</style>