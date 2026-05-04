<!-- 
  Footer.svelte
  Componente del pie de página, aparece en todas las páginas de la app
  porque lo importamos en el layout principal (+layout.svelte)
-->

<!-- 
  bg-amber-50 → fondo crema suave en modo claro
  dark:bg-gray-900 → fondo oscuro coherente con el navbar en modo oscuro
  border-t → línea fina arriba que separa el footer del contenido
  dark:border-gray-700 → línea más oscura en modo oscuro
  mt-auto → empuja el footer hacia abajo si la página tiene poco contenido
-->
<footer class="bg-amber-50 dark:bg-gray-900 border-t border-amber-200 dark:border-gray-700 mt-auto">

  <!-- 
    Contenedor centrado con ancho máximo
    max-w-6xl → no se expande más allá de ~1152px en pantallas grandes
    mx-auto → se centra horizontalmente
    px-4 → padding horizontal para que no pegue a los bordes en móvil
    py-10 → espacio vertical arriba y abajo
  -->
  <div class="max-w-6xl mx-auto px-4 py-10">

    <!-- 
      Grid de tres columnas
      grid-cols-1 → en móvil, una sola columna (las secciones se apilan)
      md:grid-cols-3 → en pantallas medianas y grandes, tres columnas en fila
      gap-8 → espacio entre columnas
      mb-8 → margen inferior antes de la línea de copyright
    -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">

      <!-- COLUMNA 1: Marca -->
      <div>
        <!-- 
          Nombre de la app con emoji de huella
          dark:text-orange-400 → naranja más suave para no saturar en fondo oscuro
        -->
        <h3 class="text-amber-700 dark:text-orange-400 font-semibold text-lg mb-2">🐾 PetFinder</h3>
        <!-- 
          Tagline corto
          dark:text-gray-400 → gris suave en modo oscuro, legible sin saturar
        -->
        <p class="text-amber-600 dark:text-gray-400 text-sm">Ayudando a reunir familias desde 2025</p>
      </div>

      <!-- COLUMNA 2: Navegación -->
      <div>
        <!-- dark:text-orange-400 → coherente con el título de marca en oscuro -->
        <h4 class="text-amber-700 dark:text-orange-400 font-semibold mb-3">Navegación</h4>
        <!-- 
          Lista de enlaces internos
          space-y-2 → espacio vertical entre cada elemento de la lista
          dark:text-gray-400 → gris legible en fondo oscuro
          dark:hover:text-orange-400 → al pasar el ratón vuelve al naranja de marca
        -->
        <ul class="space-y-2 text-sm">
          <li><a href="/" class="text-amber-600 dark:text-gray-400 hover:text-amber-800 dark:hover:text-orange-400 transition-colors">Inicio</a></li>
          <li><a href="/?tipo=perdida" class="text-amber-600 dark:text-gray-400 hover:text-amber-800 dark:hover:text-orange-400 transition-colors">Mascotas perdidas</a></li>
          <li><a href="/?tipo=encontrada" class="text-amber-600 dark:text-gray-400 hover:text-amber-800 dark:hover:text-orange-400 transition-colors">Mascotas encontradas</a></li>
          <li><a href="/como-funciona" class="text-amber-600 dark:text-gray-400 hover:text-amber-800 dark:hover:text-orange-400 transition-colors">Cómo funciona</a></li>
        </ul>
      </div>

      <!-- COLUMNA 3: Legal y contacto -->
      <div>
        <h4 class="text-amber-700 dark:text-orange-400 font-semibold mb-3">Legal</h4>
        <!-- 
          Lista de enlaces legales y contacto
          mailto: hace que al hacer clic se abra el cliente de correo
          del usuario con ese email ya puesto en el destinatario
        -->
        <ul class="space-y-2 text-sm">
          <li><a href="mailto:petfinder.app.es@gmail.com" class="text-amber-600 dark:text-gray-400 hover:text-amber-800 dark:hover:text-orange-400 transition-colors">Contacto</a></li>
          <li><a href="/privacidad" class="text-amber-600 dark:text-gray-400 hover:text-amber-800 dark:hover:text-orange-400 transition-colors">Política de privacidad</a></li>
          <li><a href="/terminos" class="text-amber-600 dark:text-gray-400 hover:text-amber-800 dark:hover:text-orange-400 transition-colors">Términos de uso</a></li>
        </ul>
      </div>

    </div>

    <!-- 
      Línea inferior con copyright
      border-t → línea separadora
      dark:border-gray-700 → línea coherente con el borde del footer en oscuro
      pt-6 → espacio entre la línea y el texto
      text-center → centra el texto
    -->
    <div class="border-t border-amber-200 dark:border-gray-700 pt-6 text-center">
      <!-- dark:text-gray-500 → gris tenue, discreto en modo oscuro -->
      <p class="text-amber-500 dark:text-gray-500 text-sm">© 2025 PetFinder · Todos los derechos reservados</p>
    </div>

  </div>
</footer>