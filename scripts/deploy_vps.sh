#!/usr/bin/env bash
set -euo pipefail
# Uso: ./scripts/deploy_vps.sh prod
PROFILE=${1:-prod}
FILE="docker-compose.${PROFILE}.yml"
if [ ! -f "$FILE" ]; then
  echo "No existe $FILE"
  exit 1
fi
echo "Construyendo e iniciando $FILE"
docker compose -f "$FILE" --env-file .env up --build -d
docker compose -f "$FILE" ps
