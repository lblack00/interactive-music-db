<!-- This file was written by Lucas Black -->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<div class="container mt-5">
				<h2>Search Results for "{{ query }}"</h2>
				<div v-if="loading" class="loading-spinner">Loading...</div>
				<div v-else-if="results.length > 0" class="results-container">
					<div
						v-for="(result, index) in results"
						:key="index"
						class="result-item"
					>
						<div v-if="filterOption === 'Artists'">
							<router-link :to="`/artist/${result.id}`">{{
								result.name
							}}</router-link>
						</div>
						<div v-else-if="filterOption === 'Releases'">
							<router-link :to="`/master/${result.id}`">
								{{ result.title }} ({{ result.year }}) - {{ result.artists }}
							</router-link>
						</div>
						<div v-else-if="filterOption === 'Tracks'">
							<router-link :to="`/release/${result.release_id}`">
								{{ result.title }} - {{ result.release_title }} ({{
									result.released
								}})
							</router-link>
						</div>
					</div>
				</div>
				<div v-else class="no-results">No results found for "{{ query }}"</div>
			</div>
		</div>
	</div>
</template>

<script>
	import axios from "axios";
	import Navbar from "./Navbar.vue";

	export default {
		name: "SearchResults",
		components: {
			Navbar,
		},
		props: {
			query: {
				type: String,
				required: true,
			},
			filterOption: {
				type: String,
				required: true,
			},
			genreOption: {
				type: String,
				required: true,
			},
		},
		data() {
			return {
				results: [],
				loading: true,
			};
		},
		async created() {
			try {
				const response = await axios.post("http://localhost:5001/search", {
					query: decodeURIComponent(this.query),
					filterOption: this.filterOption,
					genreOption: this.genreOption,
				});

				if (response.status === 200) {
					this.results = response.data.results;
				}
			} catch (error) {
				console.error("Error fetching search results:", error);
				alert("Failed to load search results.");
			} finally {
				this.loading = false;
			}
		},
	};
</script>

<style scoped>
	@import "../assets/background.css";
	body {
		font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
		background-color: #ecf0f1;
		color: #333;
		line-height: 1.6;
	}

	.container {
		background-color: #ffffff;
		padding: 40px;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		max-width: 600px;
		margin: auto;
		text-align: center;
	}

	h2 {
		font-size: 2rem;
		color: #1abc9c;
		margin-bottom: 20px;
	}

	.results-container {
		display: flex;
		flex-direction: column;
		gap: 15px;
		margin-top: 20px;
	}

	.result-item {
		padding: 15px;
		font-size: 1rem;
		color: #34495e;
		background-color: #ecf0f1;
		border: 1px solid #bdc3c7;
		border-radius: 5px;
		transition: background-color 0.3s, box-shadow 0.3s;
	}

	.result-item:hover {
		background-color: #dceef2;
		box-shadow: 0 0 5px rgba(22, 160, 133, 0.5);
	}

	.no-results {
		font-size: 1.2rem;
		color: #e74c3c;
		margin-top: 20px;
	}

	.loading-spinner {
		font-size: 1.2rem;
		color: #1abc9c;
		margin-top: 20px;
	}

	.mt-5 {
		margin-top: 40px;
	}
</style>
