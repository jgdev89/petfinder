<script>
  // Función para llamar al endpoint de login del backend
  import { login } from "$lib/api.js";
  // Función para guardar el token JWT en localStorage tras el login
  import { guardarSesion } from "$lib/auth.js";
  // goto permite redirigir al usuario a otra página
  import { goto } from "$app/navigation";

  // Variables reactivas del formulario
  let email = $state("");
  let password = $state("");
  let cargando = $state(false); // Desactiva el botón mientras se procesa
  let error = $state(""); // Mensaje de error si el login falla

  async function handleSubmit() {
    cargando = true;
    error = "";

    // Llamamos al backend con el email y password
    const datos = await login(email, password);

    if (datos.access_token) {
      // Si el backend devuelve un token, guardamos la sesión y redirigimos al inicio
      guardarSesion(datos.access_token);
      goto("/");
    } else {
      // Si no hay token, mostramos el error
      error = "Email o contraseña incorrectos.";
      cargando = false;
    }
  }
</script>

<svelte:head>
  <title>Iniciar sesión — PetFinder</title>
</svelte:head>

<main
  class="min-h-screen flex items-center justify-center px-4 bg-gray-50 dark:bg-gray-900"
>
  <div
    class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-8 flex flex-col gap-5"
  >
    <!-- Cabecera del formulario -->
    <div class="text-center mb-2">
      <p class="text-3xl mb-2">🐾</p>
      <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100">
        Iniciar sesión
      </h1>
      <p class="text-sm text-gray-400 dark:text-gray-500 mt-1">
        Bienvenido de nuevo
      </p>
    </div>

    <!-- Mensaje de error: solo se muestra si error tiene contenido -->
    {#if error}
      <p
        class="bg-red-50 dark:bg-red-900 text-red-600 dark:text-red-300 text-sm px-4 py-3 rounded-lg"
      >
        {error}
      </p>
    {/if}

    <!-- Campo email: bind:value sincroniza el input con la variable email -->
    <div class="flex flex-col gap-1">
      <label
        for="email"
        class="text-sm font-semibold text-gray-700 dark:text-gray-300"
        >Email</label
      >
      <input
        id="email"
        type="email"
        bind:value={email}
        placeholder="tu@email.com"
        disabled={cargando}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors"
      />
    </div>

    <!-- Campo contraseña -->
    <div class="flex flex-col gap-1">
      <label
        for="password"
        class="text-sm font-semibold text-gray-700 dark:text-gray-300"
        >Contraseña</label
      >
      <input
        id="password"
        type="password"
        bind:value={password}
        placeholder="Tu contraseña"
        disabled={cargando}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors"
      />
    </div>

    <!-- Enlace de recuperación de contraseña -->
    <div class="text-right">
      <a
        href="/olvide-password"
        class="text-xs text-gray-400 dark:text-gray-500 hover:text-orange-500 no-underline transition-colors"
      >
        ¿Olvidaste tu contraseña?
      </a>
    </div>

    <!-- Botón de submit: se desactiva mientras carga.
         disabled:opacity-50 lo atenúa visualmente cuando está desactivado -->
    <button
      onclick={handleSubmit}
      disabled={cargando}
      class="w-full py-2.5 bg-orange-500 text-white font-medium rounded-lg border-none cursor-pointer hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm mt-1"
    >
      {cargando ? "Entrando..." : "Entrar"}
    </button>

    <!-- Enlace al registro -->
    <p class="text-center text-sm text-gray-400 dark:text-gray-500">
      ¿No tienes cuenta? <a
        href="/registro"
        class="text-orange-500 font-medium hover:text-orange-600 no-underline"
        >Regístrate</a
      >
    </p>
  </div>
</main>
