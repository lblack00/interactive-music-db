<!-- This file was written by Jax Hendrickson -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<div role="alert" v-if="error">
				<v-alert type="error" class="ma-4" variant="tonal">
					{{ error }}
				</v-alert>
			</div>

			<main>
				<v-container class="py-4">
					<!-- Header Card -->
					<v-card class="header-card mb-8" elevation="0">
						<div class="header-content pa-8">
							<h1
								id="page-title"
								class="text-h3 font-weight-bold text-white mb-2"
							>
								Upcoming Releases
							</h1>
							<p class="text-subtitle-1 text-white text-opacity-70">
								Stay updated with the latest music releases
							</p>
						</div>
						<div class="header-pattern"></div>
					</v-card>

					<div
						v-if="loading"
						class="d-flex flex-column justify-center align-center min-vh-50"
						role="status"
						aria-label="Loading content"
					>
						<v-progress-circular
							indeterminate
							color="teal-accent-3"
							size="64"
							aria-hidden="true"
						></v-progress-circular>
						<span class="mt-4 text-h6">Loading releases...</span>
					</div>

					<div v-else>
						<div v-if="Object.keys(groupedAlbums).length > 0">
							<section
								v-for="(albums, date) in groupedAlbums"
								:key="date"
								class="release-section mb-8"
								role="region"
								:aria-labelledby="`date-${date}`"
							>
								<!-- Date Container -->
								<v-card class="date-container mb-6" elevation="0">
									<v-card-item class="py-5 px-6">
										<div
											class="d-flex align-center justify-space-between flex-wrap gap-4"
										>
											<div class="date-info">
												<div class="date-display">
													<div class="primary-date">
														<span class="date-month">{{
															formatDatePart(date, "month").toUpperCase()
														}}</span>
														<span class="date-day">{{
															formatDatePart(date, "day")
														}}</span>
														<span class="date-year">{{
															formatDatePart(date, "year")
														}}</span>
													</div>
													<div class="date-divider"></div>
													<div class="secondary-info">
														<span class="date-weekday">{{
															formatDatePart(date, "weekday")
														}}</span>
														<span class="releases-count"
															>{{ albums.length }} release{{
																albums.length !== 1 ? "s" : ""
															}}</span
														>
													</div>
												</div>
											</div>
											<v-chip
												:color="getCountdownColor(date)"
												variant="elevated"
												size="large"
												class="countdown-chip"
											>
												{{ calculateCountdown(date) }}
											</v-chip>
										</div>
									</v-card-item>

									<v-row class="px-4 pb-6">
										<v-col
											v-for="album in albums"
											:key="album.id"
											cols="12"
											sm="6"
											md="4"
											class="py-2"
										>
											<v-card class="album-card h-100" elevation="2">
												<div class="album-image-container">
													<v-img
														:src="getAlbumCover(album)"
														height="280"
														cover
														:alt="`Album cover for ${album.title}`"
													>
														<template v-slot:placeholder>
															<div
																class="d-flex align-center justify-center fill-height"
															>
																<v-progress-circular
																	indeterminate
																	color="teal-accent-3"
																	size="32"
																></v-progress-circular>
															</div>
														</template>
													</v-img>
													<div v-if="currentUser" class="album-overlay">
														<v-btn
															:icon="
																album.isFavorite
																	? 'mdi-heart'
																	: 'mdi-heart-outline'
															"
															:color="album.isFavorite ? 'error' : 'white'"
															variant="text"
															size="x-large"
															@click="toggleFavorite(album)"
															:aria-label="`${
																album.isFavorite ? 'Remove from' : 'Add to'
															} favorites`"
															class="favorite-btn"
														></v-btn>
													</div>
												</div>

												<v-card-item class="pt-4 pb-2">
													<v-card-title
														class="text-h6 font-weight-bold mb-1 text-truncate"
													>
														{{ album.title }}
													</v-card-title>
													<v-card-subtitle
														class="text-subtitle-1 text-medium-emphasis"
													>
														{{ album.artist }}
													</v-card-subtitle>
												</v-card-item>

												<v-card-actions class="px-4 pb-4 pt-2">
													<v-btn
														block
														color="teal"
														variant="elevated"
														prepend-icon="mdi-bell-ring-outline"
														@click="notifyUser(album)"
														:aria-label="`Get notified when ${album.title} is released`"
														class="notify-btn"
													>
														Notify Me
													</v-btn>
												</v-card-actions>
											</v-card>
										</v-col>
									</v-row>
								</v-card>
							</section>
						</div>

						<div v-else class="empty-state" role="status">
							<div class="empty-state-content">
								<v-icon size="64" color="teal" class="mb-4"
									>mdi-music-note-outline</v-icon
								>
								<h3 class="text-h4 font-weight-medium mb-2">
									No Upcoming Releases
								</h3>
								<p class="text-subtitle-1 text-medium-emphasis mb-6">
									Check back soon for new music releases
								</p>
								<v-btn
									color="teal"
									variant="elevated"
									size="large"
									prepend-icon="mdi-refresh"
									@click="fetchReleases"
									class="empty-state-btn"
								>
									Refresh
								</v-btn>
							</div>
						</div>
					</div>
				</v-container>
			</main>

			<!-- Add login prompt dialog -->
			<v-dialog v-model="showLoginPrompt" max-width="400px">
				<v-card class="login-prompt-card">
					<v-card-text class="text-center pa-6">
						<v-icon size="48" color="primary" class="mb-4"
							>mdi-account-lock</v-icon
						>
						<h3 class="text-h5 font-weight-bold mb-3">Please Log In</h3>
						<p class="text-subtitle-1 text-medium-emphasis mb-6">
							You need to log in to do that.
						</p>
						<div class="d-flex justify-center mb-4 gap-3">
							<v-btn color="primary" class="action-btn" @click="goToLogin">
								Log In
							</v-btn>
							<v-btn color="secondary" class="action-btn" @click="goToSignup">
								Sign Up
							</v-btn>
						</div>
						<v-btn
							variant="text"
							color="grey-darken-1"
							@click="showLoginPrompt = false"
							class="cancel-btn"
						>
							Cancel
						</v-btn>
					</v-card-text>
				</v-card>
			</v-dialog>
		</div>
	</div>
</template>

<script>
	import Navbar from "./Navbar.vue";
	import axios from "axios";

	export default {
		name: "Countdown",
		components: {
			Navbar,
		},
		data() {
			return {
				albums: [],
				loading: true,
				error: null,
				showLoginPrompt: false,
				currentUser: null,
			};
		},
		computed: {
			groupedAlbums() {
				return this.albums.reduce((acc, album) => {
					(acc[album.release_date] = acc[album.release_date] || []).push({
						...album,
						isFavorite: false,
					});
					return acc;
				}, {});
			},
		},
		methods: {
			async fetchReleases() {
				this.loading = true;
				this.error = null;

				try {
					const response = await axios.get(
						"http://localhost:5001/upcoming-releases"
					);
					this.albums = response.data.releases || [];
				} catch (error) {
					console.error("Error fetching releases:", error);
					this.error = "Unable to load releases. Please try again later.";
				} finally {
					this.loading = false;
				}
			},
			calculateCountdown(releaseDate) {
				const now = new Date();
				const release = new Date(releaseDate);
				const diffTime = release - now;
				const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

				if (diffDays < 0) return "Released";
				if (diffDays === 0) return "Out Today!";
				if (diffDays === 1) return "Tomorrow!";
				return `${diffDays} Days Left`;
			},
			getCountdownColor(releaseDate) {
				const diffDays = Math.ceil(
					(new Date(releaseDate) - new Date()) / (1000 * 60 * 60 * 24)
				);
				if (diffDays < 0) return "grey";
				if (diffDays === 0) return "teal-accent-3";
				if (diffDays <= 7) return "teal-accent-2";
				return "teal-accent-1";
			},
			formatDatePart(dateStr, part) {
				const date = new Date(dateStr);
				const options = {
					month: { month: "short" },
					day: { day: "numeric" },
					year: { year: "numeric" },
					weekday: { weekday: "long" },
				};

				return new Intl.DateTimeFormat("en-US", options[part]).format(date);
			},
			async checkUserSession() {
				try {
					const response = await axios.get(
						"http://localhost:5001/check-session",
						{
							withCredentials: true,
						}
					);
					if (response.data.logged_in) {
						this.currentUser = response.data.user;
					}
				} catch (error) {
					console.error("Error checking session:", error);
				}
			},
			notifyUser(album) {
				if (!this.currentUser) {
					this.showLoginPrompt = true;
					return;
				}

				this.$nextTick(() => {
					alert(
						`You'll be notified when "${album.title}" by ${album.artist} is released!`
					);
				});
			},
			toggleFavorite(album) {
				album.isFavorite = !album.isFavorite;
			},
			getAlbumCover(album) {
				return `https://placehold.co/600x600/14B8A6/FFFFFF?text=${encodeURIComponent(
					album.title
				)}`;
			},
			goToLogin() {
				const returnTo = this.$route.fullPath;
				this.showLoginPrompt = false;
				this.$router.push(`/login?returnTo=${encodeURIComponent(returnTo)}`);
			},
			goToSignup() {
				const returnTo = this.$route.fullPath;
				this.showLoginPrompt = false;
				this.$router.push(`/signup?returnTo=${encodeURIComponent(returnTo)}`);
			},
		},
		async created() {
			await this.checkUserSession();
			await this.fetchReleases();
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";
	@import "../../src/assets/accessibility.css";
	@import "../../src/assets/v-card.css";

	.min-vh-50 {
		min-height: 50vh;
	}

	.header-card {
		background: linear-gradient(135deg, #3cba92, #2c7a7b) !important;
		border-radius: 24px;
		position: relative;
		overflow: hidden;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.header-content {
		position: relative;
		z-index: 2;
	}

	.header-pattern {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: radial-gradient(
				circle at 20% 150%,
				rgba(255, 255, 255, 0.12) 0%,
				transparent 50%
			),
			radial-gradient(
				circle at 80% -50%,
				rgba(255, 255, 255, 0.12) 0%,
				transparent 50%
			);
		z-index: 1;
	}

	.date-container {
		background: linear-gradient(
			to bottom right,
			rgba(255, 255, 255, 0.95),
			rgba(255, 255, 255, 0.85)
		) !important;
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border-radius: 20px;
		overflow: hidden;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05),
			inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
		border: 1px solid rgba(255, 255, 255, 0.3);
	}

	.date-info {
		flex: 1;
		min-width: 300px;
	}

	.date-display {
		display: flex;
		align-items: center;
		gap: 1.5rem;
	}

	.primary-date {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.date-month {
		font-size: 2.5rem;
		font-weight: 600;
		color: #14b8a6;
		letter-spacing: 0.5px;
	}

	.date-day {
		font-size: 2.5rem;
		font-weight: 600;
		color: #334155;
		margin-right: 0.5rem;
	}

	.date-year {
		font-size: 2.5rem;
		color: #64748b;
		font-weight: 500;
		margin-left: -0.25rem;
	}

	.date-divider {
		width: 1px;
		height: 2.5rem;
		background: linear-gradient(to bottom, #64748b40, transparent);
		margin: 0 1rem;
	}

	.secondary-info {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		padding-top: 0.25rem;
	}

	.date-weekday {
		font-size: 1.25rem;
		color: #64748b;
		font-weight: 400;
	}

	.releases-count {
		font-size: 0.95rem;
		color: #64748b;
	}

	.album-card {
		background: linear-gradient(
			135deg,
			rgba(255, 255, 255, 0.95),
			rgba(255, 255, 255, 0.9)
		) !important;
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border-radius: 16px;
		overflow: hidden;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		display: flex;
		flex-direction: column;
		border: 1px solid rgba(255, 255, 255, 0.3);
	}

	.album-card:hover {
		transform: translateY(-4px);
		box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1),
			inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
		background: linear-gradient(
			135deg,
			rgba(255, 255, 255, 0.98),
			rgba(255, 255, 255, 0.95)
		) !important;
	}

	.album-image-container {
		position: relative;
		overflow: hidden;
	}

	.album-image-container::after {
		content: "";
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(to bottom, transparent 60%, rgba(0, 0, 0, 0.2));
		pointer-events: none;
	}

	.album-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(to bottom, rgba(0, 0, 0, 0.4), transparent);
		opacity: 0;
		transition: opacity 0.3s ease;
		display: flex;
		justify-content: flex-end;
		padding: 16px;
		z-index: 2;
	}

	.album-card:hover .album-overlay {
		opacity: 1;
	}

	.notify-btn {
		background: linear-gradient(135deg, #14b8a6, #0d9488) !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
		font-weight: 500;
		letter-spacing: 0.5px;
		transition: all 0.2s ease;
		text-transform: none;
		height: 44px;
	}

	.notify-btn:hover {
		transform: translateY(-1px);
		background: linear-gradient(135deg, #0d9488, #0f766e) !important;
	}

	.empty-state {
		text-align: center;
		padding: 4rem 2rem;
		background: linear-gradient(
			135deg,
			rgba(255, 255, 255, 0.95),
			rgba(255, 255, 255, 0.85)
		) !important;
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border-radius: 20px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05),
			inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
		border: 1px solid rgba(255, 255, 255, 0.3);
	}

	.empty-state-content {
		max-width: 400px;
		margin: 0 auto;
	}

	.empty-state-btn {
		text-transform: none;
		height: 48px;
		min-width: 160px;
	}

	.countdown-chip {
		background: linear-gradient(
			135deg,
			rgba(20, 184, 166, 0.15),
			rgba(20, 184, 166, 0.1)
		) !important;
		backdrop-filter: blur(8px);
		-webkit-backdrop-filter: blur(8px);
		border: 1px solid rgba(20, 184, 166, 0.2);
		color: #0f766e !important;
		height: 40px;
		font-size: 0.95rem;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
	}

	.text-medium-emphasis {
		color: rgba(0, 0, 0, 0.6) !important;
	}

	/* Add subtle animations */
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.release-section {
		animation: fadeIn 0.3s ease-out;
	}

	/* Add responsive adjustments */
	@media (max-width: 600px) {
		.date-display {
			flex-direction: column;
			align-items: flex-start;
			gap: 1rem;
		}

		.date-divider {
			width: 100%;
			height: 1px;
			margin: 0.5rem 0;
		}
	}

	/* Login prompt dialog styles */
	.login-prompt-card {
		border-radius: 24px;
		overflow: hidden;
		background: white;
		position: relative;
	}

	.login-prompt-card::before {
		content: "";
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 4px;
		background: linear-gradient(90deg, var(--primary-color) 0%, #1de9b6 100%);
	}

	.action-btn {
		min-width: 120px;
		font-weight: 600;
		letter-spacing: 0.5px;
		border-radius: 12px;
		text-transform: none;
	}

	.cancel-btn {
		font-weight: 500;
		letter-spacing: 0.5px;
		text-transform: none;
	}

	/* High contrast mode styles */
	.high-contrast .login-prompt-card {
		background: #000000 !important;
		border: 2px solid #ffffff !important;
	}

	.high-contrast .login-prompt-card::before {
		background: #ffffff !important;
	}

	.high-contrast .action-btn {
		background: #000000 !important;
		color: #ffffff !important;
		border: 2px solid #ffffff !important;
	}

	.high-contrast .action-btn:hover {
		background: #ffffff !important;
		color: #000000 !important;
	}

	.high-contrast .cancel-btn {
		color: #ffffff !important;
	}

	.high-contrast .cancel-btn:hover {
		background: rgba(255, 255, 255, 0.1) !important;
	}
</style>
