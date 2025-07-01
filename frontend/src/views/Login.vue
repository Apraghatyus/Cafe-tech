<template>
  <div class="login d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow-lg" style="width: 400px;">
      <h2 class="text-center mb-4">Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="username" class="form-label">Usuario</label>
          <input
            type="text"
            id="username"
            class="form-control"
            v-model="username"
            placeholder="Ingrese su usuario"
            required
            :disabled="loading"
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Contraseña</label>
          <input
            type="password"
            id="password"
            class="form-control"
            v-model="password"
            placeholder="Ingrese su contraseña"
            required
            :disabled="loading"
          />
        </div>
        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
          <span v-if="loading">Iniciando sesión...</span>
          <span v-else>Ingresar</span>
        </button>

        <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
          <strong>Error:</strong> {{ errorMessage }}
          <br>
          <small class="text-muted">{{ errorDetails }}</small>
        </div>
        <div v-if="successMessage" class="alert alert-success mt-3" role="alert">
          {{ successMessage }}
        </div>
      </form>
      <p class="text-center mt-3">
        ¿No tienes cuenta? <a href="#">Regístrate</a>
      </p>
    </div>
  </div>
</template>

<script>
import { login } from "../services/authService";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      loading: false,
      errorMessage: "",
      errorDetails: "",
      successMessage: ""
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.errorMessage = "";
      this.errorDetails = "";
      this.successMessage = "";

      try {
        // Llamada al servicio sin reconstruir payload aquí
        const response = await login();
        console.log("✅ login response:", response);

        // Esperamos que venga en response.data.items[0]
        const item = response.data?.items?.[0];
        if (item?.access_token) {
          // Guardamos token y rol
          localStorage.setItem("access_token", item.access_token);
          if (item.role) {
            localStorage.setItem("user_role", item.role);
          }

          this.successMessage = "¡Inicio de sesión exitoso!";
          // Redirige tras un pequeño delay
          setTimeout(() => this.$router.push("/"), 1000);
        } else {
          this.errorMessage = "No se recibió un token válido.";
        }
      } catch (err) {
        console.error("❌ Error en login:", err);
        // Manejo básico de errores
        if (err.response) {
          this.errorMessage = `Error ${err.response.status}`;
          this.errorDetails = err.response.data?.message || JSON.stringify(err.response.data);
        } else {
          this.errorMessage = err.message || "Error al conectar con el servidor";
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login {
  background-color: #f8f9fa;
}
.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
.alert {
  font-size: 0.9rem;
}
button:disabled {
  opacity: 0.6;
}
</style>
