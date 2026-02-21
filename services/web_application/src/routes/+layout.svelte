<script>
	import './layout.css';
	import '$lib/highlight.js';
	import favicon from '$lib/assets/favicon.svg';
	import { ModeWatcher, toggleMode, mode } from 'mode-watcher';
	import { Button } from '$lib/components/ui/button';
	import Sun from '@lucide/svelte/icons/sun';
	import Moon from '@lucide/svelte/icons/moon';

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<ModeWatcher />

<div class="flex min-h-svh flex-col">
	<header class="bg-background border-border sticky top-0 z-50 w-full border-b">
		<div class="mx-auto flex h-14 max-w-screen-xl items-center justify-between px-4">
			<span class="text-foreground text-lg font-semibold tracking-tight">My App</span>

			<Button class="" variant="ghost" size="icon" onclick={toggleMode} aria-label="Toggle theme">
				{#if mode.current === 'dark'}
					<Sun class="size-5" />
				{:else}
					<Moon class="size-5" />
				{/if}
			</Button>
		</div>
	</header>

	<main class="flex flex-1 flex-col">
		{@render children()}
	</main>
</div>

