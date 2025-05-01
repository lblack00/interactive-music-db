<!-- This file was written by Lucas Black -->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<div class="container mt-5">
				<div class="search-bar-header">
					<v-icon class="search-header-icon" color="#3cba92"
						>mdi-magnify</v-icon
					>
					<span class="search-header-text"
						>Search Results for "{{ query }}"</span
					>
				</div>
				<div v-if="loading" class="loading-spinner">Loading...</div>
				<div v-else-if="results.length > 0" class="results-container">
					<div
						v-for="(result, index) in results"
						:key="index"
						class="result-item"
					>
						<div v-if="filterOption === 'Artists'">
							<router-link :to="`/artist/${result.id}`" class="result-link">
								{{ result.name }}
							</router-link>
						</div>
						<div v-else-if="filterOption === 'Releases'">
							<router-link :to="`/master/${result.id}`" class="result-link">
								{{ result.title }} ({{ result.year }}) - {{ result.artists }}
							</router-link>
						</div>
						<div v-else-if="filterOption === 'Tracks'">
							<router-link
								:to="`/release/${result.release_id}`"
								class="result-link"
							>
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
		border-radius: 18px;
		box-shadow: 0 4px 24px rgba(44, 122, 123, 0.1);
		max-width: 600px;
		margin: auto;
		text-align: center;
	}

	/* Search bar style for the header */
	.search-bar-header {
		display: flex;
		align-items: center;
		justify-content: center;
		background: #fff;
		border-radius: 32px;
		box-shadow: 0 2px 12px rgba(44, 122, 123, 0.1);
		border: 1.5px solid #e0e7ef;
		padding: 0 28px 0 18px;
		min-height: 56px;
		margin-bottom: 32px;
		margin-top: 0;
		width: 100%;
		max-width: 480px;
		margin-left: auto;
		margin-right: auto;
	}
	.search-header-icon {
		margin-right: 14px;
		font-size: 1.5rem;
		flex-shrink: 0;
	}
	.search-header-text {
		font-size: 1.18rem;
		font-weight: 500;
		color: #2c7a7b;
		letter-spacing: 0.01em;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.results-container {
		display: flex;
		flex-direction: column;
		gap: 12px;
		margin-top: 0;
	}

	.result-item {
		padding: 15px 18px;
		font-size: 1rem;
		color: #34495e;
		background-color: #ecf0f1;
		border: 1px solid #bdc3c7;
		border-radius: 8px;
		transition: background-color 0.2s, box-shadow 0.2s;
		text-align: left;
	}
	.result-item:hover {
		background-color: #dceef2;
		box-shadow: 0 0 5px rgba(22, 160, 133, 0.12);
	}
	.result-link {
		color: #2c7a7b;
		font-size: 1.08rem;
		font-weight: 500;
		text-decoration: none;
		transition: color 0.18s;
		white-space: nowrap;
		text-overflow: ellipsis;
		overflow: hidden;
		width: 100%;
		display: inline-block;
	}
	.result-link:hover {
		color: #3cba92;
		text-decoration: underline;
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

	/* Dark mode styles */
	.dark-mode .container {
		background-color: #2d2d2d;
		box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .search-bar-header {
		background: #363636;
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
	}

	.dark-mode .search-header-text {
		color: rgba(255, 255, 255, 0.9);
	}

	.dark-mode .result-item {
		background-color: #363636;
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: rgba(255, 255, 255, 0.9);
	}

	.dark-mode .result-item:hover {
		background-color: #404040;
		box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
	}

	.dark-mode .result-link {
		color: #3cba92;
	}

	.dark-mode .result-link:hover {
		color: #4fd1a5;
	}

	.dark-mode .no-results {
		color: #ff6b6b;
	}

	.dark-mode .loading-spinner {
		color: #3cba92;
	}
</style>
