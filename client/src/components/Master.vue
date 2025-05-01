<!-- This file was written by Lucas Black -->
<!--ARIA Landmarks added by Chantelle Cabanilla-->
<template>
	<div class="grid-container">
		<header role="navigation">
			<Navbar />
		</header>
		<div class="content">
			<main role="main">
				<!-- Hero Section with Blurred Background -->
				<div
					class="album-hero-vibrant"
					:style="image_uri ? { backgroundImage: `url('${image_uri}')` } : {}"
				>
					<div class="album-hero-gradient-vibrant"></div>
					<div class="album-info-float-glass">
						<v-img
							:src="image_uri || '/images/UnknownSong.png'"
							width="160"
							height="160"
							class="album-cover-float-glass"
							contain
							alt="Image of master cover"
						/>
						<div class="album-info-card-glass">
							<h1 class="album-title-glass">
								<router-link
									v-if="data.artist?.[0]"
									:to="`/artist/${data.artist[0].artist_id}`"
									:aria-label="`Artist: ${data.artist[0].artist_name}`"
									class="artist-link-glass"
								>
									{{ data.artist[0].artist_name }}
								</router-link>
								- {{ data.master?.[0]?.title }}
							</h1>
							<div class="album-chips">
								<span class="album-chip">{{
									data.release?.[0]?.country || "Unknown"
								}}</span>
								<span class="album-chip">{{
									data.master?.[0]?.year || "Unknown"
								}}</span>
								<span class="album-chip">{{
									data.genre?.map((entry) => entry.genre).join(", ") ||
									"Unknown"
								}}</span>
								<span class="album-chip">{{
									data.style?.map((entry) => entry.style).join(", ") ||
									"Unknown"
								}}</span>
							</div>
							<RatingSystem
								itemType="master"
								:itemId="$route.params.master_id"
							/>
						</div>
					</div>
				</div>

				<!-- Main Content Card -->
				<div class="main-content-card-modern">
					<!-- Tracklist Section -->
					<section v-if="data.tracks?.length">
						<div class="section-card-modern">
							<h2 class="section-title-modern">Tracklist</h2>
							<hr />
							<table
								class="table tracklist-table-modern"
								aria-label="Album tracks"
							>
								<thead>
									<tr>
										<th scope="col">#</th>
										<th scope="col">Title</th>
										<th scope="col">Duration</th>
									</tr>
								</thead>
								<tbody>
									<tr
										v-for="(track, index) in data.tracks"
										:key="index"
										class="track-row-modern"
									>
										<td>{{ index + 1 }}</td>
										<td>{{ track.title }}</td>
										<td>{{ track.duration || "--:--" }}</td>
									</tr>
								</tbody>
							</table>
						</div>
					</section>

					<!-- Notes Section -->
					<section v-if="data.release?.[0]?.notes">
						<div class="section-card-modern">
							<h2 class="section-title-modern">Notes</h2>
							<hr />
							<pre class="notes-pre-modern">{{ data.release[0].notes }}</pre>
						</div>
					</section>

					<!-- Credits Section -->
					<section v-if="hasCredits" class="credits-section">
						<div class="section-card-modern">
							<h2 class="section-title-modern">Credits</h2>
							<hr />
							<div class="credits-content-modern">
								<p
									v-for="(artists, role) in groupedByRole"
									:key="role"
									class="credit-line-modern"
								>
									<span class="credit-role-modern">{{ role }}</span>
									<span class="credit-artists-modern">{{
										artists.join(", ")
									}}</span>
								</p>
							</div>
						</div>
					</section>

					<!-- Companies Section -->
					<section v-if="data.company?.length" class="company-section">
						<div class="section-card-modern">
							<h2 class="section-title-modern">Companies</h2>
							<hr />
							<div class="company-content-modern">
								<p
									v-for="(company_name, entity_type) in filteredCompanies"
									:key="entity_type"
									class="company-line-modern"
								>
									<span class="company-type-modern">{{ entity_type }}</span>
									<span class="company-names-modern">{{
										company_name.join(", ")
									}}</span>
								</p>
							</div>
						</div>
					</section>
				</div>

				<div
					v-if="loading"
					class="container mt-2"
					role="status"
					aria-live="polite"
				>
					<div class="loading">Loading...</div>
				</div>
			</main>
		</div>
	</div>
</template>

<script>
	import axios from "axios";
	import Navbar from "./Navbar.vue";
	import RatingSystem from "./RatingSystem.vue";

	export default {
		name: "Master",
		components: {
			Navbar,
			RatingSystem,
		},
		data() {
			return {
				data: {
					master: [],
					artist: [],
					release: [],
					tracks: [],
					genre: [],
					style: [],
					artist_credits: {
						artist: [],
						track_artist: [],
					},
					company: [],
				},
				image_uri: "",
				loading: true,
			};
		},
		computed: {
			filteredCompanies() {
				const companyGroups = {};

				this.data.company.forEach((company) => {
					const name = company.company_name || "Unknown Company";
					const entity_type = company.entity_type_name || "Unknown Entity";

					if (!companyGroups[entity_type]) {
						companyGroups[entity_type] = [];
					}
					if (companyGroups[entity_type] && entity_type !== "Unknown Entity") {
						companyGroups[entity_type] = [];

						if (
							!companyGroups[entity_type].includes(name) &&
							name !== "Unknown Company"
						) {
							companyGroups[entity_type].push(name);
						}
					}
				});

				return companyGroups;
			},
			hasCredits() {
				const allCredits = [
					...(this.data.artist_credits?.artist || []),
					...(this.data.artist_credits?.track_artist || []),
				];

				return allCredits.some(
					(credit) => credit.role && credit.role !== "Unknown Role"
				);
			},
			groupedByRole() {
				const allCredits = [
					...(this.data.artist_credits?.artist || []),
					...(this.data.artist_credits?.track_artist || []),
				];

				const roleGroups = {};

				allCredits.forEach((credit) => {
					const role = credit.role || "Unknown Role";
					const artistName = credit.artist_name;

					if (!role || role === "Unknown Role") {
						return;
					}

					if (!roleGroups[role]) {
						roleGroups[role] = [];
					}

					if (!roleGroups[role].includes(artistName)) {
						roleGroups[role].push(artistName);
					}
				});

				for (const role in roleGroups) {
					roleGroups[role].sort();
				}

				const orderedRoles = {};
				Object.keys(roleGroups)
					.sort()
					.forEach((role) => {
						orderedRoles[role] = roleGroups[role];
					});

				return orderedRoles;
			},
		},
		methods: {
			async getMaster() {
				try {
					const response = await axios.get("http://localhost:5001/master/", {
						params: { master_id: this.$route.params.master_id },
					});
					this.data = response.data.payload;

					if (this.data.api_data.images && this.data.api_data.images.length) {
						this.image_uri = this.data.api_data.images[0].uri;
						this.image_uri =
							this.image_uri === ""
								? "/images/UnknownSong.png"
								: this.image_uri;

						console.log(this.image_uri, this.data.api_data);
					} else {
						this.image_uri = "/images/UnknownSong.png";
					}

					this.loading = false;
				} catch (error) {
					console.error("Error fetching master:", error);
					this.loading = false;
				}
			},
		},
		created() {
			this.getMaster();
		},
	};
</script>

<style scoped>
	@import "../../src/assets/master.css";
	@import "../../src/assets/background.css";

	.album-hero-vibrant {
		position: relative;
		min-height: 340px;
		background-size: cover;
		background-position: center;
		margin-bottom: 32px;
		max-width: 1250px;
		margin-left: auto;
		margin-right: auto;
		border-radius: 28px;
		overflow: hidden;
	}
	.album-hero-gradient-vibrant {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: linear-gradient(120deg, #3cba92 0%, #2c7a7b 100%);
		opacity: 0.82;
		z-index: 1;
	}
	.album-info-float-glass {
		position: relative;
		z-index: 2;
		display: flex;
		align-items: center;
		gap: 36px;
		justify-content: flex-start;
		margin-top: 56px;
		padding: 48px;
	}
	.album-cover-float-glass {
		background: transparent;
		width: 300px;
		height: 300px;
		object-fit: cover;
		flex-shrink: 0;
		margin-bottom: 50px;
		border-radius: 12px;
	}
	.album-info-card-glass {
		background: rgba(255, 255, 255, 0.68);
		backdrop-filter: blur(10px);
		border-radius: 22px;
		box-shadow: 0 4px 24px rgba(44, 122, 123, 0.13);
		padding: 32px 36px;
		color: #1e283c;
		max-width: 520px;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: left;
		height: auto;
	}
	.album-title-glass {
		font-size: 2.3rem;
		font-weight: bold;
		margin-bottom: 10px;
		line-height: 1.2;
		color: #2c7a7b;
	}
	.artist-link-glass {
		color: #3cba92;
		text-decoration: underline;
		transition: color 0.2s;
	}
	.artist-link-glass:hover {
		color: #2c7a7b;
	}
	.album-chips {
		display: flex;
		flex-wrap: wrap;
		gap: 10px;
		margin: 12px 0 0 0;
	}
	.album-chip {
		display: inline-flex;
		align-items: center;
		background: #f7f9fa;
		color: #2c7a7b;
		border-radius: 16px;
		padding: 4px 14px;
		font-size: 1rem;
		font-weight: 500;
		box-shadow: 0 1px 4px rgba(44, 122, 123, 0.04);
		border: 1.5px solid #2c7a7b22;
	}
	.main-content-card-modern {
		background: #fff;
		border-radius: 28px;
		box-shadow: 0 6px 32px rgba(44, 122, 123, 0.1);
		padding: 48px 36px;
		margin: 70px auto 36px auto;
		max-width: 1100px;
		color: #1e283c;
	}
	.section-card-modern {
		background: #f7f9fa;
		border-radius: 18px;
		box-shadow: 0 2px 12px rgba(44, 122, 123, 0.06);
		padding: 32px 24px;
		margin-bottom: 36px;
	}
	.section-title-modern {
		color: #2c7a7b;
		font-size: 1.6rem;
		font-weight: 700;
		margin-bottom: 14px;
		margin-top: 0;
		letter-spacing: 0.5px;
	}
	hr {
		border: none;
		border-top: 2px solid #e0e0e0;
		margin: 18px 0 26px 0;
	}
	.tracklist-table-modern {
		width: 100%;
		border-radius: 14px;
		overflow: hidden;
		background: #fff;
		box-shadow: none;
	}
	.track-row-modern {
		transition: background 0.2s;
		cursor: pointer;
	}
	.track-row-modern:hover {
		background: #e6f7f3;
	}
	.notes-pre-modern {
		background: #fff;
		border-radius: 10px;
		padding: 18px;
		color: #1e283c;
		font-size: 1.05rem;
		white-space: pre-wrap;
		margin-bottom: 0;
		box-shadow: 0 1px 4px rgba(44, 122, 123, 0.04);
	}
	.credits-content-modern,
	.company-content-modern {
		margin-left: 10px;
	}
	.credit-line-modern,
	.company-line-modern {
		margin: 10px 0;
		display: flex;
		gap: 10px;
		align-items: center;
	}
	.credit-role-modern {
		background: #3cba92;
		color: #fff;
		border-radius: 10px;
		padding: 3px 12px;
		font-size: 1rem;
		font-weight: 500;
		margin-right: 10px;
	}
	.credit-artists-modern {
		color: #2c7a7b;
	}
	.company-type-modern {
		background: #2c7a7b;
		color: #fff;
		border-radius: 10px;
		padding: 3px 12px;
		font-size: 1rem;
		font-weight: 500;
		margin-right: 10px;
	}
	.company-names-modern {
		color: #2c7a7b;
	}
	.loading {
		text-align: center;
		font-size: 1.5rem;
		color: #3cba92;
		margin-top: 80px;
	}
	@media (max-width: 900px) {
		.album-info-float-glass {
			flex-direction: column;
			align-items: center;
			padding: 0 8px;
			gap: 16px;
			margin-top: 16px;
		}
		.album-info-card-glass {
			padding: 16px 8px;
			margin-left: 0;
			max-width: 100%;
			align-items: center;
			text-align: center;
		}
	}

	/* High contrast mode styles */
	.high-contrast .album-hero-vibrant,
	.high-contrast .album-hero-gradient-vibrant,
	.high-contrast .album-info-card-glass,
	.high-contrast .main-content-card-modern,
	.high-contrast .section-card-modern,
	.high-contrast .notes-pre-modern {
		background: #000 !important;
		color: #fff !important;
		border: 2px solid #fff !important;
		box-shadow: none !important;
		backdrop-filter: none !important;
	}

	.high-contrast .album-title-glass,
	.high-contrast .section-title-modern,
	.high-contrast .credit-role-modern,
	.high-contrast .company-type-modern,
	.high-contrast .credit-artists-modern,
	.high-contrast .company-names-modern,
	.high-contrast .loading {
		color: #fff !important;
	}

	.high-contrast .album-chip {
		background: #000 !important;
		color: #fff !important;
		border: 2px solid #fff !important;
		box-shadow: none !important;
	}

	.high-contrast .track-row-modern {
		background: #000 !important;
		color: #fff !important;
	}

	.high-contrast .track-row-modern:hover {
		background: #222 !important;
	}

	.high-contrast table,
	.high-contrast th,
	.high-contrast td {
		background: #000 !important;
		color: #fff !important;
		border-color: #fff !important;
	}

	.high-contrast hr {
		border-top: 2px solid #fff !important;
	}

	/* Dark mode styles */
	.dark-mode .album-hero-gradient-vibrant {
		background: linear-gradient(120deg, #2d2d2d 0%, #363636 100%);
		opacity: 0.92;
	}

	.dark-mode .album-info-card-glass {
		background: rgba(45, 45, 45, 0.95);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
		color: rgba(255, 255, 255, 0.9);
	}

	.dark-mode .album-title-glass {
		color: #3cba92;
	}

	.dark-mode .artist-link-glass {
		color: #4fd1a5;
	}

	.dark-mode .artist-link-glass:hover {
		color: #3cba92;
	}

	.dark-mode .album-chip {
		background: #363636;
		color: #3cba92;
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
	}

	.dark-mode .main-content-card-modern {
		background: #2d2d2d;
		box-shadow: 0 6px 32px rgba(0, 0, 0, 0.2);
		border: 1px solid rgba(255, 255, 255, 0.1);
		color: rgba(255, 255, 255, 0.9);
	}

	.dark-mode .section-card-modern {
		background: #363636;
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
	}

	.dark-mode .section-title-modern {
		color: #3cba92;
	}

	.dark-mode hr {
		border-top: 2px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .tracklist-table-modern {
		background: #2d2d2d;
		color: rgba(255, 255, 255, 0.9);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .tracklist-table-modern thead {
		background: #363636;
	}

	.dark-mode .tracklist-table-modern th {
		color: rgba(255, 255, 255, 0.9);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		background: #363636;
	}

	.dark-mode .tracklist-table-modern td {
		color: rgba(255, 255, 255, 0.9);
		border-bottom: 1px solid rgba(255, 255, 255, 0.05);
		background: #2d2d2d;
	}

	.dark-mode .track-row-modern {
		background: #2d2d2d;
	}

	.dark-mode .track-row-modern:hover {
		background: #404040;
	}

	.dark-mode .track-row-modern td {
		border-color: rgba(255, 255, 255, 0.1);
	}

	.dark-mode .notes-pre-modern {
		background: #2d2d2d;
		color: rgba(255, 255, 255, 0.9);
		border: 1px solid rgba(255, 255, 255, 0.1);
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
	}

	.dark-mode .credit-role-modern {
		background: #363636;
		color: #3cba92;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .credit-artists-modern {
		color: rgba(255, 255, 255, 0.9);
	}

	.dark-mode .company-type-modern {
		background: #363636;
		color: #3cba92;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.dark-mode .company-names-modern {
		color: rgba(255, 255, 255, 0.9);
	}

	.dark-mode .loading {
		color: #3cba92;
	}

	.dark-mode table,
	.dark-mode th,
	.dark-mode td {
		color: rgba(255, 255, 255, 0.9);
		border-color: rgba(255, 255, 255, 0.1);
	}
</style>
