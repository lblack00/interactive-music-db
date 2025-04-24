<!--ARIA Landmarks added by Chantelle Cabanilla-->
<!-- This file was written by Lucas Black -->
<template>
	<div class="grid-container" v-if="thread">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<main role="main">
				<v-container>
					<v-row justify="center">
						<v-col cols="12" md="8">
							<v-card class="pa-4">
								<article role="region" aria-labelledby="thread-title">
									<header>
										<div class="d-flex justify-space-between align-center">
											<h1 id="thread-title" class="text-h4 font-weight-bold mb-4">
												{{ thread.title }}
											</h1>

											<div class="d-flex align-center">
												<!-- report a thread -->
												<v-btn 
													icon
													class="mr-2"
													@click.stop.prevent="reportItem(thread, 'thread')" 
													aria-label="Report this thread"
												>
													<v-icon color="warning">mdi-flag</v-icon>
												</v-btn>

												<!-- edit/delete thread if user posted it -->
												<div v-if="isCurrentUserAuthor(thread.author)">
													<v-btn icon @click="editThread" aria-label="Edit thread" class="mr-2">
														<v-icon>mdi-pencil</v-icon>
													</v-btn>
													<v-btn icon @click="confirmDeleteThread" aria-label="Delete thread" color="error">
														<v-icon>mdi-delete</v-icon>
													</v-btn>
												</div>
											</div>
										</div>

										<!-- display author and date published -->
										<div class="d-flex align-center mb-4">
											<router-link :to="`/user/${thread.author.name}`" class="text-decoration-none">
												<img
													:src="`http://localhost:5001/static/pfp/${thread.author.id}profilepic.png`"
													alt="Profile Image"
													width="40"
													height="40"
													class="mr-3 rounded-md"
												/>
											</router-link>

											<div>
												<router-link
													:to="`/user/${thread.author.name}`"
													class="font-weight-bold text-body"
													style="text-decoration: none;"
												>
													{{ thread.author.name }}
												</router-link>
												<div class="text-caption text--secondary">
													{{ thread.date }}
												</div>
											</div>
										</div>
									</header>
									<div class="mb-4">
										<v-textarea
											v-if="isEditingThread"
											v-model="editedThreadContent"
											outlined
											rows="4"
											hide-details
										></v-textarea>
										<p v-else>{{ thread.content }}</p>
									</div>
									<div v-if="isEditingThread" class="d-flex justify-end">
										<v-btn text @click="cancelEditThread" class="mr-2">Cancel</v-btn>
										<v-btn color="primary" @click="saveThreadEdit">Save Changes</v-btn>
									</div>
								</article>

								<!-- add references to artist/release page section -->
								<section v-if="isCurrentUserAuthor(thread.author)" class="mb-4">
									<v-divider class="my-4"></v-divider>
									
									<h3 class="text-h6 font-weight-bold mb-2">Add References</h3>
									<p class="text-body-2 mb-3">Link this thread to an artist or release.</p>
									
									<v-row align="start">
										<v-col align="center" cols="12" sm="7">
											<v-autocomplete
												v-model="selectedReference"
												:items="searchResults"
												:loading="isSearching"
												v-model:search="searchQuery"
												item-title="displayName"
												item-value="id"
												label="Search artists or releases"
												placeholder="Type to search"
												outlined
												dense
												return-object
												no-filter
												:custom-filter="() => true"
												:menu-props="{ closeOnContentClick: true }"
											>
												<template v-slot:selection="{ item }">
													{{ item.raw.name }}
													<span v-if="item.raw.type === 'release'" class="text-caption ms-1">
														(Release)
													</span>
													<span v-else class="text-caption ms-1">
														(Artist)
													</span>
												</template>

												<template v-slot:item="{ props, item }">
													<v-list-item v-bind="props">
														<template v-slot:title>
															<span v-if="item.raw.type === 'release'">
																"{{ item.raw.name }}" {{ item.raw.artist }} [{{ item.raw.year }}]
															</span>
															<span v-else>{{ item.raw.name }}</span>
														</template>
														<template v-slot:subtitle>
															<span v-if="item.raw.type === 'release'">Release</span>
															<span v-else>Artist</span>
														</template>
													</v-list-item>
												</template>

												<!-- <template v-slot:append>
													<v-btn
														color="primary"
														icon
														density="compact"
														:disabled="!selectedReference"
														@click="addReference(selectedReference)"
													>
														<v-icon>mdi-plus</v-icon>
													</v-btn>
												</template> -->
											</v-autocomplete>
										</v-col>
										<v-col align="center" cols="12" sm="3">
											<v-select
												v-model="referenceType"
												hint="Filter type"
												:items="referenceTypes"
												item-title="text"
												item-value="value"
												label="Filter type"
												outlined
												return-object
												single-line
												dense
											></v-select>
										</v-col>
										<v-col align="center" cols="12" sm="2" class="d-flex justify-center">
											<v-btn
												color="primary"
												icon
												density="compact"
												:disabled="!selectedReference"
												@click="addReference(selectedReference)"
												style="margin:10px"
											>
												<v-icon>mdi-plus</v-icon>
											</v-btn>
										</v-col>
									</v-row>
								</section>

								<!-- existing references -->
								<section v-if="thread && thread.references && thread.references.length > 0" class="mb-4">
									<v-divider class="my-4"></v-divider>

									<h3 class="text-h6 font-weight-bold mb-2">References</h3>
									<v-chip-group>
										<v-chip
											v-for="ref in thread.references"
											:key="ref.id"
											:to="getReferenceLink(ref)"
											color="primary"
											outlined
											class="mr-2"
										>
											<v-icon small left>{{ getReferenceIcon(ref.reference_type) }}</v-icon>
											{{ ref.name }}
											<v-icon
												v-if="isCurrentUserAuthor(thread.author)" 
												right 
												x-small 
												class="ml-1" 
												@click.stop.prevent="confirmDeleteReference(ref)"
											>
												mdi-close
											</v-icon>
										</v-chip>
									</v-chip-group>
								</section>

								<section role="region" aria-labelledby="replies-heading">
									<h2 id="replies-heading" class="text-h5 font-weight-bold mb-4">
										Replies
									</h2>
									<v-list dense aria-label="Thread replies">
										<v-list-item v-for="reply in paginatedReplies" :key="reply.id">
											<v-list-item-content>
												<article :aria-labelledby="`reply-author-${reply.id}`">
													<div class="d-flex justify-space-between">
														<v-list-item class="pa-0">
															<!-- Container for image and text, not wrapped in a router-link -->
															<div class="d-flex align-center">
																<!-- Profile Image (Clickable if you want it) -->
																<router-link :to="`/user/${reply.author.name}`" class="text-decoration-none">
																	<img
																		:src="`http://localhost:5001/static/pfp/${reply.author.id}profilepic.png`"
																		alt="Profile Image"
																		width="40"
																		height="40"
																		class="mr-3 rounded-md"
																	/>
																</router-link>
																
																<!-- Text Content (Name + Date) -->
																<div class="d-flex flex-column">
																	<!-- Name (Clickable) -->
																	<router-link 
																		:to="`/user/${reply.author.name}`" 
																		class="font-weight-bold text--primary text-decoration-none"
																		style="color: black;"
																	>
																		{{ reply.author.name }}
																	</router-link>
																	
																	<!-- Date (Not clickable) -->
																	<v-list-item-subtitle class="text-caption text--secondary">
																		{{ reply.date }}
																	</v-list-item-subtitle>
																</div>
															</div>
														</v-list-item>
														<!-- buttons for replies -->
														<div class="d-flex">
															<v-btn icon small @click="replyToComment(reply)" aria-label="Reply to this comment">
																<v-icon small>mdi-reply</v-icon>
															</v-btn>
															<v-btn v-if="!isCurrentUserAuthor(reply.author)" icon small @click.stop="reportItem(reply, 'reply')" aria-label="Report this comment">
																<v-icon small color="warning">mdi-flag</v-icon>
															</v-btn>
															<div v-if="isCurrentUserAuthor(reply.author)">
																<v-btn icon small @click="editReply(reply)" aria-label="Edit your reply" class="ml-2">
																	<v-icon small>mdi-pencil</v-icon>
																</v-btn>
																<v-btn icon small @click="confirmDeleteReply(reply)" aria-label="Delete your reply" color="error" class="ml-2">
																	<v-icon small>mdi-delete</v-icon>
																</v-btn>
															</div>
														</div>
													</div>
													
													<v-list-item-text v-if="editingReplyId === reply.id">
														<v-textarea
															v-model="editedReplyContent"
															outlined
															rows="3"
															hide-details
															class="mt-2"
														></v-textarea>
														<div class="d-flex justify-end mt-4 mb-2">
															<v-btn text small @click="cancelEditReply" class="mr-2" aria-label="Cancel your edit">Cancel</v-btn>
															<v-btn color="primary" small @click="saveReplyEdit(reply)" aria-label="Save your edits">Save</v-btn>
														</div>
													</v-list-item-text>
													<v-list-item-text v-else>{{ reply.content }}</v-list-item-text>
													
													<!-- show parent reference if it's a reply to another comment -->
													<v-list-item-text v-if="reply.parentId" class="text-caption font-italic pl-4 my-1">
														Replying to {{ getReplyAuthorName(reply.parentId) }}
													</v-list-item-text>
												</article>
											</v-list-item-content>
										</v-list-item>
										<v-list-item v-if="thread.replies.length === 0">
											<v-list-item-content>
												<v-list-item-text class="text-center">No replies yet. Be the first to reply!</v-list-item-text>
											</v-list-item-content>
										</v-list-item>
									</v-list>

									<!-- pagination -->
									<div class="d-flex justify-center mt-4">
										<v-pagination
											v-if="totalPages > 1"
											v-model="currentPage"
											:length="totalPages"
											:total-visible="5"
											aria-label="Pagination for replies"
										></v-pagination>
									</div>
								</section>

								<v-divider class="my-4" aria-hidden="true"></v-divider>
								<section role="region" aria-labelledby="reply-form-heading">
									<h2 id="reply-form-heading" class="text-h5 font-weight-bold mb-4">
										{{ replyingTo ? `Reply to ${replyingTo}` : 'Add a Reply' }}
									</h2>
									<v-form @submit.prevent="addReply" aria-label="Reply form">
										<div role="group" aria-labelledby="reply-form-heading">
											<!-- replying to indicator -->
											<div v-if="replyingTo" class="mb-2 d-flex align-center">
												<v-chip color="primary" text-color="white" class="mr-2">
													Replying to {{ replyingTo }}
												</v-chip>
											</div>
											
											<label for="reply-textarea" class="sr-only">Your Reply</label>
											<v-textarea
												id="reply-textarea"
												v-model="newReplyContent"
												label="Your Reply"
												outlined
												rows="4"
												required
												@click.stop
												aria-required="true"
											></v-textarea>
											<div class="d-flex">
												<v-btn
													v-if="replyingTo"
													text
													@click="cancelReplyingTo"
													class="mr-2"
													color="grey darken-1"
													aria-label="Cancel reply"
												>
													<v-icon small left>mdi-close</v-icon>
													Cancel
												</v-btn>
												<v-btn
													type="submit"
													color="primary"
													aria-label="Post your reply"
												>
													Post Reply
												</v-btn>
											</div>
										</div>
									</v-form>
								</section>
							</v-card>
						</v-col>
					</v-row>
				</v-container>
			</main>
		</div>

		<!-- confirmation dialog for delete -->
		<v-dialog v-model="deleteDialog" max-width="400">
			<v-card>
				<v-card-title class="headline">Confirm Delete</v-card-title>
				<v-card-text>Are you sure you want to delete this {{ deleteType }}? This action cannot be undone.</v-card-text>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn text @click="deleteDialog = false">Cancel</v-btn>
					<v-btn color="error" text @click="performDelete">Delete</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>

		<!-- dialog for reporting -->
		<v-dialog v-model="reportDialog" max-width="500">
			<v-card>
				<v-card-title class="headline">Report {{ reportType }}</v-card-title>
				<v-card-text>
					<p>Please provide a reason for reporting this {{ reportType }}.</p>
					<v-select
						v-model="reportReason"
						:items="['Spam', 'Harassment', 'Inappropriate Content', 'Other']"
						label="Select a reason"
						outlined
						dense
					></v-select>
					<v-textarea
						v-if="reportReason === 'Other'"
						v-model="customReportReason"
						label="Describe the issue"
						outlined
						rows="2"
					></v-textarea>
				</v-card-text>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn text @click="reportDialog = false">Cancel</v-btn>
					<v-btn color="warning" text @click="submitReport">Submit Report</v-btn>
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
					<p>You need to be logged in to report, edit, delete, or reply.</p>
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
	name: "ForumThread",
	components: {
		Navbar,
	},
	data() {
		return {
			thread: null,
			isLoading: true,
			error: null,
			
			currentUser: null,
			showLoginPrompt: false,
			
			newReplyContent: "",
			replyingToId: null,
			replyingTo: null,
			editingReplyId: null,
			editedReplyContent: "",
			isEditingThread: false,
			editedThreadContent: "",
			
			itemsPerPage: 5,
			currentPage: 1,
			
			deleteDialog: false,
			deleteType: "", // "reply" or "thread"
			itemToDelete: null,

			reportDialog: false,
			reportType: "",
			reportItemData: null,
			reportReason: "",
			customReportReason: "",

			searchQuery: "",
			searchResults: [],
			isSearching: false,
			selectedReference: null,
			referenceType: { text: 'All', value: 'all' },
			referenceTypes: [
				{ text: 'All', value: 'all' },
				{ text: 'Artists', value: 'artist' },
				{ text: 'Releases', value: 'release' }
			]
		};
	},
	computed: {
		totalPages() {
			return this.thread ? Math.ceil(this.thread.replies.length / this.itemsPerPage) : 0;
		},
		paginatedReplies() {
			if (!this.thread) return [];
			const start = (this.currentPage - 1) * this.itemsPerPage;
			const end = start + this.itemsPerPage;
			return this.thread.replies.slice(start, end);
		}
	},
	created() {
		// Get the thread ID from the route params
		const threadId = this.$route.params.thread_id;
		
		// Check if user is logged in
		this.checkUserSession();
		this.fetchThreadData(threadId);
	},
	methods: {
		async checkUserSession() {
			try {
				const response = await axios.get('http://localhost:5001/check-session', {
					withCredentials: true
				});
				if (response.data.logged_in) {
					this.currentUser = response.data.user;
				}
			} catch (error) {
				console.error('Error checking session:', error);
			}
		},

		async fetchThreadData(threadId) {
			this.isLoading = true;
			this.error = null;
			
			try {
				const response = await axios.get(`http://localhost:5001/forum/thread/${threadId}`);
				this.thread = response.data;

				console.log(this.thread);

				this.isLoading = false;
			} catch (error) {
				console.error('Error fetching thread:', error);
				this.error = 'Failed to load thread data. Please try again later.';
				this.isLoading = false;
				this.$router.push({path: '/forum'});
			}
		},
		
		isCurrentUserAuthor(author) {
			return this.currentUser && author.id === this.currentUser.id;
		},
		
		replyToComment(reply) {
			this.checkUserSession();

			if (!this.currentUser) {
				this.showLoginPrompt = true;
				return;
			}
			
			this.replyingToId = reply.id;
			this.replyingTo = reply.author.name;
			
			// Scroll to reply form
			this.$nextTick(() => {
				document.getElementById('reply-form-heading').scrollIntoView({ behavior: 'smooth' });
			});
		},
		
		cancelReplyingTo() {
			this.replyingToId = null;
			this.replyingTo = null;
		},
		
		async addReply() {
			this.checkUserSession();

			if (!this.currentUser) {
				this.showLoginPrompt = true;
				return;
			}
			
			if (!this.newReplyContent.trim()) {
				return;
			}
			
			try {
				const response = await axios.post(`http://localhost:5001/forum/thread/${this.thread.id}/reply`, {
					content: this.newReplyContent,
					parentId: this.replyingToId
				}, { 
					headers: {
						Authorization: `Bearer ${localStorage.getItem('token')}`
					},
					withCredentials: true
				});
				
				// Add the new reply to the thread
				this.thread.replies.push(response.data);
				this.newReplyContent = "";
				this.replyingToId = null;
				this.replyingTo = null;
				
				// Move to last page to show the new comment
				this.currentPage = this.totalPages;
			} catch (error) {
				console.error('Error adding reply:', error);
				alert('Failed to add reply. Please try again.');
			}
		},
		
		getReplyAuthorName(replyId) {
			if (!this.thread) return 'Unknown';
			const parentReply = this.thread.replies.find(r => r.id === replyId);
			return parentReply ? parentReply.author.name : 'Unknown';
		},
		
		editReply(reply) {
			this.editingReplyId = reply.id;
			this.editedReplyContent = reply.content;
		},
		
		cancelEditReply() {
			this.editingReplyId = null;
			this.editedReplyContent = "";
		},
		
		async saveReplyEdit(reply) {
			if (!this.editedReplyContent.trim()) {
				return;
			}
			
			try {
				await axios.put(`http://localhost:5001/forum/reply/${reply.id}`, {
					content: this.editedReplyContent
				}, { 
					headers: {
						Authorization: `Bearer ${localStorage.getItem('token')}`
					},
					withCredentials: true
				});
				
				// Update local data
				const replyIndex = this.thread.replies.findIndex(r => r.id === reply.id);
				if (replyIndex !== -1) {
					this.thread.replies[replyIndex].content = this.editedReplyContent;
					this.thread.replies[replyIndex].isEdited = true;
				}
				
				this.editingReplyId = null;
				this.editedReplyContent = "";
			} catch (error) {
				console.error('Error editing reply:', error);
				alert('Failed to save changes. Please try again.');
			}
		},
		
		editThread() {
			this.isEditingThread = true;
			this.editedThreadContent = this.thread.content;
		},
		
		cancelEditThread() {
			this.isEditingThread = false;
			this.editedThreadContent = "";
		},
		
		async saveThreadEdit() {
			if (!this.editedThreadContent.trim()) {
				return;
			}
			
			try {
				await axios.put(`http://localhost:5001/forum/thread/${this.thread.id}`, {
					content: this.editedThreadContent
				}, {
					headers: {
						Authorization: `Bearer ${localStorage.getItem('token')}`
					},
					withCredentials: true
				});
				
				// Update thread in local data
				this.thread.content = this.editedThreadContent;
				this.thread.isEdited = true;
				
				this.isEditingThread = false;
				this.editedThreadContent = "";
			} catch (error) {
				console.error('Error editing thread:', error);
				alert('Failed to save changes. Please try again.');
			}
		},

		confirmDeleteReply(reply) {
			this.deleteType = "reply";
			this.itemToDelete = reply;
			this.deleteDialog = true;
		},
		
		confirmDeleteThread() {
			this.deleteType = "thread";
			this.itemToDelete = this.thread;
			this.deleteDialog = true;
		},

		confirmDeleteReference(reference) {
			this.deleteType = "reference";
			this.itemToDelete = reference;
			this.deleteDialog = true;
		},
		
		async performDelete() {
			try {
				if (this.deleteType === "reply") {
					await axios.delete(`http://localhost:5001/forum/reply/${this.itemToDelete.id}`, {
						headers: {
							Authorization: `Bearer ${localStorage.getItem('token')}`
						},
						withCredentials: true
					});
					
					// Remove from local data
					const index = this.thread.replies.findIndex(r => r.id === this.itemToDelete.id);
					if (index !== -1) {
						this.thread.replies.splice(index, 1);
					}
					
					// Adjust page if necessary
					if (this.paginatedReplies.length === 0 && this.currentPage > 1) {
						this.currentPage--;
					}
				} else if (this.deleteType === "thread") {
					await axios.delete(`http://localhost:5001/forum/thread/${this.thread.id}`, { withCredentials: true });
					
					// TODO: redirect page after thread has been deleted
					this.thread.content = "[This thread has been deleted by the author]";
					this.thread.isDeleted = true;

					// this.$router.push('/forum');
				} else if (this.deleteType === "reference") {
					const reference = this.itemToDelete;
					const referenceId = reference.reference_id;
					console.log('Removing reference with ID:', referenceId);
					
					try {
						await axios.delete(`http://localhost:5001/forum/delete-reference/${referenceId}`, { 
							withCredentials: true 
						});
						
						// Remove from local data
						const index = this.thread.references.findIndex(r => r.reference_id === referenceId);
						if (index !== -1) {
							this.thread.references.splice(index, 1);
						}
					} catch (error) {
						console.error("Error removing reference:", error);
						alert("Failed to remove reference. Please try again.");
					}
				}
			} catch (error) {
				console.error('Error deleting item:', error);
				alert('Failed to delete. Please try again.');
			} finally {
				this.deleteDialog = false;
				this.itemToDelete = null;
			}
		},
		
		reportItem(item, type) {
			this.checkUserSession();

			if (!this.currentUser) {
				this.showLoginPrompt = true;
				return;
			}
			
			this.reportType = type;
			this.reportItemData = item;
			this.reportReason = "";
			this.customReportReason = "";
			this.reportDialog = true;
		},
		
		async submitReport() {
			const reason = this.reportReason === "Other" ? this.customReportReason : this.reportReason;

			if (!reason.trim()) {
				alert("Please provide a valid reason.");
				return;
			}

			try {
				await axios.post('http://localhost:5001/forum/report', {
					type: this.reportType,
					itemId: this.reportItemData.id,
					reason: reason
				}, { withCredentials: true });
				
				alert(`Your report has been submitted. A moderator will review it.`);
				this.reportDialog = false;
			} catch (error) {
				console.error('Error submitting report:', error);
				alert('Failed to submit report. Please try again.');
			}
		},

		goToLogin() {
			const returnTo = window.location.pathname + window.location.search;
			window.location.href = `/login?returnTo=${encodeURIComponent(
				returnTo
			)}`;
		},

		goToSignup() {
			const returnTo = window.location.pathname + window.location.search;
			window.location.href = `/signup?returnTo=${encodeURIComponent(
				returnTo
			)}`;
		},

		debugSearch(value) {
			console.log("Debug search:", value);
		},

		async searchReferences(searchValue) {
			if (!this.searchQuery || this.searchQuery.length < 2) {
				this.searchResults = [];
				return;
			}
			
			this.isSearching = true;
			
			try {
				const response = await axios.get(`http://localhost:5001/search/reference`, {
					params: {
						query: this.searchQuery,
						type: this.referenceType.value
					}
				});

				this.searchResults = response.data.results;
			} catch (error) {
				console.error('Error searching references:', error);
				this.searchResults = [];
			} finally {
				this.isSearching = false;
			}
		},

		async addReference(reference) {
			if (!reference) return;

			let reference_type = reference.type;
			if (reference_type === 'master') {
				reference_type = 'release';
			}
			
			const isDuplicate = this.thread.references?.some(r => 
				r.reference_id === reference.id && r.reference_type === reference_type
			);
			if (isDuplicate) {
				alert("This reference has already been added.");
				return;
			}

			try {
				const response = await axios.post(`http://localhost:5001/forum/reference`, {
					item_type: 'thread',
					item_id: this.thread.id,
					reference_type: reference_type,
					reference_id: reference.id,
					reference_name: reference.name,
				}, { withCredentials: true });
				
				if (response.data.success) {
					if (!this.thread.references) {
						this.thread.references = [];
					}

					this.thread.references.push({
						item_type: 'thread',
						item_id: this.thread.id,
						reference_type: reference_type,
						reference_id: reference.id,
						name: reference.name,
					});

					this.selectedReference = null;
					this.searchQuery = "";
				}
			} catch (error) {
				console.error('Error adding reference:', error);
				alert('Failed to add reference. Please try again.');
			}
		},

		getReferenceIcon(type) {
			switch(type) {
				case 'artist':
					return 'mdi-account-music';
				case 'release':
					return 'mdi-album';
				default:
					return 'mdi-link';
			}
		},
		
		getReferenceLink(reference) {
			switch(reference.reference_type) {
				case 'artist':
					return `/artist/${reference.reference_id}`;
				case 'release':
					return `/master/${reference.reference_id}`;
				default:
					return '#';
			}
		}
	},
	watch: {
		searchQuery: {
			handler(newVal) {
				// console.log("Search query changed:", newVal);
				if (newVal && newVal.length >= 2) {
					this.searchReferences(newVal);
				} else {
					this.searchResults = [];
				}
			},
			immediate: false
		}
	}
};
</script>

<style scoped>
@import "../../src/assets/background.css";
/* Add explicit z-index to ensure report button remains clickable */
.v-btn[aria-label="Report this thread"] {
	position: relative;
	z-index: 500;
}

.v-btn.v-btn--icon {
	width: 38px;
	height: 38px;
	margin: 0 4px;
}

.v-btn {
	margin: 0 4px;
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