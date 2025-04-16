<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<!-- Todo: this is a mock user profile edit page which requires a user logged in -->
			<v-container>
				<v-row justify="center">
					<v-col cols="12" md="6">
						<v-card class="pa-4">
							<h1 class="text-h4 font-weight-bold mb-4">User Profile</h1>
							<p><strong>Username:</strong> {{ user.username }}</p>
							<p><strong>Email:</strong> {{ user.email }}</p>
							<p><strong>Bio:</strong> {{ user.bio }}</p>

							<v-divider class="my-4"></v-divider>

							<h2 class="text-h5 font-weight-bold mb-2">Spotify OAuth</h2>
							<p v-if="user.spotifyConnected" style="color: green">
								Connected to Spotify
							</p>
							<p v-else style="color: red">Not connected</p>

							<v-btn
								v-if="!user.spotifyConnected"
								color="green"
								@click="initiateSpotifyAuth"
								aria-label="Connect your Spotify account"
							>
								Connect Spotify
							</v-btn>
							<v-btn
								v-else
								color="red"
								@click="disconnectSpotify"
								aria-label="Disconnect your Spotify account"
							>
								Disconnect Spotify
							</v-btn>
						</v-card>
					</v-col>
				</v-row>
			</v-container>
		</div>
	</div>
</template>

<script>
	import Navbar from "./Navbar.vue";

	export default {
		name: "UserSettings",
		components: { Navbar },
		data() {
			return {
				user: {
					username: "Username",
					email: "username@example.com",
					bio: "This is my bio!",
					spotifyConnected: false,
				},
				clientId: import.meta.env.VITE_SPOTIFY_CLIENT_ID,
				redirectUri: "http://localhost:5173/",
				accessToken: "",
			};
		},
		methods: {
			saveProfile() {
				alert("Profile updated successfully!");
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
		},
	};
</script>
<style scoped>
	@import "../../src/assets/background.css";
</style>
