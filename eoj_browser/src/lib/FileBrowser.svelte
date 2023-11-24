<script lang="ts">
    import {
        Heading,
        Listgroup,
        type ListGroupItemType,
    } from "flowbite-svelte";

    export let selectedFile: string | null = null;

    let snapshots: ListGroupItemType[] = [];
    fetch("/list/files")
        .then((res) => res.json())
        .then((res: string[]) => {
            snapshots = res.map((e) => {
                return {
                    name: e,
                };
            });
        });

    function handleFileSelect(file) {
        selectedFile = file.detail.name;
        snapshots = snapshots.map((e) => {
            e.current = selectedFile == e.name;
            return e;
        });
    }
</script>

<div id="heading">
    <Heading tag="h3">Files</Heading>
</div>

<br />
{#if snapshots.length > 0}
    <Listgroup active items={snapshots} let:item on:click={handleFileSelect}>
        {item.name}
    </Listgroup>
{/if}

<style>
    #heading {
        margin: auto;
        width: fit-content;
    }
</style>
