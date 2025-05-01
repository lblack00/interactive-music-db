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
							<!-- Thread Header Card -->
							<v-card class="thread-header mb-6">
								<article role="region" aria-labelledby="thread-title">
									<header class="thread-header-content">
										<div
											class="d-flex justify-space-between align-center mb-4 thread-title-row"
										>
											<h1 id="thread-title" class="text-h4 font-weight-bold">
												{{ thread.title }}
												<span class="original-post-badge">Original Post</span>
											</h1>

											<!-- Dropdown for thread actions -->
											<v-menu offset-y>
												<template v-slot:activator="{ props }">
													<v-btn
														icon
														density="compact"
														v-bind="props"
														aria-label="Thread actions"
													>
														<v-icon small>mdi-dots-vertical</v-icon>
													</v-btn>
												</template>
												<v-list>
													<v-list-item
														@click.stop.prevent="reportItem(thread, 'thread')"
													>
														<v-list-item-title>Report</v-list-item-title>
													</v-list-item>
													<v-list-item
														v-if="isCurrentUserAuthor(thread.author)"
														@click="editThread"
													>
														<v-list-item-title>Edit</v-list-item-title>
													</v-list-item>
													<v-list-item
														v-if="isCurrentUserAuthor(thread.author)"
														@click="showAddReferenceDialog = true"
													>
														<v-list-item-title>Add Reference</v-list-item-title>
													</v-list-item>
													<v-list-item
														v-if="isCurrentUserAuthor(thread.author)"
														@click="confirmDeleteThread"
													>
														<v-list-item-title>Delete</v-list-item-title>
													</v-list-item>
												</v-list>
											</v-menu>
										</div>

										<!-- display author and date published -->
										<div class="d-flex align-center mb-4">
											<router-link
												:to="`/user/${thread.author.name}`"
												class="text-decoration-none"
											>
												<img
													:src="`http://localhost:5001${thread.author.pfp}`"
													alt="Profile Image"
													width="48"
													height="48"
													class="mr-3 rounded-md"
												/>
											</router-link>

											<div>
												<router-link
													:to="`/user/${thread.author.name}`"
													class="font-weight-bold text-body"
													style="text-decoration: none"
												>
													{{ thread.author.name }}
												</router-link>
												<div class="text-caption text--secondary">
													{{ thread.date }}
												</div>
											</div>
										</div>
									</header>
									<div class="thread-content mb-4">
										<v-textarea
											v-if="isEditingThread"
											v-model="editedThreadContent"
											outlined
											rows="4"
											hide-details
										></v-textarea>
										<p v-else class="thread-text">{{ thread.content }}</p>
									</div>
									<div v-if="isEditingThread" class="d-flex justify-end m-2">
										<v-btn text @click="cancelEditThread" class="mr-2"
											>Cancel</v-btn
										>
										<v-btn color="primary" @click="saveThreadEdit"
											>Save Changes</v-btn
										>
									</div>
								</article>
							</v-card>

							<!-- Decorative divider -->
							<div class="decorative-divider">
								<span class="divider-line"></span>
								<v-icon class="divider-icon">mdi-forum</v-icon>
								<span class="divider-line"></span>
							</div>

							<!-- Replies Section -->
							<v-card class="replies-section">
								<section role="region" aria-labelledby="replies-heading">
									<h2
										id="replies-heading"
										class="text-h5 font-weight-bold mb-4"
									>
										Replies
									</h2>
									<v-list dense aria-label="Thread replies">
										<template v-for="reply in paginatedReplies" :key="reply.id">
											<v-list-item
												:class="[
													reply.depth > 0 ? 'nested-reply' : 'top-level-reply',
													`depth-${reply.depth}`,
												]"
												:style="{
													marginLeft: `${reply.depth * 24}px`,
													maxWidth: `calc(100% - ${reply.depth * 24}px)`,
												}"
											>
												<div
													class="reddit-reply-header d-flex justify-space-between align-center"
												>
													<div class="d-flex align-center">
														<router-link
															v-if="!reply.isDeleted"
															:to="`/user/${reply.author.name}`"
															class="text-decoration-none"
														>
															<img
																:src="`http://localhost:5001${reply.author.pfp}`"
																alt="Profile Image"
																width="40"
																height="40"
																class="mr-2 rounded-md"
															/>
														</router-link>
														<router-link
															:to="`/user/${reply.author.name}`"
															class="reply-username text-decoration-none"
														>
															{{ reply.isDeleted ? "[deleted]" : reply.author.name }}
														</router-link>
														<span class="ml-2 reply-date">{{ reply.date }}</span>
													</div>
													<v-menu offset-y>
														<template v-slot:activator="{ props }">
															<v-btn
																icon
																density="compact"
																v-bind="props"
																aria-label="Reply actions"
															>
																<v-icon small>mdi-dots-vertical</v-icon>
															</v-btn>
														</template>
														<v-list>
															<v-list-item @click="replyToComment(reply)">
																<v-list-item-title>Reply</v-list-item-title>
															</v-list-item>
															<v-list-item
																v-if="!isCurrentUserAuthor(reply.author)"
																@click.stop="reportItem(reply, 'reply')"
															>
																<v-list-item-title>Report</v-list-item-title>
															</v-list-item>
															<v-list-item
																v-if="isCurrentUserAuthor(reply.author)"
																@click="editReply(reply)"
															>
																<v-list-item-title>Edit</v-list-item-title>
															</v-list-item>
															<v-list-item
																v-if="isCurrentUserAuthor(reply.author)"
																@click="confirmDeleteReply(reply)"
															>
																<v-list-item-title>Delete</v-list-item-title>
															</v-list-item>
														</v-list>
													</v-menu>
												</div>
												<div v-if="reply.parentId" class="replying-to-context">
													Replying to {{ getReplyAuthorName(reply.parentId) }}
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
														<v-btn
															text
															small
															@click="cancelEditReply"
															class="mr-2"
															aria-label="Cancel your edit"
															>Cancel</v-btn
														>
														<v-btn
															color="primary"
															small
															@click="saveReplyEdit(reply)"
															aria-label="Save your edits"
															>Save</v-btn
														>
													</div>
												</v-list-item-text>
												<v-list-item-text v-else>{{
													reply.isDeleted ? "[deleted]" : reply.content
												}}</v-list-item-text>
											</v-list-item>
										</template>
										<v-list-item v-if="flattenedReplies.length === 0">
											<v-list-item-content>
												<v-list-item-text class="text-center"
													>No replies yet. Be the first to
													reply!</v-list-item-text
												>
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
									<v-card class="reply-form-card">
										<h2
											id="reply-form-heading"
											class="text-h5 font-weight-bold mb-4"
										>
											{{
												replyingTo ? `Reply to ${replyingTo}` : "Add a Reply"
											}}
										</h2>
										<v-form @submit.prevent="addReply" aria-label="Reply form">
											<div role="group" aria-labelledby="reply-form-heading">
												<div v-if="replyingTo" class="mb-2 d-flex align-center">
													<v-chip
														color="primary"
														text-color="white"
														class="mr-2"
													>
														Replying to {{ replyingTo }}
													</v-chip>
												</div>
												<label for="reply-textarea" class="sr-only"
													>Your Reply</label
												>
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
												<div class="d-flex mt-3">
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
									</v-card>
								</section>
							</v-card>

							<!-- existing references -->
							<section
								v-if="
									thread && thread.references && thread.references.length > 0
								"
								class="references-section"
							>
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
										<v-icon small left>{{
											getReferenceIcon(ref.reference_type)
										}}</v-icon>
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
						</v-col>
					</v-row>
				</v-container>
			</main>
		</div>

		<!-- confirmation dialog for delete -->
		<v-dialog v-model="deleteDialog" max-width="400">
			<v-card>
				<v-card-title class="headline">Confirm Delete</v-card-title>
				<v-card-text
					>Are you sure you want to delete this {{ deleteType }}? This action
					cannot be undone.</v-card-text
				>
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
					<v-btn color="warning" text @click="submitReport"
						>Submit Report</v-btn
					>
				</v-card-actions>
			</v-card>
		</v-dialog>

		<!-- Add Reference dialog -->
		<v-dialog v-model="showAddReferenceDialog" max-width="550">
			<v-card class="reference-card pa-4">
				<div class="mb-2">
					<h3 class="reference-title mb-1">Add Reference</h3>
					<div class="reference-subtitle mb-4">
						Link this thread to an artist or release.
					</div>
				</div>
				<v-row align="center" class="reference-row" no-gutters>
					<v-col cols="12" sm="7" class="pr-sm-2 mb-2 mb-sm-0">
						<v-autocomplete
							v-model="selectedReference"
							:items="searchResults"
							:loading="isSearching"
							v-model:search="searchQuery"
							item-title="displayName"
							item-value="id"
							placeholder="Search artists or releases"
							outlined
							dense
							return-object
							no-filter
							:custom-filter="() => true"
							:menu-props="{ closeOnContentClick: true }"
							hide-details
						>
							<template v-slot:selection="{ item }">
								{{ item.raw.name }}
								<span
									v-if="item.raw.type === 'release'"
									class="text-caption ms-1"
									>(Release)</span
								>
								<span v-else class="text-caption ms-1">(Artist)</span>
							</template>
							<template v-slot:item="{ props, item }">
								<v-list-item v-bind="props">
									<template v-slot:title>
										<span v-if="item.raw.type === 'release'">
											"{{ item.raw.name }}" {{ item.raw.artist }} [{{
												item.raw.year
											}}]
										</span>
										<span v-else>{{ item.raw.name }}</span>
									</template>
									<template v-slot:subtitle>
										<span v-if="item.raw.type === 'release'">Release</span>
										<span v-else>Artist</span>
									</template>
								</v-list-item>
							</template>
							<template v-slot:append-inner>
								<v-progress-circular
									v-if="isSearching"
									indeterminate
									size="18"
									color="primary"
									class="mr-2"
								/>
							</template>
						</v-autocomplete>
					</v-col>
					<v-col cols="12" sm="3" class="pr-sm-2 mb-2 mb-sm-0">
						<v-select
							v-model="referenceType"
							:items="referenceTypes"
							item-title="text"
							item-value="value"
							placeholder="Type"
							outlined
							dense
							return-object
							single-line
							hide-details
						></v-select>
					</v-col>
					<v-col cols="12" sm="2" class="d-flex justify-center align-center">
						<v-btn
							color="primary"
							icon
							density="medium"
							:disabled="!selectedReference"
							@click="addReference(selectedReference)"
							class="reference-add-btn"
						>
							<v-icon>mdi-plus</v-icon>
						</v-btn>
					</v-col>
				</v-row>
				<v-card-actions class="justify-end mt-4">
					<v-btn text @click="showAddReferenceDialog = false">Cancel</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>

		<!-- Replace the login prompt overlay with v-dialog -->
		<v-dialog v-model="showLoginPrompt" max-width="400px">
			<v-card class="login-prompt-card">
				<v-card-text class="text-center pa-6">
					<v-icon size="48" color="primary" class="mb-4"
						>mdi-account-lock</v-icon
					>
					<h3 class="text-h5 font-weight-bold mb-3 dialog-title">
						Please Log In
					</h3>
					<p class="text-subtitle-1 text-medium-emphasis mb-6">
						You need to log in to do that.
					</p>
					<div class="d-flex justify-center mb-4 gap-3">
						<v-btn color="primary" class="action-btn" @click="goToLogin">
							Log In
						</v-btn>
						<v-btn color="secondary" class="action-btn" @click="goToSignup">
							Sign Up
						</v-btn>
					</div>
					<v-btn
						variant="text"
						color="grey-darken-1"
						@click="showLoginPrompt = false"
						class="cancel-btn"
					>
						Cancel
					</v-btn>
				</v-card-text>
			</v-card>
		</v-dialog>
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
				referenceType: { text: "All", value: "all" },
				referenceTypes: [
					{ text: "All", value: "all" },
					{ text: "Artists", value: "artist" },
					{ text: "Releases", value: "release" },
				],
				showAddReferenceDialog: false,
			};
		},
		computed: {
			totalPages() {
				return this.thread
					? Math.ceil(this.flattenedReplies.length / this.itemsPerPage)
					: 0;
			},
			paginatedReplies() {
				if (!this.thread) return [];
				const start = (this.currentPage - 1) * this.itemsPerPage;
				const end = start + this.itemsPerPage;
				return this.flattenedReplies.slice(start, end);
			},
			replyTree() {
				if (!this.thread || !this.thread.replies) return [];
				return this.buildReplyTree(this.thread.replies);
			},
			flattenedReplies() {
				if (!this.thread || !this.thread.replies) return [];
				return this.flattenTree(this.replyTree);
			},
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
					const response = await axios.get(
						"http://localhost:5001/check-session",
						{
							withCredentials: true,
						}
					);
					if (response.data.logged_in) {
						this.currentUser = response.data.user;
					}
				} catch (error) {
					console.error("Error checking session:", error);
				}
			},

			async fetchThreadData(threadId) {
				this.isLoading = true;
				this.error = null;

				try {
					const response = await axios.get(
						`http://localhost:5001/forum/thread/${threadId}`
					);
					this.thread = response.data;

					console.log(this.thread);

					this.isLoading = false;
				} catch (error) {
					console.error("Error fetching thread:", error);
					this.error = "Failed to load thread data. Please try again later.";
					this.isLoading = false;
					this.$router.push({ path: "/forum" });
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
					document
						.getElementById("reply-form-heading")
						.scrollIntoView({ behavior: "smooth" });
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
					const response = await axios.post(
						`http://localhost:5001/forum/thread/${this.thread.id}/reply`,
						{
							content: this.newReplyContent,
							parentId: this.replyingToId,
						},
						{
							withCredentials: true,
						}
					);

					// Add the new reply to the thread
					this.thread.replies.push(response.data);
					this.newReplyContent = "";
					this.replyingToId = null;
					this.replyingTo = null;

					// Move to last page
					this.$nextTick(() => {
						this.currentPage = this.totalPages;
					});
				} catch (error) {
					console.error("Error adding reply:", error);
					alert("Failed to add reply. Please try again.");
				}
			},

			getReplyAuthorName(replyId) {
				if (!this.thread) return "Unknown";
				const parentReply = this.thread.replies.find((r) => r.id === replyId && !r.isDeleted);
				return parentReply ? parentReply.author.name : "Unknown";
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
					await axios.put(
						`http://localhost:5001/forum/reply/${reply.id}`,
						{
							content: this.editedReplyContent,
						},
						{
							headers: {
								Authorization: `Bearer ${localStorage.getItem("token")}`,
							},
							withCredentials: true,
						}
					);

					// Update local data
					const replyIndex = this.thread.replies.findIndex(
						(r) => r.id === reply.id
					);
					if (replyIndex !== -1) {
						this.thread.replies[replyIndex].content = this.editedReplyContent;
						this.thread.replies[replyIndex].isEdited = true;
					}

					this.editingReplyId = null;
					this.editedReplyContent = "";
				} catch (error) {
					console.error("Error editing reply:", error);
					alert("Failed to save changes. Please try again.");
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
					await axios.put(
						`http://localhost:5001/forum/thread/${this.thread.id}`,
						{
							content: this.editedThreadContent,
						},
						{
							headers: {
								Authorization: `Bearer ${localStorage.getItem("token")}`,
							},
							withCredentials: true,
						}
					);

					// Update thread in local data
					this.thread.content = this.editedThreadContent;
					this.thread.isEdited = true;

					this.isEditingThread = false;
					this.editedThreadContent = "";
				} catch (error) {
					console.error("Error editing thread:", error);
					alert("Failed to save changes. Please try again.");
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
						await axios.delete(
							`http://localhost:5001/forum/reply/${this.itemToDelete.id}`,
							{
								headers: {
									Authorization: `Bearer ${localStorage.getItem("token")}`,
								},
								withCredentials: true,
							}
						);

						// Remove from local data
						const index = this.thread.replies.findIndex(
							(r) => r.id === this.itemToDelete.id
						);
						if (index !== -1) {
							this.thread.replies.splice(index, 1);
						}

						// Adjust page if necessary
						if (this.paginatedReplies.length === 0 && this.currentPage > 1) {
							this.currentPage--;
						}
					} else if (this.deleteType === "thread") {
						await axios.delete(
							`http://localhost:5001/forum/thread/${this.thread.id}`,
							{ withCredentials: true }
						);

						// TODO: redirect page after thread has been deleted
						this.thread.content =
							"[This thread has been deleted by the author]";
						this.thread.isDeleted = true;

						// this.$router.push('/forum');
					} else if (this.deleteType === "reference") {
						const reference = this.itemToDelete;
						const referenceId = reference.reference_id;
						console.log("Removing reference with ID:", referenceId);

						try {
							await axios.delete(
								`http://localhost:5001/forum/delete-reference/${referenceId}`,
								{
									withCredentials: true,
								}
							);

							// Remove from local data
							const index = this.thread.references.findIndex(
								(r) => r.reference_id === referenceId
							);
							if (index !== -1) {
								this.thread.references.splice(index, 1);
							}
						} catch (error) {
							console.error("Error removing reference:", error);
							alert("Failed to remove reference. Please try again.");
						}
					}
				} catch (error) {
					console.error("Error deleting item:", error);
					alert("Failed to delete. Please try again.");
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
				const reason =
					this.reportReason === "Other"
						? this.customReportReason
						: this.reportReason;

				if (!reason.trim()) {
					alert("Please provide a valid reason.");
					return;
				}

				try {
					await axios.post(
						"http://localhost:5001/forum/report",
						{
							type: this.reportType,
							itemId: this.reportItemData.id,
							reason: reason,
						},
						{ withCredentials: true }
					);

					alert(`Your report has been submitted. A moderator will review it.`);
					this.reportDialog = false;
				} catch (error) {
					console.error("Error submitting report:", error);
					alert("Failed to submit report. Please try again.");
				}
			},

			goToLogin() {
				const returnTo = this.$route.fullPath;
				this.showLoginPrompt = false;
				this.$router.push(`/login?returnTo=${encodeURIComponent(returnTo)}`);
			},

			goToSignup() {
				const returnTo = this.$route.fullPath;
				this.showLoginPrompt = false;
				this.$router.push(`/signup?returnTo=${encodeURIComponent(returnTo)}`);
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
					const response = await axios.get(
						`http://localhost:5001/search/reference`,
						{
							params: {
								query: this.searchQuery,
								type: this.referenceType.value,
							},
						}
					);

					this.searchResults = response.data.results;
				} catch (error) {
					console.error("Error searching references:", error);
					this.searchResults = [];
				} finally {
					this.isSearching = false;
				}
			},

			async addReference(reference) {
				if (!reference) return;

				let reference_type = reference.type;
				if (reference_type === "master") {
					reference_type = "release";
				}

				const isDuplicate = this.thread.references?.some(
					(r) =>
						r.reference_id === reference.id &&
						r.reference_type === reference_type
				);
				if (isDuplicate) {
					alert("This reference has already been added.");
					return;
				}

				try {
					const response = await axios.post(
						`http://localhost:5001/forum/reference`,
						{
							item_type: "thread",
							item_id: this.thread.id,
							reference_type: reference_type,
							reference_id: reference.id,
							reference_name: reference.name,
						},
						{ withCredentials: true }
					);

					if (response.data.success) {
						if (!this.thread.references) {
							this.thread.references = [];
						}

						this.thread.references.push({
							item_type: "thread",
							item_id: this.thread.id,
							reference_type: reference_type,
							reference_id: reference.id,
							name: reference.name,
						});

						this.selectedReference = null;
						this.searchQuery = "";
					}
				} catch (error) {
					console.error("Error adding reference:", error);
					alert("Failed to add reference. Please try again.");
				}
			},

			getReferenceIcon(type) {
				switch (type) {
					case "artist":
						return "mdi-account-music";
					case "release":
						return "mdi-album";
					default:
						return "mdi-link";
				}
			},

			getReferenceLink(reference) {
				switch (reference.reference_type) {
					case "artist":
						return `/artist/${reference.reference_id}`;
					case "release":
						return `/master/${reference.reference_id}`;
					default:
						return "#";
				}
			},

			buildReplyTree(replies) {
				// Create a map of id to reply with children array
				const replyMap = new Map();
				replies.forEach((reply) => {
					replyMap.set(reply.id, { ...reply, children: [] });
				});

				// Build the tree structure
				const rootReplies = [];
				replies.forEach((reply) => {
					const replyWithChildren = replyMap.get(reply.id);
					if (reply.parentId) {
						const parent = replyMap.get(reply.parentId);
						if (parent) {
							parent.children.push(replyWithChildren);
						} else {
							rootReplies.push(replyWithChildren);
						}
					} else {
						rootReplies.push(replyWithChildren);
					}
				});

				return rootReplies;
			},

			flattenTree(tree) {
				const flattened = [];

				function traverse(node, depth = 0) {
					flattened.push({ ...node, depth });
					node.children.forEach((child) => traverse(child, depth + 1));
				}

				tree.forEach((node) => traverse(node));
				return flattened;
			},
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
				immediate: false,
			},
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";

	.grid-container {
		overflow: visible !important;
		background-color: #f8f9fa;
		min-height: 100vh;
	}

	.content {
		padding-top: 80px;
	}

	.thread-header {
		border-radius: 12px;
		box-shadow: 0 8px 32px rgba(20, 160, 133, 0.13),
			0 4px 20px rgba(0, 0, 0, 0.08);
		margin-bottom: 0;
		background: #f5f7fa;
	}

	.thread-header-content {
		padding: 24px;
	}

	.thread-header .thread-title-row {
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.original-post-badge {
		background: #e0e3e7;
		color: #636e72;
		font-size: 0.85rem;
		font-weight: 600;
		border-radius: 6px;
		padding: 2px 10px;
		letter-spacing: 0.5px;
		margin-left: 0.5rem;
		user-select: none;
	}

	.thread-content {
		padding: 0 24px 24px;
	}

	.thread-text {
		font-size: 1.1rem;
		line-height: 1.6;
		color: #333;
	}

	.references-section {
		padding: 0 24px 24px;
	}

	.replies-section {
		border-radius: 12px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
		background: white;
		padding: 24px;
		margin-top: 0;
	}

	.decorative-divider {
		display: flex;
		align-items: center;
		justify-content: center;
		margin: 0 0 32px 0;
		gap: 0.5rem;
	}
	.decorative-divider .divider-line {
		flex: 1;
		height: 1.5px;
		background: linear-gradient(90deg, #eafaf7 0%, #b2bec3 100%);
		border: none;
	}
	.decorative-divider .divider-icon {
		color: #14a085;
		font-size: 1.3rem;
		margin: 0 8px;
	}

	.v-btn {
		text-transform: none;
		letter-spacing: 0.3px;
		font-weight: 500;
		border-radius: 8px;
		transition: all 0.2s ease;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.v-btn--icon {
		width: 38px;
		height: 38px;
		margin: 0 4px;
	}

	.v-list-item {
		border-radius: 8px;
		margin-bottom: 8px;
		transition: all 0.2s ease;
	}

	.v-list-item:hover {
		background-color: rgba(0, 0, 0, 0.02);
	}

	.v-textarea {
		border-radius: 8px;
	}

	.v-textarea .v-input__control {
		border-radius: 8px;
	}

	.v-chip {
		border-radius: 6px;
		transition: all 0.2s ease;
	}

	.v-chip:hover {
		transform: translateY(-1px);
	}

	.v-divider {
		opacity: 0.1;
	}

	/* Replace the login prompt overlay with v-dialog */
	.login-prompt-card {
		border-radius: 24px;
		overflow: hidden;
		background: white;
		position: relative;
	}

	.login-prompt-card::before {
		content: "";
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		height: 4px;
		background: linear-gradient(90deg, var(--primary-color) 0%, #1de9b6 100%);
	}

	.dialog-title {
		border-left: none !important;
		padding-left: 0 !important;
	}

	.action-btn {
		min-width: 120px;
		font-weight: 600;
		letter-spacing: 0.5px;
		border-radius: 12px;
		text-transform: none;
	}

	.cancel-btn {
		font-weight: 500;
		letter-spacing: 0.5px;
		text-transform: none;
	}

	/* High contrast mode styles */
	.high-contrast .login-prompt-card {
		background: #000000 !important;
		border: 2px solid #ffffff !important;
	}

	.high-contrast .login-prompt-card::before {
		background: #ffffff !important;
	}

	.high-contrast .action-btn {
		background: #000000 !important;
		color: #ffffff !important;
		border: 2px solid #ffffff !important;
	}

	.high-contrast .action-btn:hover {
		background: #ffffff !important;
		color: #000000 !important;
	}

	.high-contrast .cancel-btn {
		color: #ffffff !important;
	}

	.high-contrast .cancel-btn:hover {
		background: rgba(255, 255, 255, 0.1) !important;
	}

	/* Remove old login prompt styles */
	.login-prompt-overlay,
	.login-prompt-modal,
	.buttons button,
	.cancel-btn,
	.login-btn,
	.signup-btn {
		/* These styles will be removed */
	}

	/* Reddit-style reply container */
	.reddit-reply {
		margin-left: 32px;
		padding-left: 16px;
		border-left: 2.5px solid #e0e3e7;
		background: #fcfcfd;
		border-radius: 8px;
		margin-bottom: 18px;
		transition: background 0.2s;
	}

	/* Compact reply header */
	.reddit-reply-header {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 2px;
	}
	.reddit-reply-header .reply-username {
		font-weight: 600;
		color: #222;
	}
	.reddit-reply-header .reply-date {
		font-size: 0.95rem;
		color: #888;
	}

	.replying-to-context {
		font-style: italic;
		color: #7fd8c2;
		font-size: 0.97rem;
		margin-bottom: 2px;
	}

	/* Nested reply style for replies to replies */
	.nested-reply {
		margin-left: 40px;
		padding-left: 16px;
		border-left: 2.5px solid #e0e3e7;
		background: #fcfcfd;
		border-radius: 8px;
		margin-bottom: 18px;
		transition: background 0.2s;
	}

	/* Top-level reply style (no indent) */
	.top-level-reply {
		margin-left: 0;
		padding-left: 0;
		background: transparent;
		border: none;
		margin-bottom: 18px;
	}

	/* Three dots button as a gradient circle (for both reply and thread actions) */
	.v-btn[aria-label="Reply actions"],
	.v-btn[aria-label="Thread actions"] {
		background: linear-gradient(90deg, #14a085 60%, #7fd8c2 100%) !important;
		border-radius: 50%;
		box-shadow: 0 2px 8px rgba(20, 160, 133, 0.08);
		width: 38px;
		height: 38px;
		min-width: 38px;
		min-height: 38px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: background 0.2s, box-shadow 0.2s;
	}
	.v-btn[aria-label="Reply actions"]:hover,
	.v-btn[aria-label="Thread actions"]:hover {
		background: linear-gradient(90deg, #11967a 60%, #5fd8b2 100%) !important;
		box-shadow: 0 4px 16px rgba(20, 160, 133, 0.13);
	}
	.v-btn[aria-label="Reply actions"] .v-icon,
	.v-btn[aria-label="Thread actions"] .v-icon {
		color: #fff !important;
	}

	/* Add a Reply section improvements */
	.reply-form-card {
		background: transparent;
		border-radius: 12px;
		box-shadow: 0 2px 8px rgba(20, 160, 133, 0.06);
		padding: 32px 24px 24px 24px;
		margin-top: 32px;
		margin-bottom: 0;
	}
	.reply-form-card .v-btn[type="submit"] {
		background: linear-gradient(90deg, #14a085 60%, #7fd8c2 100%);
		color: #fff;
		font-weight: 600;
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(20, 160, 133, 0.1);
		padding: 0.7rem 2.2rem;
		font-size: 1.08rem;
		letter-spacing: 0.2px;
		transition: background 0.2s, box-shadow 0.2s;
	}
	.reply-form-card .v-btn[type="submit"]:hover {
		background: linear-gradient(90deg, #11967a 60%, #5fd8b2 100%);
		box-shadow: 0 4px 16px rgba(20, 160, 133, 0.18);
	}
	.reply-form-card .v-textarea {
		background: #fff;
		border-radius: 8px;
	}

	/* Replies section spacing */
	.replies-section {
		padding-bottom: 0;
	}

	/* Add new styles for nested replies */
	.depth-1 {
		border-left: 2px solid rgba(20, 160, 133, 0.2);
	}
	.depth-2 {
		border-left: 2px solid rgba(20, 160, 133, 0.3);
	}
	.depth-3 {
		border-left: 2px solid rgba(20, 160, 133, 0.4);
	}
	.depth-4 {
		border-left: 2px solid rgba(20, 160, 133, 0.5);
	}
	.depth-5 {
		border-left: 2px solid rgba(20, 160, 133, 0.6);
	}

	.nested-reply {
		background: rgba(245, 247, 250, 0.5);
		margin-bottom: 8px;
		border-radius: 8px;
		transition: all 0.2s ease;
	}

	.nested-reply:hover {
		background: rgba(245, 247, 250, 0.8);
	}

	/* Dark Mode Styles */
	.dark-mode .grid-container {
		background-color: #121212 !important;
	}

	.dark-mode .thread-header {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
	}

	.dark-mode .thread-title {
		color: #ffffff !important;
	}

	.dark-mode .thread-text {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .original-post-badge {
		background: rgba(255, 255, 255, 0.1);
		color: rgba(255, 255, 255, 0.9);
	}

	.dark-mode .replies-section {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
	}

	.dark-mode .decorative-divider .divider-line {
		background: linear-gradient(
			90deg,
			rgba(255, 255, 255, 0.1) 0%,
			rgba(255, 255, 255, 0.2) 100%
		);
	}

	.dark-mode .decorative-divider .divider-icon {
		color: var(--primary-color);
	}

	.dark-mode .v-list-item {
		background: transparent !important;
		border: none;
		margin-bottom: 8px;
		transition: background-color 0.2s ease;
	}

	.dark-mode .v-list-item:hover {
		background: rgba(255, 255, 255, 0.05) !important;
	}

	.dark-mode .v-list {
		background: transparent !important;
		padding: 0;
	}

	.dark-mode .nested-reply {
		background: transparent !important;
		border-left: 2px solid rgba(255, 255, 255, 0.1);
		margin-bottom: 8px;
		transition: background-color 0.2s ease;
	}

	.dark-mode .nested-reply:hover {
		background: rgba(255, 255, 255, 0.05) !important;
	}

	.dark-mode .v-list-item-text {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .replies-section {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
	}

	.dark-mode .replies-section .v-list {
		background: transparent !important;
		padding: 8px;
	}

	.dark-mode .reply-form-card {
		background: transparent !important;
		border: none;
	}

	.dark-mode .reply-form-card .v-textarea {
		background: rgba(255, 255, 255, 0.05) !important;
		color: #ffffff !important;
	}

	.dark-mode .reply-username,
	.dark-mode .thread-author {
		color: #ffffff !important;
		font-weight: 600;
	}

	.dark-mode .reply-date,
	.dark-mode .thread-date {
		color: rgba(255, 255, 255, 0.7) !important;
	}

	.dark-mode .replying-to-context {
		color: var(--primary-color) !important;
	}

	.dark-mode .v-list-item-title,
	.dark-mode .v-list-item-subtitle {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode h1,
	.dark-mode h2,
	.dark-mode h3,
	.dark-mode .text-h4,
	.dark-mode .text-h5,
	.dark-mode .text-h6 {
		color: #ffffff !important;
	}

	.dark-mode .text-caption,
	.dark-mode .text-subtitle-1,
	.dark-mode .text-subtitle-2 {
		color: rgba(255, 255, 255, 0.7) !important;
	}

	.dark-mode .v-card-title {
		color: #ffffff !important;
	}

	.dark-mode .v-card-text {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .thread-content p {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-list-item-content {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-menu .v-list {
		background: #2d2d2d !important;
	}

	.dark-mode .v-menu .v-list-item {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-menu .v-list-item:hover {
		background: rgba(255, 255, 255, 0.1) !important;
	}

	.dark-mode .depth-1 {
		border-left: 2px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .depth-2 {
		border-left: 2px solid rgba(255, 255, 255, 0.15);
	}

	.dark-mode .depth-3 {
		border-left: 2px solid rgba(255, 255, 255, 0.2);
	}

	.dark-mode .depth-4 {
		border-left: 2px solid rgba(255, 255, 255, 0.25);
	}

	.dark-mode .depth-5 {
		border-left: 2px solid rgba(255, 255, 255, 0.3);
	}

	.dark-mode .v-btn[aria-label="Reply actions"],
	.dark-mode .v-btn[aria-label="Thread actions"] {
		background: linear-gradient(
			90deg,
			var(--primary-color) 60%,
			#1de9b6 100%
		) !important;
		border: none;
	}

	.dark-mode .v-chip {
		background: #363636 !important;
		color: #ffffff !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .v-chip:hover {
		background: #404040 !important;
	}

	.dark-mode .v-dialog .v-card {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .v-text-field .v-field__input,
	.dark-mode .v-textarea .v-field__input {
		background: #363636 !important;
		color: #ffffff !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .v-text-field .v-field__label,
	.dark-mode .v-textarea .v-field__label {
		color: rgba(255, 255, 255, 0.7) !important;
	}

	.dark-mode .v-text-field .v-field__outline {
		--v-field-border-opacity: 0.2 !important;
		border-color: rgba(255, 255, 255, 0.2) !important;
	}

	.dark-mode .login-prompt-card {
		background: #2d2d2d !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .login-prompt-card::before {
		background: linear-gradient(
			90deg,
			var(--primary-color) 0%,
			#1de9b6 100%
		) !important;
	}

	.dark-mode .action-btn {
		background: #363636 !important;
		color: #ffffff !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .action-btn:hover {
		background: #404040 !important;
	}

	.dark-mode .cancel-btn {
		color: rgba(255, 255, 255, 0.7) !important;
	}

	.dark-mode .cancel-btn:hover {
		background: rgba(255, 255, 255, 0.1) !important;
	}

	.dark-mode .v-pagination {
		background: transparent !important;
	}

	.dark-mode .v-pagination__item {
		color: rgba(255, 255, 255, 0.9) !important;
		background: rgba(255, 255, 255, 0.1) !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .v-pagination__item--is-active {
		background: var(--primary-color) !important;
		color: #ffffff !important;
	}

	.dark-mode .v-pagination__navigation {
		background: rgba(255, 255, 255, 0.1) !important;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .v-pagination__navigation .v-icon {
		color: rgba(255, 255, 255, 0.9) !important;
	}

	.dark-mode .v-pagination__item:hover,
	.dark-mode .v-pagination__navigation:hover {
		background: rgba(255, 255, 255, 0.2) !important;
	}

	.dark-mode .v-pagination__item--is-active:hover {
		background: var(--primary-color) !important;
	}

	.dark-mode .thread-header .text-body,
	.dark-mode .thread-header .font-weight-bold,
	.dark-mode .thread-header a,
	.dark-mode cutekumber,
	.dark-mode .thread-author-name {
		color: #ffffff !important;
		text-decoration: none;
	}

	.dark-mode .thread-header .text--secondary {
		color: rgba(255, 255, 255, 0.7) !important;
	}

	.dark-mode .thread-author {
		color: #ffffff !important;
		font-weight: 600;
	}

	.dark-mode .thread-date,
	.dark-mode .text--secondary {
		color: rgba(255, 255, 255, 0.7) !important;
	}
</style>
