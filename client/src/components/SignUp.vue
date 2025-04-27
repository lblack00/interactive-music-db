<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<div class="signup-wrapper">
				<v-row no-gutters class="justify-center align-center">
					<v-col cols="12" sm="8" md="6" lg="4">
						<v-card class="signup-card" elevation="8">
							<v-alert
								v-if="formError"
								type="error"
								class="error-alert"
								elevation="0"
								border="false"
								icon="mdi-close-circle"
							>
								{{ formError }}
							</v-alert>
							<v-alert
								v-if="verificationSent && !formError"
								type="success"
								class="success-alert"
								elevation="0"
								border="false"
								icon="mdi-check-circle"
							>
								Please check your email to verify your account.
							</v-alert>
							<div class="card-decoration"></div>
							<v-card-text class="pa-8">
								<div class="text-center mb-8">
									<h2 id="signup-heading" class="text-h4 font-weight-bold mb-2">
										Create Account
									</h2>
									<p class="text-subtitle-1 text-medium-emphasis">
										Join our community today
									</p>
								</div>

								<section role="region" aria-labelledby="signup-heading">
									<form @submit.prevent="signup" aria-label="Signup form">
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
											v-model="email"
											label="Email"
											id="email"
											prepend-inner-icon="mdi-email"
											variant="outlined"
											type="email"
											required
											aria-required="true"
											autocomplete="email"
											class="mb-4 input-field"
											:class="{ focused: email }"
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
											autocomplete="new-password"
											class="mb-4 input-field"
											:class="{ focused: password }"
										/>

										<v-text-field
											v-model="confirmPassword"
											label="Confirm Password"
											id="confirmPassword"
											prepend-inner-icon="mdi-lock-check"
											:type="showConfirmPassword ? 'text' : 'password'"
											:append-inner-icon="
												showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'
											"
											@click:append-inner="
												showConfirmPassword = !showConfirmPassword
											"
											variant="outlined"
											required
											aria-required="true"
											autocomplete="new-password"
											class="mb-6 input-field"
											:class="{ focused: confirmPassword }"
										/>

										<v-btn
											type="submit"
											size="large"
											block
											class="signup-button mb-4"
											elevation="2"
										>
											<span class="button-text">Create Account</span>
										</v-btn>

										<div class="text-center">
											<router-link to="/login" class="login-link">
												Already have an account? Log in
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
				returnPath: "/",
				formError: null,
				verificationSent: false,
				showPassword: false,
				showConfirmPassword: false,
			};
		},
		created() {
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
						} else {
							this.$router.push(this.returnPath || "/");
						}
					}
				} catch (error) {
					console.error("Signup error:", error);
					const errorMessage = error.response?.data?.error || "";

					if (errorMessage.includes("email already exists")) {
						this.formError =
							"This email is already registered. Please use a different email or try logging in.";
					} else if (
						errorMessage.includes("username already exists") ||
						errorMessage.includes("username is taken")
					) {
						this.formError =
							"This username is already taken. Please choose a different username.";
					} else {
						this.formError =
							errorMessage ||
							"An error occurred during signup. Please try again.";
					}
				}
			},
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";

	.signup-wrapper {
		min-height: calc(100vh - 64px);
		display: flex;
		align-items: center;
		padding: 2rem;
		transform: translateY(-15vh);
		animation: fade-in 0.6s ease-out;
	}

	.signup-card {
		border-radius: 24px;
		background: white;
		overflow: hidden;
		position: relative;
		backdrop-filter: blur(10px);
		box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.1),
			0 6px 10px -1px rgba(0, 0, 0, 0.04);
		margin-top: -64px;
		animation: fade-in-up 0.8s ease-out;
	}

	@keyframes fade-in {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	@keyframes fade-in-up {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.card-decoration {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 4px;
		background: linear-gradient(90deg, #3cba92, #2c7a7b);
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

	.signup-button {
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

	.signup-button::before {
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

	.signup-button:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(44, 122, 123, 0.2);
	}

	.signup-button:hover::before {
		opacity: 1;
	}

	.button-text {
		position: relative;
		z-index: 1;
	}

	.login-link {
		color: #2c7a7b;
		text-decoration: none;
		font-size: 0.9rem;
		transition: all 0.3s ease;
		padding: 4px 8px;
		border-radius: 4px;
	}

	.login-link:hover {
		color: #3cba92;
		text-decoration: none;
		background: rgba(44, 122, 123, 0.05);
	}

	.error-alert {
		margin: 0;
		border-radius: 24px 24px 0 0;
		font-weight: 500;
		position: relative;
		background: #e53935 !important;
		color: white !important;
		font-size: 0.95rem;
		padding: 12px 24px;
	}

	.success-alert {
		margin: 0;
		border-radius: 24px 24px 0 0;
		font-weight: 500;
		position: relative;
		background: #00a67e !important;
		color: white !important;
		font-size: 0.95rem;
		padding: 12px 24px;
	}

	:deep(.error-alert),
	:deep(.success-alert) {
		display: flex;
		align-items: center;
	}

	:deep(.error-alert .v-alert__content),
	:deep(.success-alert .v-alert__content) {
		color: white;
		margin-left: 8px;
	}

	:deep(.error-alert .v-alert__prepend),
	:deep(.success-alert .v-alert__prepend) {
		margin-right: 0;
		align-self: center;
	}

	:deep(.error-alert .v-alert__close),
	:deep(.success-alert .v-alert__close) {
		display: none;
	}

	@media (max-width: 600px) {
		.signup-wrapper {
			padding: 1rem;
		}

		.signup-card {
			border-radius: 20px;
		}
	}
</style>
