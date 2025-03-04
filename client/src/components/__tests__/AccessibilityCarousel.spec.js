import { mount } from "@vue/test-utils";
import AccessibilityCarousel from "@/components/AccessibilityCarousel.vue";
import { describe, it, expect, beforeEach } from "vitest";

describe("AccessibilityCarousel Keyboard Navigation", () => {
	let wrapper;

	beforeEach(() => {
		// Create a simplified wrapper with just what we need
		wrapper = mount(AccessibilityCarousel, {
			props: {
				items: [{ name: "Slide 1" }, { name: "Slide 2" }, { name: "Slide 3" }],
			},
			global: {
				stubs: {
					"v-carousel": true,
					"v-carousel-item": true,
				},
			},
		});

		// Mock the carousel's structure
		wrapper.vm.$refs.carousel = {
			$el: {
				querySelectorAll: () => [1, 2, 3], // Mock 3 carousel items
			},
		};

		// Count slides to set totalSlides
		wrapper.vm.countSlides();
	});

	it("navigates to next slide with right arrow key", () => {
		// Start at first slide
		wrapper.vm.currentSlide = 0;

		// Simulate pressing right arrow key
		wrapper.vm.handleKeyDown({
			key: "ArrowRight",
			preventDefault: () => {},
		});

		// Check if now on slide 2
		expect(wrapper.vm.currentSlide).toBe(1);
		expect(wrapper.vm.statusText).toContain("Slide 2 of 3");

		return {
			success: true,
			currentSlide: wrapper.vm.currentSlide,
			message: `Successfully navigated to slide ${wrapper.vm.currentSlide + 1}`,
		};
	});

	it("navigates to previous slide with left arrow key", () => {
		// Start at second slide
		wrapper.vm.currentSlide = 1;

		// Simulate pressing left arrow key
		wrapper.vm.handleKeyDown({
			key: "ArrowLeft",
			preventDefault: () => {},
		});

		// Check if now on slide 1
		expect(wrapper.vm.currentSlide).toBe(0);
		expect(wrapper.vm.statusText).toContain("Slide 1 of 3");

		return {
			success: true,
			currentSlide: wrapper.vm.currentSlide,
			message: `Successfully navigated to slide ${wrapper.vm.currentSlide + 1}`,
		};
	});
});
