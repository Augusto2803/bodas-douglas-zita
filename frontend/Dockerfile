FROM nginx:alpine

# Remover a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiar configuração personalizada do Nginx
COPY nginx.conf /etc/nginx/conf.d/

# Copiar arquivos HTML estáticos
COPY index.html /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/

# Expor porta
EXPOSE 80
