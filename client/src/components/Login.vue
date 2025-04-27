<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<div class="login-wrapper">
				<v-row no-gutters class="justify-center align-start mt-16">
					<v-col cols="12" sm="8" md="6" lg="4">
						<v-alert
							v-if="loginError"
							type="error"
							class="mb-4 error-alert"
							elevation="2"
						>
							{{ loginError }}
						</v-alert>

						<v-card class="login-card" elevation="8">
							<div class="card-decoration"></div>
							<v-card-text class="pa-8">
								<div class="text-center mb-8">
									<h2 id="login-heading" class="text-h4 font-weight-bold mb-2">
										Welcome Back
									</h2>
									<p class="text-subtitle-1 text-medium-emphasis">
										Please sign in to continue
									</p>
								</div>

								<section role="region" aria-labelledby="login-heading">
									<form @submit.prevent="login" aria-label="Login form">
										<v-text-field
											v-model="username"
											label="Username"
											id="username"
											prepend-inner-icon="mdi-account"
											variant="outlined"
											required
											aria-required="true"
											autocomplete="username"
											class="mb-4 input-field"
											:class="{ focused: username }"
										/>

										<v-text-field
											v-model="password"
											label="Password"
											id="password"
											prepend-inner-icon="mdi-lock"
											:type="showPassword ? 'text' : 'password'"
											:append-inner-icon="
												showPassword ? 'mdi-eye' : 'mdi-eye-off'
											"
											@click:append-inner="showPassword = !showPassword"
											variant="outlined"
											required
											aria-required="true"
											autocomplete="current-password"
											class="mb-6 input-field"
											:class="{ focused: password }"
										/>

										<v-btn
											type="submit"
											size="large"
											block
											class="login-button mb-4"
											elevation="2"
										>
											<span class="button-text">Sign In</span>
										</v-btn>

										<div class="text-center">
											<router-link
												to="/forgot-password"
												class="forgot-password-link"
											>
												Forgot Password?
											</router-link>
										</div>
									</form>
								</section>
							</v-card-text>
						</v-card>
					</v-col>
				</v-row>
			</div>
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
				loginError: null,
				showPassword: false,
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

	.login-wrapper {
		min-height: calc(100vh - 64px);
		display: flex;
		align-items: center;
		padding: 2rem;
		transform: translateY(-11vh);
		animation: cardSlideIn 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
	}

	.login-card {
		border-radius: 24px;
		background: white;
		overflow: hidden;
		position: relative;
		backdrop-filter: blur(10px);
		box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.1),
			0 6px 10px -1px rgba(0, 0, 0, 0.04);
		opacity: 0;
		animation: cardFadeIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
	}

	@keyframes cardSlideIn {
		0% {
			opacity: 0;
			transform: translateY(-5vh);
		}
		100% {
			opacity: 1;
			transform: translateY(-11vh);
		}
	}

	@keyframes cardFadeIn {
		0% {
			opacity: 0;
			transform: translateY(20px) scale(0.95);
		}
		100% {
			opacity: 1;
			transform: translateY(0) scale(1);
		}
	}

	.card-decoration {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 4px;
		background: linear-gradient(90deg, #3cba92, #2c7a7b);
		transform-origin: left;
		animation: decorationWidth 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) 0.3s forwards;
		transform: scaleX(0);
	}

	@keyframes decorationWidth {
		from {
			transform: scaleX(0);
		}
		to {
			transform: scaleX(1);
		}
	}

	.text-h4,
	.text-subtitle-1 {
		opacity: 0;
		animation: textFadeIn 0.6s ease-out forwards;
	}

	.text-h4 {
		animation-delay: 0.4s;
	}

	.text-subtitle-1 {
		animation-delay: 0.5s;
	}

	.input-field {
		opacity: 0;
		animation: inputSlideIn 0.5s ease-out forwards;
	}

	.input-field:nth-child(1) {
		animation-delay: 0.6s;
	}

	.input-field:nth-child(2) {
		animation-delay: 0.7s;
	}

	.login-button {
		opacity: 0;
		animation: buttonFadeIn 0.5s ease-out 0.8s forwards;
	}

	.forgot-password-link {
		opacity: 0;
		animation: textFadeIn 0.5s ease-out 0.9s forwards;
	}

	@keyframes textFadeIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes inputSlideIn {
		from {
			opacity: 0;
			transform: translateX(-20px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	@keyframes buttonFadeIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.error-alert {
		animation: alertSlideIn 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
	}

	@keyframes alertSlideIn {
		from {
			opacity: 0;
			transform: translateY(-20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.text-medium-emphasis {
		color: rgba(0, 0, 0, 0.6) !important;
	}

	.input-field {
		transition: all 0.3s ease;
	}

	.input-field:hover :deep(.v-field__outline) {
		--v-field-border-opacity: 0.4;
	}

	.input-field.focused :deep(.v-field__outline) {
		--v-field-border-opacity: 1;
		border-color: #3cba92;
	}

	:deep(.v-field__outline) {
		--v-field-border-opacity: 0.25;
		transition: all 0.3s ease;
	}

	:deep(.v-field) {
		--v-field-border-opacity: 0.25;
		border-radius: 12px;
	}

	:deep(.v-field__input) {
		font-size: 1rem;
		padding: 8px 0;
	}

	:deep(.v-field__prepend-inner) {
		padding-inline-start: 12px;
	}

	.login-button {
		background: linear-gradient(135deg, #3cba92, #2c7a7b) !important;
		color: white !important;
		font-weight: 500;
		height: 48px;
		font-size: 1.1rem;
		text-transform: none;
		letter-spacing: 0.5px;
		transition: all 0.3s ease;
		border-radius: 12px;
		position: relative;
		overflow: hidden;
	}

	.login-button::before {
		content: "";
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(
			rgba(255, 255, 255, 0.1),
			rgba(255, 255, 255, 0)
		);
		opacity: 0;
		transition: opacity 0.3s ease;
	}

	.login-button:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(44, 122, 123, 0.2);
	}

	.login-button:hover::before {
		opacity: 1;
	}

	.button-text {
		position: relative;
		z-index: 1;
	}

	.forgot-password-link {
		color: #2c7a7b;
		text-decoration: none;
		font-size: 0.9rem;
		transition: all 0.3s ease;
		padding: 4px 8px;
		border-radius: 4px;
	}

	.forgot-password-link:hover {
		color: #3cba92;
		text-decoration: none;
		background: rgba(44, 122, 123, 0.05);
	}

	.error-alert {
		border-radius: 12px;
		font-weight: 500;
	}

	@media (max-width: 600px) {
		.login-wrapper {
			padding: 1rem;
		}

		.login-card {
			border-radius: 20px;
		}
	}
</style>
