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
						<v-col cols="12" md="2" style="position: fixed">
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
						</v-col>

						<!-- Main Content (Music List) -->
						<v-col cols="12" md="9" style="margin-left: 20%">
							<h1 class="text-h4 font-weight-bold mb-4">
								{{ username }}'s Music List
							</h1>

							<!-- User's Music Card -->
							<v-card class="pa-4 mb-4">
								<v-card-title>{{ username }}'s Music</v-card-title>
								<v-divider></v-divider>
								<v-list>
									<v-list-item
										v-for="(song, index) in userSongs"
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
												<v-btn variant="plain" @click="deleteSong(song)">
													<v-icon>mdi-delete</v-icon>
												</v-btn>

												<!-- Share Button -->
												<v-btn variant="plain" @click="shareSong(song)">
													<v-icon>mdi-share-variant</v-icon>
												</v-btn>

												<!-- Link Button (Opens External URL) -->
												<v-btn variant="plain" :to="`/master/${song.id}`">
													<v-icon>mdi-link</v-icon>
												</v-btn>

												<!-- Spotify Button (or WiFi) -->
												<v-btn variant="plain" @click="spotifyAction(song)">
													<v-icon>mdi-spotify</v-icon>
													<!-- Use mdi-wifi if preferred -->
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
												<v-btn variant="plain" @click="deleteSong(artist)">
													<v-icon>mdi-delete</v-icon>
												</v-btn>

												<!-- Share Button -->
												<v-btn variant="plain" @click="shareSong(artist)">
													<v-icon>mdi-share-variant</v-icon>
												</v-btn>

												<!-- Link Button (Opens External URL) -->
												<v-btn variant="plain" :to="`/artist/${artist.id}`">
													<v-icon>mdi-link</v-icon>
												</v-btn>

												<!-- Spotify Button (or WiFi) -->
												<v-btn variant="plain" @click="spotifyAction(artist)">
													<v-icon>mdi-spotify</v-icon>
													<!-- Use mdi-wifi if preferred -->
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
											{{ playlist.description || 'No description available' }}
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
										<p>{{ selectedPlaylist.description || 'No description available' }}</p>
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
				userSongs: [],
				userArtists: [],
				playlists: [],
				spotifyPlaylists: [],
				playlistDialog: false,
				selectedPlaylist: null,
				currentPlaylistId: null,
				currentPlaylist: null,
				userNotFound: false,
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
					
					

					// Store the fetched songs into userSongs
					this.userSongs = response.data;

					// TODO: Implement this so it grabs the artists from the user
					const response2 = await axios.get(
						`http://localhost:5001/api/musiclist/${username}/artist`
					);

					// Store the fetched artists into user artists
					this.userArtists = response2.data;
				} catch (error) {
					console.error("Error fetching music list:", error);

					this.userNotFound = true;
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
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";
</style>
