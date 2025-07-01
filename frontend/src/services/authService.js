import { publicApiV1 } from '../config/AxiosConfig';

/**
 * Autentica al usuario utilizando su DNI.
 * @param {string} dni - Documento de identidad del usuario.
 * @returns {Promise<object>} - Respuesta del servidor.
 */
export const authenticateUser = async (dni) => {
  const response = await publicApiV1.post('auth', { dni });
  return response.data;
};