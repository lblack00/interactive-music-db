<!-- This file was written by Chantelle Cabanilla -->
<template>
	<div class="accessibility-carousel-container">
		<div
			class="accessibility-carousel"
			role="region"
			:aria-label="ariaLabel || 'Image carousel'"
			tabindex="0"
			@keydown="handleKeyDown"
		>
			<!-- Carousel navigation controls visible to screen readers -->
			<div class="carousel-controls sr-only">
				<button
					ref="firstSlideBtn"
					@click="goToSlide(0)"
					aria-label="Go to first slide"
				>
					First slide
				</button>
				<button @click="previousSlide" aria-label="Previous slide">
					Previous
				</button>
				<button @click="nextSlide" aria-label="Next slide">Next</button>
				<button
					@click="goToSlide(totalSlides - 1)"
					aria-label="Go to last slide"
				>
					Last slide
				</button>
			</div>

			<!-- Status info for screen readers -->
			<div class="sr-only" aria-live="polite">
				{{ statusText }}
			</div>

			<v-carousel
				v-model="currentSlide"
				:show-arrows="showArrows"
				:height="height"
				:hide-delimiters="hideDelimiters"
				:continuous="continuous"
				ref="carousel"
				@update:model-value="updateStatus"
				class="v-carousel-wrapper"
			>
				<slot></slot>
			</v-carousel>
		</div>
	</div>
</template>

<script>
	export default {
		name: "AccessibilityCarousel",

		props: {
			showArrows: {
				type: [Boolean, String],
				default: "hover",
			},
			height: {
				type: [Number, String],
				default: undefined,
			},
			hideDelimiters: {
				type: Boolean,
				default: false,
			},
			continuous: {
				type: Boolean,
				default: true,
			},
			ariaLabel: {
				type: String,
				default: "",
			},
			showKeyboardControls: {
				type: Boolean,
				default: true,
			},

			items: {
				type: Array,
				default: () => [],
			},
		},

		data() {
			return {
				currentSlide: 0,
				totalSlides: 0,
				statusText: "",
			};
		},

		mounted() {
			this.countSlides();

			this.updateStatus();

			this.$el.addEventListener("focus", this.handleFocus);
		},

		beforeUnmount() {
			this.$el.removeEventListener("focus", this.handleFocus);
		},

		methods: {
			countSlides() {
				if (this.items && this.items.length > 0) {
					this.totalSlides = this.items.length;
				} else if (this.$refs.carousel) {
					const carouselItems =
						this.$refs.carousel.$el.querySelectorAll(".v-carousel-item");
					this.totalSlides = carouselItems.length;
				}
			},

			nextSlide() {
				if (this.currentSlide < this.totalSlides - 1) {
					this.currentSlide++;
				} else if (this.continuous) {
					this.currentSlide = 0;
				}
				this.updateStatus();
			},

			previousSlide() {
				if (this.currentSlide > 0) {
					this.currentSlide--;
				} else if (this.continuous) {
					this.currentSlide = this.totalSlides - 1;
				}
				this.updateStatus();
			},

			goToSlide(index) {
				if (index >= 0 && index < this.totalSlides) {
					this.currentSlide = index;
					this.updateStatus();
				}
			},

			handleKeyDown(event) {
				switch (event.key) {
					case "ArrowRight":
						event.preventDefault();
						this.nextSlide();
						break;
					case "ArrowLeft":
						event.preventDefault();
						this.previousSlide();
						break;
					case "Home":
						event.preventDefault();
						this.goToSlide(0);
						break;
					case "End":
						event.preventDefault();
						this.goToSlide(this.totalSlides - 1);
						break;
				}
			},

			handleFocus() {
				this.$refs.firstSlideBtn?.focus();
			},

			updateStatus() {
				// Create informative status message for screen readers
				const current = this.currentSlide + 1;
				this.statusText = `Slide ${current} of ${this.totalSlides}`;
				if (
					this.items &&
					this.items.length > 0 &&
					this.items[this.currentSlide]
				) {
					const item = this.items[this.currentSlide];
					// Use item name or title if available
					if (item.name) {
						this.statusText += `: ${item.name}`;
					} else if (item.title) {
						this.statusText += `: ${item.title}`;
					}
				}
				this.$emit("slide-change", this.currentSlide);
			},
		},
	};
</script>

<style scoped>
	.accessibility-carousel-container {
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.accessibility-carousel {
		position: relative;
		outline: none;
		width: 100%;
		max-width: 800px;
	}

	.accessibility-carousel:focus-visible {
		outline: 2px solid #1976d2;
		border-radius: 8px;
	}

	.v-carousel-wrapper {
		width: 100%;
		border-radius: 15px !important;
	}

	/* Override Vuetify's default width if needed */
	:deep(.v-carousel) {
		width: 100% !important;
	}

	/* Ensure carousel item content is centered */
	:deep(.v-carousel-item) {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border-width: 0;
	}

	.keyboard-controls {
		margin-top: 10px;
		text-align: center;
		color: #555;
		font-size: 14px;
		background-color: rgba(255, 255, 255, 0.8);
		padding: 5px 10px;
		border-radius: 4px;
	}
</style>
