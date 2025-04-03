<template>
	<div class="grid-container">
		<div class="content">
			<header role="navigation">
				<Navbar />
			</header>

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
								></v-text-field>
								<v-textarea
									v-model="user.bio"
									label="Bio"
									outlined
									rows="3"
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
											:src="user.profileImage"
											height="200"
											width="200"
											class="mt-2 mx-auto"
											style="object-fit: fill; display: block"
										/>
									</v-col>

									<!-- New Profile Image Preview -->
									<v-col cols="5" class="text-center" v-if="newProfileImage">
										<p class="font-weight-bold">New</p>
										<img
											:src="newProfileImage"
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

	export default {
		name: "userSettings",
		components: { Navbar },
		data() {
			return {
				user: {
					username: "Username",
					email: "username@example.com",
					bio: "This is my bio!",
					profileImage: "/images/UnknownPerson.png",
					spotifyConnected: false,
				},
				newProfileImage: null, // To store the preview of the new image
				profileFileError: "",
				clientId: import.meta.env.VITE_SPOTIFY_CLIENT_ID,
				redirectUri: "http://localhost:5173/",
				colorblindMode: "Default",
				enablePatterns: false,
				showLabels: false,
				accessToken: "",
			};
		},
		methods: {
			saveProfile() {
				alert("Profile updated successfully!");
				// Needs to be implemented
			},
			handleFileUpload(event) {
				const file = event.target.files[0]; // Get the selected file

				if (!file) return; // If no file is selected, do nothing

				if (file.size > 1024 * 1024) {
					// Check if file is larger than 1MB
					this.profileFileError = "File size must be less than 1MB.";
					return;
				}

				this.profileFileError = ""; // Clear any previous errors

				const reader = new FileReader();
				reader.onload = (e) => {
					this.newProfileImage = e.target.result; // Update new profile image preview
				};
				reader.readAsDataURL(file);
			},

			//For Colorblind settings
			injectSVGFilters() {
				// Skip if filters are already injected
				if (document.getElementById("colorblind-filters")) {
					return;
				}

				// Create SVG filters
				const svgFilters = `
					<svg xmlns="http://www.w3.org/2000/svg" style="display: none;" id="colorblind-filters">
					<!-- Protanopia (Red-Blind) Filter -->
					<filter id="protanopia-filter">
						<feColorMatrix type="matrix" 
						values="0.567, 0.433, 0,     0, 0
								0.558, 0.442, 0,     0, 0
								0,     0.242, 0.758, 0, 0
								0,     0,     0,     1, 0"/>
					</filter>
					
					<!-- Deuteranopia (Green-Blind) Filter -->
					<filter id="deuteranopia-filter">
						<feColorMatrix type="matrix" 
						values="0.625, 0.375, 0,   0, 0
								0.7,   0.3,   0,   0, 0
								0,     0.3,   0.7, 0, 0
								0,     0,     0,   1, 0"/>
					</filter>
					
					<!-- Tritanopia (Blue-Blind) Filter -->
					<filter id="tritanopia-filter">
						<feColorMatrix type="matrix" 
						values="0.95, 0.05,  0,     0, 0
								0,    0.433, 0.567, 0, 0
								0,    0.475, 0.525, 0, 0
								0,    0,     0,     1, 0"/>
					</filter>

					<!-- Achromatopsia (Grayscale) Filter -->
					<filter id="achromatopsia-filter">
					<feColorMatrix 
						type="matrix" 
						values="0.299, 0.587, 0.114, 0, 0
								0.299, 0.587, 0.114, 0, 0
								0.299, 0.587, 0.114, 0, 0
								0,     0,     0,     1, 0"/>
					</filter>
					</svg>
				`;

				// Insert SVG filters into the document
				const div = document.createElement("div");
				div.innerHTML = svgFilters;
				document.body.appendChild(div.firstChild);
			},
			applyColorblindMode() {
				//remove any existing colorblind classes
				document.body.classList.remove(
					"protanopia",
					"deuteranopia",
					"tritanopia",
					"achromatopsia",
					"high-contrast"
				);

				//apply the correct class based on selection
				switch (this.colorblindMode) {
					case "Red-Blind (Protanopia)":
						document.body.classList.add("protanopia");
						break;
					case "Green-Blind (Deuteranopia)":
						document.body.classList.add("deuteranopia");
						break;
					case "Blue-Blind (Tritanopia)":
						document.body.classList.add("tritanopia");
						break;
					case "Grayscale (achromatopsia)":
						document.body.classList.add("achromatopsia");
						break;
					case "High Contrast":
						document.body.classList.add("high-contrast");
						break;
					default:
						break;
				}

				// Save setting to localStorage for persistence
				localStorage.setItem("colorblindMode", this.colorblindMode);
			},

			applyAccessibilitySettings() {
				// For the enable patterns switch
				if (this.enablePatterns) {
					document.body.classList.add("enable-patterns");
				} else {
					document.body.classList.remove("enable-patterns");
				}

				// For the show labels switch
				if (this.showLabels) {
					document.body.classList.add("show-labels");
				} else {
					document.body.classList.remove("show-labels");
				}

				// Save settings to localStorage
				localStorage.setItem("enablePatterns", this.enablePatterns);
				localStorage.setItem("showLabels", this.showLabels);
			},

			previewAccessibilityChanges() {
				// Apply both color and other accessibility settings
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
			this.injectSVGFilters();

			// Load saved colorblind mode
			const savedColorblindMode = localStorage.getItem("colorblindMode");
			if (savedColorblindMode) {
				this.colorblindMode = savedColorblindMode;
				this.applyColorblindMode();
			}

			// Load saved accessibility settings
			const savedEnablePatterns =
				localStorage.getItem("enablePatterns") === "true";
			const savedShowLabels = localStorage.getItem("showLabels") === "true";

			if (savedEnablePatterns || savedShowLabels) {
				this.enablePatterns = savedEnablePatterns;
				this.showLabels = savedShowLabels;
				this.applyAccessibilitySettings();
			}
		},
	};
</script>
<style scoped>
	@import "../../src/assets/background.css";
	@import "../assets/accessibility.css";
</style>
