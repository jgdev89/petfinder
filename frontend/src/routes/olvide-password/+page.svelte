<script>
  import { goto } from '$app/navigation';

  let email = $state('');
  let cargando = $state(false);
  let enviado = $state(false);
  let error = $state('');

  async function handleSubmit() {
    cargando = true;
    error = '';
    try {
      const res = await fetch('http://localhost:8000/usuarios/solicitar-reseteo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });
      if (res.ok) {
        enviado = true;
      } else {
        error = 'Ha ocurrido un error. Inténtalo de nuevo.';
      }
    } catch (e) {
      error = 'No se pudo conectar con el servidor.';
    }
    cargando = false;
  }
</script>

<main class="min-h-screen flex items-center justify-center px-4 bg-gray-50 dark:bg-gray-900">
  <div class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-8 flex flex-col gap-5">

    {#if enviado}
      <div class="text-center">
        <p class="text-4xl mb-4">✉️</p>
        <h1 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-2">Revisa tu email</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">Si el email está registrado, recibirás un enlace para restablecer tu contraseña en breve.</p>
      </div>
    {:else}
      <div class="text-center mb-2">
        <p class="text-3xl mb-2">🔑</p>
        <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100">¿Olvidaste tu contraseña?</h1>
        <p class="text-sm text-gray-400 dark:text-gray-500 mt-1">Te enviaremos un enlace para restablecerla</p>
      </div>

      {#if error}
        <p class="bg-red-50 dark:bg-red-900 text-red-600 dark:text-red-300 text-sm px-4 py-3 rounded-lg">{error}</p>
      {/if}

      <div class="flex flex-col gap-1">
        <label for="email" class="text-sm font-semibold text-gray-700 dark:text-gray-200">Email</label>
        <input id="email" type="email" bind:value={email} placeholder="tu@email.com" disabled={cargando}
          class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors" />
      </div>

      <button onclick={handleSubmit} disabled={cargando}
        class="w-full py-2.5 bg-orange-500 text-white font-medium rounded-lg border-none cursor-pointer hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm">
        {cargando ? 'Enviando...' : 'Enviar enlace'}
      </button>

      <p class="text-center text-sm text-gray-400 dark:text-gray-500">
        <a href="/login" class="text-orange-500 font-medium hover:text-orange-600 no-underline">Volver al login</a>
      </p>
    {/if}

  </div>
</main>