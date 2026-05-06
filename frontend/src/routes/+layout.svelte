<script>
  // Importamos los estilos globales de Tailwind
  import "../app.css";
  // Importamos el favicon (icono de la pestaña del navegador)
  import favicon from "$lib/assets/favicon.png";
  // Importamos las funciones de autenticación y el store del token
  import { recuperarSesion, cerrarSesion, token } from "$lib/auth.js";
  // onMount ejecuta código cuando el componente se monta en el navegador
  import { onMount } from "svelte";
  // goto permite navegar a otra ruta programáticamente
  import { goto } from "$app/navigation";
  // Importamos footer
  import Footer from "$lib/components/Footer.svelte";

  // $props() recibe las props del componente. "children" es el contenido
  // de las páginas hijas que se renderizará dentro de este layout
  let { children } = $props();

  // Estado reactivo del token actual (null = no logueado)
  let tokenActual = $state(null);
  // Controla si el menú hamburguesa está abierto en móvil
  let menuAbierto = $state(false);
  // Controla si el modo oscuro está activo
  let modoOscuro = $state(false);

  onMount(() => {
    // Recuperamos la sesión guardada en localStorage al cargar la app
    recuperarSesion();

    // Comprobamos si el usuario tenía el modo oscuro activado
    const guardado = localStorage.getItem("tema");
    if (guardado === "oscuro") {
      modoOscuro = true;
      // Añadimos la clase "dark" al <html> para activar el modo oscuro de Tailwind
      document.documentElement.classList.add("dark");
    }
  });

  // Nos suscribimos al store del token para saber si hay sesión activa.
  // Cada vez que el token cambie, tokenActual se actualiza automáticamente.
  token.subscribe((valor) => {
    tokenActual = valor;
  });

  // Cierra la sesión, cierra el menú móvil y redirige al inicio
  function handleCerrarSesion() {
    cerrarSesion();
    menuAbierto = false;
    goto("/");
  }

  // Alterna entre modo oscuro y claro, y guarda la preferencia en localStorage
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

<!-- svelte:head permite modificar el <head> del HTML desde cualquier componente -->
<svelte:head>
  <link rel="icon" type="image/png" href={favicon} />
</svelte:head>

<!-- Barra de navegación fija en la parte superior (sticky) -->
<nav
  class="sticky top-0 z-50 bg-white dark:bg-gray-900 border-b border-orange-100 dark:border-gray-700 shadow-sm"
>
  <div class="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
    <!-- Logo que lleva al inicio -->
    <a href="/" class="flex items-center gap-2 no-underline">
    <img src={favicon} alt="PetFinder" class="w-8 h-8" />
    <span class="text-xl font-bold text-orange-500 tracking-tight">PetFinder</span>
  </a>

    <!-- Botón hamburguesa: solo visible en móvil (md:hidden).
         Al pulsarlo abre o cierra el menú móvil -->
    <button
      class="md:hidden flex flex-col gap-1.5 p-1 border-none bg-transparent cursor-pointer"
      onclick={() => (menuAbierto = !menuAbierto)}
      aria-label="Menú"
    >
      <span class="block w-6 h-0.5 bg-gray-600 dark:bg-gray-300 rounded"></span>
      <span class="block w-6 h-0.5 bg-gray-600 dark:bg-gray-300 rounded"></span>
      <span class="block w-6 h-0.5 bg-gray-600 dark:bg-gray-300 rounded"></span>
    </button>

    <!-- Enlaces de escritorio: ocultos en móvil (hidden), visibles en md en adelante -->
    <div class="hidden md:flex items-center gap-6">
      <!-- Mostramos enlaces distintos según si hay sesión activa o no -->
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
        <!-- Botón de toggle de tema: muestra sol si está en oscuro, luna si está en claro -->
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
        <!-- Botón de registro con fondo naranja -->
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

  <!-- Menú móvil desplegable: solo visible cuando menuAbierto es true -->
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
      <!-- Botón de tema en el menú móvil: muestra texto en vez de emoji -->
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

<!-- 
  {@render children()} renderiza el contenido de la página actual
  dentro de este layout. Es como un "slot" en versiones anteriores de Svelte -->
<!-- 
  Envolvemos todo en un div flex columna para que el footer
  siempre quede pegado abajo aunque la página tenga poco contenido
-->
<div class="min-h-screen flex flex-col">
  {@render children()}
  <Footer />
</div>
