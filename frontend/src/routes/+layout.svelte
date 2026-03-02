<script>
  import favicon from '$lib/assets/favicon.svg';
  import { recuperarSesion, cerrarSesion, token } from '$lib/auth.js';
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  let { children } = $props();

  let tokenActual = $state(null);

  onMount(() => {
    recuperarSesion();
  });

  // Nos suscribimos al store para saber si hay sesión activa
  token.subscribe(valor => {
    tokenActual = valor;
  });

  function handleCerrarSesion() {
    cerrarSesion();
    goto('/');
  }
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<nav>
  <a href="/" class="logo">🐾 PetFinder</a>

  <div class="enlaces">
    {#if tokenActual}
      <a href="/mascotas/nueva">Publicar</a>
      <a href="/mensajes">Mensajes</a>
      <button onclick={handleCerrarSesion}>Cerrar sesión</button>
    {:else}
      <a href="/login">Entrar</a>
      <a href="/registro">Registrarse</a>
    {/if}
  </div>
</nav>

{@render children()}

<style>
  nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem 2rem;
    border-bottom: 1px solid #eee;
    background: white;
    position: sticky;
    top: 0;
    z-index: 100;
  }

  .logo {
    font-size: 1.2rem;
    font-weight: bold;
    text-decoration: none;
    color: #333;
  }

  .enlaces {
    display: flex;
    align-items: center;
    gap: 1.2rem;
  }

  .enlaces a {
    text-decoration: none;
    color: #555;
    font-size: 0.95rem;
  }

  .enlaces a:hover {
    color: #333;
  }

  .enlaces button {
    background: none;
    border: 1px solid #ddd;
    padding: 0.4rem 0.8rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.95rem;
    color: #555;
  }

  .enlaces button:hover {
    background: #f5f5f5;
  }
</style>