const BASE_URL = 'http://localhost:8000';

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
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username: email, password })
    });
    return res.json();
}