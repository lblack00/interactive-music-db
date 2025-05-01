<!-- This file was written by Matthew Stenvold -->
<template>
	<NotFound v-if="userNotFound" />

	<div v-else class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<v-container>
				<v-row>
					<!-- Left Sidebar (Skinny Scrollable Vertical Card) -->
					<!-- <v-col cols="12" md="2" style="position: fixed">
						<v-card class="pa-4 d-flex flex-column" max-height="80vh">
							<v-card-title>Menu</v-card-title>
							<v-divider></v-divider>
							<v-list class="overflow-y-auto" style="flex: 1">
								<v-list-item>
									<v-btn block>Button 1</v-btn>
								</v-list-item>
								<v-list-item>
									<v-btn block>Button 2</v-btn>
								</v-list-item>
								<v-list-item>
									<v-btn block>Button 3</v-btn>
								</v-list-item>
								<v-list-item>
									<v-btn block>Button 4</v-btn>
								</v-list-item>
								<v-list-item>
									<v-btn block>Button 5</v-btn>
								</v-list-item>
								<v-list-item>
									<v-btn block>Button 6</v-btn>
								</v-list-item>
							</v-list>
						</v-card>
					</v-col> -->

					<!-- Main Content Area -->
					<v-col cols="12">
						<!-- Profile Header -->
						<v-card class="profile-header mb-6" elevation="3">
							<v-row no-gutters align="center" class="pa-4">
								<v-col cols="12" sm="auto" class="text-center text-sm-left">
									<router-link :to="`/user/${username}`">
										<v-avatar size="120" class="profile-avatar">
											<v-img :src="UserProfilePic" alt="Profile"></v-img>
										</v-avatar>
									</router-link>
								</v-col>
								<v-col class="pl-4">
									<h1 class="text-h4 font-weight-bold mb-2">
										{{ username }}'s Music List
									</h1>
									<div class="stats-container">
										<div class="stat-item">
											<div class="stat-value">{{ userSongs.length }}</div>
											<div class="stat-label">Songs Rated</div>
										</div>
										<div class="stat-item">
											<div class="stat-value">{{ userArtists.length }}</div>
											<div class="stat-label">Artists Rated</div>
										</div>
										<div class="stat-item">
											<div class="stat-value">
												{{ averageRatingBackend }}
											</div>
											<div class="stat-label">Avg Rating</div>
										</div>
									</div>
								</v-col>
							</v-row>
						</v-card>

						<!-- Music and Artists Cards -->
						<v-row>
							<v-col cols="12" md="6">
								<v-card class="mb-4 scrollable-card">
									<v-card-title class="gradient-title pa-4">
										<div
											class="d-flex align-center justify-space-between w-100"
										>
											<span>{{ username }}'s Songs</span>
											<div class="list-actions">
												<v-menu offset-y>
													<template v-slot:activator="{ props }">
														<v-btn
															v-bind="props"
															variant="text"
															density="comfortable"
														>
															<v-icon>mdi-sort</v-icon>
															Sort
														</v-btn>
													</template>
													<v-list>
														<v-list-item
															@click="setSort('title', 'asc', 'songs')"
														>
															<v-list-item-title>Title (A-Z)</v-list-item-title>
														</v-list-item>
														<v-list-item
															@click="setSort('title', 'desc', 'songs')"
														>
															<v-list-item-title>Title (Z-A)</v-list-item-title>
														</v-list-item>
														<v-list-item
															@click="setSort('rating', 'desc', 'songs')"
														>
															<v-list-item-title
																>Rating (High to Low)</v-list-item-title
															>
														</v-list-item>
														<v-list-item
															@click="setSort('rating', 'asc', 'songs')"
														>
															<v-list-item-title
																>Rating (Low to High)</v-list-item-title
															>
														</v-list-item>
														<v-list-item
															@click="setSort('date', 'desc', 'songs')"
														>
															<v-list-item-title
																>Date Rated (Newest)</v-list-item-title
															>
														</v-list-item>
														<v-list-item
															@click="setSort('date', 'asc', 'songs')"
														>
															<v-list-item-title
																>Date Rated (Oldest)</v-list-item-title
															>
														</v-list-item>
													</v-list>
												</v-menu>
											</div>
										</div>
									</v-card-title>
									<v-divider></v-divider>
									<v-list v-if="userSongs.length > 0" class="scrollable-list">
										<v-list-item
											v-for="(song, index) in userSongs"
											:key="'user-' + index"
											class="list-item-hover"
										>
											<v-row align="center" class="w-100">
												<!-- Song Title Column -->
												<v-col cols="5">
													<router-link
														:to="`/master/${song.id}`"
														class="text-decoration-none"
													>
														<v-list-item-title
															class="text-primary wrapped-text"
															>{{ song.name }}</v-list-item-title
														>
													</router-link>
												</v-col>

												<!-- Rating Column -->
												<v-col cols="2">
													<v-list-item-subtitle class="rating-text">
														<strong>{{ song.rating }}/10</strong>
													</v-list-item-subtitle>
												</v-col>

												<!-- Date Column -->
												<v-col cols="3">
													<v-list-item-subtitle>{{
														formatDate(song.created_at)
													}}</v-list-item-subtitle>
												</v-col>

												<!-- Action Buttons Column -->
												<v-col cols="2" class="d-flex justify-end">
													<!-- Edit Button -->
													<v-btn
														variant="plain"
														@click="editRating(song, 'master')"
													>
														<v-icon>mdi-pencil</v-icon>
													</v-btn>

													<!-- Delete Button -->
													<v-btn
														v-if="isListOwner"
														variant="plain"
														@click="confirmDelete(song, 'master', index)"
													>
														<v-icon>mdi-delete</v-icon>
													</v-btn>
												</v-col>
											</v-row>
										</v-list-item>
									</v-list>
									<div v-else class="empty-state pa-4 text-center">
										<v-icon size="64" color="grey-lighten-1"
											>mdi-music-note-off</v-icon
										>
										<div class="text-h6 mt-4">No Songs Rated Yet</div>
										<div class="text-body-2 text-grey">
											Start rating some songs to build your list!
										</div>
									</div>
								</v-card>
							</v-col>

							<v-col cols="12" md="6">
								<v-card class="mb-4 scrollable-card">
									<v-card-title class="gradient-title pa-4">
										<div
											class="d-flex align-center justify-space-between w-100"
										>
											<span>{{ username }}'s Artists</span>
											<div class="list-actions">
												<v-menu offset-y>
													<template v-slot:activator="{ props }">
														<v-btn
															v-bind="props"
															variant="text"
															density="comfortable"
														>
															<v-icon>mdi-sort</v-icon>
															Sort
														</v-btn>
													</template>
													<v-list>
														<v-list-item
															@click="setSort('title', 'asc', 'artists')"
														>
															<v-list-item-title>Title (A-Z)</v-list-item-title>
														</v-list-item>
														<v-list-item
															@click="setSort('title', 'desc', 'artists')"
														>
															<v-list-item-title>Title (Z-A)</v-list-item-title>
														</v-list-item>
														<v-list-item
															@click="setSort('rating', 'desc', 'artists')"
														>
															<v-list-item-title
																>Rating (High to Low)</v-list-item-title
															>
														</v-list-item>
														<v-list-item
															@click="setSort('rating', 'asc', 'artists')"
														>
															<v-list-item-title
																>Rating (Low to High)</v-list-item-title
															>
														</v-list-item>
														<v-list-item
															@click="setSort('date', 'desc', 'artists')"
														>
															<v-list-item-title
																>Date Rated (Newest)</v-list-item-title
															>
														</v-list-item>
														<v-list-item
															@click="setSort('date', 'asc', 'artists')"
														>
															<v-list-item-title
																>Date Rated (Oldest)</v-list-item-title
															>
														</v-list-item>
													</v-list>
												</v-menu>
											</div>
										</div>
									</v-card-title>
									<v-divider></v-divider>
									<v-list v-if="userArtists.length > 0" class="scrollable-list">
										<v-list-item
											v-for="(artist, index) in userArtists"
											:key="'user-' + index"
											class="list-item-hover"
										>
											<v-row align="center" class="w-100">
												<!-- Song Title Column -->
												<v-col cols="5">
													<router-link
														:to="`/artist/${artist.id}`"
														class="text-decoration-none"
													>
														<v-list-item-title
															class="text-primary wrapped-text"
															>{{ artist.name }}</v-list-item-title
														>
													</router-link>
												</v-col>

												<!-- Rating Column -->
												<v-col cols="2">
													<v-list-item-subtitle class="rating-text">
														<strong>{{ artist.rating }}/10</strong>
													</v-list-item-subtitle>
												</v-col>

												<!-- Date Column -->
												<v-col cols="3">
													<v-list-item-subtitle>{{
														formatDate(artist.created_at)
													}}</v-list-item-subtitle>
												</v-col>

												<!-- Action Buttons Column -->
												<v-col cols="2" class="d-flex justify-end">
													<!-- Edit Button -->
													<v-btn
														variant="plain"
														@click="editRating(artist, 'artist')"
													>
														<v-icon>mdi-pencil</v-icon>
													</v-btn>

													<!-- Delete Button -->
													<v-btn
														v-if="isListOwner"
														variant="plain"
														@click="confirmDelete(artist, 'artist', index)"
													>
														<v-icon>mdi-delete</v-icon>
													</v-btn>
												</v-col>
											</v-row>
										</v-list-item>
									</v-list>
									<div v-else class="empty-state pa-4 text-center">
										<v-icon size="64" color="grey-lighten-1"
											>mdi-account-music-off</v-icon
										>
										<div class="text-h6 mt-4">No Artists Rated Yet</div>
										<div class="text-body-2 text-grey">
											Start rating some artists to build your list!
										</div>
									</div>
								</v-card>
							</v-col>
						</v-row>

						<!-- Spotify Playlists -->
						<v-row>
							<v-col
								v-for="(playlist, index) in spotifyStore.playlists"
								:key="'spotify-' + index"
								cols="12"
								sm="6"
								md="4"
							>
								<v-card class="mb-4 playlist-card">
									<v-img
										v-if="playlist.images && playlist.images.length > 0"
										:src="playlist.images[0].url"
										height="150"
										cover
									>
										<template v-slot:placeholder>
											<v-row
												class="fill-height ma-0"
												align="center"
												justify="center"
											>
												<v-progress-circular
													indeterminate
													color="grey-lighten-5"
												></v-progress-circular>
											</v-row>
										</template>
									</v-img>
									<v-card-title class="text-truncate">{{
										playlist.name
									}}</v-card-title>
									<v-card-subtitle
										>{{ playlist.tracks.total }} tracks</v-card-subtitle
									>
									<v-card-text class="text-truncate">
										{{
											decodeHTML(playlist.description) ||
											"No description available"
										}}
									</v-card-text>
									<v-card-actions>
										<v-btn
											color="primary"
											variant="elevated"
											@click="playPlaylist(playlist)"
										>
											<v-icon class="mr-2">mdi-play</v-icon>
											Play
										</v-btn>
										<v-spacer></v-spacer>
										<v-btn
											color="success"
											variant="text"
											:href="playlist.external_urls.spotify"
											target="_blank"
										>
											<v-icon small>mdi-spotify</v-icon>
										</v-btn>
										<v-btn icon @click="showPlaylistDetails(playlist)">
											<v-icon>mdi-dots-vertical</v-icon>
										</v-btn>
									</v-card-actions>
								</v-card>
							</v-col>
						</v-row>
					</v-col>
				</v-row>
			</v-container>
		</div>
	</div>

	<!-- Confirmation Dialog -->
	<v-dialog v-model="deleteDialog" max-width="500px">
		<v-card>
			<v-card-title class="headline">Confirm Deletion</v-card-title>
			<v-card-text>
				Are you sure you want to delete this item from your list?
			</v-card-text>
			<v-card-actions>
				<v-btn text @click="cancelDelete">Cancel</v-btn>
				<v-btn color="error" text @click="deleteEntry">Delete</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>

	<v-dialog v-model="ratingDialog" max-width="600px">
		<v-card>
			<v-card-title>Edit Rating</v-card-title>
			<v-card-text>
				<!-- Ownership Note -->
				<div v-if="!isListOwner" class="text-caption text-grey mb-2">
					Note: This will update your own rating, not the list owner's.
				</div>

				<!-- Rating System -->
				<RatingSystem :itemType="currentItemType" :itemId="currentItemId" />
			</v-card-text>
			<v-card-actions class="justify-end">
				<v-btn text @click="handleCloseRatingDialog">Close</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>

	<!-- Playlist Dialog -->
	<v-dialog v-model="playlistDialog" max-width="600px">
		<v-card v-if="selectedPlaylist">
			<v-img
				v-if="selectedPlaylist.images && selectedPlaylist.images.length > 0"
				:src="selectedPlaylist.images[0].url"
				height="200"
				cover
			></v-img>
			<v-card-title>{{ selectedPlaylist.name }}</v-card-title>
			<v-card-subtitle>
				By {{ selectedPlaylist.owner.display_name }} -
				{{ selectedPlaylist.tracks.total }} tracks
			</v-card-subtitle>
			<v-card-text>
				<p>
					{{
						decodeHTML(selectedPlaylist.description) ||
						"No description available"
					}}
				</p>
				<p class="mt-4">
					<strong>Public:</strong> {{ selectedPlaylist.public ? "Yes" : "No" }}
				</p>
				<p>
					<strong>Collaborative:</strong>
					{{ selectedPlaylist.collaborative ? "Yes" : "No" }}
				</p>
			</v-card-text>
			<v-card-actions>
				<v-btn
					color="primary"
					variant="elevated"
					@click="playPlaylistFromDialog()"
				>
					<v-icon class="mr-2">mdi-play</v-icon>
					Play
				</v-btn>
				<v-btn
					color="success"
					variant="text"
					:href="selectedPlaylist.external_urls.spotify"
					target="_blank"
				>
					<v-icon left>mdi-spotify</v-icon>
					Open in Spotify
				</v-btn>
				<v-spacer></v-spacer>
				<v-btn color="grey" variant="text" @click="playlistDialog = false">
					Close
				</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>

	<!-- Now Playing Card -->
	<v-card v-if="currentPlaylistId" class="pa-4 mb-4 now-playing-card">
		<v-card-title class="d-flex align-center">
			<span
				>Now Playing:
				{{ currentPlaylist ? currentPlaylist.name : "Unknown Playlist" }}</span
			>
			<v-spacer></v-spacer>
			<v-btn icon @click="closePlayer">
				<v-icon>mdi-close</v-icon>
			</v-btn>
		</v-card-title>
		<v-divider></v-divider>
		<div class="spotify-player-container">
			<iframe
				:src="`https://open.spotify.com/embed/playlist/${currentPlaylistId}`"
				width="100%"
				height="450"
				frameborder="0"
				allowtransparency="true"
				allow="encrypted-media"
			></iframe>
		</div>
	</v-card>
</template>

<script>
	import Navbar from "./Navbar.vue";
	import axios from "axios";
	import NotFound from "./NotFound.vue";
	import RatingSystem from "./RatingSystem.vue";
	import { useSpotifyStore } from "../stores/spotify";

	export default {
		name: "MusicList",
		components: {
			Navbar,
			NotFound,
			RatingSystem,
		},
		data() {
			return {
				username: this.$route.params.username || "",
				userId: null,
				UserProfilePic: null,
				userSongs: [],
				userTracks: [],
				userArtists: [],
				playlists: [],
				playlistDialog: false,
				selectedPlaylist: null,
				currentPlaylistId: null,
				currentPlaylist: null,
				userNotFound: false,
				isListOwner: false,
				deleteDialog: false, // Controls the visibility of the dialog
				ratingDialog: false,
				itemToDelete: null, // Holds the item data to delete
				itemTypeToDelete: null, // Holds the item type to delete (either 'master' or 'artist')
				itemIndexToDelete: null, // Holds the index of the item in the list to remove
				sortDirection: "desc",
				sortIcon: "mdi-sort-descending",
				averageRatingBackend: "0.00",
			};
		},
		computed: {
			spotifyStore() {
				return useSpotifyStore();
			},
			averageRating() {
				const allRatings = [...this.userSongs, ...this.userArtists].map(
					(item) => item.rating
				);
				if (allRatings.length === 0) return 0;
				return allRatings.reduce((a, b) => a + b, 0) / allRatings.length;
			},
		},
		watch: {
			"$route.params.username": {
				immediate: true,
				handler(newUsername) {
					this.username = newUsername;
					this.initPage(); // Re-run your setup logic here
				},
			},
		},
		async created() {
			await this.initPage();
			this.spotifyStore.fetchSpotifyPlaylists();
		},
		methods: {
			async initPage() {
				await this.getUserId();
				this.getPFP();
				await this.fetchMusicList();
				await this.fetchUserRatingStats(this.userId);
				const savedPlaylistId = localStorage.getItem("lastPlayedPlaylistId");
				const savedPlaylistData = localStorage.getItem(
					"lastPlayedPlaylistData"
				);
				if (savedPlaylistId && savedPlaylistData) {
					this.currentPlaylistId = savedPlaylistId;
					this.currentPlaylist = JSON.parse(savedPlaylistData);
				}
				this.isListOwner = await this.isSessionUser(this.username, "username");
			},
			async getUserId() {
				try {
					const response = await axios.get(
						`http://localhost:5001/get-user-id/${this.username}`
					);
					this.userId = response.data.id;
				} catch (error) {}
			},
			async getPFP() {
				try {
					const imageResponse = await axios.get(
						`http://localhost:5001/get-profile-image/${this.userId}`
					);
					this.UserProfilePic = `http://localhost:5001${imageResponse.data.image_url}`;
				} catch (error) {
					console.warn("Failed to load profile image:", error);
					this.UserProfilePic = null; // or a default placeholder if you'd like
				}
			},
			async isSessionUser(identifier, type = "id") {
				try {
					const response = await axios.get(
						"http://localhost:5001/is-session-user",
						{
							params: {
								identifier: identifier,
								type: type,
							},
							withCredentials: true,
						}
					);

					return response.data.match;
				} catch (error) {
					console.error("Error checking session user:", error);
					return false;
				}
			},
			async fetchMusicList() {
				try {
					const username = this.username; // Get username from data

					const response = await axios.get(
						`http://localhost:5001/api/musiclist/${username}/master`
					);

					// Store the fetched songs into userSongs
					this.userSongs = response.data;
					const response2 = await axios.get(
						`http://localhost:5001/api/musiclist/${username}/artist`
					);

					// Store the fetched artists into user artists
					this.userArtists = response2.data;

					// const response3 = await axios.get(
					// 	`http://localhost:5001/api/musiclist/${username}/release`
					// );

					// // Store the fetched releases into user releases
					// this.userReleases = response3.data;
				} catch (error) {
					console.error("Error fetching music list:", error);

					this.userNotFound = true;
				}
			},
			editRating(item, itemType = "artist") {
				// Set current itemType ('artist' or 'master') and item ID for the dialog
				this.currentItemType = itemType;
				this.currentItemId = item.id; // Both artist and master objects have an 'id' attribute
				this.ratingDialog = true; // Open the dialog
			},
			// Trigger the confirmation dialog
			confirmDelete(item, itemType, index = null) {
				this.itemToDelete = item; // Store the item to be deleted
				this.itemTypeToDelete = itemType; // Store the item type
				this.indexToDelete = index; // Store the index of the item in the list
				this.deleteDialog = true; // Show the confirmation dialog
			},

			// Cancel the deletion
			cancelDelete() {
				this.deleteDialog = false; // Hide the dialog
				this.itemToDelete = null; // Clear the stored item
				this.itemTypeToDelete = null; // Clear the item type
				this.indexToDelete = null; // Clear the index
			},

			// Proceed with the deletion
			async deleteEntry() {
				// Close the dialog
				this.deleteDialog = false;

				// Call deleteRating to delete the rating from the backend and remove it from the list
				await this.deleteRating(
					this.itemTypeToDelete,
					this.itemToDelete.id,
					this.indexToDelete
				);

				// Clear the stored item after deletion
				this.itemToDelete = null;
				this.itemTypeToDelete = null;
				this.indexToDelete = null;
			},

			async deleteRating(itemType, itemId, index = null) {
				try {
					const response = await axios.delete(
						"http://localhost:5001/delete-user-rating",
						{
							params: {
								item_type: itemType,
								item_id: itemId,
							},
							withCredentials: true,
						}
					);

					if (response.data.message === "Rating deleted successfully") {
						console.log(`Rating deleted for ${itemType} with ID ${itemId}`);

						// Remove from local list if index is provided
						if (itemType === "artist" && index !== null) {
							this.userArtists.splice(index, 1);
						} else if (itemType === "master" && index !== null) {
							this.userSongs.splice(index, 1);
						}
					} else {
						console.log(`No rating found for ${itemType} with ID ${itemId}`);
					}
				} catch (error) {
					console.error(
						`Error deleting rating for ${itemType} with ID ${itemId}:`,
						error
					);
				}
			},
			async handleCloseRatingDialog() {
				this.ratingDialog = false;

				if (this.isListOwner) {
					try {
						const response = await axios.get(
							"http://localhost:5001/generic-user-rating",
							{
								params: {
									item_type: this.currentItemType,
									item_id: this.currentItemId,
									user_id: this.userId,
								},
							}
						);

						const data = response.data;

						if (response.status === 200) {
							console.log("Updated Rating:", data.rating);

							// Update the appropriate item in userSongs or userArtists
							const targetArray =
								this.currentItemType === "master"
									? this.userSongs
									: this.userArtists;
							console.log(this.userSongs);
							const itemToUpdate = targetArray.find(
								(item) => item.id === this.currentItemId
							);
							if (itemToUpdate) {
								itemToUpdate.rating = data.rating;
							} else {
								console.warn(
									`Item with ID ${this.currentItemId} not found in ${
										this.currentItemType === "master"
											? "userSongs"
											: "userArtists"
									}`
								);
							}
						} else {
							console.error("Failed to fetch rating:", data.error);
						}
					} catch (error) {
						console.error("Error fetching rating:", error);
					}
				}
			},
			showPlaylistDetails(playlist) {
				this.selectedPlaylist = playlist;
				this.playlistDialog = true;
			},
			playPlaylist(playlist) {
				this.spotifyStore.setCurrentPlaylist(playlist);
				this.playlistDialog = false;
			},
			playPlaylistFromDialog() {
				if (this.selectedPlaylist) {
					this.playPlaylist(this.selectedPlaylist);
				}
			},
			closePlayer() {
				this.currentPlaylistId = null;
				this.currentPlaylist = null;
				localStorage.removeItem("lastPlayedPlaylistId");
				localStorage.removeItem("lastPlayedPlaylistData");
			},
			decodeHTML(html) {
				const txt = document.createElement("textarea");
				txt.innerHTML = html;
				return txt.value;
			},
			setSort(sortBy, order, listType) {
				let arr = listType === "songs" ? this.userSongs : this.userArtists;
				if (sortBy === "title") {
					arr.sort((a, b) => {
						const aTitle = (a.name || "").toLowerCase();
						const bTitle = (b.name || "").toLowerCase();
						if (aTitle < bTitle) return order === "asc" ? -1 : 1;
						if (aTitle > bTitle) return order === "asc" ? 1 : -1;
						return 0;
					});
				} else if (sortBy === "rating") {
					arr.sort((a, b) =>
						order === "asc" ? a.rating - b.rating : b.rating - a.rating
					);
				} else if (sortBy === "date") {
					arr.sort((a, b) => {
						const aDate = new Date(a.created_at);
						const bDate = new Date(b.created_at);
						return order === "asc" ? aDate - bDate : bDate - aDate;
					});
				}
				// Force Vue to update the list
				if (listType === "songs") this.userSongs = [...arr];
				else this.userArtists = [...arr];
			},
			formatDate(dateString) {
				const date = new Date(dateString);
				const now = new Date();
				const diffTime = Math.abs(now - date);
				const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

				if (diffDays === 1) return "Yesterday";
				if (diffDays < 7) return `${diffDays} days ago`;
				if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
				if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
				return `${Math.floor(diffDays / 365)} years ago`;
			},
			async fetchUserRatingStats(userId) {
				try {
					const response = await axios.get(
						"http://localhost:5001/user-rating-stats",
						{
							params: { user_id: userId },
							withCredentials: true,
						}
					);
					if (response.status === 200 && response.data) {
						this.averageRatingBackend = response.data.average_rating
							? parseFloat(response.data.average_rating).toFixed(2)
							: "0.00";
					} else {
						this.averageRatingBackend = "0.00";
					}
				} catch (error) {
					this.averageRatingBackend = "0.00";
				}
			},
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

	.gradient-title {
		background: linear-gradient(135deg, #3cba92, #2c7a7b);
		color: white;
		position: relative;
		overflow: hidden;
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		font-size: 1.5rem;
		padding: 20px 24px;
		border-top-left-radius: 24px;
		border-top-right-radius: 24px;
	}

	.gradient-title::before {
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
		border-top-left-radius: 24px;
		border-top-right-radius: 24px;
	}

	.profile-avatar {
		border: 4px solid rgba(255, 255, 255, 0.9);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	/* Scrollable card styles */
	.scrollable-card {
		height: 600px; /* Fixed height for the card */
		display: flex;
		flex-direction: column;
		border-radius: 24px;
		overflow: hidden; /* This ensures content doesn't overflow rounded corners */
	}

	.scrollable-list {
		flex: 1;
		overflow-y: auto;
		scrollbar-width: thin;
		scrollbar-color: rgba(67, 97, 238, 0.2) rgba(67, 97, 238, 0.05);
		padding: 12px;
	}

	/* Update list items to have rounded corners */
	.v-list-item {
		border-radius: 12px;
		margin-bottom: 8px;
		transition: background-color 0.2s ease;
		align-items: flex-start;
		padding: 12px;
	}

	.v-list-item:hover {
		background-color: rgba(60, 186, 146, 0.05);
	}

	/* High Contrast Mode Styles */
	.high-contrast .profile-header {
		background: #000000 !important;
		border: 2px solid #ffffff !important;
		box-shadow: none !important;
	}

	.high-contrast .profile-header::before {
		display: none !important;
	}

	.high-contrast .profile-avatar {
		border: 2px solid #ffffff !important;
		box-shadow: none !important;
	}

	.high-contrast .gradient-title {
		background: #000000 !important;
		border: 2px solid #ffffff !important;
		box-shadow: none !important;
	}

	.high-contrast .gradient-title::before {
		display: none !important;
	}

	.v-container {
		max-width: 1400px;
		margin: 0 auto;
		padding: 24px;
	}

	.rating-text {
		font-size: 1.1rem;
		color: #3cba92;
		text-align: left;
	}

	/* High Contrast Mode */
	.high-contrast .rating-text {
		color: #ffffff !important;
	}

	.wrapped-text {
		white-space: normal;
		word-wrap: break-word;
		line-height: 1.4;
	}

	.v-row {
		align-items: flex-start;
	}

	.stats-container {
		display: flex;
		gap: 24px;
		margin-top: 16px;
	}

	.stat-item {
		background: rgba(255, 255, 255, 0.1);
		padding: 8px 16px;
		border-radius: 12px;
		text-align: center;
	}

	.stat-value {
		font-size: 1.5rem;
		font-weight: bold;
		color: white;
	}

	.stat-label {
		font-size: 0.875rem;
		color: rgba(255, 255, 255, 0.8);
	}

	.list-item-hover {
		transition: all 0.2s ease;
	}

	.list-item-hover:hover {
		transform: translateX(4px);
		background-color: rgba(60, 186, 146, 0.05);
	}

	.empty-state {
		padding: 48px 24px;
		color: var(--v-text-disabled);
	}

	.list-actions {
		opacity: 0.8;
		transition: opacity 0.2s ease;
	}

	.list-actions:hover {
		opacity: 1;
	}

	/* Animation for list items */
	.v-list-item {
		animation: fadeIn 0.3s ease-in-out;
	}

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

	/* High contrast adjustments */
	.high-contrast .stat-item {
		background: rgba(255, 255, 255, 0.2) !important;
		border: 1px solid rgba(255, 255, 255, 0.3) !important;
	}

	/* Dark Mode Styles */
	.dark-mode .grid-container {
		background-color: #121212 !important;
	}

	.dark-mode .profile-header {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
	}

	.dark-mode .gradient-title {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .gradient-title::before {
		background: linear-gradient(
			135deg,
			rgba(20, 160, 133, 0.15) 0%,
			rgba(20, 160, 133, 0) 100%
		);
	}

	.dark-mode .profile-avatar {
		border: 4px solid rgba(255, 255, 255, 0.2);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
	}

	.dark-mode .scrollable-card {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
	}

	.dark-mode .v-list-item {
		background: transparent !important;
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-list-item:hover {
		background: rgba(255, 255, 255, 0.05) !important;
	}

	.dark-mode .rating-text {
		color: var(--primary-color) !important;
	}

	.dark-mode .stat-item {
		background: rgba(255, 255, 255, 0.05) !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .stat-value {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .stat-label {
		color: rgba(255, 255, 255, 0.7) !important;
	}

	.dark-mode .list-item-hover:hover {
		background: rgba(255, 255, 255, 0.05) !important;
	}

	.dark-mode .v-card-title {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-card-subtitle {
		color: rgba(255, 255, 255, 0.7) !important;
	}

	.dark-mode .v-card-text {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-btn {
		color: rgba(255, 255, 255, 0.9) !important;
		background: #363636 !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .v-btn:hover {
		background: #404040 !important;
		border-color: rgba(255, 255, 255, 0.2);
	}

	.dark-mode .v-btn--icon {
		color: rgba(255, 255, 255, 0.9) !important;
		background: #363636 !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .v-btn--icon:hover {
		background: #404040 !important;
		border-color: rgba(255, 255, 255, 0.2);
	}

	.dark-mode .v-btn.variant--text {
		background: transparent !important;
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-btn.variant--text:hover {
		background: rgba(255, 255, 255, 0.1) !important;
	}

	.dark-mode .v-btn.color--primary {
		background: var(--primary-color) !important;
		color: #ffffff !important;
		border: none;
	}

	.dark-mode .v-btn.color--primary:hover {
		background: #0d9488 !important;
	}

	.dark-mode .v-btn.color--success {
		background: #2e7d32 !important;
		color: #ffffff !important;
		border: none;
	}

	.dark-mode .v-btn.color--success:hover {
		background: #1b5e20 !important;
	}

	.dark-mode .v-btn.color--error {
		background: #c62828 !important;
		color: #ffffff !important;
		border: none;
	}

	.dark-mode .v-btn.color--error:hover {
		background: #b71c1c !important;
	}

	.dark-mode .v-menu .v-list {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .v-menu .v-list-item {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-menu .v-list-item:hover {
		background: rgba(255, 255, 255, 0.1) !important;
	}

	.dark-mode .v-dialog .v-card {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .v-dialog .v-card-title {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-dialog .v-card-text {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-dialog .v-btn {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-dialog .v-btn:hover {
		background: rgba(255, 255, 255, 0.1) !important;
	}

	.dark-mode .now-playing-card {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .playlist-card {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .empty-state {
		color: rgba(255, 255, 255, 0.7) !important;
	}

	.dark-mode .v-divider {
		border-color: rgba(255, 255, 255, 0.1) !important;
	}

	.dark-mode .text-grey {
		color: rgba(255, 255, 255, 0.7) !important;
	}

	.dark-mode .text-caption {
		color: rgba(255, 255, 255, 0.7) !important;
	}
</style>
