<script>
  // Importamos la función para obtener mascotas del backend
  import { listarMascotas } from "$lib/api.js";
  // Importamos las listas de especies y provincias disponibles
  import { ESPECIES, PROVINCIAS } from "$lib/datos.js";
  // Componente del mapa interactivo
  import Mapa from "$lib/Mapa.svelte";
  // onMount ejecuta código cuando el componente se carga en el navegador
  import { onMount } from "svelte";
  import { slide } from "svelte/transition";

  // Número de tarjetas que se muestran por página
  const POR_PAGINA = 9;

  // $state() declara variables reactivas en Svelte 5.
  // Cuando cambian, el HTML se actualiza automáticamente.
  let mascotas = $state([]);      // Lista completa de mascotas del backend
  let cargando = $state(true);    // Controla si mostramos "Cargando..."
  let mostrarMapa = $state(false); // Controla si el mapa está visible
  let paginaActual = $state(1);   // Página activa en la paginación

  // Variables reactivas para cada filtro del buscador
  let filtroTipo = $state("");
  let filtroEspecie = $state("");
  let filtroProvincia = $state("");
  let filtroNombre = $state("");

  // $derived calcula valores derivados de otras variables reactivas.
  // Se recalculan automáticamente cada vez que cambia mascotas o paginaActual.

  // Total de páginas: dividimos el total de mascotas entre las que caben por página
  let totalPaginas = $derived(Math.ceil(mascotas.length / POR_PAGINA));

  // Mascotas de la página actual: slice extrae solo el trozo del array que corresponde
  // Ejemplo: página 2 con 9 por página → slice(9, 18)
  let mascotasPagina = $derived(
    mascotas.slice((paginaActual - 1) * POR_PAGINA, paginaActual * POR_PAGINA)
  );

  // Función asíncrona que pide las mascotas al backend con los filtros activos
  async function cargarMascotas() {
    cargando = true;
    paginaActual = 1; // Siempre volvemos a la página 1 al cambiar filtros

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

  // Cambia a la página indicada y hace scroll suave al inicio de la página
  function irAPagina(n) {
    paginaActual = n;
    window.scrollTo({ top: 0, behavior: 'smooth' });
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
    <h1 class="text-3xl font-bold text-gray-800 mb-2">Encuentra a tu mascota</h1>
    <p class="text-gray-500">Casos de mascotas perdidas y encontradas en España</p>
  </div>

  <!-- Buscador y filtros -->
  <div class="flex flex-col gap-3 mb-6">

    <!-- Input de búsqueda por nombre.
         bind:value sincroniza el valor con filtroNombre.
         oninput llama a cargarMascotas cada vez que el usuario escribe -->
    <input
      type="text"
      bind:value={filtroNombre}
      placeholder="🔍 Buscar por nombre..."
      oninput={cargarMascotas}
      class="w-full px-4 py-2.5 border border-gray-200 rounded-xl text-sm bg-white focus:outline-none focus:border-orange-400 transition-colors"
    />

    <div class="flex flex-wrap gap-2">

      <!-- Select de tipo: bind:value sincroniza con filtroTipo.
           aria-label mejora la accesibilidad para lectores de pantalla -->
      <select bind:value={filtroTipo} aria-label="Filtrar por tipo" onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:outline-none focus:border-orange-400">
        <option value="">Todos los tipos</option>
        <option value="perdida">Perdida</option>
        <option value="encontrada">Encontrada</option>
      </select>

      <!-- Select de especie: genera las opciones dinámicamente desde el array ESPECIES -->
      <select bind:value={filtroEspecie} aria-label="Filtrar por especie" onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:outline-none focus:border-orange-400">
        <option value="">Todas las especies</option>
        <!-- #each itera sobre el array y crea una <option> por cada elemento -->
        {#each ESPECIES as especie}
          <option value={especie}>{especie}</option>
        {/each}
      </select>

      <!-- Select de provincia: igual que el de especie pero con PROVINCIAS -->
      <select bind:value={filtroProvincia} aria-label="Filtrar por provincia" onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 rounded-lg text-sm bg-white focus:outline-none focus:border-orange-400">
        <option value="">Todas las provincias</option>
        {#each PROVINCIAS as provincia}
          <option value={provincia}>{provincia}</option>
        {/each}
      </select>

      <!-- Botón limpiar: resetea todos los filtros y recarga las mascotas -->
      <button
        onclick={() => { filtroTipo = ""; filtroEspecie = ""; filtroProvincia = ""; filtroNombre = ""; cargarMascotas(); }}
        class="px-3 py-2 border border-gray-200 rounded-lg text-sm text-gray-500 bg-white hover:bg-gray-50 cursor-pointer transition-colors">
        Limpiar
      </button>

      <!-- Botón mapa: alterna entre mostrar y ocultar el mapa.
           Las clases cambian dinámicamente según el estado de mostrarMapa -->
      <button
        class="px-3 py-2 rounded-lg text-sm cursor-pointer transition-colors {mostrarMapa ? 'bg-orange-500 text-white border border-orange-500' : 'bg-white border border-gray-200 text-gray-600 hover:bg-gray-50'}"
        onclick={() => (mostrarMapa = !mostrarMapa)}>
        {mostrarMapa ? "Ocultar mapa" : "🗺️ Ver en mapa"}
      </button>
    </div>
  </div>

  <!-- El mapa solo se renderiza si mostrarMapa es true.
       transition:slide añade una animación de deslizamiento al aparecer/desaparecer -->
  {#if mostrarMapa}
    <div transition:slide class="mb-6 rounded-xl overflow-hidden">
      <!-- Pasamos la lista completa de mascotas al componente Mapa como prop -->
      <Mapa {mascotas} />
    </div>
  {/if}

  <!-- Renderizado condicional según el estado de la carga -->
  {#if cargando}
    <div class="text-center py-16 text-gray-400">Cargando...</div>

  {:else if mascotas.length === 0}
    <!-- Si no hay mascotas que coincidan con los filtros -->
    <div class="text-center py-16 text-gray-400">
      <p class="text-4xl mb-3">🐾</p>
      <p>No hay mascotas que coincidan con los filtros.</p>
    </div>

  {:else}
    <!-- Contador de resultados y página actual -->
    <p class="text-sm text-gray-400 mb-4">
      {mascotas.length} {mascotas.length === 1 ? 'resultado' : 'resultados'}
      · Página {paginaActual} de {totalPaginas}
    </p>

    <!-- Grid de tarjetas: 1 columna en móvil, 2 en tablet, 3 en escritorio -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Iteramos sobre mascotasPagina (solo las de la página actual) en lugar
           de mascotas completo. Esto es lo que implementa la paginación visual. -->
      {#each mascotasPagina as mascota}
        <!-- Cada tarjeta es un enlace al detalle de la mascota -->
        <a href="/mascotas/{mascota.id}" class="no-underline">
          <div class="bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow cursor-pointer">

            <!-- Si tiene imagen la mostramos, si no mostramos un emoji placeholder -->
            {#if mascota.imagenes && mascota.imagenes.length > 0}
              <img
                src="http://localhost:8000{mascota.imagenes[0].url}"
                alt={mascota.nombre ?? "Mascota"}
                class="w-full h-48 object-cover"
              />
            {:else}
              <div class="w-full h-48 bg-orange-50 flex items-center justify-center text-4xl">🐾</div>
            {/if}

            <div class="p-4">
              <div class="flex items-center gap-2 mb-2">
                <!-- Badge de tipo: rojo si perdida, verde si encontrada -->
                <span class="text-xs font-semibold px-2 py-0.5 rounded-full {mascota.tipo === 'perdida' ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'}">
                  {mascota.tipo}
                </span>
                <span class="text-xs text-gray-500">{mascota.especie}</span>
              </div>
              <!-- ?? es el operador nullish: si nombre es null muestra "Sin nombre" -->
              <h2 class="font-semibold text-gray-800 text-base mb-1">{mascota.nombre ?? "Sin nombre"}</h2>
              <p class="text-xs text-gray-500 mb-2">📍 {mascota.localidad}, {mascota.provincia}</p>
              <!-- line-clamp-2 limita el texto a 2 líneas con puntos suspensivos -->
              <p class="text-sm text-gray-500 line-clamp-2">{mascota.descripcion ?? ""}</p>
            </div>
          </div>
        </a>
      {/each}
    </div>

    <!-- Controles de paginación: solo se muestran si hay más de una página -->
    {#if totalPaginas > 1}
      <div class="flex justify-center items-center gap-2 mt-8">

        <!-- Botón anterior: desactivado si estamos en la primera página -->
        <button
          onclick={() => irAPagina(paginaActual - 1)}
          disabled={paginaActual === 1}
          class="px-3 py-2 rounded-lg border border-gray-200 text-sm text-gray-500 bg-white hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer transition-colors">
          ← Anterior
        </button>

        <!-- Botones numerados: uno por cada página.
             Array.from genera un array [1, 2, 3, ...totalPaginas] -->
        {#each Array.from({ length: totalPaginas }, (_, i) => i + 1) as n}
          <button
            onclick={() => irAPagina(n)}
            class="px-3 py-2 rounded-lg border text-sm cursor-pointer transition-colors {n === paginaActual ? 'bg-orange-500 text-white border-orange-500' : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'}">
            {n}
          </button>
        {/each}

        <!-- Botón siguiente: desactivado si estamos en la última página -->
        <button
          onclick={() => irAPagina(paginaActual + 1)}
          disabled={paginaActual === totalPaginas}
          class="px-3 py-2 rounded-lg border border-gray-200 text-sm text-gray-500 bg-white hover:bg-gray-50 disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer transition-colors">
          Siguiente →
        </button>

      </div>
    {/if}
  {/if}

</main>