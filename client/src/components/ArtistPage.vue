<!-- This file was written by Lucas Black -->
<!--ARIA Landmakes added by Chantelle Cabanilla-->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<main role="main">
				<div class="artist-page-flex">
					<!-- Sidebar Artist Header -->
					<div class="artist-sidebar-header">
						<v-avatar size="140" class="artist-avatar mb-4">
							<v-img
								:src="image_uri || '/images/UnknownPerson.png'"
								alt="Profile photo of artist"
							/>
						</v-avatar>
						<h1 class="artist-header-title mb-2">
							{{ data.artist?.[0]?.name }}
						</h1>
						<div class="artist-header-chips mb-2">
							<v-chip class="artist-chip" size="small"
								>Born: December 13, 1989</v-chip
							>
							<v-chip class="artist-chip" size="small"
								>Genre: Pop, Country</v-chip
							>
							<v-chip class="artist-chip" size="small"
								>Aliases: {{ data.aliases?.join(", ") || "None" }}</v-chip
							>
						</div>
						<div class="artist-header-stars mb-2">
							<RatingSystem
								itemType="artist"
								:itemId="$route.params.artist_id"
							/>
						</div>
						<div class="artist-header-bio mt-3">
							<p v-if="data.artist?.[0]?.profile">
								{{ data.artist[0].profile }}
							</p>
						</div>
					</div>

					<!-- Main Content -->
					<div class="artist-main-content">
						<v-card class="artist-discography-card">
							<!-- Stat Cards Row INSIDE the discography card -->
							<v-row class="artist-stats-row mb-4" justify="center">
								<v-col cols="12" md="4">
									<v-card
										class="artist-stat-card stat-card-vertical"
										elevation="2"
									>
										<div class="text-overline mb-2 text-center">TOP ALBUM</div>
										<v-img
											src="/images/UnknownSong.png"
											height="64"
											width="64"
											class="stat-card-img mx-auto mb-2"
										/>
										<div class="font-weight-bold stat-card-title text-center">
											Divide
										</div>
										<div class="text-caption stat-card-year text-center">
											2017
										</div>
									</v-card>
								</v-col>
								<v-col cols="12" md="4">
									<v-card
										class="artist-stat-card stat-card-vertical"
										elevation="2"
									>
										<div class="text-overline mb-2 text-center">TOP SONG</div>
										<v-img
											src="/images/UnknownSong.png"
											height="64"
											width="64"
											class="stat-card-img mx-auto mb-2"
										/>
										<div class="font-weight-bold stat-card-title text-center">
											Shape of You
										</div>
										<div class="text-caption stat-card-year text-center">
											2017
										</div>
									</v-card>
								</v-col>
								<v-col cols="12" md="4">
									<v-card
										class="artist-stat-card stat-card-vertical"
										elevation="2"
									>
										<div class="text-overline mb-2 text-center">
											RECENT RELEASE
										</div>
										<v-img
											src="/images/UnknownSong.png"
											height="64"
											width="64"
											class="stat-card-img mx-auto mb-2"
										/>
										<div class="font-weight-bold stat-card-title text-center">
											Autumn Variations
										</div>
										<div class="text-caption stat-card-year text-center">
											2023
										</div>
									</v-card>
								</v-col>
							</v-row>
							<!-- End Stat Cards Row -->
							<h2 class="artist-discography-title">Discography</h2>
							<v-row aria-label="Albums List">
								<v-col
									v-for="(release, index) in data.discography"
									:key="index"
									cols="12"
									sm="6"
									md="4"
									lg="3"
								>
									<article aria-labelledby="album-title-{{index}}">
										<v-card class="artist-discography-album-card" outlined>
											<v-img
												v-if="!loadingImages"
												:src="getDiscographyImage(release.master_id)"
												height="160"
												width="160"
												class="artist-discography-album-img"
												contain
												:alt="`Release cover`"
											/>
											<v-img
												v-else
												src="/images/UnknownSong.png"
												height="160"
												width="160"
												class="artist-discography-album-img"
												contain
												:alt="`Release cover`"
											/>
											<v-card-title>
												<router-link
													:key="index"
													:to="`/master/${release.master_id}`"
													:aria-label="`View details for album`"
													class="artist-discography-album-link"
													>{{ release.title }}</router-link
												>
											</v-card-title>
										</v-card>
									</article>
								</v-col>
							</v-row>
						</v-card>
					</div>
				</div>

				<div v-if="!data" class="loading" role="status" aria-live="polite">
					Loading...
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
		name: "ArtistPage",
		components: {
			Navbar,
			RatingSystem,
		},
		data() {
			return {
				data: {
					artist: [],
					discography: [],
					aliases: [],
				},
				loading: true,
				loadingImages: true,
				image_uri: "",
				discography_images: {},
				sortBy: "release_date",
			};
		},
		methods: {
			getArtistImage() {
				console.log("Artist data in getArtistImage:", this.data); // Debug log
				console.log("Artist images:", this.data.artist?.[0]?.images); // Debug log
				const artistImage = this.data.artist?.[0]?.images?.[0]?.uri;
				console.log("Selected image URL:", artistImage); // Debug log
				return artistImage || "/images/UnknownPerson.png";
			},

			async getArtist() {
				try {
					console.log("Fetching artist with ID:", this.$route.params.artist_id); // Debug log
					const response = await axios.get("http://localhost:5001/artist", {
						params: { artist_id: this.$route.params.artist_id },
					});
					console.log("Raw API response:", response.data); // Debug log
					this.data = response.data.payload;

					if (this.data.api_data.images && this.data.api_data.images.length) {
						this.image_uri = this.data.api_data.images[0].uri;
						this.image_uri =
							this.image_uri === ""
								? "/images/UnknownSong.png"
								: this.image_uri;
					} else {
						this.image_uri = "/images/UnknownSong.png";
					}

					this.loading = false;
					console.log("Processed artist data:", this.data); // Debug log
				} catch (error) {
					console.error("Error fetching artist:", error);
					console.log("Error details:", error.response?.data); // Debug log
					this.loading = false;
				}
			},

			async getDiscographyImages() {
				try {
					console.log(
						"Fetching discography images with ID:",
						this.$route.params.artist_id
					);
					const response = await axios.get(
						"http://localhost:5001/artist-discography-images",
						{
							params: { artist_id: this.$route.params.artist_id },
						}
					);
					console.log("Raw API response:", response.data);
					this.discography_images = response.data.payload;
					this.loadingImages = false;
					console.log(
						"Processed discography image data:",
						this.discography_images
					); // Debug log
				} catch (error) {
					console.error("Error fetching artist:", error);
					console.log("Error details:", error.response?.data); // Debug log
					this.loadingImages = false;
				}
			},

			getDiscographyImage(masterId) {
				const image = this.discography_images[masterId];
				return image || "/images/UnknownSong.png";
			},
		},
		created() {
			this.getArtist();
			this.getDiscographyImages();
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";
	@import "../../src/assets/accessibility.css";

	.artist-page-flex {
		display: flex;
		gap: 32px;
		align-items: flex-start;
		max-width: 1400px;
		margin: 0 auto;
	}
	.artist-sidebar-header {
		background: linear-gradient(135deg, #3cba92, #2c7a7b);
		border-radius: 36px;
		padding: 36px 24px 36px 24px;
		min-width: 370px;
		max-width: 420px;
		display: flex;
		flex-direction: column;
		align-items: center;
		color: #fff;
		box-shadow: 0 4px 24px rgba(44, 122, 123, 0.13);
		margin-top: 0;
	}
	.artist-avatar {
		border: 4px solid rgba(255, 255, 255, 0.9);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		width: 140px;
		height: 140px;
	}
	.artist-header-title {
		color: #fff;
		font-size: 2.1rem;
		font-weight: bold;
		margin-bottom: 10px;
		line-height: 1.2;
		text-align: center;
	}
	.artist-header-chips {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
		justify-content: center;
		margin-bottom: 8px;
	}
	.artist-chip {
		background: #e0f7fa;
		color: #2c7a7b;
		font-weight: 600;
		font-size: 0.95rem;
		border-radius: 12px;
		padding: 2px 12px;
	}
	.artist-header-stars {
		margin-bottom: 8px;
	}
	.artist-header-bio {
		margin-top: 18px;
		color: #e0f2f1;
		font-size: 1.08rem;
		text-align: center;
		word-break: break-word;
	}
	.artist-main-content {
		flex: 1;
		min-width: 0;
		margin-top: 0;
	}
	.artist-stats-row {
		max-width: 1100px;
		margin: 0 auto 0 auto;
	}
	.artist-stat-card {
		border-radius: 16px;
		background: linear-gradient(135deg, #3cba92, #2c7a7b);
		color: white;
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 2px 12px rgba(44, 122, 123, 0.13);
		transition: all 0.2s ease;
		margin-bottom: 18px;
		min-height: 120px;
		display: flex;
		flex-direction: column;
		justify-content: center;
	}
	.stat-card-flex {
		display: flex;
		flex-direction: column;
		justify-content: center;
		height: 100%;
	}
	.stat-card-content {
		min-height: 56px;
	}
	.stat-card-img {
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(44, 122, 123, 0.13);
		background: #fff;
	}
	.stat-card-title {
		font-size: 1.15rem;
		font-weight: 700;
		color: #fff;
		margin-bottom: 2px;
	}
	.stat-card-year {
		color: #b2dfdb;
		font-size: 0.98rem;
	}
	.artist-discography-card {
		background: #fff;
		border-radius: 28px;
		box-shadow: 0 6px 32px rgba(44, 122, 123, 0.1);
		padding: 36px 32px;
		margin: 0 auto 36px auto;
		max-width: 1100px;
	}
	.artist-discography-title {
		color: #2c7a7b;
		font-size: 1.6rem;
		font-weight: 700;
		margin-bottom: 24px;
		margin-top: 0;
		letter-spacing: 0.5px;
	}
	.artist-discography-album-card {
		background: rgba(255, 255, 255, 0.68);
		backdrop-filter: blur(8px);
		border-radius: 18px;
		box-shadow: 0 4px 18px rgba(44, 122, 123, 0.1);
		transition: transform 0.18s, box-shadow 0.18s;
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: 24px;
	}
	.artist-discography-album-card:hover {
		transform: translateY(-6px) scale(1.03);
		box-shadow: 0 8px 32px rgba(44, 122, 123, 0.18);
	}
	.artist-discography-album-img {
		border-radius: 14px;
		box-shadow: 0 4px 16px rgba(44, 122, 123, 0.1);
		margin-bottom: 10px;
		object-fit: cover;
	}
	.artist-discography-album-link {
		color: #2c7a7b;
		font-weight: 700;
		font-size: 1.1rem;
		text-decoration: none;
		transition: color 0.18s;
	}
	.artist-discography-album-link:hover {
		color: #3cba92;
		text-decoration: underline;
	}
	.stat-card-vertical {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 200px;
		padding: 24px 0 24px 0;
	}
	.stat-card-img {
		border-radius: 12px;
		box-shadow: 0 2px 8px rgba(44, 122, 123, 0.13);
		background: #fff;
		object-fit: cover;
	}
	.stat-card-title {
		font-size: 1.15rem;
		font-weight: 700;
		color: #fff;
		margin-bottom: 2px;
	}
	.stat-card-year {
		color: #b2dfdb;
		font-size: 0.98rem;
	}
	.stat-card-rating-number {
		font-size: 3.2rem;
		font-weight: 900;
		color: #fff;
		text-align: center;
		margin-bottom: 6px;
		margin-top: 2px;
		letter-spacing: 1px;
	}
</style>
