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
  let usuarioActualId = $state(null);
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
        usuarioActualId = perfil.id;
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
    if (!tokenActual) {
      goto("/login");
      return;
    }
    mostrarFormulario = true;
  }

  async function handleEnviar() {
    enviando = true;
    errorMensaje = "";

    const tokenActual = get(token);
    const datos = await enviarMensaje(
      {
        destinatario_id: mascota.usuario_id,
        mascota_id: mascota.id,
        asunto,
        contenido,
      },
      tokenActual,
    );

    if (datos.id) {
      mostrarFormulario = false;
      mensajeEnviado = true;
    } else if (datos.detail) {
      errorMensaje = datos.detail;
    } else {
      errorMensaje = "Ha ocurrido un error. Inténtalo de nuevo.";
    }
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
  <main>
    <p>Cargando...</p>
  </main>
{:else if error || !mascota}
  <main>
    <a href="/">← Volver al listado</a>
    <p class="error">No se ha encontrado esta mascota.</p>
  </main>
{:else}
  <main>
    <a href="/" class="volver">← Volver al listado</a>

    <div class="cabecera">
      <span class="tipo {mascota.tipo}">{mascota.tipo}</span>
      <h1>{mascota.nombre ?? "Sin nombre"}</h1>
    </div>

    {#if imagenes.length > 0}
      <div class="galeria">
        {#each imagenes as img}
          <img
            src="http://localhost:8000{img.url}"
            alt={mascota.nombre ?? "Mascota"}
            class="foto-detalle"
          />
        {/each}
      </div>
    {/if}

    <div class="info">
      <p><strong>Especie:</strong> {mascota.especie}</p>
      {#if mascota.raza}<p><strong>Raza:</strong> {mascota.raza}</p>{/if}
      {#if mascota.color}<p><strong>Color:</strong> {mascota.color}</p>{/if}
      <p><strong>Ubicación:</strong> {mascota.localidad}, {mascota.provincia}</p>
      <p><strong>Fecha:</strong> {mascota.fecha_suceso}</p>
      <p><strong>Estado:</strong> {mascota.estado}</p>
    </div>

    {#if mascota.descripcion}
      <div class="descripcion">
        <h2>Descripción</h2>
        <p>{mascota.descripcion}</p>
      </div>
    {/if}

    {#if esDueno}
      <div class="acciones-dueno">
        <h2>Gestionar publicación</h2>
        <div class="botones-dueno">
          <a href="/mascotas/{mascota.id}/editar" class="btn-editar">Editar</a>
          {#if mascota.estado === "activo"}
            <button onclick={handleResolver} class="btn-resolver">
              Marcar como resuelto
            </button>
          {/if}
          <button onclick={handleEliminar} class="btn-eliminar">
            Eliminar
          </button>
        </div>
      </div>
    {/if}

    <div class="contacto">
      <h2>¿Tienes información?</h2>
      <p>Si has visto a esta mascota o tienes alguna información, contacta con quien publicó este caso.</p>

      {#if mensajeEnviado}
        <p class="exito">✓ Mensaje enviado correctamente.</p>
      {:else if mostrarFormulario}
        <div class="formulario-mensaje">
          {#if errorMensaje}
            <p class="error">{errorMensaje}</p>
          {/if}
          <div class="campo">
            <label for="asunto">Asunto</label>
            <input id="asunto" type="text" bind:value={asunto} placeholder="Ej: He visto a tu perro" disabled={enviando} />
          </div>
          <div class="campo">
            <label for="contenido">Mensaje</label>
            <textarea id="contenido" bind:value={contenido} placeholder="Escribe aquí tu mensaje..." rows="4" disabled={enviando}></textarea>
          </div>
          <div class="botones">
            <button class="btn-enviar" onclick={handleEnviar} disabled={enviando}>
              {enviando ? "Enviando..." : "Enviar mensaje"}
            </button>
            <button class="btn-cancelar" onclick={() => (mostrarFormulario = false)} disabled={enviando}>
              Cancelar
            </button>
          </div>
        </div>
      {:else}
        <button class="btn-contactar" onclick={abrirFormulario}>Contactar</button>
      {/if}
    </div>
  </main>
{/if}

<style>
  main {
    max-width: 700px;
    margin: 0 auto;
    padding: 2rem;
  }

  .volver {
    display: inline-block;
    margin-bottom: 1.5rem;
    color: #555;
    text-decoration: none;
  }

  .volver:hover { color: #000; }

  .cabecera {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  h1 { margin: 0; }

  .tipo {
    font-size: 0.8rem;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-weight: bold;
    white-space: nowrap;
  }

  .perdida { background: #ffe0e0; color: #c00; }
  .encontrada { background: #e0ffe0; color: #060; }

  .info {
    background: #f5f5f5;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
    margin-bottom: 1.5rem;
  }

  .descripcion { margin-bottom: 1.5rem; }
  .descripcion h2 { font-size: 1.1rem; margin-bottom: 0.5rem; }

  .acciones-dueno {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
  }

  .acciones-dueno h2 {
    font-size: 1.1rem;
    margin-bottom: 1rem;
  }

  .botones-dueno {
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
  }

  .btn-editar {
    padding: 0.5rem 1rem;
    background: #333;
    color: white;
    border-radius: 6px;
    text-decoration: none;
    font-size: 0.95rem;
  }

  .btn-resolver {
    padding: 0.5rem 1rem;
    background: #060;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.95rem;
  }

  .btn-eliminar {
    padding: 0.5rem 1rem;
    background: white;
    color: #c00;
    border: 1px solid #c00;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.95rem;
  }

  .btn-eliminar:hover { background: #ffe0e0; }

  .contacto {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 2rem;
  }

  .contacto h2 { font-size: 1.1rem; margin-bottom: 0.5rem; }
  .contacto > p { color: #555; margin-bottom: 1rem; }

  .btn-contactar {
    background: #333;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
  }

  .formulario-mensaje {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
  }

  .campo { display: flex; flex-direction: column; gap: 0.3rem; }

  label { font-size: 0.9rem; font-weight: bold; color: #333; }

  input, textarea {
    padding: 0.6rem 0.8rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
  }

  input:focus, textarea:focus { outline: none; border-color: #555; }

  .botones { display: flex; gap: 0.8rem; }

  .btn-enviar {
    background: #333;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
  }

  .btn-enviar:disabled { background: #aaa; cursor: not-allowed; }

  .btn-cancelar {
    background: white;
    color: #333;
    border: 1px solid #ddd;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
  }

  .exito {
    color: #060;
    background: #e0ffe0;
    padding: 0.6rem 0.8rem;
    border-radius: 6px;
  }

  .error {
    color: #c00;
    background: #ffe0e0;
    padding: 0.6rem 0.8rem;
    border-radius: 6px;
  }

  .galeria {
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
  }

  .foto-detalle {
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
  }
</style>