<script lang="ts">
    import {
        Checkbox,
        Heading,
        Listgroup,
        ListgroupItem,
        Popover,
        Button,
        ButtonGroup,
        Modal,
    } from "flowbite-svelte";

    import dayjs from "dayjs";
    import localizedFormat from "dayjs/plugin/localizedFormat";
    dayjs.extend(localizedFormat);

    export let baseFile: string;

    let askDeleteConfirmation = false;

    interface FileVersionDetails {
        file_name: string;
        href: string;
        comment?: string;
        checked: boolean;
    }

    var diffDisabled = false;
    var deleteDisabled = false;
    var numberOfCheckboxesChecked = 0;

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
        numberOfCheckboxesChecked = 0;
    }

    function checkBoxChange() {
        numberOfCheckboxesChecked = versions.filter((e) => e.checked).length;
    }

    function handleDelete() {
        const versionsToDelete = versions
            .filter((e) => e.checked)
            .map((e) => e.file_name);
        fetch(`/delete`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                baseFile: baseFile,
                versions: versionsToDelete,
            }),
        }).then(() => {
            versions = versions.filter((e) => !e.checked);
        });
    }

    const handleDiff = async () => {
        const versionsToDiff = versions
            .filter((e) => e.checked)
            .sort((a, b) => parseFloat(a.file_name) - parseFloat(b.file_name));
        await fetch(`/diff`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                baseFile: baseFile,
                first: versionsToDiff[0].file_name,
                second: versionsToDiff[1].file_name,
            }),
        });
    };

    $: fetch_versions(baseFile);
    $: deleteDisabled = numberOfCheckboxesChecked == 0;
    $: diffDisabled = numberOfCheckboxesChecked != 2;
</script>

<div style="margin: auto; width: fit-content">
    <ButtonGroup>
        <Button
            size="xs"
            pill="true"
            disabled={deleteDisabled}
            on:click={() => {
                askDeleteConfirmation = true;
            }}>Delete</Button
        >
        <Button
            size="xs"
            pill="true"
            disabled={diffDisabled}
            on:click={handleDiff}>Diff</Button
        >
    </ButtonGroup>
</div>

<br />

<div id="heading">
    <Heading tag="h3">Versions</Heading>
</div>

<br />

{#if versions.length > 0}
    <Listgroup active>
        {#each versions as version}
            <ListgroupItem href={version.href}>
                <div style="display: flex;">
                    <Checkbox
                        bind:checked={version.checked}
                        on:change={checkBoxChange}
                    />
                    {dayjs.unix(parseFloat(version.file_name)).format("lll")}
                </div>
            </ListgroupItem>
            {#if version.comment}
                <Popover placement="left">
                    <div style="max-width: 20rem; word-wrap: break-word">
                        {version.comment}
                    </div>
                </Popover>
            {/if}
        {/each}
    </Listgroup>
{/if}

<Modal bind:open={askDeleteConfirmation} autoclose outsideclose size="xs">
    <h3 class="mb-5 text-lg font-normal text-gray-500 dark:text-gray-400">
        Are you sure you want to delete these versions?
    </h3>
    <svelte:fragment slot="footer">
        <Button on:click={handleDelete}>Delete</Button>
        <Button color="alternative">Cancel</Button>
    </svelte:fragment>
</Modal>

<style>
    #heading {
        margin: auto;
        width: fit-content;
    }
</style>
