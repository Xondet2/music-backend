const API_URL = "http://127.0.0.1:8000/api";

// Buscar en iTunes
export async function buscarCanciones(query) {
  const response = await fetch(`${API_URL}/buscar/?q=${query}`);
  return response.json();
}

// Playlist
export async function listarCanciones() {
  const response = await fetch(`${API_URL}/playlist/`);
  return response.json();
}

export async function agregarCancion(cancion) {
  const response = await fetch(
    `${API_URL}/playlist/agregar/?titulo=${encodeURIComponent(cancion.titulo)}&artista=${encodeURIComponent(cancion.artista)}`
  );
  return response.json();
}

// Reproductor
export async function reproducirCancion(id) {
  const response = await fetch(`${API_URL}/reproducir/${id}/`);
  return response.json();
}

export async function verHistorial() {
  const response = await fetch(`${API_URL}/historial/`);
  return response.json();
}
