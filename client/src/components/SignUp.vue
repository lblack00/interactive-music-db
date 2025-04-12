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
						<v-alert v-if="formError" type="error" class="mt-10" >
							{{ formError }}
						</v-alert>
					</v-col>
				</v-row>

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

				<v-alert v-if="verificationSent" type="success" class="mt-10">
					Please check your email to verify your account.
				</v-alert>
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
				formError: null,
				verificationSent: false,
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
					this.formError = "Passwords do not match";
					return;
				}

				this.formError = null;

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
						withCredentials: true,
					});

					if (response.status === 201) {
						if (response.data.requiresVerification) {
							this.verificationSent = true;
							// Don't redirect, show verification message instead
						} else {
							this.$router.push(this.returnPath || "/");
						}
					}
				} catch (error) {
					console.error("Signup error:", error);
					this.formError = error.response?.data?.error || "An error occurred during signup. Please try again.";
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
