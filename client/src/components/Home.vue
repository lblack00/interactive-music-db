<!-- This file was written by Jax Hendrickson -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->

<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<main>
				<p class="note note1">
					<img src="../assets/dblnote.svg" alt="double note" />
				</p>
				<p class="record"><img src="../assets/record.svg" alt="Record" /></p>
				<p class="note note0">
					<img src="../assets/snglnote.svg" alt="single note" />
				</p>
				<div class="welcome-message" aria-label="Welcome message">
					<strong
						>MUSIC
						<br />
						DISCOVERY
						<br />
						REIMAGINED</strong
					>
				</div>

				<p class="description">
					The world's most comprehensive music database and community. Rate,
					review, and discover your next favorite track.
				</p>
				<div
					class="search-container"
					role="search"
					aria-label="Search for music"
				>
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
										{{ result.title }} ({{ result.year }}) -
										{{ result.artists }}
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
						<label for="filter-option" class="sr-only"
							>Select filter type</label
						>
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
						<h3 id="featured-songs-title" class="carousel-title">
							Featured Songs
						</h3>
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
		</div>
	</div>
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
			const createMaster = (id, name) => ({
				id,
				image: "/images/UnknownSong.png",
				link: `/master/${id}`,
				loading: false,
				name,
			});

			const createArtist = (id, name) => ({
				id,
				image: "/images/UnknownPerson.png",
				link: `/artist/${id}`,
				loading: false,
				name,
			});

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
					createMaster(763819, "Ed Sheeran - A Team"),
					createMaster(483665, "Taylor Swift - We Are Never..."),
					createMaster(74524, "Linkin Park - Papercut"),
					createMaster(267064, "Metallica - Evil Never Dies"),
					createMaster(1293228, "Frank Ocean - Chanel"),
				],
				popularArtists: [
					createArtist(1124645, "Taylor Swift"),
					createArtist(18839, "Metallica"),
					createArtist(40029, "Linkin Park"),
					createArtist(2184482, "Ed Sheeran"),
					createArtist(2013868, "Frank Ocean"),
				],
				trendingNow: [
					createMaster(876374, "Blank Space"),
					createMaster(308202, "Master of Puppets"),
					createMaster(1503117, "Blackout"),
					createMaster(1547600, "I Don't Care"),
					createMaster(1046042, "Blonde"),
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

			async loadMasterImage(song) {
				if (song.loading) return;

				song.loading = true;

				try {
					const masterId = song.id;
					const response = await axios.get(
						`http://localhost:5001/get-master-image`,
						{
							params: { master_id: masterId },
						}
					);

					if (response.status === 200 && response.data.payload) {
						song.image = response.data.payload;
					}
				} catch (error) {
					console.log(`Error loading image for master ID ${song.id}:`, error);
				} finally {
					song.loading = false;
				}
			},

			async loadArtistImage(artist) {
				if (artist.loading) return;

				artist.loading = true;

				try {
					const artistId = artist.id;
					const response = await axios.get(
						`http://localhost:5001/get-artist-image`,
						{
							params: { artist_id: artistId },
						}
					);

					if (response.status === 200 && response.data.payload) {
						artist.image = response.data.payload;
					}
				} catch (error) {
					console.log(`Error loading image for artist ID ${artist.id}:`, error);
				} finally {
					artist.loading = false;
				}
			},

			loadImages() {
				this.featuredSongs.forEach((song) => {
					this.loadMasterImage(song);
				});

				this.popularArtists.forEach((artist) => {
					this.loadArtistImage(artist);
				});

				this.trendingNow.forEach((song) => {
					this.loadMasterImage(song);
				});
			},
		},
		mounted() {
			this.loadImages();
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";
	@import "../../src/assets/homepage.css";
	@import "../../src/assets/accessibility.css";

	/* Content Animations */
	.welcome-message {
		animation: fadeSlideDown 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
		opacity: 0;
	}

	.description {
		animation: fadeSlideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.2s forwards;
		opacity: 0;
	}

	.search-container {
		animation: fadeIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.4s forwards;
		opacity: 0;
	}

	.search-input-container {
		animation: expandWidth 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.6s forwards;
		transform-origin: center;
		transform: scaleX(0.8);
		opacity: 0;
	}

	.dropdown-container {
		animation: fadeIn 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) 0.8s forwards;
		opacity: 0;
	}

	.container {
		animation: contentFadeUp 1s cubic-bezier(0.2, 0.8, 0.2, 1) 0.6s forwards;
		opacity: 0;
	}

	.carousel-title {
		animation: slideInLeft 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
		opacity: 0;
	}

	article {
		opacity: 0;
		animation: fadeScale 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
	}

	article:nth-child(1) {
		animation-delay: 0.8s;
	}
	article:nth-child(2) {
		animation-delay: 1s;
	}
	article:nth-child(3) {
		animation-delay: 1.2s;
	}

	/* Animation Keyframes */
	@keyframes fadeSlideDown {
		from {
			opacity: 0;
			transform: translateY(-20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes fadeSlideUp {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	@keyframes expandWidth {
		from {
			opacity: 0;
			transform: scaleX(0.8);
		}
		to {
			opacity: 1;
			transform: scaleX(1);
		}
	}

	@keyframes contentFadeUp {
		from {
			opacity: 0;
			transform: translateY(30px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes slideInLeft {
		from {
			opacity: 0;
			transform: translateX(-20px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	@keyframes fadeScale {
		from {
			opacity: 0;
			transform: scale(0.95);
		}
		to {
			opacity: 1;
			transform: scale(1);
		}
	}

	/* Search Preview Animations */
	.search-preview {
		animation: fadeInDown 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
	}

	.preview-item {
		opacity: 0;
		animation: fadeSlideIn 0.3s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
	}

	.preview-item:nth-child(1) {
		animation-delay: 0.1s;
	}
	.preview-item:nth-child(2) {
		animation-delay: 0.2s;
	}
	.preview-item:nth-child(3) {
		animation-delay: 0.3s;
	}

	.preview-footer {
		opacity: 0;
		animation: fadeIn 0.3s ease-out 0.4s forwards;
	}

	@keyframes fadeInDown {
		from {
			opacity: 0;
			transform: translateY(-10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes fadeSlideIn {
		from {
			opacity: 0;
			transform: translateX(-10px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}
</style>
