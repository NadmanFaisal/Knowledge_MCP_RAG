# MCP_Server

Ensure Ollama is installed correctly and running as a systemctl service.

## Check Ollama systemctl service:

```
sudo systemctl status ollama.service
```

```
```
## To run Open WebUI:
```

```
sudo docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

```
