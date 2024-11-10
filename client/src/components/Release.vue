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
		getMessage() {
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
		this.getMessage();
	},
};
</script>