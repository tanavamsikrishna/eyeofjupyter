<script lang="ts">
    import { NavBrand, Navbar, type ListGroupItemType } from "flowbite-svelte";
    import FileBrowser from "./lib/FileBrowser.svelte";
    import VersionBrowser from "./lib/VersionBrowser.svelte";

    let selectedFile: string | null = null;
</script>

<Navbar>
    <NavBrand href="/">
        <span
            class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
            >Eye of Jupyter</span
        >
    </NavBrand>
</Navbar>

<main>
    <div style="display: flex; gap: 2rem">
        <div>
            <FileBrowser bind:selectedFile></FileBrowser>
        </div>
        {#if selectedFile !== null}
            <div>
                <VersionBrowser baseFile={selectedFile} />
            </div>
        {/if}
    </div>
</main>

<style>
    main {
        width: fit-content;
        margin: auto;
        margin-top: 5rem;
    }
</style>
