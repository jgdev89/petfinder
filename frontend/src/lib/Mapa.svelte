<script>
  import { onMount, onDestroy } from "svelte";

  // Las mascotas llegan como prop desde la página principal.
  let { mascotas } = $props();

  let mapContainer;
  let mapa;

  // Nominatim tiene un límite de uso — esperamos 1 segundo entre peticiones
  // para no ser bloqueados.
  async function geocodificar(localidad, provincia) {
    const query = `${localidad}, ${provincia}, España`;
    const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=1`;

    try {
      const res = await fetch(url, {
        headers: {
          // Nominatim requiere un User-Agent identificativo.
          "User-Agent": "PetFinder-TFG/1.0",
        },
      });
      const datos = await res.json();
      if (datos.length > 0) {
        return { lat: parseFloat(datos[0].lat), lng: parseFloat(datos[0].lon) };
      }
    } catch (e) {
      console.error("Error geocodificando:", e);
    }
    return null;
  }

  function esperar(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  onMount(async () => {
    // Leaflet solo funciona en el navegador (no en SSR),
    // por eso lo importamos dentro de onMount.
    const L = await import("leaflet");
    await import("leaflet/dist/leaflet.css");

    // Corregimos el icono por defecto de Leaflet que falla con bundlers.
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl:
        "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
      iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
      shadowUrl:
        "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
    });

    // Centramos el mapa en España.
    mapa = L.map(mapContainer).setView([40.4, -3.7], 6);

    // Cargamos las teselas (tiles) de OpenStreetMap.
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(mapa);

    // Geocodificamos cada mascota y añadimos su marcador.
    for (const mascota of mascotas) {
      const coords = await geocodificar(mascota.localidad, mascota.provincia);
      if (coords) {
        const imagenHtml =
          mascota.imagenes && mascota.imagenes.length > 0
            ? `<img src="http://localhost:8000${mascota.imagenes[0].url}" style="width:100%;height:120px;object-fit:cover;border-radius:4px;margin-bottom:6px;" />`
            : "";

        const popup = `
      <div style="width:180px;">
        ${imagenHtml}
        <strong>${mascota.nombre ?? "Sin nombre"}</strong><br>
        ${mascota.especie} · ${mascota.tipo}<br>
        <a href="/mascotas/${mascota.id}">Ver más</a>
      </div>
    `;

        L.marker([coords.lat, coords.lng]).addTo(mapa).bindPopup(popup);
      }
      // Esperamos 1 segundo entre peticiones a Nominatim.
      await esperar(1000);
    }
  });

  onDestroy(() => {
    // Limpiamos el mapa cuando el componente se desmonta
    // para evitar errores si se navega a otra página.
    if (mapa) mapa.remove();
  });
</script>

<div bind:this={mapContainer} class="mapa"></div>

<style>
  .mapa {
    width: 100%;
    height: 450px;
    border-radius: 8px;
    border: 1px solid #ddd;
    margin-top: 2rem;
  }
</style>
