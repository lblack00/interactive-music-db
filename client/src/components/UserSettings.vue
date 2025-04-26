<template>
	<div
		class="grid-container"
		:class="[
			colorblindClass,
			{
				'enable-patterns': enablePatterns,
				'show-labels': showLabels,
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
								<!-- Accessibility Section -->
								<v-card class="section-card mb-6 pa-5" variant="outlined">
									<h2 class="section-title">Accessibility Settings</h2>
									<v-select
										v-model="colorblindMode"
										label="Color Vision Mode"
										:items="[
											'Default',
											'Red-Blind (Protanopia)',
											'Green-Blind (Deuteranopia)',
											'Blue-Blind (Tritanopia)',
											'Grayscale (achromatopsia)',
											'High Contrast',
										]"
										variant="outlined"
										@update:model-value="applyColorblindMode"
										class="mb-4 rounded-input"
									></v-select>
									<v-switch
										v-model="enablePatterns"
										label="Enable Patterns on UI Elements"
										hint="Adds textures to buttons to make them more distinguishable"
										persistent-hint
										@update:model-value="applyAccessibilitySettings"
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

	const colorblindMode = ref(accessibilityStore.colorblindMode);
	const enablePatterns = ref(accessibilityStore.enablePatterns);
	const showLabels = ref(accessibilityStore.showLabels);

	// Watch for store changes
	watch(
		() => accessibilityStore.colorblindMode,
		(newValue) => {
			colorblindMode.value = newValue;
		}
	);

	watch(
		() => accessibilityStore.enablePatterns,
		(newValue) => {
			enablePatterns.value = newValue;
		}
	);

	watch(
		() => accessibilityStore.showLabels,
		(newValue) => {
			showLabels.value = newValue;
		}
	);

	const applyColorblindMode = () => {
		accessibilityStore.setColorblindMode(colorblindMode.value);
	};

	const applyAccessibilitySettings = () => {
		accessibilityStore.setEnablePatterns(enablePatterns.value);
	};

	onMounted(() => {
		getCurrentSettings();

		// Handle Spotify callback if needed
		if (window.location.search.includes("code")) {
			handleSpotifyCallback();
		}
		setInterval(refreshAccessToken, 50 * 60 * 1000);

		// Initialize values from store
		colorblindMode.value = accessibilityStore.colorblindMode;
		enablePatterns.value = accessibilityStore.enablePatterns;
		showLabels.value = accessibilityStore.showLabels;

		// Apply saved settings
		applyColorblindMode();
		applyAccessibilitySettings();
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
			appElement.classList.remove(
				"protanopia",
				"deuteranopia",
				"tritanopia",
				"achromatopsia",
				"high-contrast",
				"enable-patterns",
				"show-labels"
			);
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
	}
	.settings-card {
		border-radius: 22px;
		box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08), 0 1.5px 6px rgba(0, 0, 0, 0.04);
		background: var(--background-color);
		color: var(--text-color);
		padding-bottom: 32px;
	}
	.section-card {
		border-radius: 16px;
		background: #f8fafc;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
		border: 1px solid #e3e9f3;
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
	}
	.section-title {
		font-size: 1.25rem;
		font-weight: 600;
		color: #26326a;
		margin-bottom: 18px;
		border-left: 4px solid #42a5f5;
		padding-left: 12px;
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
	.achromatopsia .save-btn,
	.achromatopsia .spotify-btn {
		font-weight: 900 !important;
		text-shadow: 0 2px 6px #fff, 0 -2px 6px #000;
		background-color: #bdbdbd !important;
		color: #222 !important;
	}
</style>
