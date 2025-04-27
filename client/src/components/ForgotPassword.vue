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
		justify-content: center;
		transform: translateY(-11vh);
		animation: fadeIn 0.6s ease-out;
	}

	.forgot-card {
		width: 100%;
		max-width: 480px;
		border-radius: 16px;
		box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1),
			0 8px 10px -6px rgba(0, 0, 0, 0.1);
		position: relative;
		overflow: hidden;
		animation: slideUp 0.6s ease-out;
	}

	.forgot-card::before {
		content: "";
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 4px;
		background: linear-gradient(135deg, #3cba92 0%, #2c7a7b 100%);
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	@keyframes slideUp {
		from {
			transform: translateY(20px);
			opacity: 0;
		}
		to {
			transform: translateY(0);
			opacity: 1;
		}
	}

	.v-enter-active,
	.v-leave-active {
		transition: opacity 0.3s ease;
	}

	.v-enter-from,
	.v-leave-to {
		opacity: 0;
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
		background: linear-gradient(135deg, #3cba92 0%, #2c7a7b 100%);
		color: white;
		font-weight: 600;
		letter-spacing: 0.5px;
		text-transform: none;
		transition: all 0.3s ease;
		position: relative;
		overflow: hidden;
	}

	.forgot-button:hover {
		transform: translateY(-1px);
		box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
	}

	.forgot-button:active {
		transform: translateY(1px);
	}

	.button-text {
		position: relative;
		z-index: 1;
	}

	.login-link {
		color: #3cba92;
		text-decoration: none;
		font-weight: 500;
		transition: color 0.3s ease;
	}

	.login-link:hover {
		color: #2c7a7b;
	}

	.error-alert,
	.success-alert {
		margin-bottom: 1rem;
		border-radius: 12px;
	}

	.error-alert {
		background-color: #fee2e2 !important;
		color: #991b1b !important;
	}

	.success-alert {
		background-color: #dcfce7 !important;
		color: #166534 !important;
	}

	@media (max-width: 600px) {
		.forgot-wrapper {
			padding: 1rem;
			transform: translateY(-8vh);
		}

		.forgot-card {
			margin-top: -32px;
		}
	}
</style>
