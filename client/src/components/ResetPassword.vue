<!-- This file was written by Jax Hendrickson -->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<div class="reset-wrapper">
				<v-row no-gutters class="justify-center align-start mt-16">
					<v-col cols="12" sm="8" md="6" lg="4">
						<v-alert
							v-if="error"
							type="error"
							class="mb-4 error-alert"
							elevation="2"
						>
							{{ error }}
						</v-alert>
						<v-alert
							v-if="success"
							type="success"
							class="mb-4 success-alert"
							elevation="2"
						>
							{{ success }}
						</v-alert>

						<v-card class="reset-card" elevation="8">
							<div class="card-decoration"></div>
							<v-card-text class="pa-8">
								<div class="text-center mb-8">
									<h2
										id="reset-password-heading"
										class="text-h4 font-weight-bold mb-2"
									>
										Set New Password
									</h2>
									<p class="text-subtitle-1 text-medium-emphasis">
										Enter your new password below
									</p>
								</div>

								<section role="region" aria-labelledby="reset-password-heading">
									<form
										@submit.prevent="resetPassword"
										aria-label="Password reset form"
									>
										<v-text-field
											v-model="password"
											label="New Password"
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
											class="mb-6 input-field"
											:class="{ focused: confirmPassword }"
										/>

										<v-btn
											type="submit"
											size="large"
											block
											class="reset-button mb-4"
											elevation="2"
										>
											<span class="button-text">Reset Password</span>
										</v-btn>
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
		name: "ResetPassword",
		components: {
			Navbar,
		},
		data() {
			return {
				password: "",
				confirmPassword: "",
				error: null,
				success: null,
				showPassword: false,
				showConfirmPassword: false,
			};
		},
		methods: {
			async resetPassword() {
				this.error = null;
				this.success = null;

				if (this.password !== this.confirmPassword) {
					this.error = "Passwords do not match";
					return;
				}

				try {
					const token = this.$route.query.token;
					const response = await axios.post(
						"http://localhost:5001/reset-password",
						{
							token: token,
							password: this.password,
						}
					);

					this.success =
						"Password reset successful. You can now login with your new password.";
					setTimeout(() => {
						this.$router.push("/login");
					}, 3000);
				} catch (error) {
					this.error =
						error.response?.data?.error ||
						"An error occurred. Please try again.";
				}
			},
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";

	.reset-wrapper {
		min-height: calc(100vh - 64px);
		display: flex;
		align-items: flex-start;
		padding: 2rem;
	}

	.reset-card {
		border-radius: 24px;
		background: white;
		overflow: hidden;
		position: relative;
		backdrop-filter: blur(10px);
		box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.1),
			0 6px 10px -1px rgba(0, 0, 0, 0.04);
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

	.reset-button {
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

	.reset-button::before {
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

	.reset-button:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(44, 122, 123, 0.2);
	}

	.reset-button:hover::before {
		opacity: 1;
	}

	.button-text {
		position: relative;
		z-index: 1;
	}

	.error-alert,
	.success-alert {
		border-radius: 12px;
		font-weight: 500;
	}

	@media (max-width: 600px) {
		.reset-wrapper {
			padding: 1rem;
		}

		.reset-card {
			border-radius: 20px;
		}
	}
</style>
