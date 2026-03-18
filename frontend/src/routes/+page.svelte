<script>
  // Importamos la función para obtener mascotas del backend
  import { listarMascotas } from "$lib/api.js";
  // Importamos las listas de especies y provincias disponibles
  import { ESPECIES, PROVINCIAS } from "$lib/datos.js";
  // Componente del mapa interactivo
  import Mapa from "$lib/Mapa.svelte";
  // onMount ejecuta código cuando el componente se carga en el navegador
  import { onMount } from "svelte";

  // $state() es la forma de declarar variables reactivas en Svelte 5.
  // Cuando cambian, el HTML se actualiza automáticamente.
  let mascotas = $state([]); // Lista de mascotas que viene del backend
  let cargando = $state(true); // Controla si mostramos "Cargando..."
  let mostrarMapa = $state(false); // Controla si el mapa está visible o no

  // Variables reactivas para cada filtro del buscador
  let filtroTipo = $state("");
  let filtroEspecie = $state("");
  let filtroProvincia = $state("");
  let filtroNombre = $state("");

  // Función asíncrona que pide las mascotas al backend con los filtros activos
  async function cargarMascotas() {
    cargando = true;

    // Construimos el objeto de filtros solo con los que tienen valor
    const filtros = {};
    if (filtroTipo) filtros.tipo = filtroTipo;
    if (filtroEspecie) filtros.especie = filtroEspecie;
    if (filtroProvincia) filtros.provincia = filtroProvincia;
    if (filtroNombre) filtros.nombre = filtroNombre;

    // Llamamos al backend y guardamos el resultado en mascotas
    mascotas = await listarMascotas(filtros);
    cargando = false;
  }

  // onMount: se ejecuta una sola vez cuando la página termina de cargarse
  onMount(() => {
    cargarMascotas();
  });
</script>

<!-- svelte:head permite modificar el <head> del HTML, como el título de la pestaña -->
<svelte:head>
  <title>PetFinder — Encuentra a tu mascota</title>
</svelte:head>

<main class="max-w-5xl mx-auto px-4 py-8">
  <!-- Sección hero: título y subtítulo centrados -->
  <div class="text-center mb-8">
    <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-2">
      Encuentra a tu mascota
    </h1>
    <p class="text-gray-500 dark:text-gray-400">
      Casos de mascotas perdidas y encontradas en España
    </p>
  </div>

  <!-- Buscador y filtros -->
  <div class="flex flex-col gap-3 mb-6">
    <!-- Input de búsqueda por nombre. bind:value sincroniza el valor con filtroNombre.
         oninput llama a cargarMascotas cada vez que el usuario escribe -->
    <input
      type="text"
      bind:value={filtroNombre}
      placeholder="🔍 Buscar por nombre..."
      oninput={cargarMascotas}
      class="w-full px-4 py-2.5 border border-gray-200 dark:border-gray-600 rounded-xl text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors"
    />

    <div class="flex flex-wrap gap-2">
      <!-- Select de tipo: bind:value sincroniza con filtroTipo.
           aria-label mejora la accesibilidad para lectores de pantalla -->
      <select
        bind:value={filtroTipo}
        aria-label="Filtrar por tipo"
        onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400"
      >
        <option value="">Todos los tipos</option>
        <option value="perdida">Perdida</option>
        <option value="encontrada">Encontrada</option>
      </select>

      <!-- Select de especie: genera las opciones dinámicamente desde el array ESPECIES -->
      <select
        bind:value={filtroEspecie}
        aria-label="Filtrar por especie"
        onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400"
      >
        <option value="">Todas las especies</option>
        <!-- #each itera sobre el array y crea una <option> por cada elemento -->
        {#each ESPECIES as especie}
          <option value={especie}>{especie}</option>
        {/each}
      </select>

      <!-- Select de provincia: igual que el de especie pero con PROVINCIAS -->
      <select
        bind:value={filtroProvincia}
        aria-label="Filtrar por provincia"
        onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400"
      >
        <option value="">Todas las provincias</option>
        {#each PROVINCIAS as provincia}
          <option value={provincia}>{provincia}</option>
        {/each}
      </select>

      <!-- Botón limpiar: resetea todos los filtros y recarga las mascotas -->
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

      <!-- Botón mapa: alterna entre mostrar y ocultar el mapa.
           Las clases cambian dinámicamente según el estado de mostrarMapa -->
      <button
        class="px-3 py-2 rounded-lg text-sm cursor-pointer transition-colors {mostrarMapa
          ? 'bg-orange-500 text-white border border-orange-500'
          : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'}"
        onclick={() => (mostrarMapa = !mostrarMapa)}
      >
        {mostrarMapa ? "Ocultar mapa" : "🗺️ Ver en mapa"}
      </button>
    </div>
  </div>

  <!-- El mapa solo se renderiza si mostrarMapa es true -->
  {#if mostrarMapa}
    <div class="mb-6 rounded-xl overflow-hidden">
      <!-- Pasamos la lista de mascotas al componente Mapa como prop -->
      <Mapa {mascotas} />
    </div>
  {/if}

  <!-- Renderizado condicional según el estado de la carga -->
  {#if cargando}
    <div class="text-center py-16 text-gray-400 dark:text-gray-500">
      Cargando...
    </div>
  {:else if mascotas.length === 0}
    <!-- Si no hay mascotas que coincidan con los filtros -->
    <div class="text-center py-16 text-gray-400 dark:text-gray-500">
      <p class="text-4xl mb-3">🐾</p>
      <p>No hay mascotas que coincidan con los filtros.</p>
    </div>
  {:else}
    <!-- Grid de tarjetas de mascotas -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each mascotas as mascota}
        <!-- Cada tarjeta es un enlace al detalle de la mascota -->
        <a href="/mascotas/{mascota.id}" class="no-underline">
          <div
            class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow cursor-pointer"
          >
            <!-- Si tiene imagen la mostramos, si no mostramos un emoji -->
            {#if mascota.imagenes && mascota.imagenes.length > 0}
              <img
                src="http://localhost:8000{mascota.imagenes[0].url}"
                alt={mascota.nombre ?? "Mascota"}
                class="w-full h-48 object-cover"
              />
            {:else}
              <div
                class="w-full h-48 bg-orange-50 dark:bg-gray-700 flex items-center justify-center text-4xl"
              >
                🐾
              </div>
            {/if}

            <div class="p-4">
              <div class="flex items-center gap-2 mb-2">
                <!-- Badge de tipo: rojo si perdida, verde si encontrada -->
                <span
                  class="text-xs font-semibold px-2 py-0.5 rounded-full {mascota.tipo ===
                  'perdida'
                    ? 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-300'
                    : 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300'}"
                >
                  {mascota.tipo}
                </span>
                <span class="text-xs text-gray-500 dark:text-gray-500"
                  >{mascota.especie}</span
                >
              </div>
              <!-- ?? es el operador nullish: si nombre es null muestra "Sin nombre" -->
              <h2
                class="font-semibold text-gray-800 dark:text-gray-100 text-base mb-1"
              >
                {mascota.nombre ?? "Sin nombre"}
              </h2>
              <p class="text-xs text-gray-500 dark:text-gray-500 mb-2">
                📍 {mascota.localidad}, {mascota.provincia}
              </p>
              <!-- line-clamp-2 limita el texto a 2 líneas con puntos suspensivos -->
              <p class="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
                {mascota.descripcion ?? ""}
              </p>
            </div>
          </div>
        </a>
      {/each}
    </div>
  {/if}
</main>
