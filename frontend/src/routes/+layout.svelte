<script>
  import favicon from '$lib/assets/favicon.svg';
  import { recuperarSesion } from '$lib/auth.js';
  import { onMount } from 'svelte';

  let { children } = $props();

  // onMount se ejecuta una sola vez cuando la app arranca en el navegador.
  // Lo usamos aquí porque localStorage solo existe en el navegador,
  // no en el servidor. Si lo llamáramos fuera de onMount, fallaría.
  onMount(() => {
    recuperarSesion();
  });
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

{@render children()}