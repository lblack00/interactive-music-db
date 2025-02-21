<template>
  <Navbar />

  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-4">
          <h1 class="text-h4 font-weight-bold mb-4">{{ thread.title }}</h1>

          <div class="d-flex align-center mb-4">
            <div>
              <div class="font-weight-bold">{{ thread.author.name }}</div>
              <div class="text-caption text--secondary">{{ thread.date }}</div>
            </div>
          </div>

          <div class="mb-4">
            <p>{{ thread.content }}</p>
          </div>

          <v-divider class="my-4"></v-divider>
          <h2 class="text-h5 font-weight-bold mb-4">Replies</h2>
          <v-list dense>
            <v-list-item v-for="reply in thread.replies" :key="reply.id">
              <v-list-item-content>
                <v-list-item-title class="font-weight-bold">{{ reply.author.name }}</v-list-item-title>
                <v-list-item-subtitle class="text-caption text--secondary">{{ reply.date }}</v-list-item-subtitle>
                <v-list-item-text>{{ reply.content }}</v-list-item-text>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-divider class="my-4"></v-divider>
          <h2 class="text-h5 font-weight-bold mb-4">Add a Reply</h2>
          <v-form @submit.prevent="addReply">
            <v-textarea
              v-model="newReplyContent"
              label="Your Reply"
              outlined
              rows="4"
              required
            ></v-textarea>
            <v-btn type="submit" color="primary" class="mt-3">Post Reply</v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Navbar from './Navbar.vue';

export default {
  name: 'ForumThread',
  components: {
    Navbar
  },
  data() {
    return {
      thread: {
        title: 'Welcome to the Forum!',
        author: {
          name: 'Admin'
        },
        date: 'February 19, 2025',
        content: 'We are excited to welcome you to our new music forum. Feel free to discuss your favorite albums, songs, and artists here!',
        replies: [
          {
            id: 1,
            author: {
              name: 'User1'
            },
            date: 'February 19, 2025',
            content: 'Thank you for setting this up! Looking forward to great discussions.'
          },
          {
            id: 2,
            author: {
              name: 'User2'
            },
            date: 'February 19, 2025',
            content: 'Excited to be here! Let\'s talk about music!'
          }
        ]
      },
      newReplyContent: ''
    };
  },
  methods: {
    addReply() {
      if (this.newReplyContent.trim()) {
        const newReply = {
          id: this.thread.replies.length + 1,
          author: {
            name: 'CurrentUser'
          },
          date: new Date().toLocaleDateString(),
          content: this.newReplyContent
        };
        this.thread.replies.push(newReply);
        this.newReplyContent = '';
      }
    }
  }
};
</script>
