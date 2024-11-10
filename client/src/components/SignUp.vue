<template>
	<div class='container'>
		<h2>Sign Up</h2>
		<form @submit.prevent='signup'>
			<div class='row'>
				<label for='username'>Username:</label>
				<input type='username' id='username' v-model='username' required>
			</div>
			<div class='row'>
				<label for='email'>Email:</label>
				<input type='email' id='email' v-model='email' required>
			</div>
			<div class='row'>
				<label for='password'>Password:</label>
				<input type='password' id='password' v-model='password' required>
			</div>
			<div class='row'>
				<label for='confirmPassword'>Confirm Password:</label>
				<input type='password' id='confirmPassword' v-model='confirmPassword' required>
			</div>
			<button type='submit'>Sign Up</button>
		</form>
	</div>
</template>

<script>
import axios from 'axios';

export default {
	name: 'SignUp',
	data() {
		return {
			username: '',
			email: '',
			password: '',
			confirmPassword: '',
		};
	},
	methods: {
		async signup() {
			if (this.password != this.confirmPassword) {
				alert('Password do not match!');
				return;
			}

			try {
				const path = 'http://localhost:5001/signup';
				const response = await axios.post(path, {
					username: this.username,
					email: this.email,
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