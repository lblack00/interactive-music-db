import { defineStore } from "pinia";
import { ref } from "vue";

export const useSpotifyStore = defineStore("spotify", () => {
	const currentPlaylistId = ref(null);
	const currentPlaylist = ref(null);
	const isPlaying = ref(false);

	function setCurrentPlaylist(playlist) {
		currentPlaylist.value = playlist;
		currentPlaylistId.value = playlist.id;
		localStorage.setItem("lastPlayedPlaylistId", playlist.id);
		localStorage.setItem("lastPlayedPlaylistData", JSON.stringify(playlist));
	}

	function clearPlaylist() {
		currentPlaylist.value = null;
		currentPlaylistId.value = null;
		localStorage.removeItem("lastPlayedPlaylistId");
		localStorage.removeItem("lastPlayedPlaylistData");
	}

	function setIsPlaying(playing) {
		isPlaying.value = playing;
	}

	return {
		currentPlaylistId,
		currentPlaylist,
		isPlaying,
		setCurrentPlaylist,
		clearPlaylist,
		setIsPlaying,
	};
});
