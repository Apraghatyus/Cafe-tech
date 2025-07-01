// vue.config.js
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  
  // Configuración del servidor de desarrollo
  devServer: {
    host: '0.0.0.0',
    port: 8080,
    allowedHosts: 'all',
    
    // Configuración del proxy para evitar problemas de CORS
    proxy: {
      '/api': {
        target: 'http://localhost:9000',
        changeOrigin: true,
        secure: false,
        logLevel: 'debug',
        onError: function (err, req, res) {
          console.log('❌ Proxy Error:', err.message);
        },
        onProxyReq: function (proxyReq, req, res) {
          console.log('🔄 Proxy Request:', req.method, req.url);
        },
        onProxyRes: function (proxyRes, req, res) {
          console.log('✅ Proxy Response:', proxyRes.statusCode, req.url);
        }
      }
    }
  },
  
  configureWebpack: {
    devtool: 'source-map'
  }
})