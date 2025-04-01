<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<main role="main">
				<v-row no-gutters class="justify-center">
					<v-col cols="4">
						<v-alert v-if="loginError" type="error" class="mt-10" >
							{{ loginError }}
						</v-alert>
					</v-col>
				</v-row>

				<div class="container mt-5">
					<h2 id="login-heading">Login</h2>

					<section role="region" aria-labelledby="login-heading">
						<form @submit.prevent="login" aria-label="Login form">
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

							<div class="row" role="form" aria-labelledby="password-label">
								<label id="password-label" for="password">Password</label>
								<input
									type="password"
									id="password"
									v-model="password"
									required
									aria-required="true"
									autocomplete="current-password"
								/>
							</div>
							<button type="submit">Login</button>
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
		name: "Login",
		components: {
			Navbar,
		},
		data() {
			return {
				username: "",
				password: "",
				returnPath: "/",
				loginError: null
			};
		},
		created() {
			// Get return path from URL query parameters
			const returnTo = this.$route.query.returnTo;
			if (returnTo) {
				this.returnPath = returnTo;
				console.log("Setting return path to:", returnTo);
			}
		},
		methods: {
			async login() {
				this.loginError = null;

				try {
					const path = "http://localhost:5001/login";
					const response = await axios.post(
						path,
						{
							username: this.username,
							password: this.password,
						},
						{
							withCredentials: true,
						}
					);

					if (response.status == 200) {
						console.log("Login successful, returning to:", this.returnPath);
						// Use replace instead of push to avoid browser history issues
						await this.$router.replace(this.returnPath);
					} else {
						this.loginError = error.response.data.error || "Error logging on";
					}
				} catch (error) {
					console.error("Login error:", error);
					this.loginError = error.response.data.error || "Error logging on";
				}
			},
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";
	@import "../../src/assets/login.css";
</style>
