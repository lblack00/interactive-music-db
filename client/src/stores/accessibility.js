import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useAccessibilityStore = defineStore("accessibility", () => {
	const colorblindMode = ref(
		localStorage.getItem("colorblindMode") || "Default"
	);
	const enablePatterns = ref(localStorage.getItem("enablePatterns") === "true");
	const showLabels = ref(localStorage.getItem("showLabels") === "true");
	const darkMode = ref(localStorage.getItem("darkMode") === "true");

	const accessibilityClasses = computed(() => {
		const classes = [];

		// Add colorblind class
		switch (colorblindMode.value) {
			case "Red-Blind (Protanopia)":
				classes.push("protanopia");
				break;
			case "Green-Blind (Deuteranopia)":
				classes.push("deuteranopia");
				break;
			case "Blue-Blind (Tritanopia)":
				classes.push("tritanopia");
				break;
			case "Grayscale (achromatopsia)":
				classes.push("achromatopsia");
				break;
			case "High Contrast":
				classes.push("high-contrast");
				break;
		}

		// Add additional classes
		if (enablePatterns.value) classes.push("enable-patterns");
		if (showLabels.value) classes.push("show-labels");
		if (darkMode.value) classes.push("dark-mode");

		return classes;
	});

	function setColorblindMode(mode) {
		colorblindMode.value = mode;
		localStorage.setItem("colorblindMode", mode);
	}

	function setEnablePatterns(value) {
		enablePatterns.value = value;
		localStorage.setItem("enablePatterns", value);
	}

	function setShowLabels(value) {
		showLabels.value = value;
		localStorage.setItem("showLabels", value);
	}

	function setDarkMode(value) {
		darkMode.value = value;
		localStorage.setItem("darkMode", value);
	}

	return {
		colorblindMode,
		enablePatterns,
		showLabels,
		darkMode,
		accessibilityClasses,
		setColorblindMode,
		setEnablePatterns,
		setShowLabels,
		setDarkMode,
	};
});
