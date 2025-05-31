#!/bin/bash
# entrypoint.sh
set -euo pipefail

LOG_FILE="/home/jovyan/init_user_env.log"
USERNAME="jovyan"
USER_FILE="/home/${USERNAME}/.jupyterhub_user"

log() {
  echo "[$(date)] $1" >> "$LOG_FILE"
}

log "Starting container..."

# 仅检查 JUPYTERHUB_USER，否则使用 USER 环境变量
JUPYTERHUB_USER="${JUPYTERHUB_USER:-${USER:-}}"

if [ -z "$JUPYTERHUB_USER" ]; then
  log "ERROR: User name is empty after all attempts"
  exit 1
fi

log "Using user: '$JUPYTERHUB_USER'"

# 写入用户信息并设置权限
echo "$JUPYTERHUB_USER" > "$USER_FILE" || { log "ERROR: Failed to write file"; exit 1; }
chown "$(id -u $USERNAME):$(id -g $USERNAME)" "$USER_FILE"
chmod 644 "$USER_FILE"

log "User file created successfully"
log "Executing original command: $*"
exec "$@"