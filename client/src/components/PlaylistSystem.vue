<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<header role="navigation">
		
	</header>

	<main role="main">
		<v-container>
			<h1 id="playlist-heading" class="text-h4 font-weight-bold mb-4">
				Create a Playlist
			</h1>

			<section role="region" aria-labelledby="playlist-heading">
				<div role="form" aria-label="Add song to playlist">
					<v-text-field
						v-model="newSong"
						label="Add a song"
						outlined
						dense
						class="mb-2"
						aria-label="Song name"
					/>
					<v-btn
						color="primary"
						@click="addSong"
						:disabled="!newSong"
						aria-label="Add song to playlist"
						>Add</v-btn
					>
				</div>

				<div role="region" aria-label="Playlist songs" class="mt-4">
					<v-list v-if="playlist.length">
						<v-list-item
							v-for="(song, index) in playlist"
							:key="index"
							class="d-flex justify-space-between"
						>
							<span>{{ song }}</span>
							<v-btn
								icon
								@click="removeSong(index)"
								style="font-size: 12px; width: 24px; height: 24px"
								:aria-label="`Remove from playlist`"
							>
								<v-icon color="red" aria-hidden="true">mdi-delete</v-icon>
							</v-btn>
						</v-list-item>
					</v-list>

					<p v-else class="mt-4 text-grey" role="status">
						No songs in the playlist yet.
					</p>
				</div>
			</section>
		</v-container>
	</main>
</template>

<script>
	import Navbar from "./Navbar.vue";

	export default {
		name: "PlaylistSystem",
		components: {
			Navbar,
		},
		data() {
			return {
				newSong: "",
				playlist: [],
			};
		},
		methods: {
			addSong() {
				if (this.newSong) {
					this.playlist.push(this.newSong);
					this.newSong = "";
				}
			},
			removeSong(index) {
				this.playlist.splice(index, 1);
			},
		},
	};
</script>

<style scoped>
	.text-grey {
		color: grey;
	}
</style>
