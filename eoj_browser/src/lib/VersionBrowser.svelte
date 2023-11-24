<script lang="ts">
    import {
        Heading,
        Listgroup,
        type ListGroupItemType,
    } from "flowbite-svelte";

    export let baseFile: string;

    let versions: ListGroupItemType[] = [];

    function fetch_versions(baseFile: string) {
        fetch(`/list/versions/${baseFile}`)
            .then((resp) => resp.json())
            .then((resp) => {
                versions = resp.map((e) => {
                    return {
                        name: e,
                        href: `snapshot/${baseFile}/${e}`,
                    };
                });
            });
    }

    $: fetch_versions(baseFile);
</script>

<div id="heading">
    <Heading tag="h3">Versions</Heading>
</div>

<br />

{#if versions.length > 0}
    <Listgroup active items={versions} let:item>
        {item.name}
    </Listgroup>
{/if}

<style>
    #heading {
        margin: auto;
        width: fit-content;
    }
</style>
