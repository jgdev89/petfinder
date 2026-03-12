<script>
  import { miPerfil, misMascotas } from '$lib/api.js';
  import { token } from '$lib/auth.js';
  import { get } from 'svelte/store';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let usuario = $state(null);
  let mascotas = $state([]);
  let cargando = $state(true);

  onMount(async () => {
    const tokenActual = get(token);
    if (!tokenActual) { goto('/login'); return; }
    usuario = await miPerfil(tokenActual);
    mascotas = await misMascotas(tokenActual);
    cargando = false;
  });
</script>

{#if cargando}
  <main class="max-w-5xl mx-auto px-4 py-8">
    <p class="text-gray-400 dark:text-gray-500">Cargando...</p>
  </main>
{:else}
  <main class="max-w-5xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-6">Mi perfil</h1>

    <!-- Info usuario -->
    <div class="bg-gray-50 dark:bg-gray-800 rounded-xl px-5 py-4 flex flex-col gap-2 text-sm text-gray-600 dark:text-gray-300 mb-8">
      <p><span class="font-semibold text-gray-700 dark:text-gray-200">Nombre:</span> {usuario.nombre}</p>
      <p><span class="font-semibold text-gray-700 dark:text-gray-200">Email:</span> {usuario.email}</p>
      {#if usuario.telefono}
        <p><span class="font-semibold text-gray-700 dark:text-gray-200">Teléfono:</span> {usuario.telefono}</p>
      {/if}
    </div>

    <!-- Mis publicaciones -->
    <h2 class="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-4">Mis publicaciones</h2>

    {#if mascotas.length === 0}
      <div class="text-center py-12 text-gray-400 dark:text-gray-500">
        <p class="text-4xl mb-3">🐾</p>
        <p class="mb-3">No has publicado ninguna mascota todavía.</p>
        <a href="/mascotas/nueva" class="px-5 py-2 bg-orange-500 text-white text-sm font-medium rounded-full no-underline hover:bg-orange-600 transition-colors">
          Publicar ahora
        </a>
      </div>
    {:else}
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {#each mascotas as mascota}
          <a href="/mascotas/{mascota.id}" class="no-underline">
            <div class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
              {#if mascota.imagenes && mascota.imagenes.length > 0}
                <img
                  src="http://localhost:8000{mascota.imagenes[0].url}"
                  alt={mascota.nombre ?? 'Mascota'}
                  class="w-full h-44 object-cover"
                />
              {:else}
                <div class="w-full h-44 bg-orange-50 dark:bg-gray-700 flex items-center justify-center text-3xl">🐾</div>
              {/if}

              <div class="p-4 flex flex-col gap-2">
                <div class="flex items-center gap-2 flex-wrap">
                  <span class="text-xs font-semibold px-2 py-0.5 rounded-full {mascota.tipo === 'perdida' ? 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-300' : 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300'}">
                    {mascota.tipo}
                  </span>
                  <span class="text-xs font-medium px-2 py-0.5 rounded-full {mascota.estado === 'activo' ? 'bg-blue-50 text-blue-500 dark:bg-blue-900 dark:text-blue-300' : 'bg-gray-100 text-gray-400 dark:bg-gray-700 dark:text-gray-500'}">
                    {mascota.estado}
                  </span>
                </div>
                <h3 class="font-semibold text-gray-800 dark:text-gray-100 text-sm m-0">{mascota.nombre ?? 'Sin nombre'}</h3>
                <p class="text-xs text-gray-400 dark:text-gray-500">{mascota.especie} · 📍 {mascota.localidad}, {mascota.provincia}</p>
              </div>
            </div>
          </a>
        {/each}
      </div>
    {/if}
  </main>
{/if}