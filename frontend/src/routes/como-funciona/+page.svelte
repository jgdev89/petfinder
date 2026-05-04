<!-- frontend/src/routes/como-funciona/+page.svelte -->
<svelte:head>
  <title>Cómo funciona — PetFinder</title>
</svelte:head>

<main class="max-w-3xl mx-auto px-4 py-12">

  <div class="text-center mb-12">
    <h1 class="text-3xl font-bold text-gray-800 dark:text-gray-100 mb-3">¿Cómo funciona PetFinder?</h1>
    <p class="text-gray-500 dark:text-gray-400">Una plataforma sencilla para reunir mascotas perdidas con sus familias</p>
  </div>

  <!-- Pasos -->
  <div class="flex flex-col gap-8 mb-16">

    <!-- Paso 1 -->
    <div class="flex gap-5 items-start">
      <div class="w-12 h-12 rounded-full bg-orange-100 dark:bg-orange-900 flex items-center justify-center text-orange-500 font-bold text-lg shrink-0">1</div>
      <div>
        <h2 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-1">Crea una cuenta</h2>
        <p class="text-gray-500 dark:text-gray-400 text-sm leading-relaxed">Regístrate gratis con tu nombre, email y contraseña. Solo te llevará un minuto y podrás empezar a publicar casos de inmediato.</p>
      </div>
    </div>

    <!-- Paso 2 -->
    <div class="flex gap-5 items-start">
      <div class="w-12 h-12 rounded-full bg-orange-100 dark:bg-orange-900 flex items-center justify-center text-orange-500 font-bold text-lg shrink-0">2</div>
      <div>
        <h2 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-1">Publica el caso</h2>
        <p class="text-gray-500 dark:text-gray-400 text-sm leading-relaxed">¿Has perdido a tu mascota o has encontrado una? Publica un caso con una foto, la descripción y la ubicación. Cuanta más información incluyas, más fácil será encontrarla.</p>
      </div>
    </div>

    <!-- Paso 3 -->
    <div class="flex gap-5 items-start">
      <div class="w-12 h-12 rounded-full bg-orange-100 dark:bg-orange-900 flex items-center justify-center text-orange-500 font-bold text-lg shrink-0">3</div>
      <div>
        <h2 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-1">La comunidad te ayuda</h2>
        <p class="text-gray-500 dark:text-gray-400 text-sm leading-relaxed">Cualquier usuario que reconozca a tu mascota puede contactarte directamente a través de la plataforma. Recibirás sus mensajes en tu bandeja de entrada.</p>
      </div>
    </div>

    <!-- Paso 4 -->
    <div class="flex gap-5 items-start">
      <div class="w-12 h-12 rounded-full bg-orange-100 dark:bg-orange-900 flex items-center justify-center text-orange-500 font-bold text-lg shrink-0">4</div>
      <div>
        <h2 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-1">¡Reunidos!</h2>
        <p class="text-gray-500 dark:text-gray-400 text-sm leading-relaxed">Cuando tu mascota vuelva a casa, marca el caso como resuelto para que la comunidad sepa que ya está a salvo.</p>
      </div>
    </div>

  </div>

  <!-- Consejos -->
  <div class="bg-orange-50 dark:bg-gray-800 rounded-2xl p-6 mb-10">
    <h2 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-4">💡 Consejos para encontrar antes a tu mascota</h2>
    <ul class="flex flex-col gap-3 text-sm text-gray-600 dark:text-gray-400">
      <li class="flex gap-2"><span class="text-orange-500">•</span> Incluye siempre una foto clara y reciente.</li>
      <li class="flex gap-2"><span class="text-orange-500">•</span> Describe señas particulares: manchas, cicatrices, collar, chip, etc.</li>
      <li class="flex gap-2"><span class="text-orange-500">•</span> Indica la fecha y lugar exacto donde se perdió o fue encontrada.</li>
      <li class="flex gap-2"><span class="text-orange-500">•</span> Revisa los mensajes recibidos con frecuencia.</li>
      <li class="flex gap-2"><span class="text-orange-500">•</span> Si encuentras una mascota, publícala aunque no sepas de quién es.</li>
    </ul>
  </div>

  <!-- CTA -->
  <div class="text-center">
    <a href="/registro" class="inline-block px-8 py-3 bg-orange-500 hover:bg-orange-600 text-white font-medium rounded-full no-underline transition-colors">
      Empezar ahora
    </a>
  </div>

</main>