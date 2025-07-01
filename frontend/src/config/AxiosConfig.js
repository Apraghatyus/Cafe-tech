import axios from 'axios';
import { getBackendUrl } from './environment';

export const publicApiV1 = axios.create({
  baseURL: getBackendUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
});