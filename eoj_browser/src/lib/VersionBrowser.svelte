<script lang="ts">
    import {
        Checkbox,
        Heading,
        Listgroup,
        ListgroupItem,
        Popover,
        Button,
        ButtonGroup,
    } from "flowbite-svelte";

    import { TrashBinOutline } from "flowbite-svelte-icons";

    import FileDiffIcon from "./assets/images/icons8-compare-files-32.png";

    export let baseFile: string;

    interface FileVersionDetails {
        file_name: string;
        href: string;
        comment?: string;
        checked: boolean;
    }

    let versions: FileVersionDetails[] = [];

    function fetch_versions(baseFile: string) {
        fetch(`/list/versions/${baseFile}`)
            .then((resp) => resp.json())
            .then((resp) => {
                versions = resp.map((e) => {
                    return {
                        file_name: e.file_name,
                        href: `snapshot/${baseFile}/${e.file_name}`,
                        comment: e.comment,
                        checked: false,
                    };
                });
            });
    }

    $: fetch_versions(baseFile);
</script>

<div style="margin: auto; width: fit-content">
    <ButtonGroup>
        <Button><TrashBinOutline size="xs" /></Button>
        <Button
            ><img
                alt="file diff"
                src={FileDiffIcon}
                style="height: 12px; width: 12px;"
            /></Button
        >
    </ButtonGroup>
</div>

<div id="heading">
    <Heading tag="h3">Versions</Heading>
</div>

<br />

{#if versions.length > 0}
    <Listgroup active>
        {#each versions as version}
            <ListgroupItem href={version.href}>
                <div style="display: flex;">
                    <Checkbox bind:checked={version.checked} />
                    {new Date(parseFloat(version.file_name) * 1000)}
                </div>
            </ListgroupItem>
            {#if version.comment}
                <Popover placement="left">
                    <div style="max-width: 20rem;">
                        {version.comment}
                    </div>
                </Popover>
            {/if}
        {/each}
    </Listgroup>
{/if}

<style>
    #heading {
        margin: auto;
        width: fit-content;
    }
</style>
