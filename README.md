# lab-pipecat

Testes com o [Pipecat](https://github.com/pipecat-ai/pipecat), framework Python para agentes de voz e
multimodais em tempo real: bot de voz no navegador e bot de telefonia, em português.

- Análise completa do repo: [`ANALISE.md`](ANALISE.md)
- Data dos testes: 2026-09-29

## Projetos

| Pasta | O que é | Estado |
|---|---|---|
| [`pipecat-teste/`](pipecat-teste) | Bot de voz **no navegador**. STT + LLM no Groq, voz Piper local em português. | Funciona. É a melhor demonstração. |
| [`pipecat-gemini/`](pipecat-gemini) | Mesmo bot com Gemini (STT, LLM e TTS). | Funciona, mas o plano gratuito estoura o limite (429). Mantido como referência. |
| [`pipecat-telefone/`](pipecat-telefone) | Bot de **telefonia** (Twilio) com a persona "Rafael", vendedor do Peugeot 208 2027. | Bot e servidor OK. O trial da Twilio não conectou o áudio (ver abaixo). |

Cada projeto tem `server/bot.py`, `server/.env.example` e `server/pyproject.toml`.

## Como rodar (Windows)

Requisitos: Python 3.11+, [`uv`](https://docs.astral.sh/uv/) e as chaves de API nos `.env`.

```powershell
cd pipecat-teste\server
copy .env.example .env      # preencha GROQ_API_KEY e GROQ_MODEL
uv sync
$env:PYTHONUTF8="1"; uv run bot.py
```

Abra http://localhost:7860, permita o microfone e converse.

- `GROQ_MODEL` usado nos testes: `openai/gpt-oss-20b` (confira a lista da sua conta).
- A voz `pt_BR-faber-medium` do Piper é baixada na primeira conexão (~60 MB).
- `PYTHONUTF8=1` evita erro de codificação do banner no console do Windows.

### Telefonia (`pipecat-telefone`)

```powershell
# 1) túnel público (veja pipecat-telefone\tools\LEIAME.md para baixar o cloudflared)
.\pipecat-telefone\tools\cloudflared.exe tunnel --url http://localhost:7860
# 2) bot, com o host do túnel (sem https://)
cd pipecat-telefone\server
uv run bot.py -t twilio -x <host>.trycloudflare.com
# 3) outro terminal: ligar para um número verificado
uv run call.py --to +55DDDNUMERO --from +1NUMEROTWILIO --host <host>.trycloudflare.com
# diagnóstico (somente leitura): status e erros de uma chamada
uv run call_info.py latest
```

## O que fizemos, em ordem

1. Instalamos o CLI do Pipecat (`uv tool install "pipecat-ai[cli]"`). O `pipecat.exe` foi bloqueado pelo
   Smart App Control do Windows (não é assinado); passamos a chamar o módulo pelo Python assinado.
2. Criamos o projeto pelo scaffold (`pipecat init`), com `--no-context-hub` para não alterar a
   configuração dos agentes de código.
3. Groq: o cadastro falhou no início; depois funcionou e virou o STT + LLM principal.
4. Gemini como alternativa: o TTS gratuito limita a 3 req/min e o LLM a 5 req/min. Inviável para conversa.
5. Voz local com **Piper** (`pt_BR-faber-medium`), sem limite e sem conta. O STT do Groq vem fixo em
   inglês: ajustamos para `Language.PT`.
6. Telefonia: projeto `pipecat-telefone`, cloudflared como túnel, `call.py` para ligar.
7. Persona de vendas (Rafael, Peugeot 208 2027) com regra de não inventar preço nem ficha técnica e de
   admitir que é assistente virtual se perguntado.

## Lições aprendidas

- **Limites gratuitos derrubam voz em tempo real.** O TTS costuma ser o gargalo: uma requisição por frase.
- **O scaffold do Gemini usa credenciais do Google Cloud** no TTS; trocamos por `api_key=` no `bot.py`.
- **Trial da Twilio:**
  - `Twiml=` inline na API é recusado (`HTTP 400`, "trial accounts have limited parameter access").
  - O parâmetro `Method` também foi recusado; `To`, `From` e `Url` funcionam.
  - Com `Url` apontando para o nosso túnel, a Twilio faz o `POST /` e recebe o TwiML correto (`200 OK`),
    mas **não abre o WebSocket**: toca uma mensagem de teste em inglês e desliga (3 s, sem erro registrado).
    Hipótese não confirmada: o trial não libera `<Connect><Stream>`.
  - Próximos passos possíveis: saldo mínimo na Twilio, ou testar Telnyx/Plivo.
- Número de celular comum não serve: é preciso um número de provedor VoIP com API.
- Custo por minuto: somar telefonia + STT + LLM + TTS (ver `ANALISE.md`).

## Segurança

- `.env` está no `.gitignore`; só o `.env.example` de cada projeto vai para o Git.
- Conferido antes do envio: nenhuma chave, número de telefone ou Account SID nos arquivos versionados.
- `cloudflared.exe` (54 MB) e os modelos `.onnx` não são versionados.
- Se você reutilizar este código, gere chaves e tokens novos; nunca cole credenciais em conversas ou prints.
