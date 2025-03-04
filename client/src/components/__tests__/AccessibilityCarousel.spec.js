//This file was written by Chantelle Cabanilla
import { mount } from "@vue/test-utils";
import AccessibilityCarousel from "@/components/AccessibilityCarousel.vue";
import { describe, it, expect, beforeEach } from "vitest";

describe("AccessibilityCarousel Keyboard Navigation", () => {
	let wrapper;

	beforeEach(() => {
		wrapper = mount(AccessibilityCarousel, {
			global: {
				stubs: {
					"v-carousel": true,
					"v-carousel-item": true,
				},
			},
		});

		// Set up proper mocks and data for testing
		wrapper.vm.totalSlides = 3;
		wrapper.vm.currentSlide = 0;
	});

	it("navigates to next slide with right arrow key", () => {
		// Directly test the keyboard handler
		wrapper.vm.handleKeyDown({
			key: "ArrowRight",
			preventDefault: () => {},
		});

		expect(wrapper.vm.currentSlide).toBe(1);
	});

	it("navigates to previous slide with left arrow key", () => {
		wrapper.vm.currentSlide = 1;

		// Test previous slide functionality
		wrapper.vm.handleKeyDown({
			key: "ArrowLeft",
			preventDefault: () => {},
		});

		expect(wrapper.vm.currentSlide).toBe(0);
	});
});
