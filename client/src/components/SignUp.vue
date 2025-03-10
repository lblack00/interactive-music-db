<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<div class="grid-container">
		<div class="content">
			<header role="navigation">
				<Navbar />
			</header>

			<main role="main">
				<div class="container mt-5">
					<h2 id="signup-heading">Sign Up</h2>
					<section role="region" aria-labelledby="signup-heading">
						<form @submit.prevent="signup" aria-label="Signup form">
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
								aria-labelledby="confirmPasswordlabel"
							>
								<label id="confirmPassword-label" for="confirmPassword"
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
							<button type="submit" aria-label="Complete signup">
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
				returnPath: "/", // Default to home
			};
		},
		created() {
			// Store the previous path if it exists
			if (this.$route.query.returnTo) {
				this.returnPath = decodeURIComponent(this.$route.query.returnTo);
			}
		},
		methods: {
			async signup() {
				if (this.password !== this.confirmPassword) {
					alert("Passwords do not match!");
					return;
				}

				try {
					const path = "http://localhost:5001/signup";
					const data = {
						username: this.username,
						email: this.email,
						password: this.password,
					};

					const response = await axios.post(path, data, {
						headers: {
							"Content-Type": "application/json",
						},
						withCredentials: true, // Important for CORS with credentials
					});

					if (response.status === 201) {
						console.log("Signup successful");
						this.$router.push(this.returnPath || "/");
					}
				} catch (error) {
					console.error("Signup error:", error);
					if (error.response?.data?.error) {
						alert(error.response.data.error);
					} else {
						alert("An error occurred during signup. Please try again.");
					}
				}
			},
		},
	};
</script>

<style scoped>
	@import "../assets/login.css";
	@import "../assets/background.css";
	.mt-3 {
		margin-top: 20px;
	}
</style>
