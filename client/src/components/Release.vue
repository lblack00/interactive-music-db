<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<main role="main">
				<div class="container mt-2" v-if="data && data.release">
					<section role="region" aria-labelledby="release-title">
						<div class="row">
							<h1 id="release-title">
								<router-link
									v-if="data.artist?.[0]"
									:to="`/artist/${data.artist[0].artist_id}`"
									:aria-label="`Artist: ${data.artist[0].artist_name}`"
								>
									{{ data.artist[0].artist_name }}
								</router-link>
								- {{ data.release?.[0]?.title }}
							</h1>

							<div class="grid-container-no-min-height">
								<div class="content">
									<v-row>
										<v-col cols="12" md="6">
											<v-img
												:src="image_uri || '/images/UnknownSong.png'"
												width="400"
												height="400"
												contain
												alt="Image of master cover"
												class="justify-center"
											/>
										</v-col>
										<v-col cols="12" md="6">
											<br class="mt-16" />
											<section role="region" aria-label="Album details">
												<p>
													Country: {{ data.release?.[0]?.country || "Unknown" }}
												</p>
												<p>
													Released: {{ data.master?.[0]?.year || "Unknown" }}
												</p>
												<p>
													Genre:
													{{
														data.genre
															?.map((entry) => entry.genre)
															.join(", ") || "Unknown"
													}}
												</p>
												<p>
													Style:
													{{
														data.style
															?.map((entry) => entry.style)
															.join(", ") || "Unknown"
													}}
												</p>
											</section>
										</v-col>
									</v-row>
									<br />
									<RatingSystem
										itemType="master"
										:itemId="$route.params.release_id"
									/>
								</div>
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
								<table class="table table-hover" aria-label="Release tracks">
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
						<div class="row" v-if="data.release?.[0]?.notes">
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
						<div class="row" v-if="hasCredits">
							<h2 id="credits-heading">Credits</h2>
							<hr aria-hidden="true" />
							<div class="credit-list">
								<p
									v-for="(credit, index) in filteredTrackArtists"
									:key="`track-${index}`"
								>
									{{ credit.role }} - {{ credit.artist_name }}
								</p>
								<p
									v-for="(credit, index) in filteredArtists"
									:key="`artist-${index}`"
								>
									{{ credit.role }} - {{ credit.artist_name }}
								</p>
							</div>
						</div>
					</section>

					<br v-if="data.company?.length" />

					<section
						role="region"
						aria-labelledby="companies-heading"
						v-if="data.company?.length"
					>
						<div class="row" v-if="data.company?.length">
							<h2 id="companies-heading">Companies</h2>
							<hr aria-hidden="true" />
							<div class="company-list">
								<p v-for="(company, index) in filteredCompanies" :key="index">
									{{ company.entity_type_name }} - {{ company.company_name }}
								</p>
							</div>
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
		name: "Release",
		components: {
			Navbar,
			RatingSystem,
		},
		data() {
			return {
				data: {
					release: [],
					artist: [],
					tracks: [],
					genre: [],
					style: [],
					track_artist: [],
					company: [],
				},
				loading: true,
				image_uri: "",
			};
		},
		computed: {
			filteredTrackArtists() {
				return this.data.track_artist?.filter((x) => x.role !== null) || [];
			},
			filteredArtists() {
				return this.data.artist?.filter((x) => x.role !== null) || [];
			},
			filteredCompanies() {
				return this.data.company?.filter((x) => x.company_name !== null) || [];
			},
			hasCredits() {
				return (
					this.data.track_artist?.some((x) => x.role !== null) ||
					false ||
					this.data.artist?.some((x) => x.role !== null) ||
					false
				);
			},
		},
		methods: {
			async getRelease() {
				try {
					const response = await axios.get("http://localhost:5001/release/", {
						params: { release_id: this.$route.params.release_id },
					});
					this.data = response.data.payload;

					if (this.data.api_data.images && this.data.api_data.images.length) {
						this.image_uri = this.data.api_data.images[0].uri;
						this.image_uri =
							this.image_uri === ""
								? "/images/UnknownSong.png"
								: this.image_uri;

						console.log(this.image_uri, this.data.api_data);
					} else {
						this.image_uri = "/images/UnknownSong.png";
					}

					this.loading = false;
				} catch (error) {
					console.error("Error fetching release:", error);
					this.loading = false;
				}
			},
		},
		created() {
			this.getRelease();
		},
	};
</script>

<style scoped>
	@import "../../src/assets/master.css";
	@import "../../src/assets/background.css";
</style>
