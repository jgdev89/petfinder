<script>
  // Funciones para obtener mensajes y marcarlos como leídos
  import { obtenerMensajes, marcarMensajeLeido } from '$lib/api.js';
  import { token } from '$lib/auth.js';
  import { goto } from '$app/navigation';
  // onMount ejecuta código cuando el componente se monta en el navegador
  import { onMount } from 'svelte';

  let mensajes = $state([]);
  let cargando = $state(true);
  // Guardamos el token para usarlo en marcarLeido sin tener que leerlo de nuevo
  let tokenActualGuardado = $state(null);

  onMount(() => {
    // Nos suscribimos al store del token para saber cuándo está disponible
    const unsuscribir = token.subscribe(async (tokenActual) => {
      // null significa que el store aún no ha cargado, esperamos
      if (tokenActual === null) return;
      // undefined significa que no hay sesión, redirigimos al login
      if (tokenActual === undefined) { goto('/login'); return; }

      tokenActualGuardado = tokenActual;
      mensajes = await obtenerMensajes(tokenActual);
      cargando = false;
      // Cancelamos la suscripción una vez que ya tenemos los datos
      unsuscribir();
    });

    // Si tras 1 segundo seguimos cargando, asumimos que no hay sesión
    setTimeout(() => { if (cargando) goto('/login'); }, 1000);
  });

  // Marca un mensaje como leído al hacer clic.
  // Si ya está leído no hace nada
  async function marcarLeido(mensaje) {
    if (mensaje.leido) return;
    await marcarMensajeLeido(mensaje.id, tokenActualGuardado);
    // Actualizamos el array local con map: devuelve un nuevo array
    // donde el mensaje clickado tiene leido: true
    mensajes = mensajes.map(m => m.id === mensaje.id ? { ...m, leido: true } : m);
  }

  // Convierte una fecha ISO en formato legible en español
  // ej: "2024-03-12T10:00:00" → "12 de marzo de 2024"
  function formatearFecha(fechaStr) {
    const fecha = new Date(fechaStr);
    return fecha.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });
  }
</script>

<svelte:head>
  <title>Mensajes — PetFinder</title>
</svelte:head>

<main class="max-w-2xl mx-auto px-4 py-8">
  <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-6">Mensajes recibidos</h1>

  {#if cargando}
    <p class="text-gray-400 dark:text-gray-500">Cargando...</p>

  {:else if mensajes.length === 0}
    <div class="text-center py-12 text-gray-400 dark:text-gray-500">
      <p class="text-4xl mb-3">✉️</p>
      <p>No tienes mensajes todavía.</p>
    </div>

  {:else}
    <div class="flex flex-col gap-3">
      {#each mensajes as mensaje}
        <!-- Las clases cambian dinámicamente según si el mensaje está leído o no.
             role="button" y tabindex="0" hacen el div accesible por teclado -->
        <div
          class="relative border rounded-xl p-4 cursor-pointer transition-all {mensaje.leido ? 'border-gray-100 dark:border-gray-700 opacity-60 hover:opacity-80' : 'border-l-4 border-l-orange-400 border-gray-100 dark:border-gray-700 bg-orange-50 dark:bg-orange-950 hover:bg-orange-100 dark:hover:bg-orange-900'}"
          onclick={() => marcarLeido(mensaje)}
          role="button"
          tabindex="0"
        >
          <!-- Badge "Nuevo": solo visible en mensajes no leídos -->
          {#if !mensaje.leido}
            <span class="absolute top-3 right-3 bg-orange-500 text-white text-xs font-semibold px-2 py-0.5 rounded-full">
              Nuevo
            </span>
          {/if}

          <div class="flex justify-between items-start mb-2 pr-16">
            <span class="font-semibold text-gray-800 dark:text-gray-100 text-sm">{mensaje.asunto}</span>
            <span class="text-xs text-gray-400 dark:text-gray-500 whitespace-nowrap ml-3">{formatearFecha(mensaje.fecha_envio)}</span>
          </div>

          <p class="text-sm text-gray-600 dark:text-gray-300 leading-relaxed mb-3">{mensaje.contenido}</p>

          <!-- Enlace a la mascota relacionada: stopPropagation evita que el clic
               en el enlace marque el mensaje como leído al mismo tiempo -->
          {#if mensaje.mascota_id}
            <a href="/mascotas/{mensaje.mascota_id}"
              class="text-xs text-orange-500 hover:text-orange-600 no-underline font-medium transition-colors"
              onclick={(e) => e.stopPropagation()}
            >
              Ver mascota →
            </a>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</main>