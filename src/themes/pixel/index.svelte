<script lang="ts">
    import { format } from 'date-fns';
    import type { PageData } from '../../routes/$types';
    import { createMemoList } from '$lib/memo.svelte';
    
    let { data, config }: { data: PageData, config: any } = $props();
    const memoList = createMemoList(() => data, config);
</script>

<div class="min-h-screen bg-[#fff1e8] text-[#1d2b53] font-mono p-4 image-pixelated relative overflow-hidden">
    <!-- Background Decor -->
    <div class="fixed top-10 left-10 text-4xl opacity-20 rotate-12 pointer-events-none">☁️</div>
    <div class="fixed top-20 right-20 text-4xl opacity-20 -rotate-6 pointer-events-none">⭐</div>
    <div class="fixed bottom-20 left-20 text-4xl opacity-20 rotate-6 pointer-events-none">🍄</div>
    
    <div class="max-w-3xl mx-auto relative z-10">
        <!-- Header -->
        <header class="mb-12 text-center p-6 border-4 border-[#1d2b53] bg-[#ffec27] shadow-[8px_8px_0px_#1d2b53] rounded-sm">
            <h1 class="text-3xl md:text-5xl font-black uppercase mb-4 tracking-widest text-[#1d2b53] drop-shadow-sm flex items-center justify-center gap-4">
                <span class="animate-bounce inline-block">👾</span> {config.title} <span class="animate-bounce inline-block animation-delay-200">👾</span>
            </h1>
            
            <div class="bg-white border-2 border-[#1d2b53] p-3 inline-block rounded-sm">
                <div class="flex justify-center flex-wrap gap-4 text-xs md:text-sm font-bold uppercase">
                    <div class="flex items-center gap-1">👤 <span class="text-[#f83800]">{config.author}</span></div>
                    <div class="flex items-center gap-1">🪙 <span class="text-[#ffa300]">{data.memos.length}</span></div>
                    <div class="flex items-center gap-1">📅 <span class="text-[#29adff]">{new Date().getFullYear()}</span></div>
                </div>
            </div>
            
            {#if memoList.selectedTag}
                <div class="mt-6">
                    <button class="bg-[#ff004d] text-white border-2 border-[#1d2b53] px-4 py-2 text-xs uppercase font-bold hover:scale-105 transition-transform shadow-[4px_4px_0px_#1d2b53]" onclick={() => memoList.selectTag(null)}>
                        Key Item: #{memoList.selectedTag} <span class="ml-2">✕</span>
                    </button>
                </div>
            {/if}
        </header>

        <!-- Memos -->
        <div class="space-y-10">
            {#each Object.entries(memoList.groupedMemos) as [dateKey, memos]}
                <div>
                    <div class="inline-block bg-[#29adff] border-2 border-[#1d2b53] px-3 py-1 text-white font-bold text-sm mb-4 shadow-[4px_4px_0px_#1d2b53] -rotate-1">
                        Level {format(new Date(dateKey + 'T00:00:00'), 'MM.dd')}
                    </div>
                    
                    <div class="space-y-6">
                        {#each memos as memo}
                            <div class="flex gap-4 items-start group">
                                <div class="w-10 h-10 shrink-0 bg-white border-2 border-[#1d2b53] flex items-center justify-center text-xl shadow-[4px_4px_0px_rgba(29,43,83,0.2)] rounded-sm group-hover:-translate-y-1 transition-transform">
                                    {['🍎', '⭐', '💎', '🔑', '❤️', '🧱'][Math.floor(Math.random() * 6)]}
                                </div>
                                
                                <div class="flex-1 bg-white border-2 border-[#1d2b53] p-5 relative rounded-sm shadow-[6px_6px_0px_#c2c3c7]">
                                    <div class="absolute -top-3 right-4 bg-[#ffccaa] border-2 border-[#1d2b53] px-2 py-0.5 text-[10px] font-bold uppercase rounded-sm">
                                        TIME {format(memo.date, 'HH:mm')}
                                    </div>

                                    <div class="prose prose-sm max-w-none font-bold text-[#1d2b53]
                                        prose-headings:text-[#ff004d] prose-headings:font-black prose-a:text-[#29adff] prose-a:no-underline hover:prose-a:underline
                                        [&_img]:border-4 [&_img]:border-[#1d2b53] [&_img]:pixel-render [&_img]:rounded-sm [&_img]:shadow-[4px_4px_0px_#1d2b53]">
                                        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                                        {@html memo.content}
                                    </div>
                                    
                                    <div class="mt-4 flex flex-wrap gap-2 pt-3 border-t-2 border-dashed border-[#c2c3c7]">
                                        {#each memo.tags || [] as tag}
                                            <button 
                                                class="text-[10px] font-bold uppercase bg-[#00e436] text-[#1d2b53] border border-[#1d2b53] px-2 py-1 hover:bg-[#ffec27] transition-colors shadow-[2px_2px_0px_#1d2b53]"
                                                onclick={() => memoList.selectTag(tag)}
                                            >
                                                #{tag}
                                            </button>
                                        {/each}
                                    </div>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            {/each}
        </div>

        {#if memoList.visibleCount < data.memos.length}
            <div class="mt-16 text-center">
                <button 
                    class="bg-[#83769c] text-white border-4 border-[#1d2b53] px-8 py-3 uppercase font-black text-lg hover:bg-[#ffccaa] hover:text-[#1d2b53] transition-colors shadow-[8px_8px_0px_#1d2b53] active:translate-y-1 active:shadow-[4px_4px_0px_#1d2b53]"
                    onclick={memoList.loadMore}
                >
                    ▼ Load Next Stage
                </button>
            </div>
        {/if}

        <footer class="mt-20 text-center text-xs font-bold uppercase text-[#1d2b53]/50 pb-10">
            <p>Ready Player One • Credit 00</p>
        </footer>
    </div>
</div>

<style>
    .image-pixelated {
        image-rendering: pixelated;
    }
    :global(.pixel-render) {
        image-rendering: pixelated;
    }
    .animation-delay-200 {
        animation-delay: 200ms;
    }
</style>
