<script>
  import { obtenerMascota } from '$lib/api.js';
  import { page } from '$app/state';

  let mascota = $state(null);
  let cargando = $state(true);
  let error = $state(false);

  async function cargar() {
    try {
      mascota = await obtenerMascota(page.params.id);
    } catch (e) {
      error = true;
    } finally {
      cargando = false;
    }
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
      <h1>{mascota.nombre ?? 'Sin nombre'}</h1>
    </div>

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

    <div class="contacto">
      <h2>¿Tienes información?</h2>
      <p>Si has visto a esta mascota o tienes alguna información, contacta con quien publicó este caso.</p>
      <button disabled>Enviar mensaje (próximamente)</button>
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

  .volver:hover {
    color: #000;
  }

  .cabecera {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  h1 {
    margin: 0;
  }

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

  .descripcion {
    margin-bottom: 1.5rem;
  }

  .descripcion h2 {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
  }

  .contacto {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 2rem;
  }

  .contacto h2 {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
  }

  .contacto p {
    color: #555;
    margin-bottom: 1rem;
  }

  .contacto button {
    background: #ccc;
    border: none;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    cursor: not-allowed;
    color: #666;
  }

  .error {
    color: #c00;
    margin-top: 1rem;
  }
</style>