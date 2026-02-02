<script lang="ts">
    import { format } from 'date-fns';
    import type { PageData } from '../../routes/$types';
    import { createMemoList } from '$lib/memo.svelte';
    
    let { data, config }: { data: PageData, config: any } = $props();
    const memoList = createMemoList(() => data, config);
</script>

<div class="min-h-screen bg-[#f5f5f7] text-gray-900 font-sans p-5 md:p-10">
    <div class="max-w-2xl mx-auto space-y-8">
        <!-- Header Card -->
        <header class="bg-white rounded-3xl p-8 shadow-sm border border-gray-100 flex flex-col items-center text-center">
            <div class="w-20 h-20 bg-gray-100 rounded-full mb-6 overflow-hidden">
                 <!-- Avatar Placeholder -->
                 <div class="w-full h-full flex items-center justify-center text-2xl font-bold text-gray-400">
                    {config.author[0]}
                 </div>
            </div>
            <h1 class="text-2xl font-bold tracking-tight mb-2">{config.title}</h1>
            <p class="text-sm text-gray-500 max-w-sm">{config.description}</p>
            
            {#if memoList.selectedTag}
                <button class="mt-6 bg-black text-white px-4 py-2 rounded-full text-xs font-medium hover:scale-105 transition-transform" onclick={() => memoList.selectTag(null)}>
                    Filtering by #{memoList.selectedTag} <span class="opacity-50 ml-1">✕</span>
                </button>
            {/if}
        </header>

        <!-- Bento Grid / Stream -->
        <div class="grid grid-cols-1 gap-6">
            {#each Object.entries(memoList.groupedMemos) as [dateKey, memos]}
                <div class="flex items-center gap-4 py-4">
                    <span class="h-px flex-1 bg-gray-200"></span>
                    <span class="text-xs font-semibold text-gray-400 uppercase tracking-widest">{format(new Date(dateKey + 'T00:00:00'), 'MMMM dd')}</span>
                    <span class="h-px flex-1 bg-gray-200"></span>
                </div>
                
                {#each memos as memo}
                    <article class="bg-white rounded-3xl p-6 shadow-[0_2px_20px_rgba(0,0,0,0.04)] border border-gray-100 hover:shadow-[0_8px_30px_rgba(0,0,0,0.06)] transition-shadow duration-300">
                        <div class="flex justify-between items-center mb-4">
                            <span class="text-xs font-medium text-gray-400">{format(memo.date, 'HH:mm')}</span>
                            <div class="flex gap-2">
                                {#each memo.tags || [] as tag}
                                    <button 
                                        class="text-[10px] font-bold uppercase tracking-wider text-gray-400 hover:text-black transition-colors bg-gray-50 px-2 py-1 rounded-md"
                                        onclick={() => memoList.selectTag(tag)}
                                    >
                                        #{tag}
                                    </button>
                                {/each}
                            </div>
                        </div>

                        <div class="prose prose-neutral prose-sm max-w-none 
                            prose-p:text-gray-600 prose-headings:text-gray-900 prose-a:text-blue-600 prose-a:no-underline hover:prose-a:underline
                            prose-img:rounded-2xl prose-img:shadow-sm prose-img:my-4 prose-img:w-full
                            [&_p]:leading-relaxed">
                            <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                            {@html memo.content}
                        </div>
                    </article>
                {/each}
            {/each}
        </div>

        {#if memoList.visibleCount < data.memos.length}
            <div class="text-center pt-8">
                <button 
                    class="bg-white border border-gray-200 text-gray-600 py-3 px-8 rounded-full text-sm font-medium shadow-sm hover:shadow-md hover:border-gray-300 hover:text-black transition-all"
                    onclick={memoList.loadMore}
                >
                    Load More
                </button>
            </div>
        {/if}

        <footer class="text-center py-12 text-xs text-gray-400">
            <p>&copy; {new Date().getFullYear()} {config.author}. All rights reserved.</p>
        </footer>
    </div>
</div>
