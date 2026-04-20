<script>
  import { onMount, onDestroy } from "svelte";

  // Las mascotas llegan como prop desde la página principal.
  // Ahora incluyen latitud y longitud guardadas en la BD.
  let { mascotas } = $props();

  // Referencia al elemento div del DOM donde Leaflet inicializará el mapa.
  // bind:this nos da acceso directo al nodo DOM real.
  let mapContainer;
  let mapa;

  onMount(async () => {
    // Leaflet solo funciona en el navegador (no en SSR),
    // por eso lo importamos dinámicamente dentro de onMount.
    const L = await import("leaflet");
    await import("leaflet/dist/leaflet.css");

    // Corregimos el icono por defecto de Leaflet que falla con bundlers modernos
    // porque no puede resolver las rutas relativas de los PNG del marcador.
    // La solución es apuntar directamente a las URLs absolutas de unpkg.com.
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
      iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
      shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
    });

    // Inicializamos el mapa centrado en España con zoom nivel 6
    mapa = L.map(mapContainer).setView([40.4, -3.7], 6);

    // Cargamos las teselas (tiles) de OpenStreetMap — gratuitas y sin API key
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(mapa);

    // Iteramos sobre las mascotas y colocamos un marcador por cada una
    // que tenga coordenadas guardadas en la base de datos.
    // Ya no llamamos a Nominatim aquí — las coordenadas vienen del backend.
    for (const mascota of mascotas) {

      // Si la mascota no tiene coordenadas (la geocodificación falló al publicar),
      // simplemente la saltamos — no aparecerá en el mapa.
      if (!mascota.latitud || !mascota.longitud) continue;

      // Construimos el HTML del popup con imagen si la tiene
      const imagenHtml = mascota.imagenes && mascota.imagenes.length > 0
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

      // Añadimos el marcador al mapa con las coordenadas guardadas en la BD
      L.marker([parseFloat(mascota.latitud), parseFloat(mascota.longitud)])
        .addTo(mapa)
        .bindPopup(popup);
    }
  });

  onDestroy(() => {
    // Limpiamos el mapa cuando el componente se desmonta
    // para evitar errores si el usuario navega a otra página
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