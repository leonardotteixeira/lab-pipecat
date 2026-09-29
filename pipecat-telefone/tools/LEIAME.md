# tools/

Aqui fica o `cloudflared.exe` (tunel da Cloudflare que da uma URL publica ao bot local).
O binario tem ~54 MB e **nao e versionado** (esta no `.gitignore`).

Para baixar de novo (Windows, 64 bits):

```powershell
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile cloudflared.exe
```

O binario oficial e assinado, entao o Smart App Control do Windows o aceita.

Uso:

```powershell
.\cloudflared.exe tunnel --url http://localhost:7860
```

A URL `https://<algo>.trycloudflare.com` muda a cada execucao.
