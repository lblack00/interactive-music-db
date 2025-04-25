<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<v-container>
				<v-row justify="center">
					<v-col cols="12" md="10" lg="8">
						<!-- Profile Header -->
						<v-card class="profile-header mb-6" elevation="3">
							<v-row no-gutters align="center" class="pa-4">
								<v-col cols="12" sm="auto" class="text-center text-sm-left">
									<v-avatar size="120" class="profile-avatar">
										<v-img :src="user.profileImage" alt="Profile"></v-img>
									</v-avatar>
								</v-col>
								<v-col class="pl-4">
									<h1 class="text-h4 font-weight-bold mb-2">
										{{ user.username }}
									</h1>
									<p class="text-subtitle-1 text-medium-emphasis mb-4">
										{{ user.bio }}
									</p>
									<div class="d-flex flex-wrap gap-2">
										<router-link :to="'/musiclist/' + this.user.username">
											<v-chip
												color="deep-purple"
												prepend-icon="mdi-format-list-bulleted"
												variant="elevated"
											>
												Music List
											</v-chip>
										</router-link>
										<v-chip
											v-if="user.spotifyConnected"
											color="success"
											prepend-icon="mdi-spotify"
											variant="elevated"
										>
											Connected to Spotify
										</v-chip>
										<v-chip
											color="primary"
											prepend-icon="mdi-music-note"
											variant="elevated"
										>
											{{ userMetrics.totalRatings }} Entries Rated
										</v-chip>
										<v-chip
											color="info"
											prepend-icon="mdi-clock-outline"
											variant="elevated"
										>
											{{ userMetrics.totalHours }}h Listened
										</v-chip>
									</div>
								</v-col>
							</v-row>
						</v-card>

						<!-- Main Content -->
						<v-card elevation="3">
							<v-window v-model="activeTab" class="pa-6">
								<v-window-item value="metrics">
									<v-row>
										<!-- Quick Stats -->
										<v-col
											cols="12"
											md="4"
											v-for="stat in quickStats"
											:key="stat.title"
										>
											<v-card
												class="stat-card pa-4"
												:elevation="2"
												:color="stat.color"
											>
												<div class="text-overline mb-1">{{ stat.title }}</div>
												<div class="text-h4 mb-2">{{ stat.value }}</div>
												<div class="text-caption">{{ stat.subtitle }}</div>
											</v-card>
										</v-col>

										<!-- Top Genres -->
										<v-col cols="12" md="6">
											<v-card class="genre-card pa-4" elevation="2">
												<v-card-title class="text-h6">
													<v-icon start color="primary" class="mr-2"
														>mdi-music</v-icon
													>
													Top Genres
												</v-card-title>
												<v-card-text>
													<div
														v-for="genre in userMetrics.topGenres"
														:key="genre.name"
														class="mb-4"
													>
														<div class="d-flex justify-space-between mb-1">
															<span class="text-subtitle-2">{{
																genre.name
															}}</span>
															<span class="text-subtitle-2"
																>{{ genre.percentage }}%</span
															>
														</div>
														<v-progress-linear
															:model-value="genre.percentage"
															:color="getGenreColor(genre.name)"
															height="8"
															rounded
														></v-progress-linear>
													</div>
												</v-card-text>
											</v-card>
										</v-col>

										<!-- Recent Activity -->
										<v-col cols="12" md="6">
											<v-card class="activity-card pa-4" elevation="2">
												<v-card-title class="text-h6">
													<v-icon start color="primary" class="mr-2"
														>mdi-history</v-icon
													>
													Recent Activity
												</v-card-title>
												<v-card-text class="pa-0">
													<div class="activity-container">
														<v-timeline density="compact" align="start">
															<v-timeline-item
																v-for="(
																	activity, index
																) in userMetrics.recentActivity"
																:key="index"
																:dot-color="getActivityColor(activity.type)"
																size="small"
																class="w-100"
															>
																<div class="timeline-content w-100">
																	<!-- Title and time on the same line -->
																	<div
																		class="d-flex justify-space-between align-center w-100"
																	>
																		<div
																			class="text-subtitle-2 font-weight-medium"
																		>
																			<router-link
																				:to="activity.url"
																				class="text-decoration-none text-primary"
																				style="color: inherit"
																			>
																				{{ activity.title }}
																			</router-link>
																		</div>
																		<div
																			class="text-caption text-medium-emphasis"
																		>
																			{{ timeAgo(activity.date) }}
																		</div>
																	</div>

																	<!-- Description below -->
																	<div
																		class="text-caption text-medium-emphasis mt-1"
																	>
																		{{ activity.description }}
																	</div>
																</div>
															</v-timeline-item>
														</v-timeline>
													</div>
													<div class="activity-footer">
														<v-btn
															variant="text"
															color="primary"
															class="mt-2"
															@click="loadMoreActivities"
														>
															View More Activity
															<v-icon end>mdi-chevron-down</v-icon>
														</v-btn>
													</div>
												</v-card-text>
											</v-card>
										</v-col>
									</v-row>
								</v-window-item>
							</v-window>
						</v-card>
					</v-col>
				</v-row>
			</v-container>
		</div>
	</div>
</template>

<script>
	import Navbar from "./Navbar.vue";
	import { format } from "date-fns";
	import axios from "axios";

	export default {
		name: "UserSettings",
		components: { Navbar },
		data() {
			return {
				activeTab: "metrics",
				user: {
					username: this.$route.params.username,
					id: null,
					bio: null,
					spotifyConnected: true,
					profileImage: null,
				},
				userMetrics: {
					totalHours: 247,
					totalRatings: null,
					averageRating: null,
					topGenres: [
						{ name: "Rock", percentage: 35 },
						{ name: "Pop", percentage: 25 },
						{ name: "Jazz", percentage: 20 },
						{ name: "Classical", percentage: 15 },
						{ name: "Electronic", percentage: 5 },
					],
					recentActivity: [
						{
							type: "rating",
							date: "Thu, 24 Apr 2025 21:47:05 GMT",
							title: "New Rating",
							description: "Gave '/master/5' 5 stars",
							url: "/master/5",
						},
					],
				},
				currentTime: null,
				clientId: import.meta.env.VITE_SPOTIFY_CLIENT_ID,
				redirectUri: "http://localhost:5173/",
				accessToken: "",
			};
		},
		computed: {
			quickStats() {
				return [
					{
						title: "LISTENING TIME",
						value: `${this.userMetrics.totalHours}h`,
						subtitle: "Total hours of music enjoyed",
						color: "#3cba92",
					},
					{
						title: "AVERAGE RATING",
						value: this.userMetrics.averageRating,
						subtitle: "Out of 10 stars",
						color: "#2c7a7b",
					},
					{
						title: "ENTRIES RATED",
						value: this.userMetrics.totalRatings,
						subtitle: "Total ratings given",
						color: "#3cba92",
					},
				];
			},
		},
		methods: {
			async getProfile() {
				try {
					const response = await axios.get(
						`http://localhost:5001/get-user-id/${this.user.username}`
					);
					this.user.id = response.data.id;

					// Attempt to load profile image (fail gracefully)
					try {
						const imageResponse = await axios.get(
							`http://localhost:5001/get-profile-image/${this.user.id}`
						);
						this.user.profileImage = `http://localhost:5001${imageResponse.data.image_url}`;
					} catch (error) {
						console.warn("Failed to load profile image:", error);
						this.user.profileImage = null;
					}

					// Attempt to load bio (fail gracefully)
					try {
						const bioResponse = await axios.get(
							`http://localhost:5001/get-bio/${this.user.id}`
						);
						this.user.bio = bioResponse.data.bio;
					} catch (error) {
						console.warn("Failed to load bio:", error);
						this.user.bio = "";
					}

					// Fetch user rating stats
					await this.fetchUserRatingStats(this.user.id);

					// Fetch recent activities
					const activities = await this.getRecentUserActivity(this.user.id, 10);
					this.userMetrics.recentActivity = activities;
				} catch (error) {
					console.error("Error finding user:", error);
					this.$router.push("/404");
				}
			},
			async fetchUserTopGenres() {
				try {
					const response = await axios.get(
						"http://localhost:5001/user-top-genres",
						{
							params: { user_id: this.user.id },
							withCredentials: true,
						}
					);

					if (response.status === 200) {
						this.userMetrics.topGenres = response.data;
						console.log("Fetched top genres:", this.userMetrics.topGenres);
					}
				} catch (error) {
					console.error("Failed to fetch top genres:", error);
					// Keep default hardcoded genres as fallback
				}
			},
			async fetchUserRatingStats(userId) {
				try {
					console.log("Fetching rating stats for user:", userId);
					const response = await axios.get(
						"http://localhost:5001/user-rating-stats",
						{
							params: { user_id: userId },
							withCredentials: true,
						}
					);

					if (response.status === 200 && response.data) {
						const { total_ratings, average_rating } = response.data;
						console.log("Rating stats response:", response.data);

						// Update the metrics
						this.userMetrics.totalRatings = total_ratings || 0;
						this.userMetrics.averageRating = average_rating
							? parseFloat(average_rating).toFixed(2)
							: "0.00";

						console.log("Updated metrics:", {
							totalRatings: this.userMetrics.totalRatings,
							averageRating: this.userMetrics.averageRating,
						});
					} else {
						console.warn("No rating stats data received");
						this.userMetrics.totalRatings = 0;
						this.userMetrics.averageRating = "0.00";
					}
				} catch (error) {
					console.error("Failed to fetch user rating stats:", error);
					this.userMetrics.totalRatings = 0;
					this.userMetrics.averageRating = "0.00";
				}
			},
			async getRecentUserActivity(userId, limit = 10) {
				try {
					console.log("Fetching recent activity for user:", userId);
					const response = await axios.get(
						"http://localhost:5001/user-recent-activity",
						{
							params: { user_id: userId, limit: limit },
							withCredentials: true,
						}
					);

					if (response.status === 200 && response.data) {
						console.log("Raw API Response:", response.data);

						const processedActivities = response.data.map((activity) => {
							let title = "";
							if (activity.action_type === "artist_rating") {
								title = "New Artist Rating";
							} else if (activity.action_type === "master_rating") {
								title = "New Song Rating";
							} else if (activity.action_type === "forum_thread") {
								title = "New Thread Created";
							} else if (activity.action_type === "forum_reply") {
								title = "New Reply";
							}

							return {
								type: activity.action_type,
								date: activity.created_at,
								title: title,
								description: activity.description,
								url: activity.relevant_url,
							};
						});

						console.log("Processed Activities:", processedActivities);
						return processedActivities;
					} else {
						console.warn("No activity data received");
						return [];
					}
				} catch (error) {
					console.error("Error fetching recent activity:", error);
					return [];
				}
			},
			async initiateSpotifyAuth() {
				try {
					const state = this.generateRandomString(16);
					const codeVerifier = this.generateCodeVerifier();
					const codeChallenge = await this.generateCodeChallenge(codeVerifier);

					localStorage.setItem("spotify_auth_state", state);
					localStorage.setItem("code_verifier", codeVerifier);

					const scope = "user-read-private user-read-email";
					const authUrl = new URL("https://accounts.spotify.com/authorize");
					authUrl.searchParams.append("client_id", this.clientId);
					authUrl.searchParams.append("response_type", "code");
					authUrl.searchParams.append("redirect_uri", this.redirectUri);
					authUrl.searchParams.append("scope", scope);
					authUrl.searchParams.append("state", state);
					authUrl.searchParams.append("code_challenge", codeChallenge);
					authUrl.searchParams.append("code_challenge_method", "S256");

					window.location.href = authUrl.toString();
				} catch (error) {
					console.error("Error initiating Spotify authentication:", error);
				}
			},
			disconnectSpotify() {
				this.user.spotifyConnected = false;
				alert("Disconnected from Spotify");
			},
			generateRandomString(length) {
				let text = "";
				const possible =
					"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
				for (let i = 0; i < length; i++) {
					text += possible.charAt(Math.floor(Math.random() * possible.length));
				}
				return text;
			},
			generateCodeVerifier() {
				const array = new Uint8Array(32);
				window.crypto.getRandomValues(array);
				return btoa(String.fromCharCode.apply(null, array))
					.replace(/\+/g, "-")
					.replace(/\//g, "_")
					.replace(/=+$/, "");
			},
			async generateCodeChallenge(codeVerifier) {
				const encoder = new TextEncoder();
				const data = encoder.encode(codeVerifier);
				const digest = await window.crypto.subtle.digest("SHA-256", data);
				return btoa(String.fromCharCode.apply(null, new Uint8Array(digest)))
					.replace(/\+/g, "-")
					.replace(/\//g, "_")
					.replace(/=+$/, "");
			},
			getGenreColor(genre) {
				const colors = {
					Rock: "#3cba92",
					Pop: "#2c7a7b",
					Jazz: "#3cba92",
					Classical: "#2c7a7b",
					Electronic: "#3cba92",
				};
				return colors[genre] || "#3cba92";
			},
			getActivityColor(type) {
				const colors = {
					master_rating: "#ff6f61", // Coral red for master ratings
					artist_rating: "#f4a300", // A warm amber for artist ratings
					forum_reply: "#2c7a7b",
					forum_thread: "#3cba92",
				};
				return colors[type] || "#000000";
			},
			formatDate(dateString) {
				return format(new Date(dateString), "MMM d");
			},
			timeAgo(dateString) {
				const itemTime = new Date(Date.parse(dateString)).getTime();
				const currentTime = this.currentTime.getTime();
				const diffInSeconds = Math.floor((currentTime - itemTime) / 1000);

				console.log(
					`[timeAgo] Now: ${currentTime} (${new Date(
						currentTime
					).toISOString()}) | Item: ${itemTime} (${new Date(
						itemTime
					).toISOString()}) | Diff: ${diffInSeconds}s`
				);

				const intervals = [
					{ label: "year", seconds: 31536000 },
					{ label: "month", seconds: 2592000 },
					{ label: "day", seconds: 86400 },
					{ label: "hour", seconds: 3600 },
					{ label: "minute", seconds: 60 },
					{ label: "second", seconds: 1 },
				];

				for (const interval of intervals) {
					const count = Math.floor(diffInSeconds / interval.seconds);
					if (count > 0) {
						return `${count} ${interval.label}${count > 1 ? "s" : ""} ago`;
					}
				}

				return "just now";
			},
			async loadMoreActivities() {
				const currentLimit = this.userMetrics.recentActivity.length;
				const newActivities = await this.getRecentUserActivity(
					this.user.id,
					currentLimit + 10
				);
				this.userMetrics.recentActivity = newActivities;
			},
		},
		created() {
			this.currentTime = new Date();
			this.getProfile().then(() => {
				// After profile is loaded and we have user.id
				this.fetchUserTopGenres();
			});
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";

	.profile-header {
		border-radius: 24px;
		background: linear-gradient(135deg, #3cba92, #2c7a7b);
		box-shadow: none;
		color: white;
		position: relative;
		overflow: hidden;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.profile-header::before {
		content: "";
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(
			135deg,
			rgba(255, 255, 255, 0.05) 0%,
			rgba(255, 255, 255, 0) 100%
		);
		pointer-events: none;
	}

	.profile-avatar {
		border: 4px solid rgba(255, 255, 255, 0.9);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	.text-medium-emphasis {
		color: rgba(255, 255, 255, 0.85) !important;
	}

	.stat-card {
		border-radius: 16px;
		background: linear-gradient(135deg, #3cba92, #2c7a7b);
		transition: all 0.2s ease;
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: white;
	}

	.stat-card:hover {
		transform: translateY(-4px);
	}

	.genre-card,
	.activity-card {
		border-radius: 12px;
		height: 100%;
	}

	.timeline-content {
		padding: 12px 16px;
		background-color: rgba(67, 97, 238, 0.08);
		border-radius: 12px;
		margin-bottom: 12px;
		border: 1px solid rgba(67, 97, 238, 0.1);
		width: 100%; /* Ensures the content takes up full width */
		box-sizing: border-box; /* Ensures padding is included in width calculation */
	}

	:deep(.v-timeline-item__body) {
		display: flex;
		width: 100%;
	}

	.timeline-content .text-subtitle-2 {
		color: rgba(0, 0, 0, 0.87);
		font-weight: 500;
	}

	.timeline-content .text-caption.text-medium-emphasis {
		color: rgba(0, 0, 0, 0.6) !important;
	}

	.v-timeline .text-caption {
		color: rgba(0, 0, 0, 0.6);
	}

	.gap-2 {
		gap: 8px;
	}

	/* Custom scrollbar for timeline */
	.activity-container::-webkit-scrollbar {
		width: 4px;
	}

	.activity-container::-webkit-scrollbar-track {
		background: rgba(67, 97, 238, 0.05);
		border-radius: 2px;
	}

	.activity-container::-webkit-scrollbar-thumb {
		background: rgba(67, 97, 238, 0.2);
		border-radius: 2px;
		transition: background 0.2s ease;
	}

	.activity-container::-webkit-scrollbar-thumb:hover {
		background: rgba(67, 97, 238, 0.3);
	}

	/* For Firefox */
	.activity-container {
		scrollbar-width: thin;
		scrollbar-color: rgba(67, 97, 238, 0.2) rgba(67, 97, 238, 0.05);
	}

	.activity-container {
		max-height: 400px;
		overflow-y: auto;
		position: relative;
		padding-right: 8px;
	}

	.activity-container::after {
		content: "";
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		height: 40px;
		background: linear-gradient(
			to bottom,
			rgba(255, 255, 255, 0) 0%,
			rgba(255, 255, 255, 0.8) 50%,
			rgba(255, 255, 255, 1) 100%
		);
		pointer-events: none;
	}

	.activity-footer {
		text-align: center;
		padding-top: 8px;
	}
</style>
