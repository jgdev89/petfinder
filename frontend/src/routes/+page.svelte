<script>
  import { listarMascotas } from "$lib/api.js";
  import { ESPECIES, PROVINCIAS } from "$lib/datos.js";
  import Mapa from "$lib/Mapa.svelte";
  import { onMount } from "svelte";

  let mascotas = $state([]);
  let cargando = $state(true);
  let mostrarMapa = $state(false);

  let filtroTipo = $state("");
  let filtroEspecie = $state("");
  let filtroProvincia = $state("");
  let filtroNombre = $state("");

  async function cargarMascotas() {
    cargando = true;
    const filtros = {};
    if (filtroTipo) filtros.tipo = filtroTipo;
    if (filtroEspecie) filtros.especie = filtroEspecie;
    if (filtroProvincia) filtros.provincia = filtroProvincia;
    if (filtroNombre) filtros.nombre = filtroNombre;
    mascotas = await listarMascotas(filtros);
    cargando = false;
  }

  onMount(() => {
    cargarMascotas();
  });
</script>

<main class="max-w-5xl mx-auto px-4 py-8">

  <!-- Hero -->
  <div class="text-center mb-8">
    <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-2">Encuentra a tu mascota</h1>
    <p class="text-gray-500 dark:text-gray-400">Casos de mascotas perdidas y encontradas en España</p>
  </div>

  <!-- Buscador -->
  <div class="flex flex-col gap-3 mb-6">
    <input
      type="text"
      bind:value={filtroNombre}
      placeholder="🔍 Buscar por nombre..."
      oninput={cargarMascotas}
      class="w-full px-4 py-2.5 border border-gray-200 dark:border-gray-600 rounded-xl text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors"
    />

    <div class="flex flex-wrap gap-2">
      <select
        bind:value={filtroTipo}
        onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400"
      >
        <option value="">Todos los tipos</option>
        <option value="perdida">Perdida</option>
        <option value="encontrada">Encontrada</option>
      </select>

      <select
        bind:value={filtroEspecie}
        onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400"
      >
        <option value="">Todas las especies</option>
        {#each ESPECIES as especie}
          <option value={especie}>{especie}</option>
        {/each}
      </select>

      <select
        bind:value={filtroProvincia}
        onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400"
      >
        <option value="">Todas las provincias</option>
        {#each PROVINCIAS as provincia}
          <option value={provincia}>{provincia}</option>
        {/each}
      </select>

      <button
        onclick={() => {
          filtroTipo = "";
          filtroEspecie = "";
          filtroProvincia = "";
          filtroNombre = "";
          cargarMascotas();
        }}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors"
      >
        Limpiar
      </button>

      <button
        class="px-3 py-2 rounded-lg text-sm cursor-pointer transition-colors {mostrarMapa ? 'bg-orange-500 text-white border border-orange-500' : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'}"
        onclick={() => (mostrarMapa = !mostrarMapa)}
      >
        {mostrarMapa ? "Ocultar mapa" : "🗺️ Ver en mapa"}
      </button>
    </div>
  </div>

  {#if mostrarMapa}
    <div class="mb-6 rounded-xl overflow-hidden">
      <Mapa {mascotas} />
    </div>
  {/if}

  {#if cargando}
    <div class="text-center py-16 text-gray-400 dark:text-gray-500">Cargando...</div>
  {:else if mascotas.length === 0}
    <div class="text-center py-16 text-gray-400 dark:text-gray-500">
      <p class="text-4xl mb-3">🐾</p>
      <p>No hay mascotas que coincidan con los filtros.</p>
    </div>
  {:else}
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each mascotas as mascota}
        <a href="/mascotas/{mascota.id}" class="no-underline">
          <div class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow cursor-pointer">

            {#if mascota.imagenes && mascota.imagenes.length > 0}
              <img
                src="http://localhost:8000{mascota.imagenes[0].url}"
                alt={mascota.nombre ?? "Mascota"}
                class="w-full h-48 object-cover"
              />
            {:else}
              <div class="w-full h-48 bg-orange-50 dark:bg-gray-700 flex items-center justify-center text-4xl">
                🐾
              </div>
            {/if}

            <div class="p-4">
              <div class="flex items-center gap-2 mb-2">
                <span class="text-xs font-semibold px-2 py-0.5 rounded-full {mascota.tipo === 'perdida' ? 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-300' : 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300'}">
                  {mascota.tipo}
                </span>
                <span class="text-xs text-gray-400 dark:text-gray-500">{mascota.especie}</span>
              </div>
              <h2 class="font-semibold text-gray-800 dark:text-gray-100 text-base mb-1">{mascota.nombre ?? "Sin nombre"}</h2>
              <p class="text-xs text-gray-400 dark:text-gray-500 mb-2">📍 {mascota.localidad}, {mascota.provincia}</p>
              <p class="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">{mascota.descripcion ?? ""}</p>
            </div>

          </div>
        </a>
      {/each}
    </div>
  {/if}

</main>