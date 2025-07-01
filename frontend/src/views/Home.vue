<template>
  <div class="home">
    <!-- Hero Section -->
    <div class="hero bg-dark text-white text-center py-5" style="background-image: url('/images/coffee-hero.jpg'); background-size: cover; background-position: center;">
      <div class="container">
        <h1 class="display-4 fw-bold">¡Bienvenidos a Nuestra Cafetería!</h1>
        <p class="lead">El mejor café, las mejores experiencias</p>
        <a href="#menu" class="btn btn-primary btn-lg mt-3">Explorar Menú</a>
      </div>
    </div>

    <!-- About Section -->
    <div class="about py-5 bg-light text-center">
      <div class="container">
        <h2 class="display-5 fw-bold">¿Quiénes somos?</h2>
        <p class="mt-3 fs-5">
          Somos una cafetería apasionada por el café de calidad, ofreciendo un ambiente acogedor para disfrutar con amigos y familia.
        </p>
      </div>
    </div>

    <!-- Specials Section -->
    <div class="specials py-5">
      <div class="container text-center">
        <h2 class="display-5 fw-bold">Especialidades</h2>
        <div class="row mt-4">
          <!-- Item 1 -->
          <div class="col-md-4">
            <div class="card">
              <img src="/images/special1.jpg" class="card-img-top" alt="Especialidad 1">
              <div class="card-body">
                <h5 class="card-title">Espresso Clásico</h5>
                <p class="card-text">Un espresso perfecto con granos seleccionados.</p>
              </div>
            </div>
          </div>
          <!-- Item 2 -->
          <div class="col-md-4">
            <div class="card">
              <img src="/images/special2.jpg" class="card-img-top" alt="Especialidad 2">
              <div class="card-body">
                <h5 class="card-title">Cappuccino Cremoso</h5>
                <p class="card-text">La combinación perfecta de café y espuma de leche.</p>
              </div>
            </div>
          </div>
          <!-- Item 3 -->
          <div class="col-md-4">
            <div class="card">
              <img src="/images/special3.jpg" class="card-img-top" alt="Especialidad 3">
              <div class="card-body">
                <h5 class="card-title">Latte de Vainilla</h5>
                <p class="card-text">Un toque dulce para alegrar tu día.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
};
</script>

<style scoped>
.hero {
  height: 70vh;
  background-blend-mode: darken;
}
</style>