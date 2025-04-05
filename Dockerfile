# Use uma imagem base que suporte múltiplos serviços
FROM docker:24-dind

# Instale docker-compose
RUN apk add --no-cache docker-compose

# Copie todos os arquivos necessários
COPY . /app
WORKDIR /app

# Comando para iniciar todos os serviços
CMD ["docker-compose", "-f", "docker-compose.yaml", "up", "--build"]
