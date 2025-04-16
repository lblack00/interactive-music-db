<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<div
		class="grid-container"
		:class="[
			colorblindClass,
			{ 'enable-patterns': enablePatterns, 'show-labels': showLabels },
		]"
	>
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<main role="main">
				<v-row no-gutters class="justify-center">
					<v-col cols="4">
						<v-alert v-if="signupError" type="error" class="mt-10">
							{{ signupError }}
						</v-alert>
					</v-col>
				</v-row>

				<div class="container mt-5">
					<h2 id="signup-heading">Sign Up</h2>

					<section role="region" aria-labelledby="signup-heading">
						<form @submit.prevent="signup" aria-label="Sign up form">
							<div class="row" role="form" aria-labelledby="username-label">
								<label id="username-label" for="username">Username</label>
								<input
									type="username"
									id="username"
									v-model="username"
									required
									aria-required="true"
									autocomplete="username"
								/>
							</div>

							<div class="row" role="form" aria-labelledby="email-label">
								<label id="email-label" for="email">Email</label>
								<input
									type="email"
									id="email"
									v-model="email"
									required
									aria-required="true"
									autocomplete="email"
								/>
							</div>

							<div class="row" role="form" aria-labelledby="password-label">
								<label id="password-label" for="password">Password</label>
								<input
									type="password"
									id="password"
									v-model="password"
									required
									aria-required="true"
									autocomplete="new-password"
								/>
							</div>

							<div
								class="row"
								role="form"
								aria-labelledby="confirm-password-label"
							>
								<label id="confirm-password-label" for="confirmPassword"
									>Confirm Password</label
								>
								<input
									type="password"
									id="confirmPassword"
									v-model="confirmPassword"
									required
									aria-required="true"
									autocomplete="new-password"
								/>
							</div>

							<button type="submit" aria-label="Create new account">
								Sign Up
							</button>
						</form>
					</section>
				</div>
			</main>
		</div>
	</div>
</template>

<script>
	import axios from "axios";
	import Navbar from "./Navbar.vue";

	export default {
		name: "SignUp",
		components: {
			Navbar,
		},
		data() {
			return {
				username: "",
				email: "",
				password: "",
				confirmPassword: "",
				signupError: null,
				colorblindMode: localStorage.getItem("colorblindMode") || "Default",
				enablePatterns: localStorage.getItem("enablePatterns") === "true",
				showLabels: localStorage.getItem("showLabels") === "true",
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
			async signup() {
				this.signupError = null;

				if (this.password !== this.confirmPassword) {
					this.signupError = "Passwords do not match";
					return;
				}

				try {
					const path = "http://localhost:5001/signup";
					const response = await axios.post(path, {
						username: this.username,
						email: this.email,
						password: this.password,
					});

					if (response.status === 200) {
						await this.$router.push("/login");
					} else {
						this.signupError = "Error creating account";
					}
				} catch (error) {
					console.error("Signup error:", error);
					this.signupError =
						error.response.data.error || "Error creating account";
				}
			},
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";
	@import "../../src/assets/login.css";
</style>
