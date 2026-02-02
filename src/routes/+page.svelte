<script lang="ts">
    import type { PageData } from './$types';
    import { config } from '../../moire.config';
    import { onMount } from 'svelte';
    
    let { data }: { data: PageData } = $props();
    let ThemeComponent = $state<any>(null);

    $effect(() => {
        const theme = config.theme || 'receipt';
        // Dynamic import based on theme name
        // We need to map string to import path
        const themes: Record<string, () => Promise<any>> = {
            'receipt': () => import('$themes/receipt/index.svelte'),
            'cyberpunk': () => import('$themes/cyberpunk/index.svelte'),
            'academic': () => import('$themes/academic/index.svelte'),
            'bento': () => import('$themes/bento/index.svelte'),
            'pixel': () => import('$themes/pixel/index.svelte')
        };

        const loader = themes[theme] || themes['receipt'];
        loader().then(module => {
            ThemeComponent = module.default;
        });
    });
</script>

{#if ThemeComponent}
    <ThemeComponent {data} {config} />
{:else}
    <!-- Simple loading state to avoid flash -->
    <div class="min-h-screen flex items-center justify-center">Loading...</div>
{/if}
