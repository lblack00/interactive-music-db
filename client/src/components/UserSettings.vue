<template>
	<div
		class="grid-container"
		:class="[
			{
				'high-contrast': highContrast,
				'dark-mode': darkMode,
			},
		]"
	>
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content settings-content">
			<v-container class="py-10">
				<v-row justify="center">
					<v-col cols="12" md="8" lg="6">
						<v-card class="settings-card" elevation="2">
							<v-card-title class="settings-title">
								User Settings
							</v-card-title>
							<v-form @submit.prevent="saveProfile" class="px-4">
								<!-- Profile Section -->
								<v-card class="section-card mb-6 pa-5" variant="outlined">
									<h2 class="section-title">Profile Information</h2>
									<v-text-field
										v-model="user.username"
										label="Username"
										variant="outlined"
										required
										class="mb-4 rounded-input"
									></v-text-field>
									<v-text-field
										v-model="user.email"
										label="Email"
										variant="outlined"
										required
										readonly
										class="mb-4 rounded-input"
									></v-text-field>
									<v-textarea
										v-model="user.bio"
										label="Bio"
										variant="outlined"
										placeholder="Tell us something about yourself..."
										rows="3"
										:counter="500"
										maxlength="500"
										class="mb-4 rounded-input"
									></v-textarea>
								</v-card>
								<!-- Profile Picture Section -->
								<v-card class="section-card mb-6 pa-5" variant="outlined">
									<h2 class="section-title">Profile Picture</h2>
									<v-row class="mb-4" align="center" justify="center">
										<v-col cols="6" class="text-center">
											<p class="text-subtitle-2 mb-2">Current Picture</p>
											<v-img
												:src="originalUser.profileImage"
												height="140"
												width="140"
												class="mx-auto rounded-img profile-img-shadow"
												cover
											></v-img>
										</v-col>
										<v-col
											cols="6"
											class="text-center"
											v-if="user.profileImage"
										>
											<p class="text-subtitle-2 mb-2">New Picture</p>
											<v-img
												:src="user.profileImage"
												height="140"
												width="140"
												class="mx-auto rounded-img profile-img-shadow"
												cover
											></v-img>
										</v-col>
									</v-row>
									<v-file-input
										label="Upload New Profile Picture"
										accept="image/*"
										@change="handleFileUpload"
										variant="outlined"
										prepend-icon="mdi-camera"
										:hint="profileFileError || 'Maximum file size: 1MB'"
										:persistent-hint="!!profileFileError"
										:error-messages="profileFileError"
										class="rounded-input"
									></v-file-input>
								</v-card>
								<!-- Display Settings Section -->
								<v-card class="section-card mb-6 pa-5" variant="outlined">
									<h2 class="section-title">Display Settings</h2>
									<v-switch
										v-model="darkMode"
										label="Dark Mode"
										hint="Enable dark theme for better visibility in low-light conditions"
										persistent-hint
										@update:model-value="handleDarkModeChange"
										:disabled="highContrast"
										class="mb-4 rounded-switch"
									></v-switch>
									<v-switch
										v-model="highContrast"
										label="High Contrast"
										hint="Enable high contrast mode for better visibility"
										persistent-hint
										@update:model-value="handleHighContrastChange"
										:disabled="darkMode"
										class="mb-4 rounded-switch"
									></v-switch>
								</v-card>
								<!-- Spotify Section -->
								<v-card class="section-card mb-6 pa-5" variant="outlined">
									<h2 class="section-title">Spotify Integration</h2>
									<div class="d-flex align-center mb-4">
										<v-icon
											:color="user.spotifyConnected ? 'success' : 'error'"
											class="mr-2"
										>
											{{
												user.spotifyConnected
													? "mdi-check-circle"
													: "mdi-close-circle"
											}}
										</v-icon>
										<span
											:class="
												user.spotifyConnected ? 'text-success' : 'text-error'
											"
										>
											{{
												user.spotifyConnected
													? "Connected to Spotify"
													: "Not connected to Spotify"
											}}
										</span>
									</div>
									<v-btn
										v-if="!user.spotifyConnected"
										color="success"
										prepend-icon="mdi-spotify"
										@click="initiateSpotifyAuth"
										block
										class="spotify-btn"
									>
										Connect Spotify
									</v-btn>
									<v-btn
										v-else
										color="error"
										prepend-icon="mdi-spotify"
										@click="disconnectSpotify"
										block
										class="spotify-btn"
									>
										Disconnect Spotify
									</v-btn>
								</v-card>
								<!-- Save Button -->
								<v-btn
									type="submit"
									color="primary"
									size="x-large"
									block
									class="save-btn mt-8"
									:loading="saving"
									style="font-weight: bold; letter-spacing: 2px"
								>
									Save Changes
								</v-btn>
							</v-form>
						</v-card>
					</v-col>
				</v-row>
			</v-container>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted, onBeforeUnmount, computed, watch } from "vue";
	import { useAccessibilityStore } from "../stores/accessibility";
	import Navbar from "./Navbar.vue";
	import axios from "axios";

	const accessibilityStore = useAccessibilityStore();

	const darkMode = ref(accessibilityStore.darkMode);
	const highContrast = ref(accessibilityStore.highContrast);

	// Watch for store changes
	watch(
		() => accessibilityStore.darkMode,
		(newValue) => {
			darkMode.value = newValue;
		}
	);

	watch(
		() => accessibilityStore.highContrast,
		(newValue) => {
			highContrast.value = newValue;
		}
	);

	const handleDarkModeChange = (value) => {
		if (value) {
			highContrast.value = false;
			accessibilityStore.setHighContrast(false);
		}
		darkMode.value = value;
		accessibilityStore.setDarkMode(value);
	};

	const handleHighContrastChange = (value) => {
		if (value) {
			darkMode.value = false;
			accessibilityStore.setDarkMode(false);
		}
		highContrast.value = value;
		accessibilityStore.setHighContrast(value);
	};

	onMounted(() => {
		getCurrentSettings();

		// Handle Spotify callback if needed
		if (window.location.search.includes("code")) {
			handleSpotifyCallback();
		}
		setInterval(refreshAccessToken, 50 * 60 * 1000);

		// Initialize settings from store
		darkMode.value = accessibilityStore.darkMode;
		highContrast.value = accessibilityStore.highContrast;

		// Apply saved settings
		handleDarkModeChange(accessibilityStore.darkMode);
		handleHighContrastChange(accessibilityStore.highContrast);
	});

	const loggedIn = ref(false);
	const user = ref({
		id: null,
		username: null,
		email: null,
		bio: null,
		profileImage: null,
		spotifyConnected: false,
	});
	const originalUser = ref({
		username: null,
		bio: null,
		profileImage: null,
	});
	const newProfileImage = ref(null); // To store the preview of the new image
	const profileFileError = ref("");
	const profileFile = ref(null);

	const clientId = import.meta.env.VITE_SPOTIFY_CLIENT_ID;
	const redirectUri = "http://localhost:5173/user-settings";
	const accessToken = ref("");

	const colorblindClass = computed(() => {
		switch (colorblindMode.value) {
			case "Red-Blind (Protanopia)":
				return "protanopia";
			case "Green-Blind (Deuteranopia)":
				return "deuteranopia";
			case "Blue-Blind (Tritanopia)":
				return "tritanopia";
			case "Grayscale (achromatopsia)":
				return "achromatopsia";
			case "High Contrast":
				return "high-contrast";
			default:
				return "";
		}
	});

	const getCurrentSettings = async () => {
		try {
			const response = await axios.get("http://localhost:5001/check-session", {
				withCredentials: true,
			});

			loggedIn.value = response.data.logged_in;
			if (response.data.logged_in) {
				user.value.username = response.data.user.username;
				user.value.id = response.data.user.id;
				user.value.email = response.data.user.email;

				originalUser.value.username = response.data.user.username;

				const imageResponse = await axios.get(
					`http://localhost:5001/get-profile-image/${user.value.id}`
				);
				originalUser.value.profileImage = `http://localhost:5001${imageResponse.data.image_url}`;

				const bioResponse = await axios.get(
					`http://localhost:5001/get-bio/${user.value.id}`
				);
				user.value.bio = bioResponse.data.bio;
				originalUser.value.bio = user.value.bio;

				try {
					const spotifyResponse = await axios.get(
						`http://localhost:5001/get-spotify-status`,
						{ withCredentials: true }
					);
					user.value.spotifyConnected = spotifyResponse.data.connected;

					if (
						user.value.spotifyConnected &&
						localStorage.getItem("spotify_access_token")
					) {
						accessToken.value = localStorage.getItem("spotify_access_token");
					}
				} catch (error) {}
			} else {
				// Redirect to 404
				router.push("/404");
			}
		} catch (error) {
			console.error("Error checking session:", error);
			loggedIn.value = false;
			user.value = null;
		}
	};

	const saveProfile = async () => {
		let success = true;

		if (user.value.username !== originalUser.value.username) {
			try {
				const response = await axios.post(
					"http://localhost:5001/update-username",
					{
						new_username: user.value.username,
					},
					{
						withCredentials: true,
					}
				);
				originalUser.value.username = user.value.username;
			} catch (error) {
				success = false;
				console.error("Error updating username:", error);
				if (error.response && error.response.status === 409) {
					alert("That username is already taken.");
				}
				user.value.username = originalUser.value.username;
			}
		}

		if (user.value.bio !== originalUser.value.bio) {
			try {
				const response = await axios.post(
					"http://localhost:5001/update-bio",
					{ bio: user.value.bio },
					{ withCredentials: true }
				);
				originalUser.value.bio = user.value.bio;
			} catch (error) {
				success = false;
				console.error("Error updating bio:", error);
			}
		}

		if (
			user.value.profileImage !== originalUser.value.profileImage &&
			user.value.profileImage
		) {
			try {
				const formData = new FormData();
				formData.append("image", profileFile.value);

				await axios.post("http://localhost:5001/update-user-pfp", formData, {
					withCredentials: true,
					headers: {
						"Content-Type": "multipart/form-data",
					},
				});

				originalUser.value.profileImage = user.value.profileImage;
				user.value.profileImage = null;
			} catch (error) {
				success = false;
				console.error("Error uploading profile image:", error);
			}
		}

		if (success) {
			alert("Changes saved successfully!");
		} else {
			alert("Some changes were unsuccessful. Please try again.");
		}
	};

	const handleFileUpload = (event) => {
		const file = event.target.files[0];

		if (!file) return;

		if (file.size > 1024 * 1024) {
			profileFileError.value = "File size must be less than 1MB.";
			return;
		}

		profileFileError.value = "";
		profileFile.value = file; // <-- Save the file for later upload

		const reader = new FileReader();
		reader.onload = (e) => {
			user.value.profileImage = e.target.result; // For preview
		};
		reader.readAsDataURL(file);
	};

	// For Spotify

	const initiateSpotifyAuth = async () => {
		try {
			const state = generateRandomString(16);
			const codeVerifier = generateCodeVerifier();
			const codeChallenge = await generateCodeChallenge(codeVerifier);

			localStorage.setItem("spotify_auth_state", state);
			localStorage.setItem("code_verifier", codeVerifier);

			const scope = "user-read-private user-read-email";
			const authUrl = new URL("https://accounts.spotify.com/authorize");
			authUrl.searchParams.append("client_id", clientId);
			authUrl.searchParams.append("response_type", "code");
			authUrl.searchParams.append("redirect_uri", redirectUri);
			authUrl.searchParams.append("scope", scope);
			authUrl.searchParams.append("state", state);
			authUrl.searchParams.append("code_challenge_method", "S256");
			authUrl.searchParams.append("code_challenge", codeChallenge);

			window.location.href = authUrl.toString();
		} catch (error) {
			console.error("Error initiating Spotify auth:", error);
		}
	};
	const handleSpotifyCallback = async () => {
		const urlParams = new URLSearchParams(window.location.search);
		const code = urlParams.get("code");
		const state = urlParams.get("state");
		const storedState = localStorage.getItem("spotify_auth_state");

		if (!code || state !== storedState) {
			alert("Authorization failed. Try again.");
			return;
		}

		localStorage.removeItem("spotify_auth_state");

		try {
			const response = await fetch("https://accounts.spotify.com/api/token", {
				method: "POST",
				headers: { "Content-Type": "application/x-www-form-urlencoded" },
				body: new URLSearchParams({
					client_id: clientId,
					grant_type: "authorization_code",
					code: code,
					redirect_uri: redirectUri,
					code_verifier: localStorage.getItem("code_verifier"),
				}),
			});

			const data = await response.json();
			if (data.access_token) {
				accessToken.value = data.access_token;
				localStorage.setItem("spotify_access_token", data.access_token);
				localStorage.setItem("spotify_refresh_token", data.refresh_token);

				try {
					await axios.post(
						"http://localhost:5001/update-spotify-tokens",
						{
							access_token: data.access_token,
							refresh_token: data.refresh_token,
							expires_in: data.expires_in,
							connected: true,
						},
						{ withCredentials: true }
					);
					alert("Spotify connected successfully!");
					user.value.spotifyConnected = true;
				} catch (error) {
					console.error("Error saving Spotify tokens:", error);
				}
			} else {
				alert("Failed to retrieve access token");
			}
		} catch (error) {
			console.error("Error during token exchange:", error);
		}
	};
	const refreshAccessToken = async () => {
		const refreshToken = localStorage.getItem("spotify_refresh_token");
		if (!refreshToken) return;
		try {
			const response = await fetch("https://accounts.spotify.com/api/token", {
				method: "POST",
				headers: { "Content-Type": "application/x-www-form-urlencoded" },
				body: new URLSearchParams({
					client_id: clientId,
					grant_type: "refresh_token",
					refresh_token: refreshToken,
				}),
			});
			const data = await response.json();
			if (data.access_token) {
				accessToken.value = data.access_token;
				localStorage.setItem("spotify_access_token", data.access_token);
			}
		} catch (error) {
			console.error("Error refreshing access token:", error);
		}
	};
	const generateRandomString = (length) => {
		const possible =
			"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
		return Array.from(crypto.getRandomValues(new Uint8Array(length)))
			.map((x) => possible[x % possible.length])
			.join("");
	};
	const generateCodeVerifier = () => {
		return generateRandomString(128);
	};
	const generateCodeChallenge = async (codeVerifier) => {
		const encoder = new TextEncoder();
		const data = encoder.encode(codeVerifier);
		const digest = await crypto.subtle.digest("SHA-256", data);
		return base64UrlEncode(digest);
	};
	const base64UrlEncode = (buffer) => {
		let binary = "";
		const bytes = new Uint8Array(buffer);
		for (let i = 0; i < bytes.byteLength; i++) {
			binary += String.fromCharCode(bytes[i]);
		}
		return btoa(binary)
			.replace(/\+/g, "-")
			.replace(/\//g, "_")
			.replace(/=+$/, "");
	};
	const disconnectSpotify = async () => {
		try {
			await axios.post(
				"http://localhost:5001/update-spotify-tokens",
				{ connected: false },
				{ withCredentials: true }
			);
		} catch (error) {
			console.error("Error saving Spotify tokens:", error);
		}

		user.value.spotifyConnected = false;
		accessToken.value = "";
		localStorage.removeItem("spotify_access_token");
		localStorage.removeItem("spotify_refresh_token");
		alert("Spotify account disconnected.");
	};

	onBeforeUnmount(() => {
		// Clean up any applied filters
		const appElement = document.getElementById("app");
		if (appElement) {
			appElement.classList.remove("high-contrast", "dark-mode");
		}
	});
</script>

<style scoped>
	@import "../assets/background.css";
	@import "../assets/accessibility.css";

	.settings-bg {
		background: linear-gradient(135deg, #f7fafd 0%, #e3e9f3 100%);
		min-height: 100vh;
	}

	.settings-content {
		padding-top: 32px;
		padding-bottom: 32px;
		animation: fadeIn 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
	}

	.settings-card {
		border-radius: 22px;
		box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08), 0 1.5px 6px rgba(0, 0, 0, 0.04);
		background: var(--background-color);
		color: var(--text-color);
		padding-bottom: 32px;
		opacity: 0;
		animation: slideUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.2s forwards;
	}

	.section-card {
		border-radius: 16px;
		background: #f8fafc;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
		border: 1px solid #e3e9f3;
		opacity: 0;
		transform: translateY(20px);
		animation: sectionSlideIn 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
	}

	.section-card:nth-child(1) {
		animation-delay: 0.3s;
	}
	.section-card:nth-child(2) {
		animation-delay: 0.4s;
	}
	.section-card:nth-child(3) {
		animation-delay: 0.5s;
	}
	.section-card:nth-child(4) {
		animation-delay: 0.6s;
	}

	.settings-title {
		font-size: 2rem;
		font-weight: 700;
		letter-spacing: 1px;
		color: #1a237e;
		margin-bottom: 12px;
		text-align: center;
		padding-top: 24px;
		padding-bottom: 8px;
		opacity: 0;
		animation: titleFadeIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.1s forwards;
	}

	.section-title {
		font-size: 1.25rem;
		font-weight: 600;
		color: #26326a;
		margin-bottom: 18px;
		border-left: 4px solid #42a5f5;
		padding-left: 12px;
		opacity: 0;
		animation: titleSlideIn 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
		animation-delay: inherit;
	}

	.rounded-input,
	.rounded-switch {
		opacity: 0;
		animation: inputFadeIn 0.5s ease-out forwards;
	}

	.rounded-input:nth-child(1) {
		animation-delay: calc(var(--section-delay) + 0.1s);
	}
	.rounded-input:nth-child(2) {
		animation-delay: calc(var(--section-delay) + 0.2s);
	}
	.rounded-input:nth-child(3) {
		animation-delay: calc(var(--section-delay) + 0.3s);
	}

	.profile-img-shadow {
		opacity: 0;
		transform: scale(0.9);
		animation: imageFadeIn 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) 0.5s forwards;
	}

	.save-btn {
		opacity: 0;
		animation: buttonSlideUp 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) 0.7s forwards;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	@keyframes slideUp {
		from {
			opacity: 0;
			transform: translateY(30px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes sectionSlideIn {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes titleFadeIn {
		from {
			opacity: 0;
			transform: translateY(-10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes titleSlideIn {
		from {
			opacity: 0;
			transform: translateX(-20px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	@keyframes inputFadeIn {
		from {
			opacity: 0;
			transform: translateX(-15px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	@keyframes imageFadeIn {
		from {
			opacity: 0;
			transform: scale(0.9);
		}
		to {
			opacity: 1;
			transform: scale(1);
		}
	}

	@keyframes buttonSlideUp {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	/* Spotify button animation */
	.spotify-btn {
		opacity: 0;
		animation: buttonPop 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
		animation-delay: calc(var(--section-delay) + 0.2s);
	}

	@keyframes buttonPop {
		from {
			opacity: 0;
			transform: scale(0.95);
		}
		to {
			opacity: 1;
			transform: scale(1);
		}
	}

	/* Add animation for file input */
	.v-file-input {
		opacity: 0;
		animation: inputFadeIn 0.5s ease-out forwards;
		animation-delay: calc(var(--section-delay) + 0.3s);
	}

	/* Add animation for alerts and status messages */
	.v-alert {
		animation: alertSlideIn 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
	}

	@keyframes alertSlideIn {
		from {
			opacity: 0;
			transform: translateY(-20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.rounded-input .v-input__control,
	.rounded-input .v-field {
		border-radius: 12px !important;
	}

	.rounded-switch .v-input__control {
		border-radius: 12px !important;
	}

	.rounded-img {
		border-radius: 50% !important;
		border: 3px solid #e3e9f3;
	}

	.profile-img-shadow {
		box-shadow: 0 2px 12px rgba(66, 165, 245, 0.1);
	}

	.save-btn {
		border-radius: 32px;
		background: linear-gradient(90deg, var(--primary-color) 0%, #42a5f5 100%);
		color: var(--text-color);
		box-shadow: 0 2px 12px rgba(25, 118, 210, 0.15);
		transition: background 0.2s, box-shadow 0.2s;
	}

	.save-btn:hover:not(:disabled) {
		background: linear-gradient(90deg, #1565c0 0%, #1e88e5 100%);
		box-shadow: 0 4px 24px rgba(25, 118, 210, 0.22);
	}

	.v-btn--block {
		margin-left: 0;
		margin-right: 0;
	}

	.spotify-btn {
		border-radius: 24px;
		font-weight: 600;
		letter-spacing: 1px;
		margin-top: 8px;
		margin-bottom: 0;
		background: linear-gradient(90deg, #1db954 0%, #1ed760 100%);
		color: #fff;
		box-shadow: 0 2px 8px rgba(30, 215, 96, 0.1);
	}

	.spotify-btn:hover:not(:disabled) {
		filter: brightness(1.08);
		background: linear-gradient(90deg, #169c46 0%, #1db954 100%);
	}

	/* High Contrast Mode Enhancements */
	.high-contrast .settings-card {
		background: #000000 !important;
		border: 2px solid #ffffff !important;
		box-shadow: none !important;
	}

	.high-contrast .section-card {
		background: #000000 !important;
		border: 2px solid #ffffff !important;
		box-shadow: none !important;
	}

	.high-contrast .settings-title {
		color: #ffffff !important;
		text-shadow: 2px 2px 0 #000000;
	}

	.high-contrast .section-title {
		color: #ffffff !important;
		border-left: 4px solid #ffffff !important;
	}

	.high-contrast .v-field {
		background: #000000 !important;
		border: 2px solid #ffffff !important;
		color: #ffffff !important;
	}

	.high-contrast .v-field__input {
		color: #ffffff !important;
	}

	.high-contrast .v-field__label {
		color: #ffffff !important;
	}

	.high-contrast .v-field:hover {
		border-color: #ffffff !important;
	}

	.high-contrast .v-field:focus-within {
		border-color: #ffffff !important;
		box-shadow: 0 0 0 2px #ffffff !important;
	}

	.high-contrast .v-switch__track {
		background: #000000 !important;
		border: 2px solid #ffffff !important;
	}

	.high-contrast .v-switch__thumb {
		background: #ffffff !important;
	}

	.high-contrast .v-switch--active .v-switch__track {
		background: #ffffff !important;
	}

	.high-contrast .v-switch--active .v-switch__thumb {
		background: #000000 !important;
	}

	.high-contrast .v-select__selection {
		color: #ffffff !important;
	}

	.high-contrast .v-select__menu {
		background: #000000 !important;
		border: 2px solid #ffffff !important;
	}

	.high-contrast .v-list-item {
		color: #ffffff !important;
	}

	.high-contrast .v-list-item:hover {
		background: #ffffff !important;
		color: #000000 !important;
	}

	.high-contrast .v-list-item--active {
		background: #ffffff !important;
		color: #000000 !important;
	}

	.high-contrast .rounded-img {
		border: 3px solid #ffffff !important;
	}

	.high-contrast .profile-img-shadow {
		box-shadow: 0 0 0 2px #ffffff !important;
	}

	.high-contrast .v-icon {
		color: #ffffff !important;
	}

	.high-contrast .text-success {
		color: #ffffff !important;
	}

	.high-contrast .text-error {
		color: #ffffff !important;
	}

	.high-contrast .v-btn {
		border: 2px solid #ffffff !important;
	}

	.high-contrast .save-btn {
		background: #ffffff !important;
		color: #000000 !important;
		box-shadow: none !important;
	}

	.high-contrast .save-btn:hover:not(:disabled) {
		background: #ffffff !important;
		box-shadow: none !important;
	}

	.high-contrast .spotify-btn {
		background: #ffffff !important;
		color: #000000 !important;
		box-shadow: none !important;
	}

	.high-contrast .spotify-btn:hover:not(:disabled) {
		background: #ffffff !important;
		filter: none !important;
	}

	.high-contrast .v-input__details {
		color: #ffffff !important;
	}

	.high-contrast .v-messages__message {
		color: #ffffff !important;
	}

	.high-contrast .v-field__append-inner {
		color: #ffffff !important;
	}

	.high-contrast .v-field__prepend-inner {
		color: #ffffff !important;
	}

	.high-contrast .v-field__clearable {
		color: #ffffff !important;
	}

	.high-contrast .v-field__input::placeholder {
		color: rgba(255, 255, 255, 0.7) !important;
	}

	.high-contrast .v-field__input:-webkit-autofill,
	.high-contrast .v-field__input:-webkit-autofill:hover,
	.high-contrast .v-field__input:-webkit-autofill:focus {
		-webkit-text-fill-color: #ffffff !important;
		-webkit-box-shadow: 0 0 0 30px #000000 inset !important;
	}

	/* Dark Mode Styles */
	.dark-mode .settings-card {
		background: #1a1a1a !important;
		color: #ffffff !important;
	}

	.dark-mode .section-card {
		background: #2d2d2d !important;
		border-color: #404040 !important;
	}

	.dark-mode .settings-title {
		color: #ffffff !important;
	}

	.dark-mode .section-title {
		color: #ffffff !important;
		border-left-color: #42a5f5 !important;
	}

	.dark-mode .v-field {
		background: #2d2d2d !important;
		border-color: #404040 !important;
		color: #ffffff !important;
	}

	.dark-mode .v-field__input {
		color: #ffffff !important;
	}

	.dark-mode .v-field__label {
		color: #ffffff !important;
	}

	.dark-mode .v-field:hover {
		border-color: #42a5f5 !important;
	}

	.dark-mode .v-field:focus-within {
		border-color: #42a5f5 !important;
		box-shadow: 0 0 0 2px rgba(66, 165, 245, 0.2) !important;
	}

	.dark-mode .v-switch__track {
		background: #404040 !important;
	}

	.dark-mode .v-switch__thumb {
		background: #ffffff !important;
	}

	.dark-mode .v-switch--active .v-switch__track {
		background: #42a5f5 !important;
	}

	.dark-mode .v-select__selection {
		color: #ffffff !important;
	}

	.dark-mode .v-select__menu {
		background: #2d2d2d !important;
		border-color: #404040 !important;
	}

	.dark-mode .v-list-item {
		color: #ffffff !important;
	}

	.dark-mode .v-list-item:hover {
		background: #404040 !important;
	}

	.dark-mode .v-list-item--active {
		background: #42a5f5 !important;
		color: #ffffff !important;
	}

	.dark-mode .rounded-img {
		border-color: #404040 !important;
	}

	.dark-mode .profile-img-shadow {
		box-shadow: 0 2px 12px rgba(66, 165, 245, 0.1) !important;
	}

	.dark-mode .v-icon {
		color: #ffffff !important;
	}

	.dark-mode .text-success {
		color: #4caf50 !important;
	}

	.dark-mode .text-error {
		color: #f44336 !important;
	}

	.dark-mode .save-btn {
		background: linear-gradient(90deg, #1565c0 0%, #42a5f5 100%) !important;
	}

	.dark-mode .spotify-btn {
		background: linear-gradient(90deg, #1db954 0%, #1ed760 100%) !important;
	}

	.dark-mode .v-input__details {
		color: #ffffff !important;
	}

	.dark-mode .v-messages__message {
		color: #ffffff !important;
	}

	.dark-mode .v-field__append-inner {
		color: #ffffff !important;
	}

	.dark-mode .v-field__prepend-inner {
		color: #ffffff !important;
	}

	.dark-mode .v-field__clearable {
		color: #ffffff !important;
	}

	.dark-mode .v-field__input::placeholder {
		color: rgba(255, 255, 255, 0.7) !important;
	}

	.dark-mode .v-field__input:-webkit-autofill,
	.dark-mode .v-field__input:-webkit-autofill:hover,
	.dark-mode .v-field__input:-webkit-autofill:focus {
		-webkit-text-fill-color: #ffffff !important;
		-webkit-box-shadow: 0 0 0 30px #2d2d2d inset !important;
	}
</style>
