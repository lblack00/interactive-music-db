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
									placeholder="It seems you have nothing written, Tell us something about yourself..."
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
										@change="applyColorblindMode"
									></v-select>

									<v-switch
										label="Enable Patterns on UI Elements"
										hint="Adds textures to buttons to make them more distinguishable"
										persistent-hint
										@change="applyAccessibilitySettings"
									></v-switch>

									<v-switch
										label="Show Text Labels on Icons"
										hint="Displays text labels alongside icons for better clarity"
										persistent-hint
										@change="applyAccessibilitySettings"
									></v-switch>

									<div class="mt-3">
										<v-btn> Preview Accessibility Changes </v-btn>
									</div>
								</v-card>

								<h2 class="text-h5 font-weight-bold mb-2">
									Accessibility Settings
								</h2>

								<!-- Colorblind Mode Selection -->
								<v-select
									v-model="colorblindMode"
									:items="[
										'Default',
										'Red-Blind (Protanopia)',
										'Green-Blind (Deuteranopia)',
										'Blue-Blind (Tritanopia)',
										'Grayscale (achromatopsia)',
										'High Contrast',
									]"
									label="Colorblind Mode"
									outlined
									dense
									@change="applyColorblindMode"
								></v-select>

								<!-- Additional Accessibility Options -->
								<v-switch
									v-model="enablePatterns"
									label="Enable Patterns for Color Differentiation"
									@change="applyAccessibilitySettings"
								></v-switch>

								<v-switch
									v-model="showLabels"
									label="Show Additional Labels"
									@change="applyAccessibilitySettings"
								></v-switch>

								<v-btn
									color="primary"
									@click="previewAccessibilityChanges"
									class="mb-4"
								>
									Preview Changes
								</v-btn>

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

<script>
	import Navbar from "./Navbar.vue";
	import axios from "axios";

	export default {
		name: "userSettings",
		components: { Navbar },
		data() {
			return {
				loggedIn: false,
				user: {
					id: null,
					username: null,
					email: null,
					bio: null,
					profileImage: null,
					spotifyConnected: false,
				},
				originalUser: {
					id: null,
					username: null,
					email: null,
					bio: null,
					profileImage: null,
				},
				newProfileImage: null, // To store the preview of the new image
				profileFileError: "",

				errorUpdating: false,
				clientId: import.meta.env.VITE_SPOTIFY_CLIENT_ID,
				redirectUri: "http://localhost:5173/",
				colorblindMode: localStorage.getItem("colorblindMode") || "Default",
				enablePatterns: localStorage.getItem("enablePatterns") === "true",
				showLabels: localStorage.getItem("showLabels") === "true",
				accessToken: "",
			};
		},
		computed: {
			colorblindClass() {
				switch (this.colorblindMode) {
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
			},
		},
		methods: {
			async getCurrentSettings() {
				try {
					
					const response = await axios.get(
						"http://localhost:5001/check-session",
						{
							withCredentials: true,
						}
					);
					
					this.loggedIn = response.data.logged_in;
					if (response.data.logged_in) {
						this.user.username = response.data.user.username;
						this.user.id = response.data.user.id;
						this.user.email = response.data.user.email;

						this.originalUser.username = response.data.user.username;
						this.originalUser.id = response.data.user.id;
						this.originalUser.email = response.data.user.email;
						
						const imageResponse = await axios.get(
							`http://localhost:5001/get-profile-image/${this.user.id}`
						);
    				this.originalUser.profileImage = `http://localhost:5001${imageResponse.data.image_url}`;
						// console.log(imageUrl);
					}
					else {
						// Redirect to 404
						this.$router.push('/404');
					}
				} catch (error) {
					console.error("Error checking session:", error);
					this.loggedIn = false;
					this.user = null;
				}

			},

			async saveProfile() {
				if (this.user.username !== this.originalUser.username) {
					try {
						const response = await axios.post(
							"http://localhost:5001/update-username",
							{
								new_username: this.user.username
							},
							{
								withCredentials: true // if you're using session cookies
							}
						);
						console.log("Username has been updated!");
						this.originalUser.username = this.user.username;
					} catch (error) {
						this.errorUpdating = true;
						console.error("Error updating username:", error);
						if (error.response && error.response.status === 409) {
							alert("That username is already taken.");
						} else {
							alert("Error updating username");
						}
						// Revert the username on error if needed
						this.user.username = this.originalUser.username;
					}
				}

				if (this.user.bio !== this.originalUser.bio) {
					console.log("Bio has changed!");
				}

				if (this.user.profileImage !== this.originalUser.profileImage && this.user.profileImage) {
					try {
						const formData = new FormData();
						formData.append("image", this.profileFile); // file selected in handleFileUpload

						await axios.post("http://localhost:5001/update-user-pfp", formData, {
							withCredentials: true,
							headers: {
								"Content-Type": "multipart/form-data",
							},
						});

						this.originalUser.profileImage = this.user.profileImage;
						this.user.profileImage = null;
						console.log("Profile picture uploaded successfully!");
					} catch (error) {
						this.errorUpdating = true;
						console.error("Error uploading profile image:", error);
						alert("Error uploading profile image");
					}
				}

				if(!this.errorUpdating) {
					alert("Profile updated successfully!");
				}
				this.errorUpdating = false;
			},

			handleFileUpload(event) {
				const file = event.target.files[0];

				if (!file) return;

				if (file.size > 1024 * 1024) {
					this.profileFileError = "File size must be less than 1MB.";
					return;
				}

				this.profileFileError = "";
				this.profileFile = file; // <-- Save the file for later upload

				const reader = new FileReader();
				reader.onload = (e) => {
					this.user.profileImage = e.target.result; // For preview
				};
				reader.readAsDataURL(file);
			},

			applyColorblindMode() {
				const appElement = document.getElementById("app");
				if (appElement) {
					// Remove existing classes
					appElement.classList.remove(
						"protanopia",
						"deuteranopia",
						"tritanopia",
						"achromatopsia",
						"high-contrast"
					);

					// Add new class based on selected mode
					if (this.colorblindMode !== "Default") {
						appElement.classList.add(this.colorblindClass);
					}
				}
				// Save setting to localStorage for persistence
				localStorage.setItem("colorblindMode", this.colorblindMode);
			},

			applyAccessibilitySettings() {
				const appElement = document.getElementById("app");
				if (appElement) {
					// Toggle pattern class
					if (this.enablePatterns) {
						appElement.classList.add("enable-patterns");
					} else {
						appElement.classList.remove("enable-patterns");
					}

					// Toggle labels class
					if (this.showLabels) {
						appElement.classList.add("show-labels");
					} else {
						appElement.classList.remove("show-labels");
					}
				}
				// Save settings to localStorage
				localStorage.setItem("enablePatterns", this.enablePatterns);
				localStorage.setItem("showLabels", this.showLabels);
			},

			previewAccessibilityChanges() {
				this.applyColorblindMode();
				this.applyAccessibilitySettings();
				// Show a notification that changes are applied
				alert("Accessibility settings have been applied");
			},

			// For Spotify

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
					authUrl.searchParams.append("code_challenge_method", "S256");
					authUrl.searchParams.append("code_challenge", codeChallenge);

					window.location.href = authUrl.toString();
				} catch (error) {
					console.error("Error initiating Spotify auth:", error);
				}
			},
			async handleSpotifyCallback() {
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
					const response = await fetch(
						"https://accounts.spotify.com/api/token",
						{
							method: "POST",
							headers: { "Content-Type": "application/x-www-form-urlencoded" },
							body: new URLSearchParams({
								client_id: this.clientId,
								grant_type: "authorization_code",
								code: code,
								redirect_uri: this.redirectUri,
								code_verifier: localStorage.getItem("code_verifier"),
							}),
						}
					);

					const data = await response.json();
					if (data.access_token) {
						this.accessToken = data.access_token;
						localStorage.setItem("spotify_access_token", data.access_token);
						localStorage.setItem("spotify_refresh_token", data.refresh_token);
						this.user.spotifyConnected = true;
						alert("Spotify connected successfully!");
					} else {
						alert("Failed to retrieve access token");
					}
				} catch (error) {
					console.error("Error during token exchange:", error);
				}
			},
			async refreshAccessToken() {
				const refreshToken = localStorage.getItem("spotify_refresh_token");
				if (!refreshToken) return;
				try {
					const response = await fetch(
						"https://accounts.spotify.com/api/token",
						{
							method: "POST",
							headers: { "Content-Type": "application/x-www-form-urlencoded" },
							body: new URLSearchParams({
								client_id: this.clientId,
								grant_type: "refresh_token",
								refresh_token: refreshToken,
							}),
						}
					);
					const data = await response.json();
					if (data.access_token) {
						this.accessToken = data.access_token;
						localStorage.setItem("spotify_access_token", data.access_token);
					}
				} catch (error) {
					console.error("Error refreshing access token:", error);
				}
			},
			generateRandomString(length) {
				const possible =
					"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
				return Array.from(crypto.getRandomValues(new Uint8Array(length)))
					.map((x) => possible[x % possible.length])
					.join("");
			},
			generateCodeVerifier() {
				return this.generateRandomString(128);
			},
			async generateCodeChallenge(codeVerifier) {
				const encoder = new TextEncoder();
				const data = encoder.encode(codeVerifier);
				const digest = await crypto.subtle.digest("SHA-256", data);
				return this.base64UrlEncode(digest);
			},
			base64UrlEncode(buffer) {
				let binary = "";
				const bytes = new Uint8Array(buffer);
				for (let i = 0; i < bytes.byteLength; i++) {
					binary += String.fromCharCode(bytes[i]);
				}
				return btoa(binary)
					.replace(/\+/g, "-")
					.replace(/\//g, "_")
					.replace(/=+$/, "");
			},
			disconnectSpotify() {
				this.user.spotifyConnected = false;
				this.accessToken = "";
				localStorage.removeItem("spotify_access_token");
				localStorage.removeItem("spotify_refresh_token");
				alert("Spotify account disconnected.");
			},
		},
		mounted() {
			if (window.location.search.includes("code")) {
				this.handleSpotifyCallback();
			}
			setInterval(this.refreshAccessToken, 50 * 60 * 1000);

			// Apply saved settings
			this.applyColorblindMode();
			this.applyAccessibilitySettings();
		},
		beforeDestroy() {
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
		},
		created() {
			this.getCurrentSettings();
		}
	};
</script>
<style scoped>
	@import "../assets/background.css";
	@import "../assets/accessibility.css";
</style>
