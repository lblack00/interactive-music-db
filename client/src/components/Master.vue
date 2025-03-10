<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<div class="grid-container">
		<div class="content">
			<header role="navigation">
				<Navbar />
			</header>

			<main role="main">
				<div class="container mt-2" v-if="data && data.master">
					<section role="region" aria-labelledby="album-title">
						<div class="row">
							<h1 id="album-title">
								<router-link
									v-if="data.artist?.[0]"
									:to="`/artist/${data.artist[0].artist_id}`"
									:aria-label="`Artist: ${data.artist[0].artist_name}`"
								>
									{{ data.artist[0].artist_name }}
								</router-link>
								- {{ data.master?.[0]?.title }}
							</h1>

							<RatingSystem
								itemType="master"
								:itemId="$route.params.master_id"
							/>

							<div role="region" aria-label="Album details">
								<p>Country: {{ data.release?.[0]?.country || "Unknown" }}</p>
								<p>Released: {{ data.master?.[0]?.year || "Unknown" }}</p>
								<p>
									Genre:
									{{
										data.genre?.map((entry) => entry.genre).join(", ") ||
										"Unknown"
									}}
								</p>
								<p>
									Style:
									{{
										data.style?.map((entry) => entry.style).join(", ") ||
										"Unknown"
									}}
								</p>
							</div>
						</div>
					</section>

					<br />

					<section
						role="region"
						aria-labelledby="tracklist-heading"
						v-if="data.tracks?.length"
					>
						<div class="row">
							<div class="col-sm-10">
								<h2 id="tracklist-heading">Tracklist</h2>
								<hr aria-hidden="true" />
								<table class="table table-hover" aria-label="Album tracks">
									<thead>
										<tr>
											<th scope="col">Title</th>
											<th scope="col">Duration</th>
										</tr>
									</thead>
									<tbody>
										<tr v-for="(track, index) in data.tracks" :key="index">
											<td>{{ track.title }}</td>
											<td>{{ track.duration || "--:--" }}</td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>
					</section>

					<br v-if="data.release?.[0]?.notes" />

					<section
						role="region"
						aria-labelledby="notes-heading"
						v-if="data.release?.[0]?.notes"
					>
						<div class="row">
							<h2 id="notes-heading">Notes</h2>
							<hr aria-hidden="true" />
							<pre>{{ data.release[0].notes }}</pre>
						</div>
					</section>

					<br />

					<section
						role="region"
						aria-labelledby="credits-heading"
						v-if="hasCredits"
					>
						<div class="row">
							<h2 id="credits-heading">Credits</h2>
							<hr aria-hidden="true" />
							<p
								v-for="(credit, index) in data.artist_credits?.track_artist"
								:key="`track-${index}`"
							>
								{{ credit.role }} - {{ credit.artist_name }}
							</p>
							<p
								v-for="(credit, index) in data.artist_credits?.artist"
								:key="`artist-${index}`"
							>
								{{ credit.role }} - {{ credit.artist_name }}
							</p>
						</div>
					</section>

					<br v-if="data.company?.length" />
					<section
						role="region"
						aria-labelledby="companies-heading"
						v-if="data.company?.length"
					>
						<div class="row">
							<h2 id="companies-heading">Companies</h2>
							<hr aria-hidden="true" />
							<p v-for="(company, index) in filteredCompanies" :key="index">
								{{ company.entity_type_name }} - {{ company.company_name }}
							</p>
						</div>
					</section>
				</div>

				<div v-else class="container mt-2" role="status" aria-live="polite">
					<div class="loading">Loading...</div>
				</div>
			</main>
		</div>
	</div>
</template>

<script>
	import axios from "axios";
	import Navbar from "./Navbar.vue";
	import RatingSystem from "./RatingSystem.vue";

	export default {
		name: "Master",
		components: {
			Navbar,
			RatingSystem,
		},
		data() {
			return {
				data: {
					master: [],
					artist: [],
					release: [],
					tracks: [],
					genre: [],
					style: [],
					artist_credits: {
						artist: [],
						track_artist: [],
					},
					company: [],
				},
				loading: true,
			};
		},
		computed: {
			filteredCompanies() {
				return this.data.company?.filter((x) => x.company_name !== null) || [];
			},
			hasCredits() {
				return (
					this.data.artist_credits?.track_artist?.length > 0 ||
					this.data.artist_credits?.artist?.length > 0
				);
			},
		},
		methods: {
			async getMaster() {
				try {
					const response = await axios.get("http://localhost:5001/master/", {
						params: { master_id: this.$route.params.master_id },
					});
					this.data = response.data.payload;
					this.loading = false;
				} catch (error) {
					console.error("Error fetching master:", error);
					this.loading = false;
				}
			},
		},
		created() {
			this.getMaster();
		},
	};
</script>

<style scoped>
	@import "../../src/assets/master.css";
	@import "../../src/assets/background.css";
</style>
