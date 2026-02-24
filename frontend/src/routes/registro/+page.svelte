<script>
  import { registrar } from '$lib/api.js';
  import { goto } from '$app/navigation';

  let nombre = $state('');
  let email = $state('');
  let password = $state('');
  let telefono = $state('');

  let cargando = $state(false);
  let error = $state('');

  async function handleSubmit() {
    cargando = true;
    error = '';

    const datos = await registrar(nombre, email, password, telefono);

    if (datos.id) {
      // Si el backend devuelve un id, el usuario se creó correctamente.
      // Redirigimos al login para que inicie sesión con sus nuevas credenciales.
      goto('/login');
    } else if (datos.detail) {
      // FastAPI devuelve los errores en el campo "detail".
      // Por ejemplo: "El email ya está registrado".
      error = datos.detail;
      cargando = false;
    } else {
      error = 'Ha ocurrido un error. Inténtalo de nuevo.';
      cargando = false;
    }
  }
</script>

<main>
  <div class="formulario">
    <h1>Crear cuenta</h1>

    {#if error}
      <p class="error">{error}</p>
    {/if}

    <div class="campo">
      <label for="nombre">Nombre</label>
      <input
        id="nombre"
        type="text"
        bind:value={nombre}
        placeholder="Tu nombre"
        disabled={cargando}
      />
    </div>

    <div class="campo">
      <label for="email">Email</label>
      <input
        id="email"
        type="email"
        bind:value={email}
        placeholder="tu@email.com"
        disabled={cargando}
      />
    </div>

    <div class="campo">
      <label for="password">Contraseña</label>
      <input
        id="password"
        type="password"
        bind:value={password}
        placeholder="Elige una contraseña"
        disabled={cargando}
      />
    </div>

    <div class="campo">
      <label for="telefono">Teléfono <span class="opcional">(opcional)</span></label>
      <input
        id="telefono"
        type="tel"
        bind:value={telefono}
        placeholder="612345678"
        disabled={cargando}
      />
    </div>

    <button onclick={handleSubmit} disabled={cargando}>
      {cargando ? 'Creando cuenta...' : 'Crear cuenta'}
    </button>

    <p class="login">
      ¿Ya tienes cuenta? <a href="/login">Inicia sesión</a>
    </p>
  </div>
</main>

<style>
  main {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
  }

  .formulario {
    width: 100%;
    max-width: 400px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  h1 {
    margin-bottom: 0.5rem;
  }

  .campo {
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
  }

  label {
    font-size: 0.9rem;
    font-weight: bold;
    color: #333;
  }

  .opcional {
    font-weight: normal;
    color: #888;
  }

  input {
    padding: 0.6rem 0.8rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
  }

  input:focus {
    outline: none;
    border-color: #555;
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
  }

  .login {
    text-align: center;
    font-size: 0.9rem;
    color: #555;
  }
</style>