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
		<div class="content">
			<!-- Todo: this is a mock user profile edit page which requires a user logged in -->
			<v-container>
				<v-row justify="center">
					<v-col cols="12" md="6">
						<v-card class="pa-4">
							<h1 class="text-h4 font-weight-bold mb-4">User Settings</h1>
							<v-form @submit.prevent="saveProfile">
								<v-text-field
									v-model="user.username"
									label="Username"
									outlined
									required
								></v-text-field>
								<v-text-field
									v-model="user.email"
									label="Email"
									outlined
									required
									readonly
								></v-text-field>
								<v-textarea
									v-model="user.bio"
									placeholder="It seems you have nothing written. Tell us something about yourself..."
									label="Bio"
									outlined
									rows="3"
									:counter="500"
									maxlength="500"
								></v-textarea>

								<!-- Profile Picture Section -->
								<h2 class="text-h5 font-weight-bold mt-4">Profile Picture</h2>

								<!-- 
						TODO: Fix this so the size changes dynammically when window size is changed, as 
						it currentyly is permanantly 200x200
						-->
								<v-row justify="center">
									<!-- Current Profile Image -->
									<v-col cols="5" class="text-center">
										<p class="font-weight-bold">Current</p>
										<img
											:src="originalUser.profileImage"
											height="200"
											width="200"
											class="mt-2 mx-auto"
											style="object-fit: fill; display: block"
										/>
									</v-col>

									<!-- New Profile Image Preview -->
									<v-col cols="5" class="text-center" v-if="user.profileImage">
										<p class="font-weight-bold">New</p>
										<img
											:src="user.profileImage"
											height="200"
											width="200"
											class="mt-2 mx-auto"
											style="object-fit: fill; display: block"
										/>
									</v-col>
								</v-row>

								<v-file-input
									label="Upload New Profile Picture (No larger than 1MB)"
									accept="image/*"
									@change="handleFileUpload"
									class="mt-4"
								/>
								<p v-if="profileFileError" style="color: red">
									{{ profileFileError }}
								</p>

								<v-divider class="my-4"></v-divider>
								<h2 class="text-h5 font-weight-bold mb-2">Accessibility</h2>
								<v-card class="mb-4 pa-3">
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
									></v-select>

									<v-switch
										v-model="enablePatterns"
										label="Enable Patterns on UI Elements"
										hint="Adds textures to buttons to make them more distinguishable"
										persistent-hint
										@update:model-value="applyAccessibilitySettings"
									></v-switch>

									<v-switch
										v-model="showLabels"
										label="Show Text Labels on Icons"
										hint="Displays text labels alongside icons for better clarity"
										persistent-hint
										@update:model-value="applyAccessibilitySettings"
									></v-switch>
								</v-card>

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
									>Connect Spotify</v-btn
								>
								<v-btn v-else color="red" @click="disconnectSpotify"
									>Disconnect Spotify</v-btn
								>
								<v-divider class="my-4"></v-divider>
								<v-btn type="submit" color="primary">Save Changes</v-btn>
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
		accessibilityStore.setShowLabels(showLabels.value);
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
</style>
