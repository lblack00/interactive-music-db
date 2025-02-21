<template>
  <Navbar />

  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-4">
          <h1 class="text-h4 font-weight-bold mb-4">Admin Dashboard</h1>

          <h2 class="text-h5 font-weight-bold mb-4">Pending User Edits</h2>
          <v-list dense>
            <v-list-item v-for="change in pendingChanges" :key="change.id">
              <v-list-item-content>
                <v-list-item-title class="font-weight-bold">{{ change.postTitle }}</v-list-item-title>
                <v-list-item-subtitle class="text-caption text--secondary">
                  Edited by: {{ change.author.name }} on {{ change.date }}
                </v-list-item-subtitle>
                <v-list-item-text>
                  <strong>Suggested Edit:</strong> {{ change.suggestedEdit }}
                </v-list-item-text>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn color="success" @click="approveChange(change.id)">Approve</v-btn>
                <v-btn color="error" class="ml-2" @click="rejectChange(change.id)">Reject</v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>

          <v-divider class="my-4"></v-divider>

          <h2 class="text-h5 font-weight-bold mb-4">Manage User Posts</h2>
          <v-list dense>
            <v-list-item v-for="post in userPosts" :key="post.id">
              <v-list-item-content>
                <v-list-item-title class="font-weight-bold">{{ post.title }}</v-list-item-title>
                <v-list-item-subtitle class="text-caption text--secondary">
                  Posted by: {{ post.author.name }} on {{ post.date }}
                </v-list-item-subtitle>
                <v-list-item-text>{{ post.content }}</v-list-item-text>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn color="error" @click="deletePost(post.id)">Delete</v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Navbar from './Navbar.vue';

export default {
  name: 'AdminDashboard',
  components: {
    Navbar
  },
  data() {
    return {
      pendingChanges: [
        {
          id: 1,
          postTitle: 'Kill Em\' All',
          author: { name: 'User3' },
          date: 'February 20, 2025',
          suggestedEdit: 'Updated the notes on Kill Em\' All by Metallica.'
        }
      ],
      userPosts: [
        {
          id: 1,
          title: 'Favorite Music Genres',
          author: { name: 'User1' },
          date: 'February 18, 2025',
          content: 'Did you guys see what Ye posted on X?'
        }
      ]
    };
  },
  methods: {
    approveChange(changeId) {
      this.pendingChanges = this.pendingChanges.filter(change => change.id !== changeId);
    },
    rejectChange(changeId) {
      this.pendingChanges = this.pendingChanges.filter(change => change.id !== changeId);
    },
    deletePost(postId) {
      this.userPosts = this.userPosts.filter(post => post.id !== postId);
    }
  }
};
</script>
