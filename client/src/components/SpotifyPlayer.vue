<template>
	<v-card
		v-if="spotifyStore.currentPlaylistId"
		class="spotify-player-card pa-3 mb-3"
	>
		<!-- Minimized Bar -->
		<div v-if="minimized" class="minimized-bar d-flex align-center">
			<v-icon class="mr-2" size="18">mdi-music</v-icon>
			<span class="wrap-title minimized-title"
				>Now Playing:
				{{ spotifyStore.currentPlaylist?.name || "Unknown Playlist" }}</span
			>
			<v-spacer></v-spacer>
			<div class="button-group">
				<v-btn icon @click.stop="toggleMinimize" size="x-small">
					<v-icon size="18">mdi-chevron-up</v-icon>
				</v-btn>
				<v-btn icon @click.stop="closePlayer" size="x-small">
					<v-icon size="18">mdi-close</v-icon>
				</v-btn>
			</div>
		</div>

		<!-- Full Player -->
		<template v-else>
			<v-card-title class="d-flex align-center">
				<span class="wrap-title full-title">
					Now Playing:
					{{ spotifyStore.currentPlaylist?.name || "Unknown Playlist" }}
				</span>
				<v-spacer></v-spacer>
				<div class="button-group">
					<v-btn icon @click="toggleMinimize" size="x-small">
						<v-icon size="18">mdi-chevron-down</v-icon>
					</v-btn>
					<v-btn icon @click="closePlayer" size="x-small">
						<v-icon size="18">mdi-close</v-icon>
					</v-btn>
				</div>
			</v-card-title>
			<v-divider></v-divider>
		</template>
		<!-- Always render the iframe, but hide it when minimized -->
		<div class="spotify-player-container" :class="{ minimized: minimized }">
			<iframe
				:src="`https://open.spotify.com/embed/playlist/${spotifyStore.currentPlaylistId}`"
				width="100%"
				:height="minimized ? 0 : 490"
				frameborder="0"
				allowtransparency="true"
				allow="encrypted-media"
				style="transition: height 0.2s; display: block"
			></iframe>
		</div>
	</v-card>
</template>

<script setup>
	import { ref } from "vue";
	import { useSpotifyStore } from "../stores/spotify";

	const spotifyStore = useSpotifyStore();
	const minimized = ref(false);

	function closePlayer() {
		spotifyStore.clearPlaylist();
	}
	function toggleMinimize() {
		minimized.value = !minimized.value;
	}
</script>

<style scoped>
	.v-card-title {
		color: white;
		background: rgba(30, 40, 60, 0.95);
		padding: 18px 20px 14px 20px;
		border-top-left-radius: 20px;
		border-top-right-radius: 20px;
		font-weight: 600;
		font-size: 1.15rem;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
	}
	.spotify-player-card {
		position: fixed;
		bottom: 20px;
		right: 20px;
		width: 320px;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: white;
		z-index: 1000;
		border-radius: 20px;
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
		transition: height 0.2s;
	}

	.spotify-player-container {
		border-radius: 12px;
		overflow: hidden;
		height: 500px;
		transition: height 0.2s;
	}
	.spotify-player-container.minimized {
		height: 0 !important;
		min-height: 0 !important;
		padding: 0 !important;
	}

	.minimized-bar {
		background: rgba(30, 40, 60, 0.95);
		color: white;
		padding: 14px 20px 12px 20px;
		border-radius: 20px;
		width: 100%;
		min-height: 40px;
		box-sizing: border-box;
		display: flex;
		align-items: center;
		border: none;
		font-weight: 600;
		font-size: 1.15rem;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
	}

	.button-group {
		display: flex;
		gap: 2px;
		flex-shrink: 0;
	}

	.wrap-title {
		white-space: normal;
		word-break: break-word;
		overflow-wrap: anywhere;
		max-width: 140px;
		display: inline-block;
	}

	.minimized-title {
		max-width: 140px;
	}
	.full-title {
		max-width: 200px;
	}
</style>
