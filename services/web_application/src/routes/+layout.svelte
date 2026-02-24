<script>
	import './layout.css';
	import '$lib/highlight.js';
	import favicon from '$lib/assets/favicon.svg';
	import { ModeWatcher, toggleMode, mode } from 'mode-watcher';
	import { Button } from '$lib/components/ui/button';
	import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
	import { page } from '$app/stores';
	import Sun from '@lucide/svelte/icons/sun';
	import Moon from '@lucide/svelte/icons/moon';
	import ChevronDown from '@lucide/svelte/icons/chevron-down';

	const navLinks = [
		{ href: '/', label: 'Home' },
		{ href: '/calendar', label: 'Calendar' },
		{ href: '/login-01', label: 'Login' },
		{ href: '/signup-01', label: 'Sign Up' },
		{ href: '/sidebar-09', label: 'Sidebar' },
	];

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<ModeWatcher />

<div class="flex min-h-svh flex-col">
	<header class="bg-background border-border sticky top-0 z-50 w-full border-b">
		<div class="mx-auto flex h-14 max-w-screen-xl items-center justify-between px-4">
			<div class="flex items-center gap-4">
				<span class="text-foreground text-lg font-semibold tracking-tight">My App</span>

				<DropdownMenu.Root>
					<DropdownMenu.Trigger>
						{#snippet child({ props })}
							<Button class="" variant="outline" size="sm" {...props}>
								Pages <ChevronDown class="size-4" />
							</Button>
						{/snippet}
					</DropdownMenu.Trigger>
					<DropdownMenu.Content align="start">
						{#each navLinks as link}
							<DropdownMenu.Item
								class={$page.url.pathname === link.href ? 'bg-accent' : ''}
							>
								{#snippet child({ props })}
									<a href={link.href} {...props}>{link.label}</a>
								{/snippet}
							</DropdownMenu.Item>
						{/each}
					</DropdownMenu.Content>
				</DropdownMenu.Root>
			</div>

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

