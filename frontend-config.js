// 前端API配置
// 部署时需要修改此文件中的API地址

// 开发环境配置
const DEV_CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    ENVIRONMENT: 'development'
};

// 生产环境配置
const PROD_CONFIG = {
    // 请替换为您的实际部署URL
    API_BASE_URL: 'https://your-app.railway.app',  // Railway部署URL
    // API_BASE_URL: 'https://your-app.onrender.com',  // Render部署URL
    ENVIRONMENT: 'production'
};

// 自动检测环境
const isDevelopment = window.location.hostname === 'localhost' ||
    window.location.hostname === '127.0.0.1' ||
    window.location.hostname.includes('localhost');

// 导出当前配置
const CONFIG = isDevelopment ? DEV_CONFIG : PROD_CONFIG;

// 使用示例：
// fetch(`${CONFIG.API_BASE_URL}/api/cities?count=10`)
//     .then(response => response.json())
//     .then(data => console.log(data));

console.log('🌐 API配置已加载:', CONFIG);
