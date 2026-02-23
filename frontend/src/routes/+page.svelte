<script>
  import { listarMascotas } from '$lib/api.js';

  let mascotas = $state([]);
  let cargando = $state(true);

  async function cargarMascotas() {
    mascotas = await listarMascotas();
    cargando = false;
  }

  cargarMascotas();
</script>

<main>
  <h1>PetFinder</h1>
  <p>Mascotas perdidas y encontradas en España</p>

  {#if cargando}
    <p>Cargando...</p>
  {:else if mascotas.length === 0}
    <p>No hay mascotas publicadas todavía.</p>
  {:else}
    <div class="listado">
      {#each mascotas as mascota}
        <div class="tarjeta">
          <span class="tipo {mascota.tipo}">{mascota.tipo}</span>
          <h2>{mascota.nombre ?? 'Sin nombre'}</h2>
          <p>{mascota.especie} · {mascota.localidad}, {mascota.provincia}</p>
          <p>{mascota.descripcion}</p>
          <a href="/mascotas/{mascota.id}">Ver más</a>
        </div>
      {/each}
    </div>
  {/if}
</main>

<style>
  main {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
  }

  .listado {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1rem;
    margin-top: 2rem;
  }

  .tarjeta {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
  }

  .tipo {
    font-size: 0.8rem;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-weight: bold;
  }

  .perdida { background: #ffe0e0; color: #c00; }
  .encontrada { background: #e0ffe0; color: #060; }
</style>