<script>
  import { obtenerMascota, editarMascota, obtenerImagenes, subirImagen, eliminarImagen } from '$lib/api.js';
  import { token } from '$lib/auth.js';
  import { ESPECIES, PROVINCIAS } from '$lib/datos.js';
  import { page } from '$app/state';
  import { get } from 'svelte/store';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let tipo = $state('perdida');
  let nombre = $state('');
  let especie = $state('');
  let localidad = $state('');
  let provincia = $state('');
  let fecha_suceso = $state('');
  let descripcion = $state('');
  let raza = $state('');
  let color = $state('');

  let imagenes = $state([]);
  let nuevaImagen = $state(null);

  let cargando = $state(true);
  let guardando = $state(false);
  let error = $state('');

  onMount(async () => {
    const tokenActual = get(token);
    if (!tokenActual) {
      goto('/login');
      return;
    }

    const mascota = await obtenerMascota(page.params.id);
    imagenes = await obtenerImagenes(page.params.id);

    tipo = mascota.tipo;
    nombre = mascota.nombre ?? '';
    especie = mascota.especie;
    localidad = mascota.localidad;
    provincia = mascota.provincia;
    fecha_suceso = mascota.fecha_suceso;
    descripcion = mascota.descripcion ?? '';
    raza = mascota.raza ?? '';
    color = mascota.color ?? '';

    cargando = false;
  });

  async function handleEliminarImagen(imagenId) {
    const tokenActual = get(token);
    await eliminarImagen(imagenId, tokenActual);
    imagenes = imagenes.filter(img => img.id !== imagenId);
  }

  async function handleSubirImagen() {
    if (!nuevaImagen) return;
    const tokenActual = get(token);
    const resultado = await subirImagen(page.params.id, nuevaImagen, tokenActual);
    if (resultado.id) {
      imagenes = [...imagenes, resultado];
      nuevaImagen = null;
    }
  }

  async function handleSubmit() {
    guardando = true;
    error = '';

    const tokenActual = get(token);
    const datos = {
      tipo,
      nombre: nombre || null,
      especie,
      localidad,
      provincia,
      fecha_suceso,
      descripcion,
      raza: raza || null,
      color: color || null
    };

    const resultado = await editarMascota(page.params.id, datos, tokenActual);

    if (resultado.id) {
      goto(`/mascotas/${resultado.id}`);
    } else if (resultado.detail) {
      error = resultado.detail;
      guardando = false;
    } else {
      error = 'Ha ocurrido un error. Inténtalo de nuevo.';
      guardando = false;
    }
  }
</script>

{#if cargando}
  <main><p>Cargando...</p></main>
{:else}
  <main>
    <a href="/mascotas/{page.params.id}" class="volver">← Volver al detalle</a>

    <h1>Editar publicación</h1>

    {#if error}
      <p class="error">{error}</p>
    {/if}

    <!-- Gestión de imágenes -->
    <div class="seccion-imagenes">
      <h2>Fotos</h2>

      {#if imagenes.length > 0}
        <div class="galeria-editar">
          {#each imagenes as img}
            <div class="img-wrapper">
              <img src="http://localhost:8000{img.url}" alt="Foto mascota" />
              <button class="btn-quitar" onclick={() => handleEliminarImagen(img.id)}>✕</button>
            </div>
          {/each}
        </div>
      {:else}
        <p class="sin-fotos">Sin fotos todavía.</p>
      {/if}

      <div class="subir-nueva">
        <input
          type="file"
          accept="image/jpeg, image/png, image/webp"
          onchange={(e) => nuevaImagen = e.target.files[0]}
        />
        {#if nuevaImagen}
          <button class="btn-subir" onclick={handleSubirImagen}>Subir foto</button>
        {/if}
      </div>
    </div>

    <form>
      <div class="campo">
        <label>Tipo</label>
        <div class="radio-grupo">
          <label class="radio">
            <input type="radio" bind:group={tipo} value="perdida" />
            Perdida
          </label>
          <label class="radio">
            <input type="radio" bind:group={tipo} value="encontrada" />
            Encontrada
          </label>
        </div>
      </div>

      <div class="campo">
        <label for="especie">Especie <span class="requerido">*</span></label>
        <select id="especie" bind:value={especie} disabled={guardando}>
          <option value="">Selecciona una especie</option>
          {#each ESPECIES as e}
            <option value={e}>{e}</option>
          {/each}
        </select>
      </div>

      <div class="campo">
        <label for="nombre">Nombre <span class="opcional">(opcional)</span></label>
        <input id="nombre" type="text" bind:value={nombre} placeholder="Nombre de la mascota" disabled={guardando} />
      </div>

      <div class="fila">
        <div class="campo">
          <label for="raza">Raza <span class="opcional">(opcional)</span></label>
          <input id="raza" type="text" bind:value={raza} placeholder="Golden, siamés..." disabled={guardando} />
        </div>
        <div class="campo">
          <label for="color">Color <span class="opcional">(opcional)</span></label>
          <input id="color" type="text" bind:value={color} placeholder="Negro, blanco..." disabled={guardando} />
        </div>
      </div>

      <div class="fila">
        <div class="campo">
          <label for="localidad">Localidad <span class="requerido">*</span></label>
          <input id="localidad" type="text" bind:value={localidad} placeholder="Gijón" disabled={guardando} />
        </div>
        <div class="campo">
          <label for="provincia">Provincia <span class="requerido">*</span></label>
          <select id="provincia" bind:value={provincia} disabled={guardando}>
            <option value="">Selecciona una provincia</option>
            {#each PROVINCIAS as p}
              <option value={p}>{p}</option>
            {/each}
          </select>
        </div>
      </div>

      <div class="campo">
        <label for="fecha_suceso">Fecha del suceso <span class="requerido">*</span></label>
        <input id="fecha_suceso" type="date" bind:value={fecha_suceso} disabled={guardando} />
      </div>

      <div class="campo">
        <label for="descripcion">Descripción <span class="requerido">*</span></label>
        <textarea id="descripcion" bind:value={descripcion} placeholder="Describe la mascota..." rows="4" disabled={guardando}></textarea>
      </div>

      <button onclick={handleSubmit} disabled={guardando}>
        {guardando ? 'Guardando...' : 'Guardar cambios'}
      </button>
    </form>
  </main>
{/if}

<style>
  main {
    max-width: 600px;
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

  h1 { margin-bottom: 1.5rem; }

  h2 { font-size: 1.1rem; margin-bottom: 0.8rem; }

  .seccion-imagenes {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.2rem;
    margin-bottom: 1.5rem;
  }

  .galeria-editar {
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
  }

  .img-wrapper {
    position: relative;
    width: 120px;
    height: 120px;
  }

  .img-wrapper img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 6px;
  }

  .btn-quitar {
    position: absolute;
    top: 4px;
    right: 4px;
    background: rgba(0,0,0,0.6);
    color: white;
    border: none;
    border-radius: 50%;
    width: 22px;
    height: 22px;
    font-size: 0.75rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
  }

  .btn-quitar:hover { background: #c00; }

  .subir-nueva {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    flex-wrap: wrap;
  }

  .btn-subir {
    padding: 0.4rem 0.8rem;
    background: #333;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
  }

  .sin-fotos {
    color: #888;
    font-size: 0.9rem;
    margin-bottom: 0.8rem;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
  }

  .campo {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
    flex: 1;
  }

  .fila {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  label { font-size: 0.9rem; font-weight: bold; color: #333; }
  .requerido { color: #c00; font-weight: normal; }
  .opcional { font-weight: normal; color: #888; }

  input, textarea, select {
    padding: 0.6rem 0.8rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
    background: white;
  }

  input:focus, textarea:focus, select:focus {
    outline: none;
    border-color: #555;
  }

  .radio-grupo { display: flex; gap: 1.5rem; }

  .radio {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-weight: normal;
    cursor: pointer;
  }

  button {
    padding: 0.7rem;
    background: #333;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 1rem;
    cursor: pointer;
    margin-top: 0.5rem;
  }

  button:disabled { background: #aaa; cursor: not-allowed; }

  .error {
    background: #ffe0e0;
    color: #c00;
    padding: 0.6rem 0.8rem;
    border-radius: 6px;
    font-size: 0.9rem;
    margin-bottom: 1rem;
  }
</style>