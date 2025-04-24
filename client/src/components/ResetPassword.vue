<!-- This file was written by Jax Hendrickson -->
<template>
    <div class="grid-container">
        <header role="navigation">
            <Navbar />
        </header>
        <div class="content">
            <main role="main">
                <v-row no-gutters class="justify-center">
                    <v-col cols="4">
                        <v-alert v-if="error" type="error" class="mt-10">
                            {{ error }}
                        </v-alert>
                        <v-alert v-if="success" type="success" class="mt-10">
                            {{ success }}
                        </v-alert>
                    </v-col>
                </v-row>

                <div class="container mt-5">
                    <h2 id="reset-password-heading">Set New Password</h2>
                    <section role="region" aria-labelledby="reset-password-heading">
                        <form @submit.prevent="resetPassword" aria-label="Password reset form">
                            <div class="row" role="form">
                                <label for="password">New Password</label>
                                <input
                                    type="password"
                                    id="password"
                                    v-model="password"
                                    required
                                    aria-required="true"
                                />
                            </div>
                            <div class="row" role="form">
                                <label for="confirmPassword">Confirm Password</label>
                                <input
                                    type="password"
                                    id="confirmPassword"
                                    v-model="confirmPassword"
                                    required
                                    aria-required="true"
                                />
                            </div>
                            <button type="submit">Reset Password</button>
                        </form>
                    </section>
                </div>
            </main>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
    name: 'ResetPassword',
    components: {
        Navbar
    },
    data() {
        return {
            password: '',
            confirmPassword: '',
            error: null,
            success: null
        };
    },
    methods: {
        async resetPassword() {
            this.error = null;
            this.success = null;

            if (this.password !== this.confirmPassword) {
                this.error = 'Passwords do not match';
                return;
            }

            try {
                const token = this.$route.query.token;
                const response = await axios.post('http://localhost:5001/reset-password', {
                    token: token,
                    password: this.password
                });

                this.success = 'Password reset successful. You can now login with your new password.';
                setTimeout(() => {
                    this.$router.push('/login');
                }, 3000);
            } catch (error) {
                this.error = error.response?.data?.error || 'An error occurred. Please try again.';
            }
        }
    }
};
</script>

<style scoped>
@import "../../src/assets/background.css";
@import "../../src/assets/login.css";
</style>