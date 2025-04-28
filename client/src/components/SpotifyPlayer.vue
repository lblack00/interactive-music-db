<template>
	<v-card
		v-if="spotifyStore.currentPlaylistId || showAllPlaylists"
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

		<!-- Player section - ALWAYS render the iframe -->
		<div
			class="spotify-player-container"
			:class="{ 'player-hidden': showAllPlaylists, minimized: minimized }"
		>
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

		<!-- Conditional: Show All Playlists -->
		<div
			v-if="showAllPlaylists && !minimized"
			class="all-playlists-container playlist-list-bg"
		>
			<div class="playlist-list-header d-flex align-center">
				<v-btn icon @click="showAllPlaylists = false" size="small" class="mr-2"
					><v-icon>mdi-arrow-left</v-icon></v-btn
				>
				<span class="playlist-list-title">Your Playlists</span>
				<v-spacer></v-spacer>
			</div>
			<div class="playlist-list">
				<div
					v-for="playlist in spotifyStore.playlists"
					:key="playlist.id"
					class="playlist-row"
				>
					<v-img
						v-if="playlist.images && playlist.images.length > 0"
						:src="playlist.images[0].url"
						alt="Playlist cover"
						width="48"
						height="48"
						aspect-ratio="1"
						cover
						class="playlist-img"
					></v-img>
					<v-icon v-else size="48" class="playlist-img">mdi-music</v-icon>
					<div class="playlist-info">
						<div class="playlist-title">{{ playlist.name }}</div>
						<div class="playlist-owner">{{ playlist.owner?.display_name }}</div>
					</div>
					<v-btn
						icon
						class="playlist-play-btn"
						@click="playFromDialog(playlist)"
						><v-icon>mdi-play</v-icon></v-btn
					>
				</div>
			</div>
		</div>

		<!-- Floating See All Playlists Button -->
		<button
			v-if="!showAllPlaylists && !minimized"
			class="see-all-playlists-btn"
			@click="showAllPlaylists = true"
		>
			<v-icon>mdi-playlist-music</v-icon>
			<span class="tooltip-text">See All Playlists</span>
		</button>
	</v-card>
</template>

<script setup>
	import { ref, onMounted } from "vue";
	import { useSpotifyStore } from "../stores/spotify";

	const spotifyStore = useSpotifyStore();
	const minimized = ref(false);
	const showAllPlaylists = ref(false);

	onMounted(() => {
		spotifyStore.fetchSpotifyPlaylists();
	});

	function closePlayer() {
		spotifyStore.clearPlaylist();
		showAllPlaylists.value = false;
		minimized.value = false;
	}
	function toggleMinimize() {
		if (!minimized.value) {
			showAllPlaylists.value = false;
		}
		minimized.value = !minimized.value;
	}
	function playFromDialog(playlist) {
		spotifyStore.setCurrentPlaylist(playlist);
		showAllPlaylists.value = false;
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
		position: relative;
		z-index: 1;
	}
	.spotify-player-container.minimized {
		height: 0 !important;
		min-height: 0 !important;
		padding: 0 !important;
	}
	.spotify-player-container.player-hidden {
		position: absolute;
		opacity: 0;
		pointer-events: none;
		/* Keep it working but visually hidden */
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

	.all-playlists-container {
		padding: 0 0 16px 0;
		max-height: 490px;
		overflow-y: auto;
		position: relative;
		z-index: 2;
	}
	.see-all-playlists-btn {
		position: absolute;
		width: 40px;
		height: 40px;
		left: 50%;
		transform: translateX(-50%);
		background: rgba(128, 128, 128, 0.8);
		color: #fff;
		border: none;
		border-radius: 50%;
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
		padding: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		z-index: 2;
		transition: background 0.18s, box-shadow 0.18s;
		position: relative;
	}
	.see-all-playlists-btn:hover {
		background: #17a74a;
		box-shadow: 0 6px 20px rgba(0, 0, 0, 0.22);
	}
	.see-all-playlists-btn .tooltip-text {
		visibility: hidden;
		width: 120px;
		background-color: rgba(0, 0, 0, 0.8);
		color: #fff;
		text-align: center;
		border-radius: 6px;
		padding: 5px 0;
		position: absolute;
		z-index: 1;
		bottom: 125%;
		left: 50%;
		margin-left: -60px;
		opacity: 0;
		transition: opacity 0.3s;
		font-size: 0.85rem;
		font-weight: 600;
	}
	.see-all-playlists-btn .tooltip-text::after {
		content: "";
		position: absolute;
		top: 100%;
		left: 50%;
		margin-left: -5px;
		border-width: 5px;
		border-style: solid;
		border-color: rgba(0, 0, 0, 0.8) transparent transparent transparent;
	}
	.see-all-playlists-btn:hover .tooltip-text {
		visibility: visible;
		opacity: 1;
	}

	.playlist-list-bg {
		background: #23272f;
		border-radius: 18px;
		box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
		padding: 0 0 16px 0;
	}
	.playlist-list-header {
		padding: 18px 20px 10px 20px;
		background: #23272f;
		border-top-left-radius: 18px;
		border-top-right-radius: 18px;
		color: #fff;
		font-weight: 700;
		font-size: 1.15rem;
		margin-bottom: 0;
	}
	.playlist-list-title {
		font-size: 1.15rem;
		font-weight: 700;
		color: #fff;
	}
	.playlist-list {
		background: transparent;
		padding: 0 8px;
	}
	.playlist-list-item.reformatted {
		background: #23272f;
		border-radius: 12px;
		margin: 0 0 6px 0;
		padding: 0;
		transition: background 0.18s;
	}
	.playlist-list-item.reformatted:hover {
		background: #2e323a;
	}
	.playlist-row {
		display: flex;
		align-items: center;
		gap: 14px;
		padding: 10px 8px 10px 8px;
	}
	.playlist-img {
		border-radius: 6px;
		width: 48px !important;
		height: 48px !important;
		min-width: 48px !important;
		min-height: 48px !important;
		max-width: 48px !important;
		max-height: 48px !important;
		object-fit: cover;
		background: #222;
		display: block;
	}
	.playlist-info {
		flex: 1;
		min-width: 0;
		display: flex;
		flex-direction: column;
		justify-content: center;
	}
	.playlist-title {
		font-weight: 700;
		font-size: 1.12rem;
		color: #fff;
		white-space: normal;
		overflow: hidden;
		text-overflow: ellipsis;
		line-height: 1.2;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
		max-height: 2.6em;
	}
	.playlist-owner {
		font-size: 0.97rem;
		color: #b3b3b3;
		margin-top: 2px;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		line-height: 1.1;
	}
	.playlist-play-btn {
		margin-left: 8px;
		width: 32px;
		height: 32px;
		min-width: 32px;
		min-height: 32px;
		max-width: 32px;
		max-height: 32px;
		border: none;
		outline: none;
		border-radius: 50%;
		background: #1db954;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: background 0.18s;
		padding: 0;
	}
	.playlist-play-btn:hover {
		background: #17a74a;
	}
	.playlist-play-btn .v-icon {
		font-size: 18px !important;
		color: #fff !important;
	}
</style>
