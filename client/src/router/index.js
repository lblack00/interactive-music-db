import { createRouter, createWebHistory } from "vue-router";
import Release from "../components/Release.vue";
import Master from "../components/Master.vue";
import NotFound from "../components/NotFound.vue";
import NotAuthorized from "../components/NotAuthorized.vue";
import SignUp from "../components/SignUp.vue";
import Login from "../components/Login.vue";
import Home from "../components/Home.vue";
import ArtistPage from "../components/ArtistPage.vue";
import SearchResults from "../components/SearchResults.vue";
import Countdown from "../components/Countdown.vue";
import PlaylistSystem from "../components/PlaylistSystem.vue";
import Forum from "../components/Forum.vue";
import ForumThread from "../components/ForumThread.vue";
import UserProfile from "../components/UserProfile.vue";
import UserSettings from "@/components/UserSettings.vue";
import MusicList from "@/components/MusicList.vue";
import AdminDashboard from "../components/AdminDashboard.vue";

// Forum, ForumThread, Release, Master, AristPage, NotFound, NotAuthorized,
//   SignUp, Login, PlaylistSystem, and SearchResults were written by Lucas Black
// VerifyEmail, ForgotPassword, ResetPassword,
//   Home and Countdown were written by Jax Hendrickson
// UserSettings, UserProfile, MusicList were written by Matthew Stenvold
const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: "/release/:release_id",
			name: "Release",
			component: Release,
		},
		{
			path: "/master/:master_id",
			name: "Master",
			component: Master,
		},
		{
			path: "/:pathMatch(.*)*",
			name: "NotFound",
			component: NotFound,
		},
		{
			path: "/unauthorized",
			name: "NotAuthorized",
			component: NotAuthorized,
		},
		{
			path: "/",
			name: "Home",
			component: Home,
		},
		{
			path: "/signup",
			name: "SignUp",
			component: SignUp,
		},
		{
			path: "/login",
			name: "Login",
			component: Login,
		},
		{
			path: "/artist/:artist_id",
			name: "ArtistPage",
			component: ArtistPage,
		},
		{
			path: "/countdown",
			name: "Countdown",
			component: Countdown,
		},
		{
			path: "/playlist",
			name: "PlaylistSystem",
			component: PlaylistSystem,
		},
		{
			path: "/forum",
			name: "Forum",
			component: Forum,
		},
		{
			path: "/forum/thread/:thread_id",
			name: "ForumThread",
			component: ForumThread,
		},
		{
			path: "/user/:username",
			name: "UserProfile",
			component: UserProfile,
		},
    {
			path: "/user-settings",
			name: "UserSettings",
			component: UserSettings,
		},
		{
			path: "/admin",
			name: "AdminDashboard",
			component: AdminDashboard,
		},
    {
			path: "/musiclist/:username",
			name: "MusicList",
			component: MusicList,
		},
		{
			path: "/search/:query",
			name: "SearchResults",
			component: SearchResults,
			props: (route) => ({
				query: route.params.query,
				filterOption: route.query.filterOption,
				genreOption: route.query.genreOption,
			}),
		},
		{
			path: '/verify-email',
			name: 'VerifyEmail',
			component: () => import('../components/VerifyEmail.vue')
		},
		{
			path: '/forgot-password',
			name: 'ForgotPassword',
			component: () => import('../components/ForgotPassword.vue')
		},
		{
			path: '/reset-password',
			name: 'ResetPassword',
			component: () => import('../components/ResetPassword.vue'),
			props: route => ({ token: route.query.token })
		}
	],
});

export default router;
