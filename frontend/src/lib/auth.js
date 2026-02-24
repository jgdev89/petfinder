import { writable } from 'svelte/store';

// Este store guarda el token JWT del usuario logueado.
// writable() crea una variable global reactiva con valor inicial null,
// es decir, por defecto no hay ningún usuario logueado.
export const token = writable(null);

// Esta función se llama cuando el usuario hace login con éxito.
// Guarda el token en el store Y en localStorage para que
// si el usuario cierra el navegador y vuelve, siga logueado.
export function guardarSesion(nuevoToken) {
    token.set(nuevoToken);
    localStorage.setItem('token', nuevoToken);
}

// Esta función se llama cuando el usuario hace logout.
// Borra el token del store y del localStorage.
export function cerrarSesion() {
    token.set(null);
    localStorage.removeItem('token');
}

// Esta función se llama al arrancar la app para comprobar
// si ya había un token guardado de una sesión anterior.
export function recuperarSesion() {
    const tokenGuardado = localStorage.getItem('token');
    if (tokenGuardado) {
        token.set(tokenGuardado);
    }
}