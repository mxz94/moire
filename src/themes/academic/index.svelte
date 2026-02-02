<script lang="ts">
    import { format } from 'date-fns';
    import type { PageData } from '../../routes/$types';
    import { createMemoList } from '$lib/memo.svelte';
    
    let { data, config }: { data: PageData, config: any } = $props();
    const memoList = createMemoList(() => data, config);
</script>

<div class="min-h-screen bg-[#fdf6e3] text-[#333] font-serif p-5 md:p-10">
    <!-- Paper texture -->
    <div class="fixed inset-0 pointer-events-none opacity-40 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiB2aWV3Qm94PSIwIDAgMTAwIDEwMCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iI2ZmZiIvPjxmaWx0ZXIgaWQ9Im4iPjxmZVR1cmJ1bGVuY2UgdHlwZT0iZnJhY3RhbE5vaXNlIiBiYXNlRnJlcXVlbmN5PSIwLjUiIG51bU9jdGF2ZXM9IjUiIHN0aXRjaFRpbGVzPSJzdGl0Y2giLz48L2ZpbHRlcj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWx0ZXI9InVybCgjbikiIG9wYWNpdHk9IjAuMSIvPjwvc3ZnPg==')] z-0"></div>

    <div class="max-w-6xl mx-auto relative z-10 grid grid-cols-1 md:grid-cols-12 gap-12">
        <!-- Sidebar / Sidenotes -->
        <aside class="md:col-span-3 md:border-r border-[#333]/10 md:pr-8 md:text-right">
            <header class="sticky top-10">
                <h1 class="text-3xl font-serif font-bold italic mb-4 text-[#d33682]">{config.title}</h1>
                <div class="text-sm text-[#666] italic mb-8">
                    <p>{config.description}</p>
                    <p class="mt-4">— {config.author}</p>
                </div>
                
                {#if memoList.selectedTag}
                    <div class="mb-8">
                        <p class="text-xs font-bold uppercase tracking-wider text-[#999] mb-2">Filtered View</p>
                        <button class="bg-[#d33682]/10 text-[#d33682] px-3 py-1 rounded-full text-sm italic hover:bg-[#d33682]/20 transition-colors" onclick={() => memoList.selectTag(null)}>
                            #{memoList.selectedTag} ✕
                        </button>
                    </div>
                {/if}

                <div class="hidden md:block">
                    <p class="text-xs font-bold uppercase tracking-wider text-[#999] mb-4">Index</p>
                    <ul class="text-sm space-y-2">
                        {#each memoList.allTags as tag}
                            <li>
                                <button class="hover:text-[#d33682] hover:underline decoration-[#d33682]/30 underline-offset-4 transition-colors {memoList.selectedTag === tag ? 'text-[#d33682] font-bold' : 'text-[#666]'}" onclick={() => memoList.selectTag(tag)}>
                                    #{tag}
                                </button>
                            </li>
                        {/each}
                    </ul>
                </div>
            </header>
        </aside>

        <!-- Main Content (Manuscript) -->
        <main class="md:col-span-9 space-y-16 max-w-2xl">
            {#each Object.entries(memoList.groupedMemos) as [dateKey, memos]}
                <section>
                    <div class="flex items-baseline gap-4 mb-8 border-b border-[#333]/10 pb-2">
                        <h2 class="text-2xl font-bold italic text-[#333]">{format(new Date(dateKey + 'T00:00:00'), 'MMMM dd, yyyy')}</h2>
                        <span class="text-sm text-[#999] italic">{format(new Date(dateKey + 'T00:00:00'), 'EEEE')}</span>
                    </div>
                    
                    <div class="space-y-12">
                        {#each memos as memo}
                            <article class="group relative">
                                <!-- Marginalia / Sidenote for time -->
                                <div class="absolute -left-16 top-1 hidden xl:block text-xs font-mono text-[#999] w-12 text-right">
                                    {format(memo.date, 'HH:mm')}
                                </div>

                                <div class="xl:hidden text-xs font-mono text-[#999] mb-2">
                                    {format(memo.date, 'HH:mm')}
                                </div>

                                <div class="prose prose-stone prose-lg max-w-none 
                                    text-[#333] font-serif leading-relaxed
                                    prose-p:mb-4 prose-headings:font-normal prose-headings:italic prose-a:text-[#d33682] prose-a:no-underline prose-a:border-b prose-a:border-[#d33682]/30 hover:prose-a:border-[#d33682] hover:prose-a:bg-[#d33682]/5
                                    prose-blockquote:border-l-2 prose-blockquote:border-[#d33682] prose-blockquote:bg-[#f9f2f4] prose-blockquote:py-1 prose-blockquote:px-4 prose-blockquote:not-italic prose-blockquote:text-sm prose-blockquote:text-[#555]
                                    [&_img]:shadow-lg [&_img]:rounded-sm [&_img]:border-[4px] [&_img]:border-white [&_img]:rotate-1 group-hover:[&_img]:rotate-0 [&_img]:transition-transform [&_img]:duration-500">
                                    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                                    {@html memo.content}
                                </div>

                                <div class="mt-4 flex flex-wrap gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                                    {#each memo.tags || [] as tag}
                                        <button 
                                            class="text-xs text-[#999] hover:text-[#d33682] hover:underline"
                                            onclick={() => memoList.selectTag(tag)}
                                        >
                                            #{tag}
                                        </button>
                                    {/each}
                                </div>
                            </article>
                        {/each}
                    </div>
                </section>
            {/each}

            {#if memoList.visibleCount < data.memos.length}
                <div class="pt-12 text-center border-t border-[#333]/10">
                    <button 
                        class="text-lg italic text-[#666] hover:text-[#d33682] transition-colors"
                        onclick={memoList.loadMore}
                    >
                        ❧ Continue Reading...
                    </button>
                </div>
            {/if}

            <footer class="mt-20 text-center text-sm text-[#999] italic pb-12">
                <p>— End of Manuscript —</p>
            </footer>
        </main>
    </div>
</div>

<style>
    /* Custom refined typography overrides */
    :global(body) {
        font-variant-ligatures: common-ligatures;
    }
</style>
