import React, { useEffect, useState } from "react";
import {
  buscarCanciones,
  listarCanciones,
  agregarCancion,
  reproducirCancion,
  verHistorial,
} from "./api";

function App() {
  const [busqueda, setBusqueda] = useState("");
  const [resultados, setResultados] = useState([]);
  const [playlist, setPlaylist] = useState([]);
  const [historial, setHistorial] = useState([]);

  useEffect(() => {
    cargarPlaylist();
    cargarHistorial();
  }, []);

  async function cargarPlaylist() {
    const data = await listarCanciones();
    setPlaylist(data);
  }

  async function cargarHistorial() {
    const data = await verHistorial();
    setHistorial(data);
  }

  async function handleBuscar() {
    if (!busqueda) return;
    const data = await buscarCanciones(busqueda);
    setResultados(data);
  }

  async function handleAgregar(cancion) {
    await agregarCancion(cancion);
    cargarPlaylist();
  }

  async function handleReproducir(cancion) {
    await reproducirCancion(cancion.id);
    cargarHistorial();
  }

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🎵 Reproductor con Playlist</h1>

      {/* Buscar canciones */}
      <div>
        <input
          type="text"
          placeholder="Buscar en iTunes..."
          value={busqueda}
          onChange={(e) => setBusqueda(e.target.value)}
        />
        <button onClick={handleBuscar}>Buscar</button>
      </div>

      {/* Resultados de búsqueda */}
      <h2>Resultados</h2>
      <ul>
        {resultados.map((c, index) => (
          <li key={index}>
            {c.titulo} - {c.artista}
            <button onClick={() => handleAgregar(c)}>➕ Agregar</button>
          </li>
        ))}
      </ul>

      {/* Playlist */}
      <h2>Playlist</h2>
      <ul>
        {playlist.map((c) => (
          <li key={c.id}>
            {c.titulo} - {c.artista}
            <button onClick={() => handleReproducir(c)}>▶ Reproducir</button>
          </li>
        ))}
      </ul>

      {/* Historial */}
      <h2>Historial</h2>
      <ul>
        {historial.map((h, index) => (
          <li key={index}>
            {h.cancion} - {h.artista} ({h.fecha})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
