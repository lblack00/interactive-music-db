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
                    <h2 id="forgot-password-heading">Reset Password</h2>
                    <section role="region" aria-labelledby="forgot-password-heading">
                        <form @submit.prevent="requestReset" aria-label="Password reset form">
                            <div class="row" role="form">
                                <label for="email">Email</label>
                                <input
                                    type="email"
                                    id="email"
                                    v-model="email"
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
    name: 'ForgotPassword',
    components: {
        Navbar
    },
    data() {
        return {
            email: '',
            error: null,
            success: null
        };
    },
    methods: {
        async requestReset() {
            this.error = null;
            this.success = null;
            
            try {
                const response = await axios.post('http://localhost:5001/request-password-reset', {
                    email: this.email
                });
                
                this.success = 'If an account exists with this email, you will receive password reset instructions.';
            } catch (error) {
                this.error = 'An error occurred. Please try again later.';
                console.error('Password reset error:', error);
            }
        }
    }
};
</script>

<style scoped>
@import "../../src/assets/background.css";
@import "../../src/assets/login.css";
</style>
