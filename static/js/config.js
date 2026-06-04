// Configuração dinâmica da URL base do API
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000' 
  : window.location.origin.replace('projetocuidadopuro.onrender.com', 'projetocuidadopuro-backend.onrender.com');

console.log('API_BASE_URL:', API_BASE_URL);
