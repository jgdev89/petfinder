<script>
  // Store del token de autenticación
  import { token } from "$lib/auth.js";
  // Listas de especies y provincias disponibles
  import { ESPECIES, PROVINCIAS } from "$lib/datos.js";
  // goto permite navegar a otra ruta programáticamente
  import { goto } from "$app/navigation";
  // get lee el valor actual de un store fuera del template
  import { get } from "svelte/store";
  // Funciones para crear la mascota y subir su imagen al backend
  import { crearMascota, subirImagen } from "$lib/api.js";
  // onMount se ejecuta cuando el componente se monta en el DOM
  import { onMount } from "svelte";

  // Protección de ruta: si no hay sesión activa al cargar la página, redirige al login
  onMount(() => {
    if (!get(token)) {
      goto("/login");
    }
  });

  // Variables reactivas del formulario — $state() las hace reactivas en Svelte 5
  let tipo = $state("perdida");       // Valor por defecto: perdida
  let nombre = $state("");
  let especie = $state("");
  let localidad = $state("");
  let provincia = $state("");
  let fecha_suceso = $state("");
  let descripcion = $state("");
  let raza = $state("");
  let color = $state("");
  let imagen = $state(null);          // Archivo de imagen seleccionado
  let cargando = $state(false);       // Desactiva el formulario mientras se envía
  let error = $state("");             // Mensaje de error del backend

  async function handleSubmit() {
    cargando = true;
    error = "";
    const tokenActual = get(token);

    // Doble seguridad: si no hay token al enviar, redirigimos al login
    if (!tokenActual) {
      goto("/login");
      return;
    }

    // Construimos el objeto con los datos del formulario
    // || null convierte strings vacíos en null para los campos opcionales
    const datos = {
      tipo,
      nombre: nombre || null,
      especie,
      localidad,
      provincia,
      fecha_suceso,
      descripcion,
      raza: raza || null,
      color: color || null,
    };

    // Primero creamos la mascota en el backend
    const resultado = await crearMascota(datos, tokenActual);

    if (resultado.id) {
      // Si hay imagen seleccionada, la subimos después de crear la mascota
      // Necesitamos el ID de la mascota recién creada para asociarla
      if (imagen) await subirImagen(resultado.id, imagen, tokenActual);
      // Redirigimos al detalle de la nueva mascota
      goto(`/mascotas/${resultado.id}`);
    } else if (resultado.detail) {
      // FastAPI devuelve los errores de validación en el campo "detail"
      error = resultado.detail;
      cargando = false;
    } else {
      error = "Ha ocurrido un error. Inténtalo de nuevo.";
      cargando = false;
    }
  }
</script>

<svelte:head>
  <title>Publicar mascota — PetFinder</title>
</svelte:head>

<main class="max-w-xl mx-auto px-4 py-8">

  <!-- Enlace de vuelta al listado -->
  <a href="/" class="text-gray-400 dark:text-gray-500 hover:text-orange-500 text-sm no-underline transition-colors">
    ← Volver al listado
  </a>

  <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mt-4 mb-6">Publicar mascota</h1>

  <!-- Mensaje de error del backend, solo visible si hay error -->
  {#if error}
    <p class="bg-red-50 dark:bg-red-900 text-red-600 dark:text-red-300 text-sm px-4 py-3 rounded-lg mb-4">{error}</p>
  {/if}

  <div class="flex flex-col gap-5">

    <!-- Tipo: radio buttons para perdida/encontrada.
         bind:group sincroniza ambos radios con la variable tipo -->
    <div class="flex flex-col gap-2">
      <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">Tipo</span>
      <div class="flex gap-4">
        <label class="flex items-center gap-2 cursor-pointer text-sm text-gray-600 dark:text-gray-300">
          <input type="radio" bind:group={tipo} value="perdida" class="accent-orange-500" />
          Perdida
        </label>
        <label class="flex items-center gap-2 cursor-pointer text-sm text-gray-600 dark:text-gray-300">
          <input type="radio" bind:group={tipo} value="encontrada" class="accent-orange-500" />
          Encontrada
        </label>
      </div>
    </div>

    <!-- Especie: select con opciones generadas dinámicamente desde ESPECIES -->
    <div class="flex flex-col gap-1">
      <label for="especie" class="text-sm font-semibold text-gray-700 dark:text-gray-200">
        Especie <span class="text-red-400 font-normal">*</span>
      </label>
      <select id="especie" bind:value={especie} disabled={cargando} required
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400 transition-colors">
        <option value="">Selecciona una especie</option>
        {#each ESPECIES as e}
          <option value={e}>{e}</option>
        {/each}
      </select>
    </div>

    <!-- Nombre (opcional) -->
    <div class="flex flex-col gap-1">
      <label for="nombre" class="text-sm font-semibold text-gray-700 dark:text-gray-200">
        Nombre <span class="text-gray-400 font-normal">(opcional)</span>
      </label>
      <input id="nombre" type="text" bind:value={nombre} placeholder="Nombre de la mascota"
        disabled={cargando}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-400 focus:outline-none focus:border-orange-400 transition-colors" />
    </div>

    <!-- Raza y Color en dos columnas con grid -->
    <div class="grid grid-cols-2 gap-4">
      <div class="flex flex-col gap-1">
        <label for="raza" class="text-sm font-semibold text-gray-700 dark:text-gray-200">
          Raza <span class="text-gray-400 font-normal">(opcional)</span>
        </label>
        <input id="raza" type="text" bind:value={raza} placeholder="Golden, siamés..."
          disabled={cargando}
          class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-400 focus:outline-none focus:border-orange-400 transition-colors" />
      </div>
      <div class="flex flex-col gap-1">
        <label for="color" class="text-sm font-semibold text-gray-700 dark:text-gray-200">
          Color <span class="text-gray-400 font-normal">(opcional)</span>
        </label>
        <input id="color" type="text" bind:value={color} placeholder="Negro, blanco..."
          disabled={cargando}
          class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-400 focus:outline-none focus:border-orange-400 transition-colors" />
      </div>
    </div>

    <!-- Localidad y Provincia en dos columnas -->
    <div class="grid grid-cols-2 gap-4">
      <div class="flex flex-col gap-1">
        <label for="localidad" class="text-sm font-semibold text-gray-700 dark:text-gray-200">
          Localidad <span class="text-red-400 font-normal">*</span>
        </label>
        <!-- pattern valida que solo contenga letras españolas y espacios -->
        <input id="localidad" type="text" bind:value={localidad} placeholder="Gijón"
          disabled={cargando} required
          pattern="^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s'\-]+$"
          class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-400 focus:outline-none focus:border-orange-400 transition-colors" />
      </div>
      <div class="flex flex-col gap-1">
        <label for="provincia" class="text-sm font-semibold text-gray-700 dark:text-gray-200">
          Provincia <span class="text-red-400 font-normal">*</span>
        </label>
        <select id="provincia" bind:value={provincia} disabled={cargando} required
          class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400 transition-colors">
          <option value="">Selecciona una provincia</option>
          {#each PROVINCIAS as p}
            <option value={p}>{p}</option>
          {/each}
        </select>
      </div>
    </div>

    <!-- Fecha del suceso -->
    <div class="flex flex-col gap-1">
      <label for="fecha_suceso" class="text-sm font-semibold text-gray-700 dark:text-gray-200">
        Fecha del suceso <span class="text-red-400 font-normal">*</span>
      </label>
      <input id="fecha_suceso" type="date" bind:value={fecha_suceso} disabled={cargando} required
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400 transition-colors" />
    </div>

    <!-- Descripción: textarea de 4 filas, resize-none evita que el usuario lo redimensione -->
    <div class="flex flex-col gap-1">
      <label for="descripcion" class="text-sm font-semibold text-gray-700 dark:text-gray-200">
        Descripción <span class="text-red-400 font-normal">*</span>
      </label>
      <textarea id="descripcion" bind:value={descripcion} rows="4" disabled={cargando} required
        placeholder="Describe la mascota, dónde se perdió, señas particulares..."
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-400 focus:outline-none focus:border-orange-400 transition-colors resize-none"></textarea>
    </div>

    <!-- Input de archivo: cuando cambia guardamos el archivo en imagen -->
    <div class="flex flex-col gap-1">
      <label for="imagen" class="text-sm font-semibold text-gray-700 dark:text-gray-200">
        Foto <span class="text-gray-400 font-normal">(opcional)</span>
      </label>
      <input id="imagen" type="file" accept="image/jpeg, image/png, image/webp"
        onchange={(e) => (imagen = e.target.files[0])} disabled={cargando}
        class="text-sm text-gray-500 dark:text-gray-400 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-orange-50 file:text-orange-600 hover:file:bg-orange-100 cursor-pointer" />
      <!-- Muestra el nombre del archivo seleccionado -->
      {#if imagen}
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">📎 {imagen.name}</p>
      {/if}
    </div>

    <!-- Botón de publicar: desactivado mientras se está enviando -->
    <button onclick={handleSubmit} disabled={cargando}
      class="w-full py-2.5 bg-orange-500 text-white font-medium rounded-lg border-none cursor-pointer hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm mt-2">
      {cargando ? "Publicando..." : "Publicar"}
    </button>

  </div>
</main>