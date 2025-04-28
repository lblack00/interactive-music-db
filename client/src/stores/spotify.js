import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "axios";

export const useSpotifyStore = defineStore("spotify", () => {
	const currentPlaylistId = ref(null);
	const currentPlaylist = ref(null);
	const isPlaying = ref(false);
	const playlists = ref([]);

	async function fetchSpotifyPlaylists() {
		try {
			const path = "http://localhost:5001/get-spotify-playlists";
			const response = await axios.get(path, { withCredentials: true });
			if (response.data.items) {
				playlists.value = response.data.items;
			}
		} catch (error) {
			playlists.value = [];
			console.error("Error fetching Spotify playlists:", error);
		}
	}

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
		playlists,
		fetchSpotifyPlaylists,
		setCurrentPlaylist,
		clearPlaylist,
		setIsPlaying,
	};
});
