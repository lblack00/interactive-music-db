<!-- This file was written by Jax Hendrickson -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->

<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<main>
				<p class="record"><img src="../assets/record.svg" alt="Record" /></p>
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
	@import "../../src/assets/background.css";
	@import "../../src/assets/homepage.css";
	@import "../../src/assets/accessibility.css";
</style>
