<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<header role="navigation">
		
	</header>

	<main role="main">
		<div class="error-container" aria-labelledby="error-heading">
			<h1 id="error-heading">404 - Page Not Found</h1>
			<p>The page you are looking for does not exist.</p>
		</div>
	</main>
</template>

<script>
	import Navbar from "./Navbar.vue";

	export default {
		name: "NotFound",
		components: {
			Navbar,
		},
	};
</script>

<style scoped>
	body {
		font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
		background-color: #ecf0f1;
		color: #333;
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
	}

	.error-container {
		text-align: center;
		padding: 40px;
		background-color: #ffffff;
		width: 100%;
	}

	h1 {
		font-size: 5rem;
		color: #1abc9c;
		font-weight: bold;
		margin-bottom: 20px;
	}

	p {
		font-size: 1.2rem;
		color: #7f8c8d;
		margin-top: 10px;
	}

	@media (max-width: 768px) {
		h1 {
			font-size: 3rem;
		}

		p {
			font-size: 1rem;
		}
	}
</style>
