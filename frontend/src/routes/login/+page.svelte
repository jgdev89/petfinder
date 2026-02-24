<script>
  import { login } from '$lib/api.js';
  import { guardarSesion } from '$lib/auth.js';
  import { goto } from '$app/navigation';

  // Estas variables almacenan lo que el usuario escribe en el formulario.
  // al ser $state son reactias y se actualizan automáticamente en la interfaz.
  let email = $state('');
  let password = $state('');

  // Variables para mostrar feedback al usuario.
  let cargando = $state(false);
  let error = $state('');

  async function handleSubmit() {
    // Evitamos que el usuario pulse el botón varias veces seguidas.
    cargando = true;
    error = '';

    // Llamamos a la función login() de api.js con los datos del formulario.
    const datos = await login(email, password);

    if (datos.access_token) {
      // Si el backend devuelve un token, la sesión fue correcta.
      // Guardamos el token en el store y en localStorage.
      guardarSesion(datos.access_token);
      // Redirigimos al usuario a la página principal.
      goto('/');
    } else {
      // Si no hay token, el backend devolvió un error (email o password incorrectos).
      error = 'Email o contraseña incorrectos.';
      cargando = false;
    }
  }
</script>

<main>
  <div class="formulario">
    <h1>Iniciar sesión</h1>

    {#if error}
      <p class="error">{error}</p>
    {/if}

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
        placeholder="Tu contraseña"
        disabled={cargando}
      />
    </div>

    <button onclick={handleSubmit} disabled={cargando}>
      {cargando ? 'Entrando...' : 'Entrar'}
    </button>

    <p class="registro">
      ¿No tienes cuenta? <a href="/registro">Regístrate</a>
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

  .registro {
    text-align: center;
    font-size: 0.9rem;
    color: #555;
  }
</style>