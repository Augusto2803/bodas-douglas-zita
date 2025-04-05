FROM nginx:alpine

# Remover a configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiar a configuração personalizada
COPY nginx.conf /etc/nginx/conf.d/

# Criar diretório para uploads
RUN mkdir -p /var/www/uploads

# Expor portas
EXPOSE 80 443
