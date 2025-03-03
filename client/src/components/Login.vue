<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<header role="navigation">
		<Navbar />
	</header>

	<main role="main">
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
						alert("Login unsuccessful, please try again!");
					}
				} catch (error) {
					console.error("Login error:", error);
					alert("Login failed. Please check your credentials and try again.");
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
</style>
