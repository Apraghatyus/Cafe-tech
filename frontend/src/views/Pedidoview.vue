<template>
  <div class="pedidos-view">
    <!-- Hero Section -->
    <div class="hero-section bg-dark text-white py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-8">
            <h1 class="display-4 fw-bold mb-3">
              <i class="fas fa-clipboard-list text-warning me-3"></i>
              Gestión de Pedidos
            </h1>
            <p class="lead mb-4">Administra todos los pedidos de tu cafetería de manera eficiente</p>
            <button 
              class="btn btn-warning btn-lg fw-bold"
              @click="openCreateDialog"
            >
              <i class="fas fa-plus me-2"></i>
              Nuevo Pedido
            </button>
          </div>
          <div class="col-md-4 text-center">
            <i class="fas fa-coffee display-1 text-warning opacity-75"></i>
          </div>
        </div>
      </div>
    </div>

    <div class="container mt-4">
      <!-- Stats Cards -->
      <div class="row mb-4">
        <div class="col-md-3 mb-3" v-for="stat in stats" :key="stat.title">
          <div class="card stat-card h-100 border-0 shadow">
            <div class="card-body text-center">
              <i :class="`fas ${stat.icon} fa-2x ${stat.colorClass} mb-3`"></i>
              <h3 class="fw-bold mb-2">{{ stat.value }}</h3>
              <p class="text-muted mb-0">{{ stat.title }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters Section -->
      <div class="card mb-4 border-0 shadow">
        <div class="card-header bg-dark text-white">
          <h5 class="mb-0">
            <i class="fas fa-filter me-2"></i>
            Filtros
          </h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-4 mb-3">
              <label class="form-label">Buscar por cliente</label>
              <div class="input-group">
                <span class="input-group-text bg-warning border-warning">
                  <i class="fas fa-search"></i>
                </span>
                <input 
                  type="text" 
                  class="form-control border-warning"
                  v-model="search"
                  placeholder="Nombre del cliente..."
                >
              </div>
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Estado</label>
              <select class="form-select border-warning" v-model="selectedStatus">
                <option value="">Todos los estados</option>
                <option value="pendiente">Pendiente</option>
                <option value="enviado">Enviado</option>
                <option value="entregado">Entregado</option>
              </select>
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Fecha de entrega</label>
              <input 
                type="date" 
                class="form-control border-warning"
                v-model="selectedDate"
              >
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <button class="btn btn-outline-warning me-2" @click="clearFilters">
                <i class="fas fa-times me-1"></i>
                Limpiar Filtros
              </button>
              <button class="btn btn-warning" @click="refreshData">
                <i class="fas fa-sync-alt me-1"></i>
                Actualizar
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Pedidos Table -->
      <div class="card border-0 shadow">
        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
          <h5 class="mb-0">
            <i class="fas fa-list me-2"></i>
            Lista de Pedidos ({{ filteredPedidos.length }})
          </h5>
          <div class="d-flex gap-2">
            <button class="btn btn-sm btn-outline-warning" @click="refreshData" :disabled="loading">
              <i class="fas fa-sync-alt" :class="{ 'fa-spin': loading }"></i>
            </button>
          </div>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-warning">
                <tr>
                  <th class="fw-bold">
                    <i class="fas fa-user me-1"></i>
                    Cliente
                  </th>
                  <th class="fw-bold">
                    <i class="fas fa-coffee me-1"></i>
                    Producto
                  </th>
                  <th class="fw-bold text-center">
                    <i class="fas fa-hashtag me-1"></i>
                    Cantidad
                  </th>
                  <th class="fw-bold">
                    <i class="fas fa-calendar me-1"></i>
                    Fecha Entrega
                  </th>
                  <th class="fw-bold text-center">
                    <i class="fas fa-check-circle me-1"></i>
                    Estado
                  </th>
                  <th class="fw-bold text-center">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="loading">
                  <td colspan="6" class="text-center py-5">
                    <div class="spinner-border text-warning" role="status">
                      <span class="visually-hidden">Cargando...</span>
                    </div>
                    <p class="mt-2 mb-0">Cargando pedidos...</p>
                  </td>
                </tr>
                <tr v-else-if="filteredPedidos.length === 0">
                  <td colspan="6" class="text-center py-5 text-muted">
                    <i class="fas fa-inbox fa-3x mb-3"></i>
                    <p class="mb-0">No hay pedidos que coincidan con los filtros</p>
                  </td>
                </tr>
                <tr v-else v-for="pedido in filteredPedidos" :key="pedido.id" class="align-middle">
                  <td>
                    <div class="d-flex align-items-center">
                      <div class="avatar-circle bg-warning text-dark me-2">
                        {{ pedido.cliente.charAt(0).toUpperCase() }}
                      </div>
                      <strong>{{ pedido.cliente }}</strong>
                    </div>
                  </td>
                  <td>
                    <span class="badge bg-dark text-warning fs-6">
                      <i class="fas fa-coffee me-1"></i>
                      {{ pedido.producto }}
                    </span>
                  </td>
                  <td class="text-center">
                    <span class="badge bg-warning text-dark fs-6">
                      {{ pedido.cantidad }} unidades
                    </span>
                  </td>
                  <td>
                    <div class="d-flex align-items-center">
                      <i 
                        class="fas fa-calendar me-2"
                        :class="isDateOverdue(pedido.fecha_entrega) ? 'text-danger' : 'text-success'"
                      ></i>
                      <span :class="isDateOverdue(pedido.fecha_entrega) ? 'text-danger fw-bold' : ''">
                        {{ formatDate(pedido.fecha_entrega) }}
                      </span>
                    </div>
                  </td>
                  <td class="text-center">
                    <span 
                      class="badge fs-6"
                      :class="getStatusClass(pedido.estado)"
                    >
                      <i :class="getStatusIcon(pedido.estado)" class="me-1"></i>
                      {{ pedido.estado.toUpperCase() }}
                    </span>
                  </td>
                  <td class="text-center">
                    <div class="btn-group" role="group">
                      <button 
                        class="btn btn-sm btn-outline-primary"
                        @click="viewPedido(pedido)"
                        title="Ver detalles"
                      >
                        <i class="fas fa-eye"></i>
                      </button>
                      <button 
                        class="btn btn-sm btn-outline-warning"
                        @click="editPedido(pedido)"
                        title="Editar"
                      >
                        <i class="fas fa-edit"></i>
                      </button>
                      <button 
                        class="btn btn-sm btn-outline-danger"
                        @click="deletePedido(pedido)"
                        title="Eliminar"
                      >
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para Crear/Editar Pedido -->
    <div class="modal fade" id="pedidoModal" tabindex="-1" ref="pedidoModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">
              <i :class="editingPedido ? 'fas fa-edit' : 'fas fa-plus'" class="me-2"></i>
              {{ editingPedido ? 'Editar Pedido' : 'Nuevo Pedido' }}
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="closePedidoDialog"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="savePedido" ref="pedidoForm">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Cliente *</label>
                  <div class="input-group">
                    <span class="input-group-text bg-warning border-warning">
                      <i class="fas fa-user"></i>
                    </span>
                    <input 
                      type="text" 
                      class="form-control border-warning"
                      v-model="pedidoForm.cliente"
                      required
                      placeholder="Nombre del cliente"
                    >
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Producto *</label>
                  <div class="input-group">
                    <span class="input-group-text bg-warning border-warning">
                      <i class="fas fa-coffee"></i>
                    </span>
                    <select class="form-select border-warning" v-model="pedidoForm.producto_id" required>
                      <option value="">Seleccionar producto</option>
                      <option v-for="producto in productos" :key="producto.id" :value="producto.id">
                        {{ producto.nombre }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Cantidad *</label>
                  <div class="input-group">
                    <span class="input-group-text bg-warning border-warning">
                      <i class="fas fa-hashtag"></i>
                    </span>
                    <input 
                      type="number" 
                      class="form-control border-warning"
                      v-model.number="pedidoForm.cantidad"
                      min="1"
                      required
                      placeholder="1"
                    >
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Fecha de Entrega *</label>
                  <div class="input-group">
                    <span class="input-group-text bg-warning border-warning">
                      <i class="fas fa-calendar"></i>
                    </span>
                    <input 
                      type="date" 
                      class="form-control border-warning"
                      v-model="pedidoForm.fecha_entrega"
                      :min="new Date().toISOString().split('T')[0]"
                      required
                    >
                  </div>
                </div>
                <div class="col-12 mb-3">
                  <label class="form-label">Estado *</label>
                  <div class="input-group">
                    <span class="input-group-text bg-warning border-warning">
                      <i class="fas fa-check-circle"></i>
                    </span>
                    <select class="form-select border-warning" v-model="pedidoForm.estado" required>
                      <option value="pendiente">Pendiente</option>
                      <option value="enviado">Enviado</option>
                      <option value="entregado">Entregado</option>
                    </select>
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closePedidoDialog">
              Cancelar
            </button>
            <button 
              type="button" 
              class="btn btn-warning fw-bold"
              @click="savePedido"
              :disabled="saving"
            >
              <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else :class="editingPedido ? 'fas fa-save' : 'fas fa-plus'" class="me-2"></i>
              {{ editingPedido ? 'Actualizar' : 'Crear' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmación para Eliminar -->
    <div class="modal fade" id="deleteModal" tabindex="-1" ref="deleteModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">
              <i class="fas fa-exclamation-triangle me-2"></i>
              Confirmar Eliminación
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="closeDeleteDialog"></button>
          </div>
          <div class="modal-body">
            <div class="text-center">
              <i class="fas fa-trash-alt fa-3x text-danger mb-3"></i>
              <p class="mb-3">¿Estás seguro que deseas eliminar el pedido de:</p>
              <h5 class="fw-bold text-danger">{{ pedidoToDelete?.cliente }}</h5>
              <p class="text-muted">Esta acción no se puede deshacer.</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteDialog">
              Cancelar
            </button>
            <button 
              type="button" 
              class="btn btn-danger fw-bold"
              @click="confirmDelete"
              :disabled="deleting"
            >
              <span v-if="deleting" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="fas fa-trash me-2"></i>
              Eliminar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast Container -->
    <div class="toast-container position-fixed top-0 end-0 p-3">
      <div 
        class="toast"
        :class="{ 'show': toast.show }"
        ref="toastElement"
      >
        <div class="toast-header" :class="toast.headerClass">
          <i :class="toast.icon" class="me-2"></i>
          <strong class="me-auto">{{ toast.title }}</strong>
          <button type="button" class="btn-close" @click="hideToast"></button>
        </div>
        <div class="toast-body">
          {{ toast.message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PedidosView',
  data() {
    return {
      // Estados generales
      loading: false,
      saving: false,
      deleting: false,
      
      // Búsqueda y filtros
      search: '',
      selectedStatus: '',
      selectedDate: '',
      
      // Datos
      pedidos: [
        {
          id: 1,
          cliente: 'María López',
          producto_id: 1,
          producto: 'Espresso Clásico',
          cantidad: 3,
          fecha_entrega: '2025-07-10',
          estado: 'pendiente'
        },
        {
          id: 2,
          cliente: 'Juan Pérez',
          producto_id: 2,
          producto: 'Cappuccino Cremoso',
          cantidad: 1,
          fecha_entrega: '2025-07-05',
          estado: 'enviado'
        },
        {
          id: 3,
          cliente: 'Ana Torres',
          producto_id: 3,
          producto: 'Latte de Vainilla',
          cantidad: 10,
          fecha_entrega: '2025-07-15',
          estado: 'entregado'
        }
      ],
      
      productos: [
        { id: 1, nombre: 'Espresso Clásico' },
        { id: 2, nombre: 'Cappuccino Cremoso' },
        { id: 3, nombre: 'Latte de Vainilla' },
        { id: 4, nombre: 'Americano' },
        { id: 5, nombre: 'Macchiato' }
      ],
      
      // Formulario
      editingPedido: false,
      pedidoForm: {
        cliente: '',
        producto_id: '',
        cantidad: 1,
        fecha_entrega: '',
        estado: 'pendiente'
      },
      
      // Para eliminar
      pedidoToDelete: null,
      
      // Toast
      toast: {
        show: false,
        title: '',
        message: '',
        icon: '',
        headerClass: ''
      }
    }
  },
  
  computed: {
    filteredPedidos() {
      let filtered = this.pedidos;
      
      if (this.search) {
        filtered = filtered.filter(p => 
          p.cliente.toLowerCase().includes(this.search.toLowerCase())
        );
      }
      
      if (this.selectedStatus) {
        filtered = filtered.filter(p => p.estado === this.selectedStatus);
      }
      
      if (this.selectedDate) {
        filtered = filtered.filter(p => p.fecha_entrega === this.selectedDate);
      }
      
      return filtered;
    },
    
    stats() {
      return [
        {
          title: 'Total Pedidos',
          value: this.pedidos.length,
          icon: 'fa-clipboard-list',
          colorClass: 'text-primary'
        },
        {
          title: 'Pendientes',
          value: this.pedidos.filter(p => p.estado === 'pendiente').length,
          icon: 'fa-clock',
          colorClass: 'text-warning'
        },
        {
          title: 'Enviados',
          value: this.pedidos.filter(p => p.estado === 'enviado').length,
          icon: 'fa-truck',
          colorClass: 'text-info'
        },
        {
          title: 'Entregados',
          value: this.pedidos.filter(p => p.estado === 'entregado').length,
          icon: 'fa-check-circle',
          colorClass: 'text-success'
        }
      ];
    }
  },
  
  methods: {
    // Métodos de diálogo
    openCreateDialog() {
      this.editingPedido = false;
      this.resetForm();
      const modal = new bootstrap.Modal(this.$refs.pedidoModal);
      modal.show();
    },
    
    editPedido(pedido) {
      this.editingPedido = true;
      this.pedidoForm = { ...pedido };
      const modal = new bootstrap.Modal(this.$refs.pedidoModal);
      modal.show();
    },
    
    viewPedido(pedido) {
      this.showToast('Información', `Viendo detalles del pedido de ${pedido.cliente}`, 'fas fa-eye', 'bg-info text-white');
    },
    
    deletePedido(pedido) {
      this.pedidoToDelete = pedido;
      const modal = new bootstrap.Modal(this.$refs.deleteModal);
      modal.show();
    },
    
    closePedidoDialog() {
      const modal = bootstrap.Modal.getInstance(this.$refs.pedidoModal);
      if (modal) modal.hide();
      this.resetForm();
    },
    
    closeDeleteDialog() {
      const modal = bootstrap.Modal.getInstance(this.$refs.deleteModal);
      if (modal) modal.hide();
      this.pedidoToDelete = null;
    },
    
    // Métodos de formulario
    resetForm() {
      this.pedidoForm = {
        cliente: '',
        producto_id: '',
        cantidad: 1,
        fecha_entrega: '',
        estado: 'pendiente'
      };
    },
    
    async savePedido() {
      // Validar formulario
      if (!this.pedidoForm.cliente || !this.pedidoForm.producto_id || !this.pedidoForm.cantidad || !this.pedidoForm.fecha_entrega) {
        this.showToast('Error', 'Por favor completa todos los campos requeridos', 'fas fa-exclamation-triangle', 'bg-danger text-white');
        return;
      }
      
      this.saving = true;
      
      try {
        // Simular delay de API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        if (this.editingPedido) {
          // Actualizar pedido existente
          const index = this.pedidos.findIndex(p => p.id === this.pedidoForm.id);
          if (index !== -1) {
            const producto = this.productos.find(p => p.id === this.pedidoForm.producto_id);
            this.pedidos[index] = {
              ...this.pedidoForm,
              producto: producto ? producto.nombre : 'Producto no encontrado'
            };
          }
          this.showToast('Éxito', 'Pedido actualizado correctamente', 'fas fa-check', 'bg-success text-white');
        } else {
          // Crear nuevo pedido
          const producto = this.productos.find(p => p.id === parseInt(this.pedidoForm.producto_id));
          const newPedido = {
            ...this.pedidoForm,
            id: Date.now(),
            producto_id: parseInt(this.pedidoForm.producto_id),
            producto: producto ? producto.nombre : 'Producto no encontrado'
          };
          this.pedidos.push(newPedido);
          this.showToast('Éxito', 'Pedido creado correctamente', 'fas fa-check', 'bg-success text-white');
        }
        
        this.closePedidoDialog();
      } catch (error) {
        this.showToast('Error', 'Ocurrió un error al guardar el pedido', 'fas fa-exclamation-triangle', 'bg-danger text-white');
      } finally {
        this.saving = false;
      }
    },
    
    async confirmDelete() {
      this.deleting = true;
      
      try {
        // Simular delay de API
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const index = this.pedidos.findIndex(p => p.id === this.pedidoToDelete.id);
        if (index !== -1) {
          this.pedidos.splice(index, 1);
        }
        
        this.showToast('Éxito', 'Pedido eliminado correctamente', 'fas fa-check', 'bg-success text-white');
        this.closeDeleteDialog();
      } catch (error) {
        this.showToast('Error', 'Ocurrió un error al eliminar el pedido', 'fas fa-exclamation-triangle', 'bg-danger text-white');
      } finally {
        this.deleting = false;
      }
    },
    
    // Métodos de utilidad
    clearFilters() {
      this.search = '';
      this.selectedStatus = '';
      this.selectedDate = '';
    },
    
    refreshData() {
      this.loading = true;
      setTimeout(() => {
        this.loading = false;
        this.showToast('Información', 'Datos actualizados correctamente', 'fas fa-sync-alt', 'bg-info text-white');
      }, 1000);
    },
    
    getStatusClass(estado) {
      const classes = {
        'pendiente': 'bg-warning text-dark',
        'enviado': 'bg-info text-white',
        'entregado': 'bg-success text-white'
      };
      return classes[estado] || 'bg-secondary text-white';
    },
    
    getStatusIcon(estado) {
      const icons = {
        'pendiente': 'fas fa-clock',
        'enviado': 'fas fa-truck',
        'entregado': 'fas fa-check-circle'
      };
      return icons[estado] || 'fas fa-question';
    },
    
    formatDate(date) {
      return new Date(date).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },
    
    isDateOverdue(date) {
      const today = new Date();
      const deliveryDate = new Date(date);
      today.setHours(0, 0, 0, 0);
      deliveryDate.setHours(0, 0, 0, 0);
      return deliveryDate < today;
    },
    
    showToast(title, message, icon, headerClass) {
      this.toast = {
        show: true,
        title,
        message,
        icon,
        headerClass
      };
      
      setTimeout(() => {
        this.hideToast();
      }, 4000);
    },
    
    hideToast() {
      this.toast.show = false;
    }
  }
};
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #000000 0%, #333333 100%);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="coffee" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="2" fill="rgba(255,193,7,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23coffee)"/></svg>');
}

.stat-card {
  transition: all 0.3s ease;
  border-left: 4px solid #ffc107;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
}

.table th {
  border-top: none;
  font-weight: 600;
  background-color: #ffc107 !important;
  color: #000 !important;
}

.table-hover tbody tr:hover {
  background-color: rgba(255, 193, 7, 0.1);
}

.btn-warning {
  background-color: #ffc107;
  border-color: #ffc107;
  color: #000;
  font-weight: 600;
}

.btn-warning:hover {
  background-color: #e0a800;
  border-color: #d39e00;
  color: #000;
}

.btn-outline-warning {
  color: #ffc107;
  border-color: #ffc107;
}

.btn-outline-warning:hover {
  background-color: #ffc107;
  border-color: #ffc107;
  color: #000;
}

.border-warning {
  border-color: #ffc107 !important;
}

.bg-warning {
  background-color: #ffc107 !important;
}

.text-warning {
  color: #ffc107 !important;
}

.card {
  border-radius: 10px;
}

.modal-content {
  border-radius: 10px;
}

.form-control:focus,
.form-select:focus {
  border-color: #ffc107;
  box-shadow: 0 0 0 0.2rem rgba(255, 193, 7, 0.25);
}

.toast {
  border-radius: 10px;
}

.btn-group .btn {
  margin: 0 2px;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card {
  animation: fadeInUp 0.6s ease-out;
}

</style>