<script lang="ts">
    import { format } from 'date-fns';
    import type { PageData } from '../../routes/$types';
    import { createMemoList } from '$lib/memo.svelte';
    
    let { data, config }: { data: PageData, config: any } = $props();
    const memoList = createMemoList(() => data, config);
</script>

<div class="min-h-screen bg-[#050505] text-[#d946ef] font-mono p-5 relative overflow-hidden selection:bg-[#d946ef] selection:text-white">
    <!-- Scanlines overlay -->
    <div class="fixed inset-0 pointer-events-none bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPgo8cmVjdCB3aWR0aD0iNCIgaGVpZ2h0PSI0IiBmaWxsPSIjMDAwIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjwvc3ZnPg==')] z-50 opacity-50"></div>
    <div class="fixed inset-0 pointer-events-none bg-gradient-to-b from-transparent via-[rgba(217,70,239,0.03)] to-transparent bg-[length:100%_4px] animate-scanline z-50"></div>
    <!-- Vignette -->
    <div class="fixed inset-0 pointer-events-none bg-[radial-gradient(circle_at_center,transparent_50%,rgba(0,0,0,0.6)_100%)] z-40"></div>

    <div class="max-w-4xl mx-auto relative z-10 border border-[#d946ef]/20 p-8 shadow-[0_0_50px_rgba(217,70,239,0.05)] bg-[#050505]/95 backdrop-blur-md">
        <header class="mb-12 border-b border-[#d946ef]/50 pb-6 relative">
             <div class="absolute -bottom-1 right-0 w-20 h-1 bg-[#d946ef] shadow-[0_0_10px_#d946ef]"></div>

            <div class="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
                <div>
                    <h1 class="text-4xl md:text-6xl font-black tracking-tighter uppercase glitch text-white drop-shadow-[0_0_5px_rgba(217,70,239,0.8)]" data-text={config.title}>{config.title}</h1>
                    <p class="text-sm mt-3 text-[#d946ef] font-bold tracking-widest">SYSTEM_READY // {config.description}</p>
                </div>
                <div class="text-right text-[10px] text-[#a855f7] font-bold tracking-widest">
                    <p>USR: {config.author}</p>
                    <p>NET: SECURE</p>
                </div>
            </div>
            
            {#if memoList.selectedTag}
                <div class="mt-8 flex items-center gap-2 text-sm">
                    <span class="animate-pulse text-[#d946ef]">▋</span> FILTER_MODE: 
                    <button class="bg-[#d946ef] text-black px-3 py-1 hover:bg-white transition-colors font-bold uppercase tracking-wider" onclick={() => memoList.selectTag(null)}>
                        #{memoList.selectedTag} [RESET]
                    </button>
                </div>
            {/if}
        </header>

        <div class="space-y-16">
            {#each Object.entries(memoList.groupedMemos) as [dateKey, memos]}
                <div class="relative pl-8 border-l border-[#d946ef]/20">
                    <div class="absolute -left-[5px] top-0 w-2.5 h-2.5 bg-[#d946ef] shadow-[0_0_15px_#d946ef] rotate-45"></div>
                    <h2 class="text-2xl mb-8 font-black flex items-center gap-4 text-white uppercase tracking-widest">
                        <span class="opacity-30 text-[#d946ef]">0x</span>{dateKey}
                        <span class="h-px bg-gradient-to-r from-[#d946ef]/50 to-transparent flex-1"></span>
                    </h2>
                    
                    <div class="space-y-10">
                        {#each memos as memo}
                            <div class="group relative bg-[#0a0a0a] border border-[#d946ef]/10 p-6 hover:border-[#d946ef]/80 hover:bg-[#0f0f0f] hover:shadow-[0_0_30px_rgba(217,70,239,0.1)] transition-all duration-300">
                                <div class="absolute top-0 right-0 p-2 opacity-30 group-hover:opacity-100 transition-opacity">
                                    <div class="w-2 h-2 bg-[#d946ef] rounded-full animate-ping"></div>
                                </div>
                                
                                <div class="flex items-center gap-3 mb-4 text-xs font-bold text-[#a855f7] tracking-wider border-b border-[#d946ef]/10 pb-2">
                                    <span>[{format(memo.date, 'HH:mm:ss')}]</span>
                                    <span class="opacity-50">//{memo.slug.slice(-4)}</span>
                                </div>
                                
                                <div class="prose prose-invert prose-p:text-[#e9d5ff] prose-headings:text-white prose-a:text-[#d946ef] prose-strong:text-[#d946ef] max-w-none 
                                    [&_img]:border [&_img]:border-[#d946ef]/50 [&_img]:grayscale-[0.5] [&_img]:contrast-125 [&_img]:brightness-110
                                    [&_a]:decoration-[#d946ef] [&_a:hover]:bg-[#d946ef] [&_a:hover]:text-black">
                                    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                                    {@html memo.content}
                                </div>

                                <div class="mt-6 pt-4 border-t border-[#d946ef]/10 flex flex-wrap gap-2">
                                    {#each memo.tags || [] as tag}
                                        <button 
                                            class="text-[10px] text-[#d946ef] opacity-70 hover:opacity-100 hover:text-white hover:bg-[#d946ef]/20 px-2 py-1 transition-all uppercase tracking-wider border border-transparent hover:border-[#d946ef]/50"
                                            onclick={() => memoList.selectTag(tag)}
                                        >
                                            #{tag}
                                        </button>
                                    {/each}
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
                    class="border border-[#d946ef] text-[#d946ef] px-8 py-4 hover:bg-[#d946ef] hover:text-black transition-all duration-300 uppercase tracking-[0.2em] text-xs font-bold shadow-[0_0_20px_rgba(217,70,239,0.2)] hover:shadow-[0_0_40px_rgba(217,70,239,0.5)]"
                    onclick={memoList.loadMore}
                >
                    Initialize_Next_Sector()
                </button>
            </div>
        {/if}

        <footer class="mt-20 text-center text-[10px] text-[#a855f7]/50 border-t border-[#d946ef]/20 pt-8 pb-4 uppercase tracking-widest">
            <p>TERMINAL_SESSION_END // DISCONNECTED</p>
        </footer>
    </div>
</div>

<style>
    @keyframes scanline {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100%); }
    }
    .animate-scanline {
        animation: scanline 6s linear infinite;
    }
    .glitch {
        position: relative;
    }
    .glitch::before, .glitch::after {
        content: attr(data-text);
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #050505;
        opacity: 0.8;
    }
    .glitch::before {
        left: 2px;
        text-shadow: -1px 0 #00ffff;
        clip: rect(44px, 450px, 56px, 0);
        animation: glitch-anim 4s infinite linear alternate-reverse;
    }
    .glitch::after {
        left: -2px;
        text-shadow: -1px 0 #ff00ff;
        clip: rect(44px, 450px, 56px, 0);
        animation: glitch-anim2 4s infinite linear alternate-reverse;
    }
    @keyframes glitch-anim {
        0% { clip: rect(11px, 9999px, 86px, 0); }
        20% { clip: rect(62px, 9999px, 51px, 0); }
        40% { clip: rect(21px, 9999px, 14px, 0); }
        60% { clip: rect(98px, 9999px, 35px, 0); }
        80% { clip: rect(1px, 9999px, 66px, 0); }
        100% { clip: rect(81px, 9999px, 83px, 0); }
    }
    @keyframes glitch-anim2 {
        0% { clip: rect(69px, 9999px, 5px, 0); }
        20% { clip: rect(63px, 9999px, 45px, 0); }
        40% { clip: rect(96px, 9999px, 9px, 0); }
        60% { clip: rect(31px, 9999px, 77px, 0); }
        80% { clip: rect(45px, 9999px, 37px, 0); }
        100% { clip: rect(5px, 9999px, 66px, 0); }
    }
</style>
