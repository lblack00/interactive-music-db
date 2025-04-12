<template>
  <div class="grid-container">
    <header role="navigation">
      <Navbar />
    </header>
    <div class="content">
      <main role="main">
        <div class="container mt-5">
          <v-alert v-if="status === 'success'" type="success">
            Email verified successfully! You can now log in.
          </v-alert>
          <v-alert v-if="status === 'error'" type="error">
            {{ error }}
          </v-alert>
          <div v-if="status === 'verifying'" class="text-center">
            Verifying your email...
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';

export default {
  name: 'VerifyEmail',
  components: {
    Navbar,
  },
  data() {
    return {
      status: 'verifying',
      error: null,
    };
  },
  async created() {
    const token = this.$route.query.token;
    if (!token) {
      this.status = 'error';
      this.error = 'Missing verification token';
      return;
    }

    try {
      const response = await axios.get(`http://localhost:5001/verify-email?token=${token}`);
      if (response.status === 200) {
        this.status = 'success';
        // Redirect to login page after 3 seconds
        setTimeout(() => {
          this.$router.push('/login');
        }, 3000);
      }
    } catch (error) {
      this.status = 'error';
      this.error = error.response?.data?.error || 'Verification failed';
    }
  },
};
</script>
