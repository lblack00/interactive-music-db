<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<main role="main">
				<div class="error-container" aria-labelledby="error-heading">
					<h1 id="error-heading">403 - Not Authorized</h1>
					<p>You are not authorized to access the page you are requesting.</p>
				</div>
			</main>
		</div>
	</div>
</template>

<script>
	import Navbar from "./Navbar.vue";

	export default {
		name: "NotAuthorized",
		components: {
			Navbar,
		},
	};
</script>

<style scoped>
	@import "../assets/background.css";
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
		background-color: transparent;
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
