<!-- This file was written by Matthew Stenvold -->
<template>
	<NotFound v-if="userNotFound" />

	<div v-else>
		<div class="grid-container">
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

						<!-- Main Content (Music List) -->
						<v-col cols="12" md="9" style="margin-left: 20%">
							<h1 class="text-h4 font-weight-bold mb-4">
								{{ username }}'s Music List
							</h1>

							<!-- User's Music Card -->
							<v-card class="pa-4 mb-4">
								<v-card-title>{{ username }}'s Albums</v-card-title>
								<v-divider></v-divider>
								<v-list>
									<v-list-item
										v-for="(song, index) in userAlbums"
										:key="'user-' + index"
									>
										<v-row align="center" class="w-100">
											<!-- Song Title Column -->
											<v-col cols="4">
												<v-list-item-title>{{ song.name }}</v-list-item-title>
											</v-col>

											<!-- Rating Column -->
											<v-col cols="1">
												<v-list-item-subtitle
													>{{ song.rating }}/10</v-list-item-subtitle
												>
											</v-col>

											<!-- Date Column -->
											<v-col cols="2">
												<v-list-item-subtitle>{{
													new Date(song.created_at).toLocaleDateString()
												}}</v-list-item-subtitle>
											</v-col>
											<!-- Date Column -->
											<v-col cols="2">
												<v-list-item-subtitle>{{
													song.date
												}}</v-list-item-subtitle>
											</v-col>

											<!-- Action Buttons Column -->
											<v-col cols="3" class="d-flex justify-end">
												<!-- Edit Button -->
												<v-btn variant="plain" @click="editSong(song)">
													<v-icon>mdi-pencil</v-icon>
												</v-btn>

												<!-- Delete Button -->
												<v-btn variant="plain" @click="confirmDelete(song, 'master', index)">
													<v-icon>mdi-delete</v-icon>
												</v-btn>

												<!-- Link Button (Opens External URL) -->
												<v-btn variant="plain" :to="`/master/${song.id}`">
													<v-icon>mdi-link</v-icon>
												</v-btn>
											</v-col>
										</v-row>
									</v-list-item>
								</v-list>
							</v-card>

							<!-- User's Artist Card -->
							<v-card class="pa-4 mb-4">
								<v-card-title>{{ username }}'s Artists</v-card-title>
								<v-divider></v-divider>
								<v-list>
									<v-list-item
										v-for="(artist, index) in userArtists"
										:key="'user-' + index"
									>
										<v-row align="center" class="w-100">
											<!-- Song Title Column -->
											<v-col cols="4">
												<v-list-item-title>{{ artist.name }}</v-list-item-title>
											</v-col>

											<!-- Rating Column -->
											<v-col cols="1">
												<v-list-item-subtitle
													>{{ artist.rating }}/10</v-list-item-subtitle
												>
											</v-col>

											<!-- Date Column -->
											<v-col cols="2">
												<v-list-item-subtitle>{{
													new Date(artist.created_at).toLocaleDateString()
												}}</v-list-item-subtitle>
											</v-col>
											<!-- Date Column -->
											<v-col cols="2">
												<v-list-item-subtitle>{{
													artist.date
												}}</v-list-item-subtitle>
											</v-col>

											<!-- Action Buttons Column -->
											<v-col cols="3" class="d-flex justify-end">
												<!-- Edit Button -->
												<v-btn variant="plain" @click="editSong(artist)">
													<v-icon>mdi-pencil</v-icon>
												</v-btn>

												<!-- Delete Button -->
												<v-btn variant="plain" @click="confirmDelete(artist, 'artist', index)">
													<v-icon>mdi-delete</v-icon>
												</v-btn>

												<!-- Link Button (Opens External URL) -->
												<v-btn variant="plain" :to="`/artist/${artist.id}`">
													<v-icon>mdi-link</v-icon>
												</v-btn>
											</v-col>
										</v-row>
									</v-list-item>
								</v-list>
							</v-card>

							<v-row>
								<v-col v-for="(playlist, index) in spotifyPlaylists" :key="'spotify-' + index" cols="12" sm="6" md="4">
									<v-card class="mb-4 playlist-card">
										<v-img
											v-if="playlist.images && playlist.images.length > 0"
											:src="playlist.images[0].url"
											height="150"
											cover
										>
											<template v-slot:placeholder>
												<v-row class="fill-height ma-0" align="center" justify="center">
													<v-progress-circular indeterminate color="grey-lighten-5"></v-progress-circular>
												</v-row>
											</template>
										</v-img>
										<v-card-title class="text-truncate">{{ playlist.name }}</v-card-title>
										<v-card-subtitle>{{ playlist.tracks.total }} tracks</v-card-subtitle>
										<v-card-text class="text-truncate">
											{{ decodeHTML(playlist.description) || 'No description available' }}
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
										By {{ selectedPlaylist.owner.display_name }} - {{ selectedPlaylist.tracks.total }} tracks
									</v-card-subtitle>
									<v-card-text>
										<p>{{ decodeHTML(selectedPlaylist.description) || 'No description available' }}</p>
										<p class="mt-4">
											<strong>Public:</strong> {{ selectedPlaylist.public ? 'Yes' : 'No' }}
										</p>
										<p>
											<strong>Collaborative:</strong> {{ selectedPlaylist.collaborative ? 'Yes' : 'No' }}
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

							<v-card v-if="currentPlaylistId" class="pa-4 mb-4 now-playing-card">
								<v-card-title class="d-flex align-center">
									<span>Now Playing: {{ currentPlaylist ? currentPlaylist.name : 'Unknown Playlist' }}</span>
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
										allow="encrypted-media">
									</iframe>
								</div>
							</v-card>

							<!-- Playlist Cards -->
							<!-- <v-card
								v-for="(playlist, index) in playlists"
								:key="'playlist-' + index"
								class="pa-4 mb-4"
							>
								<v-card-title>{{ playlist.name }}</v-card-title>
								<v-divider></v-divider>
								<v-list>
									<v-list-item
										v-for="(song, songIndex) in playlist.songs"
										:key="'playlist-' + index + '-song-' + songIndex"
									>
										<v-list-item-content>
											<v-list-item-title>{{ song }}</v-list-item-title>
										</v-list-item-content>
									</v-list-item>
								</v-list>
							</v-card> -->
						</v-col>
					</v-row>
				</v-container>
			</div>
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
        <v-btn color="green darken-1" text @click="deleteEntry">Yes</v-btn>
        <v-btn color="red darken-1" text @click="cancelDelete">No</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
	import Navbar from "./Navbar.vue";
	import axios from "axios";
	import NotFound from "./NotFound.vue"

	export default {
		name: "MusicList",
		components: {
			Navbar,
			NotFound,
		},
		data() {
			return {
				username: this.$route.params.username || "",
				userAlbums: [],
				userTracks: [],
				userArtists: [],
				playlists: [],
				spotifyPlaylists: [],
				playlistDialog: false,
				selectedPlaylist: null,
				currentPlaylistId: null,
				currentPlaylist: null,
				userNotFound: false,
				deleteDialog: false,        // Controls the visibility of the dialog
				itemToDelete: null,         // Holds the item data to delete
				itemTypeToDelete: null,     // Holds the item type to delete (either 'master' or 'artist')
				itemIndexToDelete: null,    // Holds the index of the item in the list to remove
			};
		},
		props: {
			playlists: {
				type: Array,
				default: () => [
					{ name: "Playlist 1", songs: ["Song 1", "Song 2", "Song 3"] },
					{ name: "Playlist 2", songs: ["Track A", "Track B"] },
					{ name: "Playlist 3", songs: ["Melody X", "Tune Y", "Harmony Z"] },
				],
			},
		},
		watch: {
			"$route.params.username"(newUsername) {
				this.username = newUsername;
			},
		},
		async created() {
			await this.fetchMusicList();
			await this.fetchSpotifyPlaylists();

			const savedPlaylistId = localStorage.getItem('lastPlayedPlaylistId');
			const savedPlaylistData = localStorage.getItem('lastPlayedPlaylistData');

			if (savedPlaylistId && savedPlaylistData) {
				this.currentPlaylistId = savedPlaylistId;
				this.currentPlaylist = JSON.parse(savedPlaylistData);
			}
		},
		methods: {
			async fetchMusicList() {
				try {
					const username = this.username; // Get username from data

					const response = await axios.get(
						`http://localhost:5001/api/musiclist/${username}/master`
					);
					
					

					// Store the fetched songs into userAlbums 
					this.userAlbums = response.data;
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
			 // Trigger the confirmation dialog
			confirmDelete(item, itemType, index = null) {
				this.itemToDelete = item;  // Store the item to be deleted
				this.itemTypeToDelete = itemType;  // Store the item type
				this.indexToDelete = index;  // Store the index of the item in the list
				this.deleteDialog = true;  // Show the confirmation dialog
			},

			// Cancel the deletion
			cancelDelete() {
				this.deleteDialog = false;  // Hide the dialog
				this.itemToDelete = null;  // Clear the stored item
				this.itemTypeToDelete = null;  // Clear the item type
				this.indexToDelete = null;  // Clear the index
			},

			// Proceed with the deletion
			async deleteEntry() {
				// Close the dialog
				this.deleteDialog = false;

				// Call deleteRating to delete the rating from the backend and remove it from the list
				await this.deleteRating(this.itemTypeToDelete, this.itemToDelete.id, this.indexToDelete);

				// Clear the stored item after deletion
				this.itemToDelete = null;
				this.itemTypeToDelete = null;
				this.indexToDelete = null;
			},

			async deleteRating(itemType, itemId, index = null) {
				try {
					const response = await axios.delete('http://localhost:5001/delete-user-rating', {
						params: {
							item_type: itemType,
							item_id: itemId
						},
						withCredentials: true
					});

					if (response.data.message === 'Rating deleted successfully') {
						console.log(`Rating deleted for ${itemType} with ID ${itemId}`);
						
						// Remove from local list if index is provided
						if (itemType === 'artist' && index !== null) {
							this.userArtists.splice(index, 1);
						} else if (itemType === 'master' && index !== null) {
							this.userAlbums.splice(index, 1);
						}

					} else {
						console.log(`No rating found for ${itemType} with ID ${itemId}`);
					}
				} catch (error) {
					console.error(`Error deleting rating for ${itemType} with ID ${itemId}:`, error);
				}
			},
			async fetchSpotifyPlaylists() {
				try {
					const path = 'http://localhost:5001/get-spotify-playlists'
					const response = await axios.get(path, {
						withCredentials: true
					});

					if (response.data.items) {
						this.spotifyPlaylists = response.data.items;
					}
				} catch (error) {
					console.error("Error fetching Spotify playlists:", error);
				}
			},
			showPlaylistDetails(playlist) {
				this.selectedPlaylist = playlist;
				this.playlistDialog = true;
			},
			playPlaylist(playlist) {
				this.currentPlaylist = playlist;
				this.currentPlaylistId = playlist.id;

				localStorage.setItem('lastPlayedPlaylistId', playlist.id);
				localStorage.setItem('lastPlayedPlaylistData', JSON.stringify(playlist));

				this.playlistDialog = false;
				
				this.$nextTick(() => {
					const playerElement = document.querySelector('.now-playing-card');
					if (playerElement) {
						playerElement.scrollIntoView({ behavior: 'smooth' });
					}
				});
			},
			playPlaylistFromDialog() {
				if (this.selectedPlaylist) {
					this.playPlaylist(this.selectedPlaylist);
				}
			},
			closePlayer() {
				this.currentPlaylistId = null;
				this.currentPlaylist = null;
				localStorage.removeItem('lastPlayedPlaylistId');
				localStorage.removeItem('lastPlayedPlaylistData');
			},
			decodeHTML(html) {
				const txt = document.createElement("textarea");
				txt.innerHTML = html;
				return txt.value;
			}
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";
</style>
