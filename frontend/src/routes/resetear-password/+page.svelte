<script>
  import { goto } from "$app/navigation";
  // page nos da acceso a la URL actual, incluyendo los parámetros de búsqueda
  import { page } from "$app/state";

  // Variables reactivas del formulario
  let nuevaPassword = $state("");
  let confirmar = $state("");
  let cargando = $state(false);
  let exito = $state(false);
  let error = $state("");

  // Extraemos el token de la URL: /resetear-password?token=XXXXX
  // Si el usuario llega sin token, mostramos un error
  const token = page.url.searchParams.get("token");

  async function handleSubmit() {
    // Validaciones en el frontend antes de llamar al backend
    if (nuevaPassword !== confirmar) {
      error = "Las contraseñas no coinciden.";
      return;
    }
    if (nuevaPassword.length < 6) {
      error = "La contraseña debe tener al menos 6 caracteres.";
      return;
    }

    cargando = true;
    error = "";

    try {
      const res = await fetch(
        "http://localhost:8000/usuarios/resetear-password",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          // Enviamos el token y la nueva contraseña al backend
          body: JSON.stringify({ token, nueva_password: nuevaPassword }),
        },
      );

      if (res.ok) {
        exito = true;
        // Redirigimos al login automáticamente después de 3 segundos
        setTimeout(() => goto("/login"), 3000);
      } else {
        const datos = await res.json();
        // ?? es el operador nullish: si detail es null/undefined usa el texto por defecto
        error = datos.detail ?? "Ha ocurrido un error. Inténtalo de nuevo.";
      }
    } catch (e) {
      error = "No se pudo conectar con el servidor.";
    }
    cargando = false;
  }
</script>

<svelte:head>
  <title>Nueva contraseña — PetFinder</title>
</svelte:head>

<main
  class="min-h-screen flex items-center justify-center px-4 bg-gray-50 dark:bg-gray-900"
>
  <div
    class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 p-8 flex flex-col gap-5"
  >
    {#if !token}
      <!-- Si no hay token en la URL, el enlace no es válido -->
      <div class="text-center">
        <p class="text-4xl mb-4">⚠️</p>
        <h1 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-2">
          Enlace no válido
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
          Este enlace no es válido o ha caducado.
        </p>
        <a
          href="/olvide-password"
          class="text-orange-500 font-medium hover:text-orange-600 no-underline text-sm"
        >
          Solicitar nuevo enlace
        </a>
      </div>
    {:else if exito}
      <!-- Pantalla de éxito: se muestra tras actualizar la contraseña -->
      <div class="text-center">
        <p class="text-4xl mb-4">✅</p>
        <h1 class="text-xl font-bold text-gray-800 dark:text-gray-100 mb-2">
          Contraseña actualizada
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Redirigiendo al login en unos segundos...
        </p>
      </div>
    {:else}
      <!-- Formulario para introducir la nueva contraseña -->
      <div class="text-center mb-2">
        <p class="text-3xl mb-2">🔑</p>
        <h1 class="text-2xl font-bold text-gray-800 dark:text-gray-100">
          Nueva contraseña
        </h1>
        <p class="text-sm text-gray-400 dark:text-gray-500 mt-1">
          Elige una contraseña segura
        </p>
      </div>

      {#if error}
        <p
          class="bg-red-50 dark:bg-red-900 text-red-600 dark:text-red-300 text-sm px-4 py-3 rounded-lg"
        >
          {error}
        </p>
      {/if}

      <!-- Campo nueva contraseña -->
      <div class="flex flex-col gap-1">
        <label
          for="password"
          class="text-sm font-semibold text-gray-700 dark:text-gray-200"
          >Nueva contraseña</label
        >
        <input
          id="password"
          type="password"
          bind:value={nuevaPassword}
          placeholder="Mínimo 6 caracteres"
          disabled={cargando}
          class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors"
        />
      </div>

      <!-- Campo confirmar contraseña: debe coincidir con el anterior -->
      <div class="flex flex-col gap-1">
        <label
          for="confirmar"
          class="text-sm font-semibold text-gray-700 dark:text-gray-200"
          >Confirmar contraseña</label
        >
        <input
          id="confirmar"
          type="password"
          bind:value={confirmar}
          placeholder="Repite la contraseña"
          disabled={cargando}
          class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg text-sm bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:border-orange-400 transition-colors"
        />
      </div>

      <!-- Botón de guardar: desactivado mientras carga -->
      <button
        onclick={handleSubmit}
        disabled={cargando}
        class="w-full py-2.5 bg-orange-500 text-white font-medium rounded-lg border-none cursor-pointer hover:bg-orange-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm"
      >
        {cargando ? "Guardando..." : "Guardar contraseña"}
      </button>
    {/if}
  </div>
</main>
