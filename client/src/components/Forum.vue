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
					<!-- Gradient Header -->
					<div class="forum-gradient-header">
						<div class="forum-header-content">
							<div class="d-flex align-center">
								<div>
									<h1 id="page-title" class="forum-title">Forum Overview</h1>
									<p class="forum-subtitle">
										Discuss music, albums, artists, and more!
									</p>
								</div>
							</div>
							<v-btn
								color="primary"
								class="forum-create-btn forum-header-btn"
								variant="elevated"
								@click="handleCreateThreadClick"
								aria-label="Create a new thread"
							>
								<v-icon left>mdi-plus</v-icon> Create Thread
							</v-btn>
						</div>
					</div>

					<!-- loading indicator and error message -->
					<v-progress-linear
						v-if="isLoading"
						indeterminate
						color="primary"
					></v-progress-linear>
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
												:class="{
													'active-category': selectedCategory === category.name,
												}"
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
											{{
												selectedCategory
													? selectedCategory + " Threads"
													: "Recent Threads"
											}}
										</h2>
										<v-btn
											variant="outlined"
											color="primary"
											v-if="selectedCategory"
											@click="clearCategoryFilter"
											aria-label="Clear category filter"
											class="show-all-btn"
										>
											Show All
										</v-btn>
									</div>

									<!-- show no threads are available -->
									<div
										v-if="!isLoading && filteredThreads.length === 0"
										class="text-center py-6"
									>
										<v-icon size="64" color="grey lighten-1"
											>mdi-forum-outline</v-icon
										>
										<h3 class="mt-2">No threads found</h3>
										<p class="grey--text">
											Be the first to start a discussion!
										</p>
										<v-btn
											color="primary"
											class="mt-2 forum-create-btn"
											variant="elevated"
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
													<span class="font-weight-medium">{{
														thread.category
													}}</span>
													- {{ thread.replies }}
													{{ thread.replies === 1 ? "reply" : "replies" }} -
													Created by {{ thread.author }}
													{{ formatDate(thread.createdAt) }}
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
							:items="categories.map((cat) => cat.name)"
							label="Category"
							required
							:rules="[(v) => !!v || 'Category is required']"
							aria-label="Select thread category"
						></v-select>
						<v-text-field
							v-model="newThread.title"
							label="Thread Title"
							required
							:rules="[
								(v) => !!v || 'Title is required',
								(v) =>
									v.length <= 100 || 'Title must be less than 100 characters',
							]"
							aria-label="Thread title"
						></v-text-field>
						<v-textarea
							v-model="newThread.content"
							label="Thread Content"
							required
							:rules="[(v) => !!v || 'Content is required']"
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
						name: "General",
						link: `/forum/category/general`,
					},
					{
						name: "Artist",
						link: `/forum/category/artist`,
					},
					{
						name: "Album",
						link: `/forum/category/album`,
					},
					{
						name: "Song",
						link: `/forum/category/song`,
					},
					{
						name: "Help",
						link: `/forum/category/help`,
					},
				],
				recentThreads: [],
				showCreateThreadDialog: false,
				newThread: {
					title: "",
					category: "",
					content: "",
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
				return this.recentThreads.filter(
					(thread) => thread.category === this.selectedCategory
				);
			},
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
						timeout: 5000,
					});

					if (response.data.logged_in) {
						this.currentUser = response.data.user;
						this.isLoggedIn = true;
					} else {
						this.currentUser = null;
						this.isLoggedIn = false;
					}
				} catch (error) {
					console.error("Error checking session:", error);
					if (error.code === "ECONNABORTED") {
						this.error = "Connection timeout. Server may be unavailable.";
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
						timeout: 8000,
					});

					this.recentThreads = response.data.map((thread) => ({
						id: thread.id,
						title: thread.title,
						category: thread.category,
						replies: thread.replies,
						link: `/forum/thread/${thread.id}`,
						author: thread.author.name,
						userId: thread.author.id,
						createdAt: new Date(thread.date),
					}));
				} catch (error) {
					console.error("Error fetching threads:", error);

					if (error.code === "ECONNABORTED") {
						this.error = "Connection timeout. Server may be unavailable.";
					} else if (error.response) {
						this.error = `Error ${error.response.status}: ${
							error.response.data.message || "Failed to load thread data"
						}`;
					} else if (error.request) {
						this.error =
							"No response from server. Please check your connection.";
					} else {
						this.error = "Failed to load thread data. Please try again later.";
					}
				} finally {
					this.isLoading = false;
				}
			},

			async fetchCategories() {
				try {
					const response = await axios.get(
						`${this.apiBaseUrl}/forum/categories`,
						{
							withCredentials: true,
							timeout: 5000,
						}
					);

					this.categories = response.data.map((category) => ({
						name: category,
						link: `/forum/category/${category.toLowerCase()}`,
					}));
				} catch (error) {
					console.error("Error fetching categories:", error);
					this.categories = [
						{ name: "General", link: "/forum/category/general" },
						{ name: "Help", link: "/forum/category/help" },
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
						timeout: 8000,
					});

					this.recentThreads = response.data.map((thread) => ({
						id: thread.id,
						title: thread.title,
						category: thread.category,
						replies: thread.replies,
						link: `/forum/thread/${thread.id}`,
						author: thread.author.name,
						userId: thread.author.id,
						createdAt: new Date(thread.date),
					}));
				} catch (error) {
					console.error("Error fetching threads by category:", error);

					if (error.code === "ECONNABORTED") {
						this.error = "Connection timeout. Server may be unavailable.";
					} else if (error.response) {
						this.error = `Error ${error.response.status}: ${
							error.response.data.message || "Failed to load category data"
						}`;
					} else if (error.request) {
						this.error =
							"No response from server. Please check your connection.";
					} else {
						this.error = "Failed to load thread data. Please try again later.";
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
					const response = await axios.post(
						`${this.apiBaseUrl}/forum/thread`,
						{
							title: this.newThread.title,
							category: this.newThread.category,
							content: this.newThread.content,
						},
						{
							withCredentials: true,
						}
					);

					if (response.data) {
						const newThreadObj = {
							id: response.data.id,
							title: response.data.title,
							category: response.data.category,
							replies: 0,
							link: `/forum/thread/${response.data.id}`,
							author: response.data.author.name,
							userId: response.data.author.id,
							createdAt: new Date(response.data.date),
						};

						this.recentThreads.unshift(newThreadObj);

						this.$refs.form.reset();
						this.showCreateThreadDialog = false;

						// success message (could use a toast notification here)
						this.$emit("thread-created", newThreadObj);
						this.$router.push(newThreadObj.link);
					}
				} catch (error) {
					console.error("Error creating thread:", error);

					if (error.code === "ECONNABORTED") {
						this.formError = "Connection timeout. Server may be unavailable.";
					} else if (error.response) {
						this.formError =
							error.response.data.error ||
							`Error ${error.response.status}: Failed to create thread`;
					} else if (error.request) {
						this.formError =
							"No response from server. Please check your connection.";
					} else {
						this.formError = "Failed to create thread. Please try again later.";
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
				if (!date) return "";

				const now = new Date();
				const diffTime = Math.abs(now - date);
				const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

				if (diffDays === 0) {
					return "today";
				} else if (diffDays === 1) {
					return "yesterday";
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
		},
	};
</script>

<style scoped>
	@import "../assets/background.css";
	@import "../assets/accessibility.css";

	.grid-container {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	.v-container {
		padding-top: 40px;
		padding-bottom: 40px;
		max-width: 1100px;
	}

	.v-card {
		border-radius: 20px;
		box-shadow: 0 6px 32px rgba(20, 160, 133, 0.07),
			0 1.5px 6px rgba(20, 160, 133, 0.04);
		background: #fff;
		border: 1px solid #d0ece7;
		margin-bottom: 24px;
	}

	h1#page-title {
		font-size: 2.5rem;
		font-weight: 900;
		color: var(--primary-color);
		margin-bottom: 36px;
		letter-spacing: 1px;
		text-align: left;
		font-family: "Inter", "Segoe UI", Arial, sans-serif;
	}

	h2,
	.text-h5 {
		font-weight: 800;
		color: var(--primary-color);
		border-left: 4px solid var(--primary-color);
		padding-left: 14px;
		margin-bottom: 20px;
		background: none;
		font-size: 1.25rem;
		font-family: "Inter", "Segoe UI", Arial, sans-serif;
	}

	.v-btn {
		border-radius: 24px !important;
		font-weight: 700;
		letter-spacing: 1px;
		transition: background 0.2s, box-shadow 0.2s, transform 0.15s;
		box-shadow: none;
		font-family: "Inter", "Segoe UI", Arial, sans-serif;
	}
	.v-btn:not(.v-btn--text):hover {
		filter: brightness(1.08);
		box-shadow: 0 2px 8px rgba(20, 160, 133, 0.13);
		transform: translateY(-2px) scale(1.04);
	}

	.forum-create-btn {
		background: linear-gradient(
			90deg,
			var(--primary-color) 0%,
			#1de9b6 100%
		) !important;
		color: #fff !important;
		font-weight: 800;
		box-shadow: 0 2px 12px rgba(20, 160, 133, 0.13);
	}
	.forum-create-btn:hover {
		background: linear-gradient(
			90deg,
			#1de9b6 0%,
			var(--primary-color) 100%
		) !important;
	}

	.show-all-btn {
		border: 2px solid var(--primary-color) !important;
		color: var(--primary-color) !important;
		font-weight: 700;
		background: #eafaf7 !important;
	}
	.show-all-btn:hover {
		background: #d0ece7 !important;
	}

	/* Sidebar */
	.v-card aside,
	.v-card[role="complementary"] {
		background: #f8fafc;
		border: 1px solid #d0ece7;
		box-shadow: none;
	}

	.active-category {
		background: var(--primary-color) !important;
		color: #fff !important;
		font-weight: 800;
		border-radius: 999px !important;
		margin: 4px 0;
		padding: 8px 22px !important;
		transition: background 0.2s, color 0.2s;
		font-size: 1.08rem;
		box-shadow: 0 2px 8px rgba(20, 160, 133, 0.09);
	}

	.v-list-item {
		border-radius: 16px;
		margin-bottom: 14px;
		transition: box-shadow 0.18s, background 0.18s, transform 0.15s;
		background: transparent;
		box-shadow: 0 1px 4px rgba(20, 160, 133, 0.03);
		padding: 0 18px;
		min-height: 72px;
		display: flex;
		align-items: center;
		position: relative;
	}
	.v-list-item:hover {
		background: #eafaf7;
		box-shadow: 0 2px 8px rgba(20, 160, 133, 0.08);
		cursor: pointer;
	}

	.v-list-item .router-link {
		color: var(--primary-color);
		text-decoration: none;
		font-weight: 900;
		font-size: 1.18rem;
		letter-spacing: 0.2px;
		transition: color 0.15s, text-decoration 0.15s;
	}
	.v-list-item .router-link:hover {
		text-decoration: underline;
		color: #1de9b6;
	}

	.v-list-item-title {
		margin-bottom: 2px;
		font-size: 1.18rem;
		font-weight: 900;
	}

	.v-list-item-subtitle {
		color: #7fd8c2;
		font-size: 0.97rem;
		font-weight: 500;
		margin-top: 2px;
	}

	.v-list-item + .v-list-item {
		border-top: 1px solid #eafaf7;
	}

	.v-progress-linear {
		border-radius: 8px;
	}

	.v-dialog .v-card {
		border-radius: 22px;
		padding: 18px 0 0 0;
		background: #fff;
		border: 1px solid #d0ece7;
		box-shadow: 0 6px 32px rgba(20, 160, 133, 0.12);
	}
	.v-dialog .v-card-title {
		font-size: 1.35rem;
		font-weight: 800;
		color: var(--primary-color);
		padding-left: 28px;
	}
	.v-dialog .v-card-text {
		padding: 28px 36px 0 36px;
	}
	.v-dialog .v-card-actions {
		padding: 18px 36px 28px 36px;
	}

	.login-prompt-modal {
		border-radius: 20px;
		box-shadow: 0 6px 32px rgba(20, 160, 133, 0.13);
		background: #fff;
		padding: 36px 44px;
		text-align: center;
	}
	.login-prompt-modal h3 {
		color: var(--primary-color);
		font-weight: 800;
		margin-bottom: 14px;
	}
	.login-prompt-modal .buttons button {
		border-radius: 20px;
		font-weight: 700;
		margin: 0 10px;
		padding: 10px 24px;
		background: var(--primary-color);
		color: #fff;
		border: none;
		transition: background 0.2s;
	}
	.login-prompt-modal .buttons button:hover {
		background: #1de9b6;
	}

	/* No threads state */
	.text-center .v-icon {
		color: var(--primary-color) !important;
	}
	.text-center h3 {
		color: var(--primary-color);
		font-weight: 800;
	}
	.text-center p {
		color: #7fd8c2;
	}

	@media (max-width: 900px) {
		.v-dialog .v-card-text,
		.v-dialog .v-card-actions {
			padding-left: 10px;
			padding-right: 10px;
		}
		.v-container {
			padding-top: 16px;
			padding-bottom: 16px;
		}
	}

	.forum-gradient-header {
		width: 100%;
		background: linear-gradient(90deg, #14a085 0%, #1de9b6 100%);
		border-radius: 32px;
		margin: 32px auto 32px auto;
		max-width: 1200px;
		box-shadow: 0 4px 32px rgba(20, 160, 133, 0.13);
		padding: 36px 48px 32px 48px;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.forum-header-content {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}
	.forum-title {
		color: #fff !important;
		font-size: 2.6rem;
		font-weight: 900;
		margin-bottom: 8px;
		font-family: "Inter", "Segoe UI", Arial, sans-serif;
		text-shadow: 0 2px 8px rgba(0, 0, 0, 0.18), 0 1px 0 #14a085;
	}
	.forum-subtitle {
		color: #eafaf7;
		font-size: 1.15rem;
		font-weight: 500;
		margin-bottom: 0;
		font-family: "Inter", "Segoe UI", Arial, sans-serif;
	}
	.forum-header-btn {
		font-size: 1.1rem;
		padding: 12px 32px;
		border-radius: 24px;
		font-weight: 800;
		box-shadow: 0 2px 12px rgba(20, 160, 133, 0.13);
		background: #fff !important;
		color: var(--primary-color) !important;
	}
	.forum-header-btn:hover {
		background: #eafaf7 !important;
	}
</style>
