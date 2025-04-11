<!-- This file was written by Jax Hendrickson -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->

<template>
	<!-- <div class="grid-container"> -->
	<!-- <div class="content"> -->
	<section class="rating-system" role="region" aria-label="Rating system">
		<div
			class="stars"
			@mouseleave="resetTempRating"
			role="group"
			aria-label="Rate from 1 to 10 stars"
		>
			<span
				v-for="star in 10"
				:key="star"
				class="star"
				:class="{
					filled: star <= (tempRating || userRating || averageRating),
					'user-rated': star <= userRating,
				}"
				@mouseover="setTempRating(star)"
				@click="rateItem(star)"
				tabindex="0"
				role="button"
				:aria-label="`${star} star${star === 1 ? '' : 's'}`"
				:aria-pressed="star <= userRating"
				@keydown.enter="rateItem(star)"
				@keydown.space.prevent="rateItem(star)"
			>
				★
			</span>
		</div>
		<div class="rating-info" aria-live="polite">
			<span v-if="averageRating">{{ averageRating.toFixed(1) }} / 10</span>
			<span v-if="totalRatings">({{ totalRatings }} ratings)</span>
		</div>
		<transition name="fade">
			<div
				class="login-prompt-overlay"
				v-if="showLoginPrompt"
				role="dialog"
				aria-labelledby="login-prompt-title"
				aria-modal="true"
			>
				<div class="login-prompt-modal">
					<h3 id="login-prompt-title">Please Log In</h3>
					<p>You need to be logged in to rate items.</p>
					<div class="buttons" role="group" aria-label="Login options">
						<button
							class="cancel-btn"
							@click="showLoginPrompt = false"
							aria-label="Cancel and return to page"
						>
							Cancel
						</button>
						<button
							class="login-btn"
							@click="goToLogin"
							aria-label="Go to login page"
						>
							Log In
						</button>
						<button
							class="signup-btn"
							@click="goToSignup"
							aria-label="Go to signup page"
						>
							Sign Up
						</button>
					</div>
				</div>
			</div>
		</transition>
	</section>
	<!-- </div> -->
	<!-- </div> -->
</template>

<script>
	import axios from "axios";

	export default {
		name: "RatingSystem",
		props: {
			itemType: {
				type: String,
				required: true,
			},
			itemId: {
				required: true,
			},
		},
		data() {
			return {
				userRating: 0,
				averageRating: 0,
				totalRatings: 0,
				tempRating: 0,
				showLoginPrompt: false,
			};
		},
		watch: {
			itemId: {
				immediate: true,
				handler() {
					this.fetchRatings();
				},
			},
		},
		methods: {
			setTempRating(rating) {
				this.tempRating = rating;
			},
			resetTempRating() {
				this.tempRating = 0;
			},
			async rateItem(rating) {
				try {
					const sessionResponse = await axios.get(
						"http://localhost:5001/check-session",
						{
							withCredentials: true,
						}
					);

					if (!sessionResponse.data.logged_in) {
						this.showLoginPrompt = true;
						return;
					}

					const response = await axios.post(
						"http://localhost:5001/rate",
						{
							item_type: this.itemType,
							item_id: this.itemId,
							rating: rating,
						},
						{
							withCredentials: true,
						}
					);

					if (response.data.success) {
						this.userRating = rating;
						await this.fetchRatings();
					}
				} catch (error) {
					console.error("Error submitting rating:", error);
				}
			},
			async fetchRatings() {
				try {
					const response = await axios.get(`http://localhost:5001/ratings`, {
						params: {
							item_type: this.itemType,
							item_id: this.itemId,
						},
					});

					this.averageRating = response.data.average;
					this.totalRatings = response.data.total;

					const sessionResponse = await axios.get(
						"http://localhost:5001/check-session",
						{
							withCredentials: true,
						}
					);

					if (sessionResponse.data.logged_in) {
						const userResponse = await axios.get(
							`http://localhost:5001/user-rating`,
							{
								params: {
									item_type: this.itemType,
									item_id: this.itemId,
								},
								withCredentials: true,
							}
						);
						this.userRating = userResponse.data.rating || 0;
					}
				} catch (error) {
					console.error("Error fetching ratings:", error);
				}
			},
			goToLogin() {
				const returnTo = window.location.pathname + window.location.search;
				window.location.href = `/login?returnTo=${encodeURIComponent(
					returnTo
				)}`;
			},
			goToSignup() {
				const returnTo = window.location.pathname + window.location.search;
				window.location.href = `/signup?returnTo=${encodeURIComponent(
					returnTo
				)}`;
			},
		},
	};
</script>

<style scoped>
	@import "../assets/background.css";
	.rating-system {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.5rem;
	}

	.stars {
		display: flex;
		gap: 0.25rem;
	}

	.star {
		cursor: pointer;
		font-size: 2rem;
		color: #ddd;
		text-shadow: 0 0 1px rgba(0, 0, 0, 0.4);
		transition: all 0.2s ease-in-out;
	}

	.star:hover {
		transform: scale(1.1);
	}

	.star.filled {
		color: #ffd700;
		text-shadow: 0 0 4px rgba(255, 215, 0, 0.4);
	}

	.star.user-rated {
		color: #ffa500;
		text-shadow: 0 0 4px rgba(255, 165, 0, 0.4);
	}

	.rating-info {
		font-size: 0.9rem;
		color: #666;
	}

	.login-prompt-overlay {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(0, 0, 0, 0.7);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 9999;
		backdrop-filter: blur(3px);
	}

	.login-prompt-modal {
		background: white;
		padding: 2.5rem;
		border-radius: 12px;
		box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
		min-width: 320px;
	}

	.login-prompt-modal h3 {
		margin: 0 0 1rem 0;
		color: #1a1a1a;
		font-size: 1.5rem;
		font-weight: 600;
	}

	.login-prompt-modal p {
		margin: 0 0 1.5rem 0;
		color: #4a4a4a;
		font-size: 1rem;
		line-height: 1.5;
	}

	.buttons {
		display: flex;
		gap: 0.75rem;
		justify-content: center;
	}

	.buttons button {
		padding: 0.75rem 1.5rem;
		border: none;
		border-radius: 8px;
		cursor: pointer;
		font-weight: 500;
		font-size: 0.95rem;
		transition: all 0.2s ease;
	}

	.cancel-btn {
		background: #f0f0f0;
		color: #666;
	}

	.cancel-btn:hover {
		background: #e4e4e4;
	}

	.login-btn {
		background: #007bff;
		color: white;
	}

	.login-btn:hover {
		background: #0056b3;
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
	}

	.signup-btn {
		background: #28a745;
		color: white;
	}

	.signup-btn:hover {
		background: #218838;
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(40, 167, 69, 0.2);
	}

	.fade-enter-active,
	.fade-leave-active {
		transition: opacity 0.3s;
	}

	.fade-enter,
	.fade-leave-to {
		opacity: 0;
	}
</style>
