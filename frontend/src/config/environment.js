/**
 * Archivo de configuración del entorno
 * Aquí se almacenan las URLs y configuraciones globales del backend.
 */

export const environment = {
  backendUrl: process.env.REACT_APP_BACKEND_URL || 'http://localhost:9000/api/v1',
};

/**
 * Función para obtener la URL del backend
 * @returns {string} - URL base del backend
 */
export const getBackendUrl = () => {
  return environment.backendUrl;
};