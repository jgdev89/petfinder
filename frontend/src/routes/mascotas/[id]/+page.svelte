<script>
  import { obtenerMascota, enviarMensaje, obtenerImagenes, eliminarMascota, resolverMascota, miPerfil } from '$lib/api.js';
  import { token } from "$lib/auth.js";
  import { page } from "$app/state";
  import { get } from "svelte/store";
  import { goto } from "$app/navigation";

  let imagenes = $state([]);
  let mascota = $state(null);
  let cargando = $state(true);
  let error = $state(false);
  let esDueno = $state(false);

  let mostrarFormulario = $state(false);
  let asunto = $state("");
  let contenido = $state("");
  let enviando = $state(false);
  let mensajeEnviado = $state(false);
  let errorMensaje = $state("");

  async function cargar() {
    try {
      mascota = await obtenerMascota(page.params.id);
      imagenes = await obtenerImagenes(page.params.id);
      const tokenActual = get(token);
      if (tokenActual) {
        const perfil = await miPerfil(tokenActual);
        esDueno = perfil.id === mascota.usuario_id;
      }
    } catch (e) {
      error = true;
    } finally {
      cargando = false;
    }
  }

  function abrirFormulario() {
    const tokenActual = get(token);
    if (!tokenActual) { goto("/login"); return; }
    mostrarFormulario = true;
  }

  async function handleEnviar() {
    enviando = true;
    errorMensaje = "";
    const tokenActual = get(token);
    const datos = await enviarMensaje({ destinatario_id: mascota.usuario_id, mascota_id: mascota.id, asunto, contenido }, tokenActual);
    if (datos.id) { mostrarFormulario = false; mensajeEnviado = true; }
    else if (datos.detail) { errorMensaje = datos.detail; }
    else { errorMensaje = "Ha ocurrido un error. Inténtalo de nuevo."; }
    enviando = false;
  }

  async function handleEliminar() {
    if (!confirm("¿Seguro que quieres eliminar esta publicación?")) return;
    const tokenActual = get(token);
    await eliminarMascota(mascota.id, tokenActual);
    goto("/perfil");
  }

  async function handleResolver() {
    if (!confirm("¿Marcar este caso como resuelto?")) return;
    const tokenActual = get(token);
    await resolverMascota(mascota.id, tokenActual);
    mascota = { ...mascota, estado: "resuelto" };
  }

  cargar();
</script>

{#if cargando}
  <main class="max-w-2xl mx-auto px-4 py-8">
    <p class="text-gray-400 dark:text-gray-500">Cargando...</p>
  </main>

{:else if error || !mascota}
  <main class="max-w-2xl mx-auto px-4 py-8">
    <a href="/" class="text-gray-500 dark:text-gray-400 hover:text-orange-500 text-sm no-underline">← Volver al listado</a>
    <p class="mt-4 text-red-500 bg-red-50 dark:bg-red-900 dark:text-red-300 px-4 py-3 rounded-lg">No se ha encontrado esta mascota.</p>
  </main>

{:else}
  <main class="max-w-2xl mx-auto px-4 py-8">

    <a href="/" class="text-gray-400 dark:text-gray-500 hover:text-orange-500 text-sm no-underline transition-colors">← Volver al listado</a>

    <!-- Cabecera -->
    <div class="flex items-center gap-3 mt-4 mb-6">
      <span class="text-xs font-semibold px-2.5 py-1 rounded-full {mascota.tipo === 'perdida' ? 'bg-red-100 text-red-600 dark:bg-red-900 dark:text-red-300' : 'bg-green-100 text-green-600 dark:bg-green-900 dark:text-green-300'}">
        {mascota.tipo}
      </span>
      <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100 m-0">{mascota.nombre ?? "Sin nombre"}</h1>
      {#if mascota.estado === 'resuelto'}
        <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400">resuelto</span>
      {/if}
    </div>

    <!-- Galería -->
    {#if imagenes.length > 0}
      <div class="flex gap-3 flex-wrap mb-6">
        {#each imagenes as img}
          <img
            src="http://localhost:8000{img.url}"
            alt={mascota.nombre ?? "Mascota"}
            class="w-48 h-48 object-cover rounded-xl"
          />
        {/each}
      </div>
    {:else}
      <div class="w-full h-48 bg-orange-50 dark:bg-gray-700 rounded-xl flex items-center justify-center text-4xl mb-6">🐾</div>
    {/if}

    <!-- Info -->
    <div class="bg-gray-50 dark:bg-gray-800 rounded-xl px-5 py-4 flex flex-col gap-2 mb-6 text-sm text-gray-600 dark:text-gray-300">
      <p><span class="font-semibold text-gray-700 dark:text-gray-200">Especie:</span> {mascota.especie}</p>
      {#if mascota.raza}<p><span class="font-semibold text-gray-700 dark:text-gray-200">Raza:</span> {mascota.raza}</p>{/if}
      {#if mascota.color}<p><span class="font-semibold text-gray-700 dark:text-gray-200">Color:</span> {mascota.color}</p>{/if}
      <p><span class="font-semibold text-gray-700 dark:text-gray-200">Ubicación:</span> 📍 {mascota.localidad}, {mascota.provincia}</p>
      <p><span class="font-semibold text-gray-700 dark:text-gray-200">Fecha:</span> {mascota.fecha_suceso}</p>
      <p><span class="font-semibold text-gray-700 dark:text-gray-200">Estado:</span> {mascota.estado}</p>
    </div>

    <!-- Descripción -->
    {#if mascota.descripcion}
      <div class="mb-6">
        <h2 class="text-base font-semibold text-gray-700 dark:text-gray-200 mb-2">Descripción</h2>
        <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">{mascota.descripcion}</p>
      </div>
    {/if}

    <!-- Acciones dueño -->
    {#if esDueno}
      <div class="border border-gray-100 dark:border-gray-700 rounded-xl p-5 mb-6">
        <h2 class="text-base font-semibold text-gray-700 dark:text-gray-200 mb-3">Gestionar publicación</h2>
        <div class="flex flex-wrap gap-2">
          <a href="/mascotas/{mascota.id}/editar" class="px-4 py-2 bg-gray-800 dark:bg-gray-600 text-white text-sm rounded-lg no-underline hover:bg-gray-700 dark:hover:bg-gray-500 transition-colors">
            Editar
          </a>
          {#if mascota.estado === "activo"}
            <button onclick={handleResolver} class="px-4 py-2 bg-green-600 text-white text-sm rounded-lg border-none cursor-pointer hover:bg-green-700 transition-colors">
              Marcar como resuelto
            </button>
          {/if}
          <button onclick={handleEliminar} class="px-4 py-2 bg-white dark:bg-gray-800 text-red-500 text-sm rounded-lg border border-red-200 dark:border-red-800 cursor-pointer hover:bg-red-50 dark:hover:bg-red-900 transition-colors">
            Eliminar
          </button>
        </div>
      </div>
    {/if}

    <!-- Contacto -->
    <div class="border border-orange-100 dark:border-orange-900 rounded-xl p-5 bg-orange-50 dark:bg-gray-800">
      <h2 class="text-base font-semibold text-gray-700 dark:text-gray-200 mb-1">¿Tienes información?</h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">Si has visto a esta mascota o tienes alguna información, contacta con quien publicó este caso.</p>

      {#if mensajeEnviado}
        <p class="text-green-700 dark:text-green-300 bg-green-100 dark:bg-green-900 px-4 py-2 rounded-lg text-sm">✓ Mensaje enviado correctamente.</p>

      {:else if mostrarFormulario}
        <div class="flex flex-col gap-3">
          {#if errorMensaje}
            <p class="text-red-600 dark:text-red-300 bg-red-50 dark:bg-red-900 px-4 py-2 rounded-lg text-sm">{errorMensaje}</p>
          {/if}
          <div class="flex flex-col gap-1">
            <label for="asunto" class="text-sm font-semibold text-gray-600 dark:text-gray-300">Asunto</label>
            <input id="asunto" type="text" bind:value={asunto} placeholder="Ej: He visto a tu perro" disabled={enviando}
              class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors" />
          </div>
          <div class="flex flex-col gap-1">
            <label for="contenido" class="text-sm font-semibold text-gray-600 dark:text-gray-300">Mensaje</label>
            <textarea id="contenido" bind:value={contenido} placeholder="Escribe aquí tu mensaje..." rows="4" disabled={enviando}
              class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors resize-none"></textarea>
          </div>
          <div class="flex gap-2">
            <button onclick={handleEnviar} disabled={enviando}
              class="px-4 py-2 bg-orange-500 text-white text-sm rounded-lg border-none cursor-pointer hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
              {enviando ? "Enviando..." : "Enviar mensaje"}
            </button>
            <button onclick={() => (mostrarFormulario = false)} disabled={enviando}
              class="px-4 py-2 bg-white dark:bg-gray-700 text-gray-500 dark:text-gray-300 text-sm rounded-lg border border-gray-200 dark:border-gray-600 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors">
              Cancelar
            </button>
          </div>
        </div>

      {:else}
        <button onclick={abrirFormulario} class="px-5 py-2 bg-orange-500 text-white text-sm font-medium rounded-lg border-none cursor-pointer hover:bg-orange-600 transition-colors">
          Contactar
        </button>
      {/if}
    </div>

  </main>
{/if}