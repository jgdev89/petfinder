const BASE_URL = "http://localhost:8000";

export async function listarMascotas(filtros = {}) {
  const params = new URLSearchParams(filtros);
  const res = await fetch(`${BASE_URL}/mascotas/?${params}`);
  return res.json();
}

export async function obtenerMascota(id) {
  const res = await fetch(`${BASE_URL}/mascotas/${id}`);
  return res.json();
}

export async function login(email, password) {
  const res = await fetch(`${BASE_URL}/usuarios/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username: email, password }),
  });
  return res.json();
}

export async function registrar(nombre, email, password, telefono) {
  const res = await fetch(`${BASE_URL}/usuarios/registro`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nombre, email, password, telefono }),
  });
  return res.json();
}

// Crea una mascota nueva en el backend.
// Necesita el token JWT para identificar al usuario que la publica.
// El token se envía en la cabecera Authorization con el formato "Bearer <token>".
export async function crearMascota(datos, token) {
  const res = await fetch(`${BASE_URL}/mascotas/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(datos),
  });
  return res.json();
}

export async function enviarMensaje(datos, token) {
  const res = await fetch(`${BASE_URL}/mensajes/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(datos),
  });
  return res.json();
}

export async function obtenerMensajes(token) {
  const res = await fetch(`${BASE_URL}/mensajes/recibidos`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return res.json();
}

export async function subirImagen(mascotaId, archivo, token) {
  const formData = new FormData();
  formData.append("file", archivo);

  const res = await fetch(`${BASE_URL}/imagenes/mascota/${mascotaId}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });
  return res.json();
}

export async function obtenerImagenes(mascotaId) {
  const res = await fetch(`${BASE_URL}/imagenes/mascota/${mascotaId}`);
  return res.json();
}
