<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
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
											<br class="mt-16">
											<section role="region" aria-label="Album details">
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
											</section>
										</v-col>
									</v-row>
									<br>
									<RatingSystem
										itemType="master"
										:itemId="$route.params.master_id"
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

					<br v-if="hasCredits" />
					<section
						role="region"
						aria-labelledby="credits-heading"
						v-if="hasCredits"
						class="credits-section"
					>
						<div class="row">
							<h2 id="credits-heading">Credits</h2>
							<hr aria-hidden="true" />
							
							<div class="credits-content">
								<p v-for="(artists, role) in groupedByRole" :key="role" class="credit-line">
									{{ role }} - {{ artists.join(', ') }}
								</p>
							</div>
						</div>
					</section>

					<br v-if="data.company?.length" />
					<section
						role="region"
						aria-labelledby="companies-heading"
						v-if="data.company?.length"
						class="company-section"
					>
						<div class="row">
							<h2 id="companies-heading">Companies</h2>
							<hr aria-hidden="true" />
							<div class="company-content">
								<p v-for="(company_name, entity_type) in filteredCompanies"
									:key="entity"
									class="company-line">
									{{ entity_type }} - {{ company_name.join(', ') }}
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
				image_uri: "",
				loading: true,
				hasCredits: true,
			};
		},
		computed: {
			filteredCompanies() {
				const companyGroups = {};

				this.data.company.forEach(company => {
					const name = company.company_name || "Unknown Company";
					const entity_type = company.entity_type_name || "Unknown Entity";

					if (!companyGroups[entity_type]) {
						companyGroups[entity_type] = [];
					}
					if (companyGroups[entity_type] && entity_type !== "Unknown Entity") {
						companyGroups[entity_type] = [];

						if (!companyGroups[entity_type].includes(name) && name !== "Unknown Company") {
							companyGroups[entity_type].push(name);
						}
					}
				});

				return companyGroups;
			},
			groupedByRole() {
				const allCredits = [
					...(this.data.artist_credits?.artist || []),
					...(this.data.artist_credits?.track_artist || [])
				];

				const roleGroups = {};
				
				allCredits.forEach(credit => {
					const role = credit.role || "Unknown Role";
					const artistName = credit.artist_name;
					
					if (!role || role === "Unknown Role") {
						return;
					}

					if (!roleGroups[role]) {
						roleGroups[role] = [];
					}

					if (!roleGroups[role].includes(artistName)) {
						roleGroups[role].push(artistName);
					}
				});
				
				for (const role in roleGroups) {
					roleGroups[role].sort();
				}

				const orderedRoles = {};
				Object.keys(roleGroups).sort().forEach(role => {
					orderedRoles[role] = roleGroups[role];
				});

				if (Object.keys(roleGroups).length === 0) {
					this.hasCredits = true;
				}
				
				return orderedRoles;
			}
		},
		methods: {
			async getMaster() {
				try {
					const response = await axios.get("http://localhost:5001/master/", {
						params: { master_id: this.$route.params.master_id },
					});
					this.data = response.data.payload;

					if (this.data.api_data.images && this.data.api_data.images.length) {
						this.image_uri = this.data.api_data.images[0].uri;
						this.image_uri = this.image_uri === "" ? "/images/UnknownSong.png" : this.image_uri;

						console.log(this.image_uri, this.data.api_data);
					} else {
						this.image_uri = "/images/UnknownSong.png";
					}

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

	.credits-section .company-section {
		margin-top: 20px;
	}

	.credits-content .company-content {
		margin-left: 10px;
	}

	.credit-line .company-line {
		margin: 8px 0;
	}
</style>
