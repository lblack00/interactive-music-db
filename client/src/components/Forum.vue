<!--ARIA Landmarks added by Chantelle Cabanilla-->
<!-- This file was written by Lucas Black -->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<main role="main">
				<v-container>
					<h1 id="page-title" class="text-h4 font-weight-bold mb-4">
						Forum Overview
					</h1>
					
					<!-- button for creating a thread -->
					<v-btn 
						color="primary" 
						class="mb-4" 
						@click="handleCreateThreadClick"
						aria-label="Create a new thread"
					>
						<v-icon left>mdi-plus</v-icon> Create Thread
					</v-btn>

					<!-- loading indicator and error message -->
					<v-progress-linear v-if="isLoading" indeterminate color="primary"></v-progress-linear>
					<v-alert v-if="error" type="error" dismissible>{{ error }}</v-alert>
					
					<v-row>
						<v-col cols="12" md="4">
							<aside role="complementary" aria-labelledby="categories-heading">
								<v-card class="pa-4">
									<h2 id="categories-heading" class="text-h5 font-weight-bold">
										Categories
									</h2>
									<nav aria-label="Forum categories">
										<v-list dense>
											<v-list-item
												v-for="category in categories"
												:key="category.name"
												@click="filterByCategory(category.name)"
												:class="{ 'active-category': selectedCategory === category.name }"
											>
												<v-list-item-content>
													<v-list-item-title>
														{{ category.name }}
													</v-list-item-title>
												</v-list-item-content>
											</v-list-item>
										</v-list>
									</nav>
								</v-card>
							</aside>
						</v-col>
						<v-col cols="12" md="8">
							<section role="region" aria-labelledby="recent-threads-heading">
								<v-card class="pa-4">
									<div class="d-flex justify-space-between align-center mb-2">
										<h2
											id="recent-threads-heading"
											class="text-h5 font-weight-bold"
										>
											{{ selectedCategory ? selectedCategory + ' Threads' : 'Recent Threads' }}
										</h2>
										<v-btn 
											text 
											color="primary" 
											v-if="selectedCategory"
											@click="clearCategoryFilter"
											aria-label="Clear category filter"
										>
											Show All
										</v-btn>
									</div>
									
									<!-- show no threads are available -->
									<div v-if="!isLoading && filteredThreads.length === 0" class="text-center py-6">
										<v-icon size="64" color="grey lighten-1">mdi-forum-outline</v-icon>
										<h3 class="mt-2">No threads found</h3>
										<p class="grey--text">Be the first to start a discussion!</p>
										<v-btn 
											color="primary" 
											class="mt-2" 
											@click="handleCreateThreadClick"
											aria-label="Create the first thread"
										>
											Create Thread
										</v-btn>
									</div>
									
									<!-- show all threads -->
									<v-list dense v-else-if="!isLoading">
										<v-list-item
											v-for="thread in filteredThreads"
											:key="thread.id"
											:to="thread.link"
										>
											<v-list-item-content>
												<v-list-item-title>
													<router-link
														:to="thread.link"
														:aria-label="`${thread.title} in ${thread.category} with ${thread.replies} replies`"
														>{{ thread.title }}</router-link
													>
												</v-list-item-title>
												<v-list-item-subtitle>
													<span class="font-weight-medium">{{ thread.category }}</span> - 
													{{ thread.replies }} {{ thread.replies === 1 ? 'reply' : 'replies' }} - 
													Created by {{ thread.author }} {{ formatDate(thread.createdAt) }}
												</v-list-item-subtitle>
											</v-list-item-content>
										</v-list-item>
									</v-list>
								</v-card>
							</section>
						</v-col>
					</v-row>
				</v-container>
			</main>
		</div>
		
		<!-- dialog for creating a thread -->
		<v-dialog v-model="showCreateThreadDialog" max-width="600px">
			<v-card>
				<v-card-title>
					<h3 class="text-h5">Create New Thread</h3>
				</v-card-title>
				<v-card-text>
					<v-form ref="form" v-model="validForm" @submit.prevent="createThread">
						<v-select
							v-model="newThread.category"
							:items="categories.map(cat => cat.name)"
							label="Category"
							required
							:rules="[v => !!v || 'Category is required']"
							aria-label="Select thread category"
						></v-select>
						<v-text-field
							v-model="newThread.title"
							label="Thread Title"
							required
							:rules="[v => !!v || 'Title is required', v => v.length <= 100 || 'Title must be less than 100 characters']"
							aria-label="Thread title"
						></v-text-field>
						<v-textarea
							v-model="newThread.content"
							label="Thread Content"
							required
							:rules="[v => !!v || 'Content is required']"
							rows="6"
							aria-label="Thread content"
						></v-textarea>
					</v-form>
					<v-alert v-if="formError" type="error" class="mt-2">
						{{ formError }}
					</v-alert>
				</v-card-text>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn 
						text 
						@click="showCreateThreadDialog = false"
						aria-label="Cancel creating thread"
					>
						Cancel
					</v-btn>
					<v-btn 
						color="primary" 
						:disabled="!validForm || formSubmitting" 
						@click="createThread"
						aria-label="Submit new thread"
					>
						<v-progress-circular
							v-if="formSubmitting"
							indeterminate
							size="20"
							width="2"
							class="mr-2"
						></v-progress-circular>
						Create Thread
					</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>

		<transition name="fade">
			<div
				class="login-prompt-overlay"
				v-if="showLoginPrompt"
				role="dialog"
				aria-labelledby="login-prompt-title"
				aria-modal="true"
			>
				<div class="login-prompt-modal">
					<h3 id="login-prompt-title">Please Log In</h3>
					<p>You need to be logged in to create a thread.</p>
					<div class="buttons" role="group" aria-label="Login options">
						<button
							class="cancel-btn"
							@click="showLoginPrompt = false"
							aria-label="Cancel and return to page"
						>
							Cancel
						</button>
						<button
							class="login-btn"
							@click="goToLogin"
							aria-label="Go to login page"
						>
							Log In
						</button>
						<button
							class="signup-btn"
							@click="goToSignup"
							aria-label="Go to signup page"
						>
							Sign Up
						</button>
					</div>
				</div>
			</div>
		</transition>
	</div>
</template>

<script>
import Navbar from "./Navbar.vue";
import axios from "axios";

export default {
	name: "Forum",
	components: {
		Navbar,
	},
	data() {
		return {
			categories: [
				{
					name: 'General',
					link: `/forum/category/general`
				},
				{
					name: 'Artist',
					link: `/forum/category/artist`
				},
				{
					name: 'Album',
					link: `/forum/category/album`
				},
				{
					name: 'Song',
					link: `/forum/category/song`
				},
				{
					name: 'Help',
					link: `/forum/category/help`
				}
			],
			recentThreads: [],
			showCreateThreadDialog: false,
			newThread: {
				title: '',
				category: '',
				content: ''
			},
			validForm: false,
			selectedCategory: null,
			isLoading: false,
			error: null,
			formError: null,
			formSubmitting: false,
			apiBaseUrl: "http://localhost:5001",
			currentUser: null,
			isLoggedIn: false,
			showLoginPrompt: false,
		};
	},
	computed: {
		filteredThreads() {
			if (!this.selectedCategory) {
				return this.recentThreads;
			}
			return this.recentThreads.filter(thread => thread.category === this.selectedCategory);
		}
	},
	mounted() {
		this.checkUserSession();
		this.fetchThreads();
		// this.fetchCategories();
	},
	methods: {
		handleCreateThreadClick() {
			if (!this.currentUser) {
				this.showLoginPrompt = true;
			} else {
				this.showCreateThreadDialog = true;
			}
		},
		
		async checkUserSession() {
			this.isLoading = true;
			
			try {
				const response = await axios.get(`${this.apiBaseUrl}/check-session`, { 
					withCredentials: true,
					timeout: 5000
				});
				
				if (response.data.logged_in) {
					this.currentUser = response.data.user;
					this.isLoggedIn = true;
				} else {
					this.currentUser = null;
					this.isLoggedIn = false;
				}
			} catch (error) {
				console.error('Error checking session:', error);
				if (error.code === 'ECONNABORTED') {
					this.error = 'Connection timeout. Server may be unavailable.';
				}

				this.currentUser = null;
				this.isLoggedIn = false;
			} finally {
				this.isLoading = false;
			}
		},
		
		async fetchThreads() {
			this.isLoading = true;
			this.error = null;
			
			try {
				const response = await axios.get(`${this.apiBaseUrl}/forum/threads`, {
					withCredentials: true,
					timeout: 8000
				});

				this.recentThreads = response.data.map(thread => ({
					id: thread.id,
					title: thread.title,
					category: thread.category,
					replies: thread.replies,
					link: `/forum/thread/${thread.id}`,
					author: thread.author.name,
					userId: thread.author.id,
					createdAt: new Date(thread.date)
				}));
				
			} catch (error) {
				console.error('Error fetching threads:', error);
				
				if (error.code === 'ECONNABORTED') {
					this.error = 'Connection timeout. Server may be unavailable.';
				} else if (error.response) {
					this.error = `Error ${error.response.status}: ${error.response.data.message || 'Failed to load thread data'}`;
				} else if (error.request) {
					this.error = 'No response from server. Please check your connection.';
				} else {
					this.error = 'Failed to load thread data. Please try again later.';
				}
			} finally {
				this.isLoading = false;
			}
		},
		
		async fetchCategories() {
			try {
				const response = await axios.get(`${this.apiBaseUrl}/forum/categories`, {
					withCredentials: true,
					timeout: 5000
				});

				this.categories = response.data.map(category => ({
					name: category,
					link: `/forum/category/${category.toLowerCase()}`
				}));
				
			} catch (error) {
				console.error('Error fetching categories:', error);
				this.categories = [
					{ name: 'General', link: '/forum/category/general' },
					{ name: 'Help', link: '/forum/category/help' }
				];
			}
		},
		
		async fetchThreadsByCategory(category) {
			this.isLoading = true;
			this.error = null;
			
			try {
				const response = await axios.get(`${this.apiBaseUrl}/forum/threads`, {
					params: { category },
					withCredentials: true,
					timeout: 8000
				});
				
				this.recentThreads = response.data.map(thread => ({
					id: thread.id,
					title: thread.title,
					category: thread.category,
					replies: thread.replies,
					link: `/forum/thread/${thread.id}`,
					author: thread.author.name,
					userId: thread.author.id,
					createdAt: new Date(thread.date)
				}));
				
			} catch (error) {
				console.error('Error fetching threads by category:', error);
				
				if (error.code === 'ECONNABORTED') {
					this.error = 'Connection timeout. Server may be unavailable.';
				} else if (error.response) {
					this.error = `Error ${error.response.status}: ${error.response.data.message || 'Failed to load category data'}`;
				} else if (error.request) {
					this.error = 'No response from server. Please check your connection.';
				} else {
					this.error = 'Failed to load thread data. Please try again later.';
				}
			} finally {
				this.isLoading = false;
			}
		},
		
		async createThread() {
			if (!this.$refs.form.validate()) return;
			
			if (!this.currentUser) {
				this.showCreateThreadDialog = false;
				this.showLoginPrompt = true;
				return;
			}

			this.formSubmitting = true;
			this.formError = null;
			
			try {
				const response = await axios.post(`${this.apiBaseUrl}/forum/thread`, {
					title: this.newThread.title,
					category: this.newThread.category,
					content: this.newThread.content
				}, {
					withCredentials: true,
				});
				
				if (response.data) {
					const newThreadObj = {
						id: response.data.id,
						title: response.data.title,
						category: response.data.category,
						replies: 0,
						link: `/forum/thread/${response.data.id}`,
						author: response.data.author.name,
						userId: response.data.author.id,
						createdAt: new Date(response.data.date)
					};

					this.recentThreads.unshift(newThreadObj);
					
					this.$refs.form.reset();
					this.showCreateThreadDialog = false;
					
					// success message (could use a toast notification here)
					this.$emit('thread-created', newThreadObj);
					this.$router.push(newThreadObj.link);
				}
			} catch (error) {
				console.error('Error creating thread:', error);
				
				if (error.code === 'ECONNABORTED') {
					this.formError = 'Connection timeout. Server may be unavailable.';
				} else if (error.response) {
					this.formError = error.response.data.error || `Error ${error.response.status}: Failed to create thread`;
				} else if (error.request) {
					this.formError = 'No response from server. Please check your connection.';
				} else {
					this.formError = 'Failed to create thread. Please try again later.';
				}
			} finally {
				this.formSubmitting = false;
			}
		},
		
		filterByCategory(category) {
			this.selectedCategory = category;
			this.fetchThreadsByCategory(category);
		},
		
		clearCategoryFilter() {
			this.selectedCategory = null;
			this.fetchThreads();
		},
		
		formatDate(date) {
			if (!date) return '';
			
			const now = new Date();
			const diffTime = Math.abs(now - date);
			const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
			
			if (diffDays === 0) {
				return 'today';
			} else if (diffDays === 1) {
				return 'yesterday';
			} else if (diffDays < 7) {
				return `${diffDays} days ago`;
			} else {
				return date.toLocaleDateString();
			}
		},

		goToLogin() {
			this.showLoginPrompt = false;
			const returnTo = window.location.pathname + window.location.search;
			window.location.href = `/login?returnTo=${encodeURIComponent(
				returnTo
			)}`;
		},

		goToSignup() {
			this.showLoginPrompt = false;
			const returnTo = window.location.pathname + window.location.search;
			window.location.href = `/signup?returnTo=${encodeURIComponent(
				returnTo
			)}`;
		},
	}
};
</script>

<style scoped>
@import "../../src/assets/background.css";

.active-category {
	background-color: rgba(0, 0, 0, 0.05);
}

.v-list-item:hover {
	background-color: rgba(0, 0, 0, 0.03);
}

.grid-container {
	overflow: visible !important;
}

.content {
	padding-top: 60px;
}

.login-prompt-overlay {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
	background: rgba(0, 0, 0, 0.7);
	display: flex;
	align-items: center;
	justify-content: center;
	z-index: 9999;
	backdrop-filter: blur(3px);
}

.login-prompt-modal {
	background: white;
	padding: 2.5rem;
	border-radius: 12px;
	box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
	min-width: 320px;
}

.login-prompt-modal h3 {
	margin: 0 0 1rem 0;
	color: #1a1a1a;
	font-size: 1.5rem;
	font-weight: 600;
}

.login-prompt-modal p {
	margin: 0 0 1.5rem 0;
	color: #4a4a4a;
	font-size: 1rem;
	line-height: 1.5;
}

.buttons {
	display: flex;
	gap: 0.75rem;
	justify-content: center;
}

.buttons button {
	padding: 0.75rem 1.5rem;
	border: none;
	border-radius: 8px;
	cursor: pointer;
	font-weight: 500;
	font-size: 0.95rem;
	transition: all 0.2s ease;
}

.cancel-btn {
	background: #f0f0f0;
	color: #666;
}

.cancel-btn:hover {
	background: #e4e4e4;
}

.login-btn {
	background: #007bff;
	color: white;
}

.login-btn:hover {
	background: #0056b3;
	transform: translateY(-1px);
	box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
}

.signup-btn {
	background: #28a745;
	color: white;
}

.signup-btn:hover {
	background: #218838;
	transform: translateY(-1px);
	box-shadow: 0 4px 12px rgba(40, 167, 69, 0.2);
}

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.3s;
}

.fade-enter,
.fade-leave-to {
	opacity: 0;
}
</style>