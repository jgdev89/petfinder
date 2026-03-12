<script>
  import { token } from "$lib/auth.js";
  import { ESPECIES, PROVINCIAS } from "$lib/datos.js";
  import { goto } from "$app/navigation";
  import { get } from "svelte/store";
  import { crearMascota, subirImagen } from "$lib/api.js";

  let tipo = $state("perdida");
  let nombre = $state("");
  let especie = $state("");
  let localidad = $state("");
  let provincia = $state("");
  let fecha_suceso = $state("");
  let descripcion = $state("");
  let raza = $state("");
  let color = $state("");
  let imagen = $state(null);
  let cargando = $state(false);
  let error = $state("");

  async function handleSubmit() {
    cargando = true;
    error = "";
    const tokenActual = get(token);
    if (!tokenActual) { goto("/login"); return; }

    const datos = {
      tipo, nombre: nombre || null, especie, localidad, provincia,
      fecha_suceso, descripcion, raza: raza || null, color: color || null,
    };

    const resultado = await crearMascota(datos, tokenActual);

    if (resultado.id) {
      if (imagen) await subirImagen(resultado.id, imagen, tokenActual);
      goto(`/mascotas/${resultado.id}`);
    } else if (resultado.detail) {
      error = resultado.detail;
      cargando = false;
    } else {
      error = "Ha ocurrido un error. Inténtalo de nuevo.";
      cargando = false;
    }
  }
</script>

<main class="max-w-xl mx-auto px-4 py-8">

  <a href="/" class="text-gray-400 dark:text-gray-500 hover:text-orange-500 text-sm no-underline transition-colors">← Volver al listado</a>

  <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mt-4 mb-6">Publicar mascota</h1>

  {#if error}
    <p class="bg-red-50 dark:bg-red-900 text-red-600 dark:text-red-300 text-sm px-4 py-3 rounded-lg mb-4">{error}</p>
  {/if}

  <div class="flex flex-col gap-5">

    <!-- Tipo -->
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

    <!-- Especie -->
    <div class="flex flex-col gap-1">
      <label for="especie" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Especie <span class="text-red-400 font-normal">*</span></label>
      <select id="especie" bind:value={especie} disabled={cargando}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400 transition-colors">
        <option value="">Selecciona una especie</option>
        {#each ESPECIES as e}
          <option value={e}>{e}</option>
        {/each}
      </select>
    </div>

    <!-- Nombre -->
    <div class="flex flex-col gap-1">
      <label for="nombre" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Nombre <span class="text-gray-400 font-normal">(opcional)</span></label>
      <input id="nombre" type="text" bind:value={nombre} placeholder="Nombre de la mascota" disabled={cargando}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors" />
    </div>

    <!-- Raza y Color -->
    <div class="grid grid-cols-2 gap-4">
      <div class="flex flex-col gap-1">
        <label for="raza" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Raza <span class="text-gray-400 font-normal">(opcional)</span></label>
        <input id="raza" type="text" bind:value={raza} placeholder="Golden, siamés..." disabled={cargando}
          class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors" />
      </div>
      <div class="flex flex-col gap-1">
        <label for="color" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Color <span class="text-gray-400 font-normal">(opcional)</span></label>
        <input id="color" type="text" bind:value={color} placeholder="Negro, blanco..." disabled={cargando}
          class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors" />
      </div>
    </div>

    <!-- Localidad y Provincia -->
    <div class="grid grid-cols-2 gap-4">
      <div class="flex flex-col gap-1">
        <label for="localidad" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Localidad <span class="text-red-400 font-normal">*</span></label>
        <input id="localidad" type="text" bind:value={localidad} placeholder="Gijón" disabled={cargando}
          class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors" />
      </div>
      <div class="flex flex-col gap-1">
        <label for="provincia" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Provincia <span class="text-red-400 font-normal">*</span></label>
        <select id="provincia" bind:value={provincia} disabled={cargando}
          class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400 transition-colors">
          <option value="">Selecciona una provincia</option>
          {#each PROVINCIAS as p}
            <option value={p}>{p}</option>
          {/each}
        </select>
      </div>
    </div>

    <!-- Fecha -->
    <div class="flex flex-col gap-1">
      <label for="fecha_suceso" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Fecha del suceso <span class="text-red-400 font-normal">*</span></label>
      <input id="fecha_suceso" type="date" bind:value={fecha_suceso} disabled={cargando}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:outline-none focus:border-orange-400 transition-colors" />
    </div>

    <!-- Descripción -->
    <div class="flex flex-col gap-1">
      <label for="descripcion" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Descripción <span class="text-red-400 font-normal">*</span></label>
      <textarea id="descripcion" bind:value={descripcion} rows="4" disabled={cargando}
        placeholder="Describe la mascota, dónde se perdió, señas particulares..."
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors resize-none"></textarea>
    </div>

    <!-- Foto -->
    <div class="flex flex-col gap-1">
      <label for="imagen" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Foto <span class="text-gray-400 font-normal">(opcional)</span></label>
      <input id="imagen" type="file" accept="image/jpeg, image/png, image/webp"
        onchange={(e) => (imagen = e.target.files[0])} disabled={cargando}
        class="text-sm text-gray-500 dark:text-gray-400 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-orange-50 file:text-orange-600 hover:file:bg-orange-100 cursor-pointer" />
      {#if imagen}
        <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">📎 {imagen.name}</p>
      {/if}
    </div>

    <!-- Botón -->
    <button onclick={handleSubmit} disabled={cargando}
      class="w-full py-2.5 bg-orange-500 text-white font-medium rounded-lg border-none cursor-pointer hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm mt-2">
      {cargando ? "Publicando..." : "Publicar"}
    </button>

  </div>

</main>