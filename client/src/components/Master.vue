<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
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

					<RatingSystem itemType="master" :itemId="$route.params.master_id" />

					<div role="region" aria-label="Album details">
						<p>Country: {{ data.release?.[0]?.country || "Unknown" }}</p>
						<p>Released: {{ data.master?.[0]?.year || "Unknown" }}</p>
						<p>
							Genre:
							{{
								data.genre?.map((entry) => entry.genre).join(", ") || "Unknown"
							}}
						</p>
						<p>
							Style:
							{{
								data.style?.map((entry) => entry.style).join(", ") || "Unknown"
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
	body {
		font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
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

	h1,
	h2 {
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

	.table th,
	.table td {
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
		font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
		font-size: 1rem;
		color: #7f8c8d;
		white-space: pre-wrap;
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

		.table th,
		.table td {
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
