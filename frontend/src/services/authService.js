import { ApiUrlV1 } from '../config/AxiosConfig';

/**
 * Autentica al usuario utilizando su DNI.
 * @param {string} dni - Documento de identidad del usuario.
 * @returns {Promise<object>} - Respuesta del servidor.
 */
export const login = async (username, password) => {
  const response = await ApiUrlV1.post('login', {username, password});
  return response;
};