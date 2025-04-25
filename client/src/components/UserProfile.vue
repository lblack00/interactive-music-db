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
										<v-img
											:src="user.profileImage"
											alt="Profile"
										></v-img>
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
													<v-timeline density="compact" align="start">
														<v-timeline-item
															v-for="(
																activity, index
															) in userMetrics.recentActivity"
															:key="index"
															:dot-color="getActivityColor(activity.type)"
															size="small"
														>
															<template v-slot:opposite>
																<div class="text-caption">
																	{{ formatDate(activity.date) }}
																</div>
															</template>
															<div class="timeline-content">
																<div class="text-subtitle-2 font-weight-medium">
																	{{ activity.title }}
																</div>
																<div class="text-caption text-medium-emphasis">
																	{{ activity.description }}
																</div>
															</div>
														</v-timeline-item>
													</v-timeline>
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
							date: "2024-03-15",
							title: "New Rating",
							description: "Gave 'Bohemian Rhapsody' 5 stars",
						},
						{
							type: "listen",
							date: "2024-03-14",
							title: "Album Completed",
							description: "Finished 'Dark Side of the Moon'",
						},
						{
							type: "discovery",
							date: "2024-03-13",
							title: "New Discovery",
							description: "Added Jazz Fusion to favorite genres",
						},
						{
							type: "discovery",
							date: "2024-03-13",
							title: "New Discovery",
							description: "Added Jazz Fusion to favorite genres",
						},
						{
							type: "discovery",
							date: "2024-03-13",
							title: "New Discovery",
							description: "Added Jazz Fusion to favorite genres",
						},
					],
				},
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
					const response = await axios.get(`http://localhost:5001/get-user-id/${this.user.username}`);
					this.user.id = response.data.id;
				} catch (error) {
					console.error("Error finding user:", error);
					this.$router.push('/404');
					return; // stop here if the user doesn't exist
				}

				// Attempt to load profile image (fail gracefully)
				try {
					const imageResponse = await axios.get(
						`http://localhost:5001/get-profile-image/${this.user.id}`
					);
					this.user.profileImage = `http://localhost:5001${imageResponse.data.image_url}`;
				} catch (error) {
					console.warn("Failed to load profile image:", error);
					this.user.profileImage = null; // or a default placeholder if you'd like
				}

				// Attempt to load bio (fail gracefully)
				try {
					const bioResponse = await axios.get(`http://localhost:5001/get-bio/${this.user.id}`);
					this.user.bio = bioResponse.data.bio;
				} catch (error) {
					console.warn("Failed to load bio:", error);
					this.user.bio = ""; // or a default message like "No bio available"
				}
				this.fetchUserRatingStats(this.user.id);
				const activities = await this.getRecentUserActivity(this.user.id, 5);  // Fetch top 5 recent activities
    		console.log(activities);  // Log or handle the activities as needed
			},
			async fetchUserRatingStats(userId) {
				try {
					const response = await axios.get('http://localhost:5001/user-rating-stats', {
						params: { user_id: userId },
						withCredentials: true
					});

					if (response.status === 200) {
						const { total_ratings, average_rating } = response.data;
						console.log(`Total Ratings: ${total_ratings}, Average Rating: ${average_rating}`);
						// Store the values in your component's data if needed
						this.userMetrics.totalRatings = total_ratings;
						this.userMetrics.averageRating = parseFloat(average_rating).toFixed(2);
					}
				} catch (error) {
					console.error('Failed to fetch user rating stats:', error);
				}
			},
			async getRecentUserActivity(userId, limit = 10) {
					try {
							const response = await axios.get('http://localhost:5001/user-recent-activity', {
									params: { user_id: userId, limit: limit },
									withCredentials: true
							});
							
							if (response.status === 200) {
									return response.data;  // Returns the recent activity list
							} else {
									console.log('No activity found');
							}
					} catch (error) {
							console.error('Error fetching recent activity:', error);
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
					rating: "#3cba92",
					listen: "#2c7a7b",
					discovery: "#3cba92",
				};
				return colors[type] || "#3cba92";
			},
			formatDate(dateString) {
				return format(new Date(dateString), "MMM d");
			},
		},
		created() {
			this.getProfile();
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
	.activity-card ::-webkit-scrollbar {
		width: 6px;
	}

	.activity-card ::-webkit-scrollbar-track {
		background: #f1f1f1;
		border-radius: 3px;
	}

	.activity-card ::-webkit-scrollbar-thumb {
		background: rgba(67, 97, 238, 0.5);
	}

	.activity-card ::-webkit-scrollbar-thumb:hover {
		background: rgba(67, 97, 238, 0.7);
	}

	/* Update Vuetify theme colors */
	:deep(.v-timeline-item__dot) {
		background-color: #4361ee;
	}

	:deep(.v-progress-linear__determinate) {
		background-color: #4361ee;
	}

	:deep(.v-chip) {
		background-color: rgba(67, 97, 238, 0.1);
		color: #4361ee;
	}

	:deep(.v-chip--elevated) {
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}
</style>
