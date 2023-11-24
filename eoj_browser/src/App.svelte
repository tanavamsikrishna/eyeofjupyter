<script lang="ts">
    let snapshots: string[] = [];
    fetch("snapshots")
        .then((res) => res.json())
        .then((res) => {
            snapshots = res;
        });
</script>

<main>
    <h3>Snapshots</h3>
    {#each snapshots as snapshot}
        <a href='snapshot/{snapshot}'>{snapshot}</a>
        <br />
    {/each}
</main>

<style>
    main {
        width: fit-content;
        margin: auto;
        margin-top: 5rem;
    }
</style>
