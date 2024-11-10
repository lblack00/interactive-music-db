<template>
	<div class='container'>
		<h2>Login</h2>
		<form @submit.prevent='login'>
			<div class='row'>
				<label for='username'>Username:</label>
				<input type='username' id='username' v-model='username' required>
			</div>
			<div class='row'>
				<label for='password'>Password:</label>
				<input type='password' id='password' v-model='password' required>
			</div>
			<button type='submit'>Login</button>
		</form>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	name: 'Login',
	data() {
		return {
			username: '',
			password: '',
		};
	},
	methods: {
		async login() {
			try {
				const path = 'http://localhost:5001/login';
				const response = await axios.post(path, {
					username: this.username,
					password: this.password
				});

				// handle successful login, redirect to different page
			} catch (error) {
				console.error('Error: ', error);
			}
		},
	},
};
</script>