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
      goto('/login');
    } else if (datos.detail) {
      error = datos.detail;
      cargando = false;
    } else {
      error = 'Ha ocurrido un error. Inténtalo de nuevo.';
      cargando = false;
    }
  }
</script>

<main class="min-h-screen flex items-center justify-center px-4 bg-gray-50 dark:bg-gray-900">
  <div class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-8 flex flex-col gap-5">
    <div class="text-center mb-2">
      <p class="text-3xl mb-2">🐾</p>
      <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100">Crear cuenta</h1>
      <p class="text-sm text-gray-400 dark:text-gray-500 mt-1">Únete a PetFinder</p>
    </div>

    {#if error}
      <p class="bg-red-50 dark:bg-red-900 text-red-600 dark:text-red-300 text-sm px-4 py-3 rounded-lg">{error}</p>
    {/if}

    <div class="flex flex-col gap-1">
      <label for="nombre" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Nombre</label>
      <input id="nombre" type="text" bind:value={nombre} placeholder="Tu nombre" disabled={cargando}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors" />
    </div>

    <div class="flex flex-col gap-1">
      <label for="email" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Email</label>
      <input id="email" type="email" bind:value={email} placeholder="tu@email.com" disabled={cargando}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors" />
    </div>

    <div class="flex flex-col gap-1">
      <label for="password" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Contraseña</label>
      <input id="password" type="password" bind:value={password} placeholder="Elige una contraseña" disabled={cargando}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors" />
    </div>

    <div class="flex flex-col gap-1">
      <label for="telefono" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Teléfono <span class="text-gray-400 font-normal">(opcional)</span></label>
      <input id="telefono" type="tel" bind:value={telefono} placeholder="612345678" disabled={cargando}
        class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors" />
    </div>

    <button onclick={handleSubmit} disabled={cargando}
      class="w-full py-2.5 bg-orange-500 text-white font-medium rounded-lg border-none cursor-pointer hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm mt-1">
      {cargando ? 'Creando cuenta...' : 'Crear cuenta'}
    </button>

    <p class="text-center text-sm text-gray-400 dark:text-gray-500">
      ¿Ya tienes cuenta? <a href="/login" class="text-orange-500 font-medium hover:text-orange-600 no-underline">Inicia sesión</a>
    </p>
  </div>
</main>