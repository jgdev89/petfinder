<script>
  import "../app.css";
  import favicon from "$lib/assets/favicon.svg";
  import { recuperarSesion, cerrarSesion, token } from "$lib/auth.js";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  let { children } = $props();
  let tokenActual = $state(null);
  let menuAbierto = $state(false);
  let modoOscuro = $state(false);

  onMount(() => {
    recuperarSesion();
    const guardado = localStorage.getItem("tema");
    if (guardado === "oscuro") {
      modoOscuro = true;
      document.documentElement.classList.add("dark");
    }
  });

  token.subscribe((valor) => {
    tokenActual = valor;
  });

  function handleCerrarSesion() {
    cerrarSesion();
    menuAbierto = false;
    goto("/");
  }

  function toggleTema() {
    modoOscuro = !modoOscuro;
    if (modoOscuro) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("tema", "oscuro");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("tema", "claro");
    }
  }
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<nav
  class="sticky top-0 z-50 bg-white dark:bg-gray-900 border-b border-orange-100 dark:border-gray-700 shadow-sm"
>
  <div class="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
    <a
      href="/"
      class="text-xl font-bold text-orange-500 tracking-tight no-underline"
    >
      🐾 PetFinder
    </a>

    <!-- Hamburguesa móvil -->
    <button
      class="md:hidden flex flex-col gap-1.5 p-1 border-none bg-transparent cursor-pointer"
      onclick={() => (menuAbierto = !menuAbierto)}
      aria-label="Menú"
    >
      <span class="block w-6 h-0.5 bg-gray-600 dark:bg-gray-300 rounded"></span>
      <span class="block w-6 h-0.5 bg-gray-600 dark:bg-gray-300 rounded"></span>
      <span class="block w-6 h-0.5 bg-gray-600 dark:bg-gray-300 rounded"></span>
    </button>

    <!-- Enlaces escritorio -->
    <div class="hidden md:flex items-center gap-6">
      {#if tokenActual}
        <a
          href="/mascotas/nueva"
          class="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-orange-500 no-underline transition-colors"
          >Publicar</a
        >
        <a
          href="/mensajes"
          class="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-orange-500 no-underline transition-colors"
          >Mensajes</a
        >
        <a
          href="/perfil"
          class="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-orange-500 no-underline transition-colors"
          >Mi perfil</a
        >
        <button
          onclick={handleCerrarSesion}
          class="text-sm text-gray-400 dark:text-gray-500 border border-gray-200 dark:border-gray-600 rounded-lg px-3 py-1.5 bg-transparent cursor-pointer hover:border-orange-400 hover:text-orange-500 transition-colors"
        >
          Cerrar sesión
        </button>
        <button
          onclick={toggleTema}
          aria-label="Cambiar tema"
          class="text-xl bg-transparent border-none cursor-pointer"
        >
          {modoOscuro ? "☀️" : "🌙"}
        </button>
      {:else}
        <a
          href="/login"
          class="text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-orange-500 no-underline transition-colors"
          >Entrar</a
        >
        <a
          href="/registro"
          class="text-sm font-medium bg-orange-500 text-white px-4 py-1.5 rounded-full no-underline hover:bg-orange-600 transition-colors"
          >Registrarse</a
        >
        <button
          onclick={toggleTema}
          aria-label="Cambiar tema"
          class="text-xl bg-transparent border-none cursor-pointer"
        >
          {modoOscuro ? "☀️" : "🌙"}
        </button>
      {/if}
    </div>
  </div>

  <!-- Menú móvil desplegable -->
  {#if menuAbierto}
    <div
      class="md:hidden border-t border-orange-100 dark:border-gray-700 px-4 py-3 flex flex-col gap-3"
    >
      {#if tokenActual}
        <a
          href="/mascotas/nueva"
          onclick={() => (menuAbierto = false)}
          class="text-gray-700 dark:text-gray-300 no-underline font-medium"
          >Publicar</a
        >
        <a
          href="/mensajes"
          onclick={() => (menuAbierto = false)}
          class="text-gray-700 dark:text-gray-300 no-underline font-medium"
          >Mensajes</a
        >
        <a
          href="/perfil"
          onclick={() => (menuAbierto = false)}
          class="text-gray-700 dark:text-gray-300 no-underline font-medium"
          >Mi perfil</a
        >
        <button
          onclick={handleCerrarSesion}
          class="text-left text-gray-400 bg-transparent border-none cursor-pointer font-medium p-0"
          >Cerrar sesión</button
        >
      {:else}
        <a
          href="/login"
          onclick={() => (menuAbierto = false)}
          class="text-gray-700 dark:text-gray-300 no-underline font-medium"
          >Entrar</a
        >
        <a
          href="/registro"
          onclick={() => (menuAbierto = false)}
          class="text-gray-700 dark:text-gray-300 no-underline font-medium"
          >Registrarse</a
        >
      {/if}
      <button
        onclick={toggleTema}
        aria-label="Cambiar tema"
        class="text-left text-sm font-medium bg-transparent border-none cursor-pointer text-gray-700 dark:text-gray-300 p-0"
      >
        {modoOscuro ? "Modo claro ☀️" : "Modo oscuro 🌙"}
      </button>
    </div>
  {/if}
</nav>

{@render children()}
