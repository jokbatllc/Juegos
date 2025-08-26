# Despliegue en VPS (Ubuntu 22.04/24.04)

Esta guía describe cómo desplegar el proyecto **Juegos** en un servidor VPS con Ubuntu 22.04 o 24.04 utilizando Docker Compose y Nginx como proxy inverso.

## Requisitos
- VPS con Ubuntu 22.04 o 24.04
- Dominio apuntando a la IP (opcional)
- Puertos abiertos: 80 (HTTP) y 443 (HTTPS) si se configurará TLS más adelante

## Crear usuario `deployer` y hardening básico
```bash
sudo adduser deployer
sudo usermod -aG sudo deployer
sudo -iu deployer
```

## Instalar Docker y Docker Compose
```bash
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
docker --version
docker compose version
```

## Clonar el repositorio y preparar el entorno
```bash
cd ~
git clone https://github.com/jokbatllc/Juegos.git
cd Juegos
cp .env.example .env
# Editar .env con valores reales (SECRET_KEY, ALLOWED_HOSTS, DB_PASSWORD fuerte, DJANGO_DEBUG=0)
```

## Arranque en producción con Nginx
```bash
docker compose -f docker-compose.prod.yml --env-file .env up --build -d
docker compose -f docker-compose.prod.yml ps
```

## Crear superusuario
```bash
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## Healthcheck
- Abrir `http://TU_IP/health/` → debe responder `ok`
- Abrir `http://TU_IP/` → debe cargar la aplicación

## Logs y mantenimiento
```bash
docker compose -f docker-compose.prod.yml logs -f nginx
docker compose -f docker-compose.prod.yml logs -f web
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
docker compose -f docker-compose.prod.yml down
```

## Firewall UFW (opcional)
```bash
sudo apt-get install -y ufw
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
# sudo ufw allow 443/tcp  # si pondrás TLS
sudo ufw enable
sudo ufw status
```

## SSL/TLS (opcional)
- Opciones: Caddy (auto-TLS), nginx-proxy + acme-companion, o certbot en el host.
- Ajustar Nginx y la variable `SECURE_PROXY_SSL_HEADER` ya contemplada en la configuración.

## Servicio systemd
Para arrancar el stack automáticamente tras un reinicio:
```bash
sudo cp docs/deploy/juegos.service /etc/systemd/system/juegos.service
sudo systemctl daemon-reload
sudo systemctl enable juegos
sudo systemctl start juegos
sudo systemctl status juegos --no-pager
```

---

¡Listo! La aplicación quedará disponible en `http://TU_IP/` (o el dominio configurado).
