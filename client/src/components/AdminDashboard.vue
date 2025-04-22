<!--ARIA Landmarks added by Chantelle Cabanilla-->
<!-- Written by Lucas Black -->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<main role="main">
				<v-container>
					<v-row justify="center">
						<v-col cols="12" md="10">
							<v-card class="pa-4">
								<h1 class="text-h4 font-weight-bold mb-4" id="dashboard-title">
									Admin Dashboard
								</h1>

								<section role="region" aria-labelledby="manage-posts-title">
									<h2 class="text-h5 font-weight-bold mb-4" id="manage-posts-title">
										Manage User Reports
									</h2>

									<div class="d-flex align-center mb-3">
										<span class="mr-2">Sort by:</span>
										<v-btn-toggle v-model="sortBy" mandatory>
											<v-btn value="date" small>Date</v-btn>
											<v-btn value="author" small>Author</v-btn>
											<v-btn value="category" small>Category</v-btn>
										</v-btn-toggle>
										<v-btn icon class="ml-2" @click="toggleSortDirection">
											<v-icon>
												{{ sortDirection === 'asc' ? 'mdi-sort-descending' : 'mdi-sort-ascending' }}
											</v-icon>
										</v-btn>
									</div>

									<v-container>
										<v-row v-if="sortedPosts(true).length > 0">
											<v-col v-for="post in sortedPosts(true)" :key="post.reportId" cols="12" md="6" lg="6">
												<v-card class="mb-4" elevation="2">
													<v-card-title v-if="post.reportType==='thread'" class="text-h6 primary--text">
														{{ post.title }}
													</v-card-title>
													<v-card-title v-else class="text-h6 primary--text">
														Reply to '{{ post.title }}'
													</v-card-title>

													<v-card-subtitle>
														Posted by: {{ post.author }} on {{ post.reportCreatedAt }}
													</v-card-subtitle>

													<v-card-text>
														<v-chip class="mb-3" small :color="post.resolved ? 'success' : 'warning'" text-color="white">
															{{ post.resolved ? 'Resolved' : 'Pending' }}
														</v-chip>
														
														<v-chip class="mb-3 ml-2" small color="primary" text-color="white" v-if="post.category">
															{{ post.category }}
														</v-chip>
														
														<v-divider class="mb-3"></v-divider>
														
														<div class="content-preview">
															<strong>Report Reason: </strong>
															<p class="mt-1">{{ post.reportReason }}</p>
															<strong>Content:</strong>
															<p class="mt-1">{{ post.contentText }}</p>
														</div>
													</v-card-text>

													<v-card-actions>
														<v-spacer></v-spacer>
														<v-btn v-if="!post.isDeleted" color="error" text @click="deletePost(post, true)">
															<v-icon left>mdi-delete</v-icon>
															Delete
														</v-btn>
														<v-btn v-else color="error" text @click="deletePost(post, false)">
															<v-icon left>mdi-restore</v-icon>
															Restore
														</v-btn>
														<v-btn v-if="!post.resolved" color="primary" text @click="markAsResolved(post.reportId, true)">
															<v-icon left>mdi-check</v-icon>
															Mark Resolved
														</v-btn>
														<v-btn v-else color="primary" text @click="markAsResolved(post.reportId, false)">
															<v-icon left>mdi-undo</v-icon>
															Mark Unresolved
														</v-btn>
													</v-card-actions>
												</v-card>
											</v-col>
										</v-row>

										<v-row v-else>
												<v-col>
														<p>No pending user reports.</p>
												</v-col>
										</v-row>
									</v-container>
								</section>

								<section role="region" aria-labelledby="archived-reports-title">
									<h2 class="text-h5 font-weight-bold mb-4" id="archived-reports-title">
											Archived Reports
											 <v-chip color="success" text-color="white">{{ sortedPosts(false).length }}</v-chip>
									</h2>

									<v-container>
											<v-row v-if="sortedPosts(false).length > 0">
													<v-col v-for="post in sortedPosts(false)" :key="post.reportId" cols="12" md="6" lg="6">
															<v-card class="mb-4" elevation="2">
																<v-card-title v-if="post.reportType==='thread'" class="text-h6 primary--text">
																	{{ post.title }}
																</v-card-title>
																<v-card-title v-else class="text-h6 primary--text">
																	Reply to '{{ post.title }}'
																</v-card-title>

																<v-card-subtitle>
																	Posted by: {{ post.author }} on {{ post.reportCreatedAt }}
																</v-card-subtitle>

																<v-card-text>
																	<v-chip class="mb-3" small :color="post.resolved ? 'success' : 'warning'" text-color="white">
																		{{ post.resolved ? 'Resolved' : 'Pending' }}
																	</v-chip>
																	
																	<v-chip class="mb-3 ml-2" small color="primary" text-color="white" v-if="post.category">
																		{{ post.category }}
																	</v-chip>
																	
																	<v-divider class="mb-3"></v-divider>
																	
																	<div class="content-preview">
																		<strong>Report Reason: </strong>
																		<p class="mt-1">{{ post.reportReason }}</p>
																		<strong>Content:</strong>
																		<p class="mt-1">{{ post.contentText }}</p>
																	</div>
																</v-card-text>

																<v-card-actions>
																	<v-spacer></v-spacer>
																	<v-btn v-if="!post.isDeleted" color="error" text @click="deletePost(post, true)">
																		<v-icon left>mdi-delete</v-icon>
																		Delete
																	</v-btn>
																	<v-btn v-else color="error" text @click="deletePost(post, false)">
																		<v-icon left>mdi-restore</v-icon>
																		Restore
																	</v-btn>
																	<v-btn v-if="!post.resolved" color="primary" text @click="markAsResolved(post.reportId, true)">
																		<v-icon left>mdi-check</v-icon>
																		Mark Resolved
																	</v-btn>
																	<v-btn v-else color="primary" text @click="markAsResolved(post.reportId, false)">
																		<v-icon left>mdi-undo</v-icon>
																		Mark Unresolved
																	</v-btn>
																</v-card-actions>
															</v-card>
													</v-col>
											</v-row>
											<v-row v-else>
													<v-col>
															<p>No archived reports.</p>
													</v-col>
											</v-row>
									</v-container>
							</section>
							</v-card>
						</v-col>
					</v-row>
				</v-container>
			</main>
		</div>
	</div>
</template>

<script>
	import Navbar from "./Navbar.vue";
	import axios from 'axios';

	export default {
		name: "AdminDashboard",
		components: {
			Navbar,
		},
		data() {
			return {
				pendingChanges: [
					{
						id: 1,
						postTitle: "Kill Em' All",
						author: { name: "User3" },
						date: "February 20, 2025",
						suggestedEdit: "Updated the notes on Kill Em' All by Metallica.",
					},
				],
				sortBy: 'date',
				sortDirection: 'desc',
				loading: true,
				data: {}
			};
		},
		computed: {
			userPosts() {
				if (!this.data.reports || !this.data.content) {
					return [];
				}

				let reports = this.data.reports;
				let content = this.data.content;

				const joinedData = reports.map(report => {
					const matchingContent = content.find(item => item.id === report.item_id);

					return {
						reportId: report.id,
						reportReason: report.reason,
						reportCreatedAt: report.created_at,
						reportType: report.item_type,
						resolved: report.resolved,
						contentId: matchingContent?.id,
						title: matchingContent?.title,
						author: matchingContent?.author_name,
						category: matchingContent?.category,
						contentText: matchingContent?.content,
						isDeleted: matchingContent?.is_deleted
					};
				});

				return joinedData;
			}
		},
		created() {
			this.getReports();
		},
		methods: {
			sortedPosts(pendingOnly) {
				const userPosts = this.userPosts.filter((post) => post.resolved === !pendingOnly);

				if (!userPosts.length) return [];
				
				const sorted = [...userPosts].sort((a, b) => {
					if (this.sortBy === 'author') {
						return (a.author || '').localeCompare(b.author || '');
					} else if (this.sortBy === 'date') {
						return new Date(a.reportCreatedAt || 0) - new Date(b.reportCreatedAt || 0);
					} else if (this.sortBy === 'category') {
						return (a.category || '').localeCompare(b.category || '');
					}

					return 0;
				});

				return this.sortDirection === 'asc' ? sorted : sorted.reverse();
			},
			approveChange(changeId) {
				this.pendingChanges = this.pendingChanges.filter(
					(change) => change.id !== changeId
				);
			},
			rejectChange(changeId) {
				this.pendingChanges = this.pendingChanges.filter(
					(change) => change.id !== changeId
				);
			},
			async deletePost(report, deletedValue) {
				try {
					let path = `http://localhost:5001/admin/reports/delete-reply/${report.contentId}`;
					if (report.reportType === 'thread') {
						path = `http://localhost:5001/admin/reports/delete-thread/${report.contentId}`;
					}

					const response = await axios.put(path, {
						isDeleted: deletedValue
					}, {
						withCredentials: true
					});

					const contentIndex = this.data.content.findIndex((content) => {
						return content.id === report.contentId;
					});
					if (contentIndex !== -1) {
						this.data.content[contentIndex].is_deleted = deletedValue;
					}
				} catch (error) {
					console.error("Error deleted reported reply:", error);
				}
			},
			async markAsResolved(reportId, resolveToggle) {
				try {
					const path = `http://localhost:5001/admin/reports/resolve/${reportId}`;
					const response = await axios.put(path, {
						isResolved: resolveToggle
					}, {
						withCredentials: true
					});

					const reportIndex = this.data.reports.findIndex((report) => report.id === reportId);
					if (reportIndex !== -1) {
						const updatedReport = { ...this.data.reports[reportIndex], resolved: resolveToggle };

						this.data.reports.splice(reportIndex, 1, updatedReport);
					}
				} catch (error) {
					console.error("Error resolving report:", error);
				}
			},
			async getReports() {
				try {
					const response = await axios.get("http://localhost:5001/admin/reports", {
						withCredentials: true
					});

					this.data = response.data;
					this.loading = false;
				} catch (error) {
					console.error("Error fetching reports:", error);
					this.loading = false;

					if (error.response.status === 403) {
						this.$router.push("/unauthorized");
					}
				}
			},
			toggleSortDirection() {
				this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
			}
		},
	};
</script>

<style scoped>
	@import "../../src/assets/background.css";
</style>
