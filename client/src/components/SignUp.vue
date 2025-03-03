<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<header role="navigation">
		
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
					<div class="row" role="form" aria-labelledby="confirmPasswordlabel">
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
					<button type="submit" aria-label="Complete signup">Sign Up</button>
				</form>
			</section>
		</div>
	</main>
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
	body {
		font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
		background-color: #ecf0f1;
		color: #333;
		line-height: 1.6;
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}

	.container {
		background-color: #ffffff;
		padding: 40px;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		max-width: 400px;
		width: 100%;
		box-sizing: border-box;
		text-align: center;
	}

	h2 {
		font-size: 2rem;
		color: #1abc9c;
		margin-bottom: 20px;
	}

	form {
		display: flex;
		flex-direction: column;
		gap: 20px;
	}

	.row {
		display: flex;
		flex-direction: column;
		gap: 5px;
	}

	label {
		font-size: 1rem;
		color: #34495e;
		font-weight: 500;
		text-align: left;
	}

	input {
		padding: 12px;
		font-size: 1rem;
		color: #34495e;
		background-color: #ecf0f1;
		border: 1px solid #bdc3c7;
		border-radius: 5px;
		transition: border 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
	}

	input:focus {
		border-color: #16a085;
		outline: none;
		box-shadow: 0 0 5px rgba(22, 160, 133, 0.5);
	}

	button {
		padding: 12px;
		font-size: 1rem;
		color: #fff;
		background-color: #1abc9c;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	button:hover {
		background-color: #16a085;
	}

	button:active {
		background-color: #1e8a74;
	}

	@media (max-width: 768px) {
		.container {
			padding: 20px;
		}

		h2 {
			font-size: 1.5rem;
		}

		input {
			padding: 10px;
		}

		button {
			padding: 10px;
		}
	}

	.mt-3 {
		margin-top: 20px;
	}
</style>
