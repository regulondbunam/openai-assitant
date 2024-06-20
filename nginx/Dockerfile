# Usa una imagen base oficial de Nginx
FROM nginx:alpine

# Copia el archivo de configuración de Nginx en el contenedor
COPY nginx/nginx.conf /etc/nginx/nginx.conf


# Copia la configuración del sitio al directorio de sitios disponibles
COPY nginx/default.conf /etc/nginx/conf.d/

# Expone el puerto 80 para Nginx
EXPOSE 80