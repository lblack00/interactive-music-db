<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<div class="forgot-wrapper">
				<v-row no-gutters class="justify-center align-center">
					<v-col cols="12" sm="8" md="6" lg="4">
						<v-card class="forgot-card" elevation="8">
							<v-alert
								v-if="error"
								type="error"
								class="error-alert"
								elevation="0"
								border="false"
							>
								{{ error }}
							</v-alert>
							<v-alert
								v-if="success"
								type="success"
								class="success-alert"
								elevation="0"
								border="false"
							>
								{{ success }}
							</v-alert>
							<div class="card-decoration"></div>
							<v-card-text class="pa-8">
								<div class="text-center mb-8">
									<h2
										id="forgot-password-heading"
										class="text-h4 font-weight-bold mb-2"
									>
										Reset Password
									</h2>
									<p class="text-subtitle-1 text-medium-emphasis">
										Enter your email to receive reset instructions
									</p>
								</div>

								<section
									role="region"
									aria-labelledby="forgot-password-heading"
								>
									<form
										@submit.prevent="requestReset"
										aria-label="Password reset form"
									>
										<v-text-field
											v-model="email"
											label="Email"
											id="email"
											prepend-inner-icon="mdi-email"
											variant="outlined"
											type="email"
											required
											aria-required="true"
											class="mb-6 input-field"
											:class="{ focused: email }"
										/>

										<v-btn
											type="submit"
											size="large"
											block
											class="forgot-button mb-4"
											elevation="2"
										>
											<span class="button-text">Send Reset Link</span>
										</v-btn>

										<div class="text-center">
											<router-link to="/login" class="login-link">
												Back to Login
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
		name: "ForgotPassword",
		components: {
			Navbar,
		},
		data() {
			return {
				email: "",
				error: null,
				success: null,
			};
		},
		methods: {
			async requestReset() {
				this.error = null;
				this.success = null;

				try {
					const response = await axios.post(
						"http://localhost:5001/request-password-reset",
						{
							email: this.email,
						}
					);

					this.success =
						"If an account exists with this email, you will receive password reset instructions.";
				} catch (error) {
					this.error = "An error occurred. Please try again later.";
					console.error("Password reset error:", error);
				}
			},
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";

	.forgot-wrapper {
		min-height: calc(100vh - 64px);
		display: flex;
		align-items: center;
		padding: 2rem;
		transform: translateY(-11vh);
	}

	.forgot-card {
		border-radius: 24px;
		background: white;
		overflow: hidden;
		position: relative;
		backdrop-filter: blur(10px);
		box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.1),
			0 6px 10px -1px rgba(0, 0, 0, 0.04);
		margin-top: -64px;
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

	.forgot-button {
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

	.forgot-button::before {
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

	.forgot-button:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(44, 122, 123, 0.2);
	}

	.forgot-button:hover::before {
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
	}

	.success-alert {
		margin: 0;
		border-radius: 24px 24px 0 0;
		font-weight: 500;
		position: relative;
		background: #00a67e !important;
		color: white !important;
	}

	:deep(.success-alert .v-alert__content) {
		color: white;
	}

	:deep(.v-alert__close) {
		color: white;
	}

	@media (max-width: 600px) {
		.forgot-wrapper {
			padding: 1rem;
		}

		.forgot-card {
			border-radius: 20px;
		}
	}
</style>
