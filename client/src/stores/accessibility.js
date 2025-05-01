import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useAccessibilityStore = defineStore("accessibility", () => {
	const darkMode = ref(localStorage.getItem("darkMode") === "true");
	const highContrast = ref(localStorage.getItem("highContrast") === "true");

	const accessibilityClasses = computed(() => {
		const classes = [];

		if (darkMode.value) classes.push("dark-mode");
		if (highContrast.value) classes.push("high-contrast");

		return classes;
	});

	function setDarkMode(value) {
		darkMode.value = value;
		localStorage.setItem("darkMode", value);
	}

	function setHighContrast(value) {
		highContrast.value = value;
		localStorage.setItem("highContrast", value);
	}

	return {
		darkMode,
		highContrast,
		accessibilityClasses,
		setDarkMode,
		setHighContrast,
	};
});
