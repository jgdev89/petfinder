<script>
  import { obtenerMensajes } from '$lib/api.js';
  import { token } from '$lib/auth.js';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let mensajes = $state([]);
  let cargando = $state(true);

  onMount(() => {
    // Nos suscribimos al store token.
    // Cada vez que el token cambie (incluso al recuperarse del localStorage),
    // esta función se ejecuta con el valor actualizado.
    const unsuscribir = token.subscribe(async (tokenActual) => {
      if (tokenActual === null) return; // Aún no sabemos si hay sesión, esperamos.

      if (tokenActual === undefined) {
        goto('/login');
        return;
      }

      mensajes = await obtenerMensajes(tokenActual);
      cargando = false;
      unsuscribir(); // Dejamos de escuchar una vez que tenemos los datos.
    });

    // Si tras 1 segundo el token sigue siendo null, no hay sesión.
    setTimeout(() => {
      if (cargando) {
        goto('/login');
      }
    }, 1000);
  });

  function formatearFecha(fechaStr) {
    const fecha = new Date(fechaStr);
    return fecha.toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  }
</script>

<main>
  <h1>Mensajes recibidos</h1>

  {#if cargando}
    <p>Cargando...</p>

  {:else if mensajes.length === 0}
    <p class="vacio">No tienes mensajes todavía.</p>

  {:else}
    <div class="lista">
      {#each mensajes as mensaje}
        <div class="mensaje {mensaje.leido ? 'leido' : 'no-leido'}">
          <div class="cabecera">
            <span class="asunto">{mensaje.asunto}</span>
            <span class="fecha">{formatearFecha(mensaje.fecha_envio)}</span>
          </div>
          <p class="contenido">{mensaje.contenido}</p>
          {#if mensaje.mascota_id}
            <a href="/mascotas/{mensaje.mascota_id}" class="enlace-mascota">
              Ver mascota →
            </a>
          {/if}
          {#if !mensaje.leido}
            <span class="badge">Nuevo</span>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</main>

<style>
  main {
    max-width: 700px;
    margin: 0 auto;
    padding: 2rem;
  }

  h1 {
    margin-bottom: 1.5rem;
  }

  .vacio {
    color: #888;
  }

  .lista {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .mensaje {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1.2rem;
    position: relative;
  }

  .no-leido {
    border-left: 3px solid #333;
    background: #fafafa;
  }

  .leido {
    opacity: 0.7;
  }

  .cabecera {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
  }

  .asunto {
    font-weight: bold;
    font-size: 1rem;
  }

  .fecha {
    font-size: 0.85rem;
    color: #888;
  }

  .contenido {
    color: #444;
    margin-bottom: 0.8rem;
    line-height: 1.5;
  }

  .enlace-mascota {
    font-size: 0.85rem;
    color: #555;
    text-decoration: none;
  }

  .enlace-mascota:hover {
    color: #000;
  }

  .badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: #333;
    color: white;
    font-size: 0.7rem;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
  }
</style>