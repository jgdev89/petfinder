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
  let mascotas = $state([]);       // Lista completa de mascotas del backend
  let cargando = $state(true);     // Controla si mostramos "Cargando..."
  let mostrarMapa = $state(false); // Controla si el mapa está visible
  let paginaActual = $state(1);    // Página activa en la paginación

  // Variables reactivas para cada filtro del buscador
  let filtroTipo = $state("");
  let filtroEspecie = $state("");
  let filtroProvincia = $state("");
  let filtroNombre = $state("");

  // ── Carrusel ──────────────────────────────────────────────────────────────
  // Cada slide tiene una imagen (en /static/) y el texto que aparece encima
  const slides = [
    { imagen: "/hero1.jpg", titulo: "Ayudando a reunir familias desde 2025", subtitulo: "Porque cada mascota merece volver a casa" },
    { imagen: "/hero2.jpg", titulo: "Miles de mascotas han vuelto a casa", subtitulo: "Publica tu caso y llega a toda España" },
    { imagen: "/hero3.jpg", titulo: "Publica, encuentra, reúnete", subtitulo: "La comunidad más grande de mascotas perdidas" },
  ];

  // Índice del slide activo
  let slideActual = $state(0);
  let intervaloCarrusel;

  // Avanza al siguiente slide (vuelve al primero cuando llega al final)
  function siguienteSlide() {
    slideActual = (slideActual + 1) % slides.length;
  }

  // Retrocede al slide anterior
  function anteriorSlide() {
    slideActual = (slideActual - 1 + slides.length) % slides.length;
  }
  // ──────────────────────────────────────────────────────────────────────────

  // $derived calcula valores derivados de otras variables reactivas.
  let totalPaginas = $derived(Math.ceil(mascotas.length / POR_PAGINA));
  let mascotasPagina = $derived(
    mascotas.slice((paginaActual - 1) * POR_PAGINA, paginaActual * POR_PAGINA)
  );

  async function cargarMascotas() {
    cargando = true;
    paginaActual = 1;
    const filtros = {};
    if (filtroTipo) filtros.tipo = filtroTipo;
    if (filtroEspecie) filtros.especie = filtroEspecie;
    if (filtroProvincia) filtros.provincia = filtroProvincia;
    if (filtroNombre) filtros.nombre = filtroNombre;
    mascotas = await listarMascotas(filtros);
    cargando = false;
  }

  function irAPagina(n) {
    paginaActual = n;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  onMount(() => {
    cargarMascotas();
    // El carrusel avanza automáticamente cada 5 segundos
    intervaloCarrusel = setInterval(siguienteSlide, 5000);
    // Limpiamos el intervalo cuando el componente se desmonta
    return () => clearInterval(intervaloCarrusel);
  });
</script>

<svelte:head>
  <title>PetFinder — Encuentra a tu mascota</title>
</svelte:head>

<!-- ── CARRUSEL HERO ─────────────────────────────────────────────────────── -->
<!-- El carrusel va fuera del max-w-5xl para ocupar todo el ancho de pantalla -->
<div class="relative w-full h-72 sm:h-96 overflow-hidden">

  <!-- Imagen de fondo del slide activo -->
  <img
    src={slides[slideActual].imagen}
    alt="Hero"
    class="w-full h-full object-cover transition-opacity duration-700"
  />

  <!-- Overlay oscuro semitransparente para que el texto sea legible -->
  <div class="absolute inset-0 bg-black/40"></div>

  <!-- Texto centrado encima de la imagen -->
  <div class="absolute inset-0 flex flex-col items-center justify-center text-center px-4">
    <h1 class="text-white text-2xl sm:text-4xl font-bold drop-shadow-lg mb-2">
      {slides[slideActual].titulo}
    </h1>
    <p class="text-white/90 text-sm sm:text-lg drop-shadow">
      {slides[slideActual].subtitulo}
    </p>
    <!-- Botón de llamada a la acción -->
    <a href="/mascotas/nueva"
      class="mt-6 px-6 py-2.5 bg-orange-500 hover:bg-orange-600 text-white font-medium rounded-full no-underline transition-colors text-sm sm:text-base">
      Publicar mascota
    </a>
  </div>

  <!-- Botón anterior -->
  <button
    onclick={anteriorSlide}
    class="absolute left-3 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/40 text-white border-none rounded-full w-9 h-9 flex items-center justify-center cursor-pointer transition-colors text-lg">
    ‹
  </button>

  <!-- Botón siguiente -->
  <button
    onclick={siguienteSlide}
    class="absolute right-3 top-1/2 -translate-y-1/2 bg-white/20 hover:bg-white/40 text-white border-none rounded-full w-9 h-9 flex items-center justify-center cursor-pointer transition-colors text-lg">
    ›
  </button>

  <!-- Puntos indicadores de slide -->
  <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
    {#each slides as _, i}
      <button
        onclick={() => slideActual = i}
        class="w-2 h-2 rounded-full border-none cursor-pointer transition-colors {i === slideActual ? 'bg-white' : 'bg-white/40'}">
      </button>
    {/each}
  </div>

</div>
<!-- ──────────────────────────────────────────────────────────────────────── -->

<main class="max-w-5xl mx-auto px-4 py-8">

  <!-- Sección hero: título y subtítulo centrados -->
  <div class="text-center mb-8">
    <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-2">Encuentra a tu mascota</h1>
    <p class="text-gray-500 dark:text-gray-400">Casos de mascotas perdidas y encontradas en España</p>
  </div>

  <!-- Buscador y filtros -->
  <div class="flex flex-col gap-3 mb-6">

    <!-- Input de búsqueda por nombre -->
    <input
      type="text"
      bind:value={filtroNombre}
      placeholder="🔍 Buscar por nombre..."
      oninput={cargarMascotas}
      class="w-full px-4 py-2.5 border border-gray-200 dark:border-gray-600 rounded-xl text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors"
    />

    <div class="flex flex-wrap gap-2">

      <select bind:value={filtroTipo} aria-label="Filtrar por tipo" onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400">
        <option value="">Todos los tipos</option>
        <option value="perdida">Perdida</option>
        <option value="encontrada">Encontrada</option>
      </select>

      <select bind:value={filtroEspecie} aria-label="Filtrar por especie" onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400">
        <option value="">Todas las especies</option>
        {#each ESPECIES as especie}
          <option value={especie}>{especie}</option>
        {/each}
      </select>

      <select bind:value={filtroProvincia} aria-label="Filtrar por provincia" onchange={cargarMascotas}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400">
        <option value="">Todas las provincias</option>
        {#each PROVINCIAS as provincia}
          <option value={provincia}>{provincia}</option>
        {/each}
      </select>

      <button
        onclick={() => { filtroTipo = ""; filtroEspecie = ""; filtroProvincia = ""; filtroNombre = ""; cargarMascotas(); }}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors">
        Limpiar
      </button>

      <button
        class="px-3 py-2 rounded-lg text-sm cursor-pointer transition-colors {mostrarMapa ? 'bg-orange-500 text-white border border-orange-500' : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'}"
        onclick={() => (mostrarMapa = !mostrarMapa)}>
        {mostrarMapa ? "Ocultar mapa" : "🗺️ Ver en mapa"}
      </button>
    </div>
  </div>

  {#if mostrarMapa}
    <div transition:slide class="mb-6 rounded-xl overflow-hidden">
      <Mapa {mascotas} />
    </div>
  {/if}

  {#if cargando}
    <div class="text-center py-16 text-gray-400 dark:text-gray-500">Cargando...</div>

  {:else if mascotas.length === 0}
    <div class="w-full h-48 bg-orange-50 dark:bg-gray-700 flex items-center justify-center">
      <img src="/favicon.png" alt="sin foto" class="w-16 h-16 opacity-40" />
    </div>

  {:else}
    <p class="text-sm text-gray-400 dark:text-gray-500 mb-4">
      {mascotas.length} {mascotas.length === 1 ? 'resultado' : 'resultados'}
      · Página {paginaActual} de {totalPaginas}
    </p>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each mascotasPagina as mascota}
        <a href="/mascotas/{mascota.id}" class="no-underline">
          <div class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow cursor-pointer">

            {#if mascota.imagenes && mascota.imagenes.length > 0}
              <img
                src="http://localhost:8000{mascota.imagenes[0].url}"
                alt={mascota.nombre ?? "Mascota"}
                class="w-full h-48 object-cover"
              />
            {:else}
              <div class="w-full h-48 bg-orange-50 dark:bg-gray-700 flex items-center justify-center">
                <img src="/favicon.png" alt="sin foto" class="w-16 h-16 opacity-40" />
              </div>
            {/if}

            <div class="p-4">
              <div class="flex items-center gap-2 mb-2">
                <span class="text-xs font-semibold px-2 py-0.5 rounded-full {mascota.tipo === 'perdida' ? 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-300' : 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300'}">
                  {mascota.tipo}
                </span>
                <span class="text-xs text-gray-500 dark:text-gray-400">{mascota.especie}</span>
              </div>
              <h2 class="font-semibold text-gray-800 dark:text-gray-100 text-base mb-1">{mascota.nombre ?? "Sin nombre"}</h2>
              <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">📍 {mascota.localidad}, {mascota.provincia}</p>
              <p class="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">{mascota.descripcion ?? ""}</p>
            </div>
          </div>
        </a>
      {/each}
    </div>

    {#if totalPaginas > 1}
      <div class="flex justify-center items-center gap-2 mt-8">
        <button
          onclick={() => irAPagina(paginaActual - 1)}
          disabled={paginaActual === 1}
          class="px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-600 text-sm text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer transition-colors">
          ← Anterior
        </button>

        {#each Array.from({ length: totalPaginas }, (_, i) => i + 1) as n}
          <button
            onclick={() => irAPagina(n)}
            class="px-3 py-2 rounded-lg border text-sm cursor-pointer transition-colors {n === paginaActual ? 'bg-orange-500 text-white border-orange-500' : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'}">
            {n}
          </button>
        {/each}

        <button
          onclick={() => irAPagina(paginaActual + 1)}
          disabled={paginaActual === totalPaginas}
          class="px-3 py-2 rounded-lg border border-gray-200 dark:border-gray-600 text-sm text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-30 disabled:cursor-not-allowed cursor-pointer transition-colors">
          Siguiente →
        </button>
      </div>
    {/if}
  {/if}

</main>