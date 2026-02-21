<script>
	import './layout.css';
	import '$lib/highlight.js';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<div>
	<header class="bg-background sticky top-0 z-50 w-full">
		Hello app
	</header>

	<content>
		{@render children()}
	</content>
</div>

