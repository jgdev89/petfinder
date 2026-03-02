<script>
  import { miPerfil, misMascotas } from '$lib/api.js';
  import { token } from '$lib/auth.js';
  import { get } from 'svelte/store';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  let usuario = $state(null);
  let mascotas = $state([]);
  let cargando = $state(true);

  onMount(async () => {
    const tokenActual = get(token);
    if (!tokenActual) {
      goto('/login');
      return;
    }

    usuario = await miPerfil(tokenActual);
    mascotas = await misMascotas(tokenActual);
    cargando = false;
  });
</script>

{#if cargando}
  <main><p>Cargando...</p></main>
{:else}
  <main>
    <h1>Mi perfil</h1>

    <div class="info-usuario">
      <p><strong>Nombre:</strong> {usuario.nombre}</p>
      <p><strong>Email:</strong> {usuario.email}</p>
      {#if usuario.telefono}
        <p><strong>Teléfono:</strong> {usuario.telefono}</p>
      {/if}
    </div>

    <h2>Mis publicaciones</h2>

    {#if mascotas.length === 0}
      <p class="vacio">No has publicado ninguna mascota todavía. <a href="/mascotas/nueva">Publicar ahora</a></p>
    {:else}
      <div class="listado">
        {#each mascotas as mascota}
          <div class="tarjeta">
            {#if mascota.imagenes && mascota.imagenes.length > 0}
              <img
                src="http://localhost:8000{mascota.imagenes[0].url}"
                alt={mascota.nombre ?? 'Mascota'}
                class="foto"
              />
            {:else}
              <div class="foto-placeholder">📷</div>
            {/if}
            <div class="tarjeta-body">
              <span class="tipo {mascota.tipo}">{mascota.tipo}</span>
              <h3>{mascota.nombre ?? 'Sin nombre'}</h3>
              <p>{mascota.especie} · {mascota.localidad}, {mascota.provincia}</p>
              <span class="estado {mascota.estado}">{mascota.estado}</span>
              <a href="/mascotas/{mascota.id}">Ver más</a>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </main>
{/if}

<style>
  main {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
  }

  h1 {
    margin-bottom: 1.5rem;
  }

  h2 {
    margin: 2rem 0 1rem;
  }

  .info-usuario {
    background: #f5f5f5;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }

  .listado {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1rem;
  }

  .tarjeta {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
  }

  .foto {
    width: 100%;
    height: 160px;
    object-fit: cover;
  }

  .foto-placeholder {
    width: 100%;
    height: 160px;
    background: #f0f0f0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
  }

  .tarjeta-body {
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.4rem;
  }

  .tarjeta-body h3 {
    margin: 0;
  }

  .tarjeta-body a {
    color: #333;
    font-size: 0.9rem;
  }

  .tipo {
    font-size: 0.75rem;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-weight: bold;
    align-self: flex-start;
  }

  .perdida { background: #ffe0e0; color: #c00; }
  .encontrada { background: #e0ffe0; color: #060; }

  .estado {
    font-size: 0.75rem;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    align-self: flex-start;
  }

  .activo { background: #e0f0ff; color: #006; }
  .resuelto { background: #eee; color: #555; }

  .vacio {
    color: #555;
  }

  .vacio a {
    color: #333;
    font-weight: bold;
  }
</style>