<!-- This file was written by Jax Hendrickson -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<header role="navigation">
		<Navbar />
	</header>

	<main>
		<div class="welcome-message" aria-label="Welcome message">
			Welcome to Pass the Aux! Explore what's trending, or use the filters to
			search for your favorite songs, artists, or playlists!
		</div>

		<div class="search-container" role="search" aria-label="Search for music">
			<form @submit.prevent="performSearch" class="search-form">
				<div class="search-input-container">
					<label for="search-input" class="sr-only">Search for music</label>
					<input
						type="text"
						v-model="searchQuery"
						class="search-bar"
						placeholder="Search..."
						@input="getPreviewResults"
					/>
					<button type="submit" class="search-button">Search</button>
				</div>

				<!-- Preview Results Dropdown -->
				<div
					v-if="searchQuery && (isSearching || previewResults.length)"
					class="search-preview"
					id="search-results"
					role="listbox"
					aria-label="Search suggestions"
				>
					<div v-if="isSearching" class="preview-item" role="status">
						Searching, wait just a second...
					</div>
					<template v-else>
						<div
							v-for="(result, index) in previewResults.slice(0, 3)"
							:key="index"
							class="preview-item"
							@click="handlePreviewClick(result)"
							role="option"
							:aria-selected="false"
							tabindex="0"
						>
							<template v-if="filterOption === 'Artists'">
								{{ result.name }}
							</template>
							<template v-else-if="filterOption === 'Releases'">
								{{ result.title }} ({{ result.year }}) - {{ result.artists }}
							</template>
							<template v-else-if="filterOption === 'Tracks'">
								{{ result.title }} - {{ result.release_title }}
							</template>
						</div>
						<div class="preview-footer" @click.prevent="performSearch">
							See all results...
						</div>
					</template>
				</div>
			</form>

			<div class="dropdown-container">
				<label for="filter-option" class="sr-only">Select filter type</label>
				<select
					v-model="filterOption"
					class="filter-dropdown"
					aria-label="Filter by type"
				>
					<option value="Artists">Artists</option>
					<option value="Releases">Releases</option>
					<option value="Tracks">Tracks</option>
				</select>
				<label for="genre-option" class="sr-only">Select genre</label>
				<select
					v-model="genreOption"
					class="filter-dropdown"
					aria-label="Filter by genre"
				>
					<option value="Genres" disabled>Genres</option>
					<option value="-">-</option>
					<option value="Pop">Pop</option>
					<option value="Rock">Rock</option>
					<option value="Hip-hop">Hip-hop</option>
					<option value="Jazz">Jazz</option>
				</select>
			</div>
		</div>

		<br />
		<section class="container" aria-label="Music collections">
			<article role="region" aria-labelledby="featured-songs-title">
				<h3 id="featured-songs-title" class="carousel-title">Featured Songs</h3>
				<div>
					<AccessibilityCarousel
						ariaLabel="Featured songs carousel"
						:items="featuredSongs"
						showArrows="hover"
					>
						<v-carousel-item
							v-for="(item, i) in featuredSongs"
							:key="item"
							:value="i"
							:to="item.link"
						>
							<router-link
								:key="i"
								:to="item.link"
								:aria-label="`Featured song`"
							>
								<v-img
									:src="item.image || '/images/UnknownSong.png'"
									class="w-100 h-100"
									contain
									:alt="`Album cover for featured song`"
								/>
							</router-link>
						</v-carousel-item>
					</AccessibilityCarousel>
				</div>
			</article>
			<br />
			<br />

			<article role="region" aria-labelledby="popular-artists-title">
				<h3 id="popular-artists-title" class="carousel-title">
					Popular Artists
				</h3>
				<div>
					<AccessibilityCarousel
						ariaLabel="Popular Artists carousel"
						:items="popularArtists"
						showArrows="hover"
					>
						<v-carousel-item
							v-for="(item, i) in popularArtists"
							:key="item"
							:value="i"
							:to="item.link"
						>
							<router-link
								:key="i"
								:to="item.link"
								:aria-label="`Popular artist`"
							>
								<v-img
									:src="item.image || '/images/UnknownPerson.png'"
									class="w-100 h-100"
									contain
									:alt="`Photo of popular artist`"
								/>
							</router-link>
						</v-carousel-item>
					</AccessibilityCarousel>
				</div>
			</article>

			<br />
			<br />

			<article role="region" aria-labelledby="trending-now-title">
				<h3 id="trending-now-title" class="carousel-title">Trending Now</h3>
				<div>
					<AccessibilityCarousel
						ariaLabel="Trending songs carousel"
						:items="trendingNow"
						showArrows="hover"
					>
						<v-carousel-item
							v-for="(item, i) in trendingNow"
							:key="item"
							:value="i"
							:to="item.link"
						>
							<router-link
								:key="i"
								:to="item.link"
								:aria-label="`Trending song`"
							>
								<v-img
									:src="item.image || '/images/UnknownSong.png'"
									class="w-100 h-100"
									contain
									:alt="`Album cover for trending song`"
								/>
							</router-link>
						</v-carousel-item>
					</AccessibilityCarousel>
				</div>
			</article>
		</section>
	</main>
</template>

<script>
	import Navbar from "./Navbar.vue";
	import axios from "axios";
	import AccessibilityCarousel from "./AccessibilityCarousel.vue";

	export default {
		name: "Home",
		components: {
			Navbar,
			AccessibilityCarousel,
		},
		data() {
			return {
				searchQuery: "",
				filterOption: "Artists",
				genreOption: "-",
				previewResults: [],
				searchTimeout: null,
				isSearching: false,

				//i think it would be really intersting if the carousel looked more like a stack of cards on it's side;
				//so it could look like flipping through vinyls or albums in a store.

				featuredSongs: [
					{ image: "/images/UnknownSong.png", link: "/master/763819" }, // Ed Sheeran - A Team
					{ image: "/images/UnknownSong.png", link: "/master/483665" }, // Taylor Swift - We Are Never...
					{ image: "/images/UnknownSong.png", link: "/master/74524" }, // Linkin Park - Papercut
					{ image: "/images/UnknownSong.png", link: "/master/267064" }, // Metallica - Evil Never Dies
					{ image: "/images/UnknownSong.png", link: "/master/1293228" }, // Frank Ocean - Chanel
					{ image: "/images/UnknownSong.png", link: "/master/763819" }, // Repeat Ed Sheeran
					{ image: "/images/UnknownSong.png", link: "/master/483665" }, // Repeat Taylor Swift
				],
				popularArtists: [
					{ image: "/images/UnknownPerson.png", link: "/artist/1124645" }, // Taylor Swift
					{ image: "/images/UnknownPerson.png", link: "/artist/18839" }, // Metallica
					{ image: "/images/UnknownPerson.png", link: "/artist/40029" }, // Linkin Park
					{ image: "/images/UnknownPerson.png", link: "/artist/2184482" }, // Ed Sheeran
					{ image: "/images/UnknownPerson.png", link: "/artist/2013868" }, // Frank Ocean
					{ image: "/images/UnknownPerson.png", link: "/artist/1124645" }, // Repeat Taylor Swift
					{ image: "/images/UnknownPerson.png", link: "/artist/18839" }, // Repeat Metallica
				],
				trendingNow: [
					{ image: "/images/UnknownSong.png", link: "/master/876374" }, // Blank Space
					{ image: "/images/UnknownSong.png", link: "/master/308202" }, // Master of Puppets
					{ image: "/images/UnknownSong.png", link: "/master/1503117" }, // Blackout
					{ image: "/images/UnknownSong.png", link: "/master/1547600" }, // I Don't Care
					{ image: "/images/UnknownSong.png", link: "/master/1046042" }, // Blonde
					{ image: "/images/UnknownSong.png", link: "/master/876374" }, // Repeat Blank Space
					{ image: "/images/UnknownSong.png", link: "/master/308202" }, // Repeat Master of Puppets
				],
				currentIndex: {
					featured: 0,
					popular: 0,
					trending: 0,
				},
			};
		},
		methods: {
			async getPreviewResults() {
				if (this.searchTimeout) {
					clearTimeout(this.searchTimeout);
				}

				if (!this.searchQuery.trim()) {
					this.previewResults = [];
					this.isSearching = false;
					return;
				}

				this.isSearching = true;

				this.searchTimeout = setTimeout(async () => {
					try {
						const response = await axios.post("http://localhost:5001/search", {
							query: this.searchQuery,
							filterOption: this.filterOption,
							genreOption: this.genreOption,
						});

						if (response.status === 200) {
							this.previewResults = response.data.results;
						}
					} catch (error) {
						console.error("Error fetching preview results:", error);
					} finally {
						this.isSearching = false;
					}
				}, 300);
			},

			handlePreviewClick(result) {
				// Navigate to the appropriate page based on result type
				if (this.filterOption === "Artists") {
					this.$router.push(`/artist/${result.id}`);
				} else if (this.filterOption === "Releases") {
					this.$router.push(`/master/${result.id}`);
				} else if (this.filterOption === "Tracks") {
					this.$router.push(`/release/${result.release_id}`);
				}
			},

			performSearch() {
				console.log("Performing search...", this.searchQuery); // Debug log
				if (this.searchQuery.trim()) {
					this.$router.push({
						name: "SearchResults", // Matches the name in router
						params: {
							query: this.searchQuery,
						},
						query: {
							filterOption: this.filterOption,
							genreOption: this.genreOption,
						},
					});
				}
			},
		},
	};
</script>

<style scoped>
	.welcome-message {
		font-size: 24px;
		color: #1a1a1a;
		text-align: center;
		margin: 40px auto;
		max-width: 800px;
		line-height: 1.6;
		padding: 20px;
		border-radius: 10px;
		background: rgba(255, 255, 255, 0.9);
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}

	.search-container {
		background: white;
		padding: 30px;
		border-radius: 15px;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
		margin: 20px auto 40px;
		max-width: 800px;
	}

	.search-form {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		margin-bottom: 20px;
		position: relative;
		max-width: 800px;
	}

	.search-bar {
		border: 2px solid #e0e0e0;
		border-radius: 8px;
		padding: 15px;
		font-size: 18px;
		width: 100%;
		max-width: 600px;
		transition: all 0.3s ease;
		margin-right: 10px;
	}

	.search-bar:focus {
		border-color: blue;
		box-shadow: 0 0 0 3px rgba(0, 0, 128, 0.1);
		outline: none;
	}

	.search-button {
		background: blue;
		color: white;
		padding: 15px 30px;
		border-radius: 8px;
		font-size: 16px;
		font-weight: 600;
		transition: all 0.3s ease;
	}

	.search-button:hover {
		background: darkblue;
		transform: translateY(-2px);
		box-shadow: 0 4px 8px rgba(0, 0, 128, 0.2);
	}

	.search-results {
		width: 50%;
		background-color: #f0f0f0;
		padding: 10px;
		margin-bottom: 10px;
		border-radius: 5px;
		max-height: 150px;
		overflow-y: auto;
		border: 1px solid #ccc;
	}

	.result-item {
		padding: 5px;
		font-size: 14px;
		color: #333;
		transition: all 0.3s;
	}

	.result-item:hover {
		background-color: #ddd;
		text-decoration: underline;
		cursor: pointer;
	}

	.dropdown-container {
		display: flex;
		gap: 15px;
		justify-content: center;
	}

	.filter-dropdown {
		padding: 12px;
		border: 2px solid #e0e0e0;
		border-radius: 8px;
		font-size: 16px;
		background: white;
		cursor: pointer;
		transition: all 0.3s ease;
	}

	.filter-dropdown:hover {
		border-color: blue;
	}

	.filter-dropdown:focus {
		outline: none;
		border-color: blue;
		box-shadow: 0 0 0 3px rgba(0, 0, 128, 0.1);
	}

	.search-input-container {
		position: relative;
		width: 100%;
		display: flex;
		align-items: center;
	}

	.search-preview {
		position: absolute;
		top: 100%;
		left: 0;
		right: 0;
		background: white;
		border: 1px solid #ccc;
		border-top: none;
		border-radius: 0 0 4px 4px;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
		z-index: 1000;
		width: 100%;
	}

	.preview-item {
		padding: 12px 15px;
		cursor: pointer;
		transition: background-color 0.2s;
		color: #333;
		font-size: 14px;
		font-weight: 500;
	}

	.preview-item:hover {
		background-color: #f0f0f0;
	}

	.preview-footer {
		padding: 10px 15px;
		text-align: center;
		color: #444;
		font-size: 14px;
		font-weight: 500;
		border-top: 1px solid #eee;
		cursor: pointer;
	}

	.preview-footer:hover {
		background-color: #f0f0f0;
		color: #222;
	}

	.search-form {
		position: relative;
		width: 100%;
	}

	.search-container {
		width: 60%;
		max-width: 800px;
		margin: 20px auto;
		padding: 20px;
		background: rgba(255, 255, 255, 0.8);
		border-radius: 15px;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	}

	.welcome-message {
		width: 60%;
		max-width: 800px;
		margin: 40px auto;
		padding: 20px;
		background: rgba(255, 255, 255, 0.8);
		border-radius: 10px;
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}

	.v-carousel {
		border-radius: 15px;
	}

	/* For screen readers only - visually hidden but accessible to screen readers */
	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border-width: 0;
	}
</style>
