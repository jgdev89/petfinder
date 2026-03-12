<script>
  import { obtenerMensajes, marcarMensajeLeido } from '$lib/api.js';
  import { token } from '$lib/auth.js';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let mensajes = $state([]);
  let cargando = $state(true);
  let tokenActualGuardado = $state(null);

  onMount(() => {
    const unsuscribir = token.subscribe(async (tokenActual) => {
      if (tokenActual === null) return;
      if (tokenActual === undefined) { goto('/login'); return; }
      tokenActualGuardado = tokenActual;
      mensajes = await obtenerMensajes(tokenActual);
      cargando = false;
      unsuscribir();
    });
    setTimeout(() => { if (cargando) goto('/login'); }, 1000);
  });

  async function marcarLeido(mensaje) {
    if (mensaje.leido) return;
    await marcarMensajeLeido(mensaje.id, tokenActualGuardado);
    mensajes = mensajes.map(m => m.id === mensaje.id ? { ...m, leido: true } : m);
  }

  function formatearFecha(fechaStr) {
    const fecha = new Date(fechaStr);
    return fecha.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' });
  }
</script>

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
        <div
          class="relative border rounded-xl p-4 cursor-pointer transition-all {mensaje.leido ? 'border-gray-100 dark:border-gray-700 opacity-60 hover:opacity-80' : 'border-l-4 border-l-orange-400 border-gray-100 dark:border-gray-700 bg-orange-50 dark:bg-orange-950 hover:bg-orange-100 dark:hover:bg-orange-900'}"
          onclick={() => marcarLeido(mensaje)}
          role="button"
          tabindex="0"
        >
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