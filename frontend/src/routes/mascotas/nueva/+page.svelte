<script>
  import { crearMascota } from '$lib/api.js';
  import { token } from '$lib/auth.js';
  import { goto } from '$app/navigation';
  import { get } from 'svelte/store';

  // Campos obligatorios
  let tipo = $state('perdida');
  let nombre = $state('');
  let especie = $state('');
  let localidad = $state('');
  let provincia = $state('');
  let fecha_suceso = $state('');
  let descripcion = $state('');

  // Campos opcionales
  let raza = $state('');
  let color = $state('');

  let cargando = $state(false);
  let error = $state('');

  async function handleSubmit() {
    cargando = true;
    error = '';

    // get() lee el valor actual del store fuera de un contexto reactivo.
    // Es la forma de leer un store en una función normal (no en el template).
    const tokenActual = get(token);

    if (!tokenActual) {
      // Si no hay token, el usuario no está logueado.
      // Lo mandamos al login antes de que pueda publicar.
      goto('/login');
      return;
    }

    // Construimos el objeto con los datos del formulario.
    // Los campos opcionales solo se incluyen si tienen valor.
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

    const resultado = await crearMascota(datos, tokenActual);

    if (resultado.id) {
      // Si el backend devuelve un id, la mascota se creó correctamente.
      // Redirigimos a la página de detalle de esa mascota.
      goto(`/mascotas/${resultado.id}`);
    } else if (resultado.detail) {
      error = resultado.detail;
      cargando = false;
    } else {
      error = 'Ha ocurrido un error. Inténtalo de nuevo.';
      cargando = false;
    }
  }
</script>

<main>
  <a href="/" class="volver">← Volver al listado</a>

  <h1>Publicar mascota</h1>

  {#if error}
    <p class="error">{error}</p>
  {/if}

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
      <input
        id="especie"
        type="text"
        bind:value={especie}
        placeholder="Perro, gato, conejo..."
        disabled={cargando}
      />
    </div>

    <div class="campo">
      <label for="nombre">Nombre <span class="opcional">(opcional)</span></label>
      <input
        id="nombre"
        type="text"
        bind:value={nombre}
        placeholder="Nombre de la mascota"
        disabled={cargando}
      />
    </div>

    <div class="fila">
      <div class="campo">
        <label for="raza">Raza <span class="opcional">(opcional)</span></label>
        <input
          id="raza"
          type="text"
          bind:value={raza}
          placeholder="Golden, siamés..."
          disabled={cargando}
        />
      </div>

      <div class="campo">
        <label for="color">Color <span class="opcional">(opcional)</span></label>
        <input
          id="color"
          type="text"
          bind:value={color}
          placeholder="Negro, blanco..."
          disabled={cargando}
        />
      </div>
    </div>

    <div class="fila">
      <div class="campo">
        <label for="localidad">Localidad <span class="requerido">*</span></label>
        <input
          id="localidad"
          type="text"
          bind:value={localidad}
          placeholder="Gijón"
          disabled={cargando}
        />
      </div>

      <div class="campo">
        <label for="provincia">Provincia <span class="requerido">*</span></label>
        <input
          id="provincia"
          type="text"
          bind:value={provincia}
          placeholder="Asturias"
          disabled={cargando}
        />
      </div>
    </div>

    <div class="campo">
      <label for="fecha_suceso">Fecha del suceso <span class="requerido">*</span></label>
      <input
        id="fecha_suceso"
        type="date"
        bind:value={fecha_suceso}
        disabled={cargando}
      />
    </div>

    <div class="campo">
      <label for="descripcion">Descripción <span class="requerido">*</span></label>
      <textarea
        id="descripcion"
        bind:value={descripcion}
        placeholder="Describe la mascota, dónde se perdió, señas particulares..."
        rows="4"
        disabled={cargando}
      ></textarea>
    </div>

    <button onclick={handleSubmit} disabled={cargando}>
      {cargando ? 'Publicando...' : 'Publicar'}
    </button>
  </form>
</main>

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

  .volver:hover {
    color: #000;
  }

  h1 {
    margin-bottom: 1.5rem;
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

  label {
    font-size: 0.9rem;
    font-weight: bold;
    color: #333;
  }

  .requerido {
    color: #c00;
    font-weight: normal;
  }

  .opcional {
    font-weight: normal;
    color: #888;
  }

  input, textarea {
    padding: 0.6rem 0.8rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    font-family: inherit;
  }

  input:focus, textarea:focus {
    outline: none;
    border-color: #555;
  }

  .radio-grupo {
    display: flex;
    gap: 1.5rem;
  }

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

  button:disabled {
    background: #aaa;
    cursor: not-allowed;
  }

  .error {
    background: #ffe0e0;
    color: #c00;
    padding: 0.6rem 0.8rem;
    border-radius: 6px;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
  }
</style>