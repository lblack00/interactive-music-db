<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<header role="navigation">
		<Navbar />
	</header>

	<main role="main">
		<v-container>
			<h1 id="page-title" class="text-h4 font-weight-bold mb-4">
				Forum Overview
			</h1>

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
									>
										<v-list-item-content>
											<v-list-item-title>
												<router-link
													:to="category.link"
													:aria-label="`${category.name} category`"
													>{{ category.name }}</router-link
												>
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
							<h2 id="recent-threads-heading" class="text-h5 font-weight-bold">
								Recent Threads
							</h2>
							<v-list dense>
								<v-list-item
									v-for="thread in recentThreads"
									:key="thread.title"
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
											{{ thread.category }} - {{ thread.replies }} replies
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
</template>

<script>
	import Navbar from "./Navbar.vue";

	export default {
		name: "Forum",
		components: {
			Navbar,
		},
		data() {
			return {
				categories: [
					{ name: "General", link: "/forum/category/general" },
					{ name: "Album", link: "/forum/category/album" },
					{ name: "Song", link: "/forum/category/song" },
				],
				recentThreads: [
					{
						title: "Welcome to the Forum!",
						category: "General",
						replies: 10,
						link: "/forum/thread/1",
					},
					{
						title: "Latest Album Releases",
						category: "Album",
						replies: 25,
						link: "/forum/thread/2",
					},
					{
						title: "Song Recommendations",
						category: "Song",
						replies: 15,
						link: "/forum/thread/3",
					},
				],
			};
		},
	};
</script>
