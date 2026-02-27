<script>
  import { listarMascotas } from '$lib/api.js';
  import { ESPECIES, PROVINCIAS } from '$lib/datos.js';

  let mascotas = $state([]);
  let cargando = $state(true);

  let filtroTipo = $state('');
  let filtroEspecie = $state('');
  let filtroProvincia = $state('');
  let filtroNombre = $state('');

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

  cargarMascotas();
</script>

<main>
  <h1>PetFinder</h1>
  <p>Mascotas perdidas y encontradas en España</p>

  <div class="filtros">
    <input
      type="text"
      bind:value={filtroNombre}
      placeholder="Buscar por nombre..."
      oninput={cargarMascotas}
      class="buscador"
    />

    <div class="filtros-secundarios">
      <select bind:value={filtroTipo} onchange={cargarMascotas}>
        <option value="">Todos los tipos</option>
        <option value="perdida">Perdida</option>
        <option value="encontrada">Encontrada</option>
      </select>

      <select bind:value={filtroEspecie} onchange={cargarMascotas}>
        <option value="">Todas las especies</option>
        {#each ESPECIES as especie}
          <option value={especie}>{especie}</option>
        {/each}
      </select>

      <select bind:value={filtroProvincia} onchange={cargarMascotas}>
        <option value="">Todas las provincias</option>
        {#each PROVINCIAS as provincia}
          <option value={provincia}>{provincia}</option>
        {/each}
      </select>

      <button onclick={() => {
        filtroTipo = '';
        filtroEspecie = '';
        filtroProvincia = '';
        filtroNombre = '';
        cargarMascotas();
      }}>
        Limpiar
      </button>
    </div>
  </div>

  {#if cargando}
    <p>Cargando...</p>
  {:else if mascotas.length === 0}
    <p>No hay mascotas que coincidan con los filtros.</p>
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

  .filtros {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
    margin-top: 1.5rem;
  }

  .buscador {
    padding: 0.6rem 1rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
    width: 100%;
    box-sizing: border-box;
  }

  .buscador:focus {
    outline: none;
    border-color: #555;
  }

  .filtros-secundarios {
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
  }

  .filtros-secundarios select {
    padding: 0.5rem 0.8rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 0.95rem;
    font-family: inherit;
    background: white;
  }

  .filtros-secundarios button {
    padding: 0.5rem 1rem;
    background: white;
    border: 1px solid #ddd;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.95rem;
    color: #555;
  }

  .filtros-secundarios button:hover {
    background: #f5f5f5;
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