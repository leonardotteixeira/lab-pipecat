# repos

Estudos e testes com repositorios open source. Comecamos pelo **Pipecat** (agentes de voz em tempo real).

- Catalogo dos repos analisados: [`catalogo/`](catalogo/README.md)
- Projetos de teste: pastas `pipecat-*` abaixo

## Projetos

| Pasta | O que e | Estado |
|---|---|---|
| [`pipecat-teste/`](pipecat-teste) | Bot de voz **no navegador**. STT+LLM no Groq, voz Piper local em portugues. | Funciona. E a melhor demonstracao. |
| [`pipecat-gemini/`](pipecat-gemini) | Mesmo bot com Gemini (STT, LLM, TTS). | Funciona, mas o plano gratuito estoura o limite (429). Mantido como referencia. |
| [`pipecat-telefone/`](pipecat-telefone) | Bot de **telefonia** (Twilio) com a persona "Rafael", vendedor do Peugeot 208 2027. | Bot e servidor OK. O trial da Twilio nao conectou o audio (ver abaixo). |

Cada projeto tem `server/bot.py`, `server/.env.example` e `server/pyproject.toml`.

## Como rodar (Windows)

Pre-requisitos: Python 3.11+, [`uv`](https://docs.astral.sh/uv/), e as chaves de API nos `.env`.

```powershell
cd pipecat-teste\server
copy .env.example .env      # preencha GROQ_API_KEY e GROQ_MODEL
uv sync
$env:PYTHONUTF8="1"; uv run bot.py
```

Abra http://localhost:7860, permita o microfone e converse.

- `GROQ_MODEL` usado nos testes: `openai/gpt-oss-20b` (confira a lista da sua conta).
- A voz `pt_BR-faber-medium` do Piper e baixada na primeira conexao (~60 MB).
- `PYTHONUTF8=1` evita erro de codificacao do banner no console do Windows.

### Telefonia (`pipecat-telefone`)
```powershell
# 1) tunel publico (veja pipecat-telefone\tools\LEIAME.md para baixar o cloudflared)
.\pipecat-telefone\tools\cloudflared.exe tunnel --url http://localhost:7860
# 2) bot, com o host do tunel (sem https://)
cd pipecat-telefone\server
uv run bot.py -t twilio -x <host>.trycloudflare.com
# 3) outro terminal: ligar para um numero verificado
uv run call.py --to +55DDDNUMERO --from +1NUMEROTWILIO --host <host>.trycloudflare.com
# diagnostico (somente leitura): status e erros de uma chamada
uv run call_info.py latest
```

## O que fizemos, em ordem

1. Instalamos o CLI do Pipecat (`uv tool install "pipecat-ai[cli]"`). O `pipecat.exe` foi bloqueado
   pelo Smart App Control do Windows (nao e assinado); passamos a chamar o modulo pelo Python assinado.
2. Criamos o projeto pelo scaffold (`pipecat init`), com `--no-context-hub` para nao alterar a
   configuracao dos agentes de codigo.
3. Groq: o cadastro falhou no inicio; depois funcionou e virou o STT+LLM principal.
4. Gemini como alternativa: o TTS gratuito limita a 3 req/min e o LLM a 5 req/min. Inviavel para conversa.
5. Voz local com **Piper** (`pt_BR-faber-medium`), sem limite e sem conta. O STT do Groq vem fixo em
   ingles: ajustamos para `Language.PT`.
6. Telefonia: projeto `pipecat-telefone`, cloudflared como tunel, `call.py` para ligar.
7. Persona de vendas (Rafael, Peugeot 208 2027) com regra de nao inventar preco nem ficha tecnica e
   de admitir que e assistente virtual se perguntado.

## Licoes aprendidas

- **Limites gratuitos derrubam voz em tempo real.** O TTS costuma ser o gargalo: uma requisicao por frase.
- **O scaffold do Gemini usa credenciais do Google Cloud** no TTS; trocamos por `api_key=` no `bot.py`.
- **Trial da Twilio:**
  - `Twiml=` inline na API e recusado (`HTTP 400`, "trial accounts have limited parameter access").
  - O parametro `Method` tambem foi recusado; `To`, `From` e `Url` funcionam.
  - Com `Url` apontando para o nosso tunel, a Twilio faz o `POST /` e recebe o TwiML correto (`200 OK`),
    mas **nao abre o WebSocket**: toca uma mensagem de teste em ingles e desliga (3 s, sem erro registrado).
    Hipotese nao confirmada: o trial nao libera `<Connect><Stream>`.
  - Proximos passos possiveis: saldo minimo na Twilio, ou testar Telnyx/Plivo.
- Numero de celular comum nao serve: e preciso um numero de provedor VoIP com API.
- Dados de telefonia por minuto: somar telefonia + STT + LLM + TTS (ver `catalogo/pipecat.md`).

## Seguranca antes de subir no GitHub

- `.env` esta no `.gitignore` (raiz e de cada projeto); so o `.env.example` sobe.
- Conferido: nenhuma chave nos arquivos versionaveis.
- O **Auth Token da Twilio foi exposto em conversa**: gere um novo no console da Twilio e atualize o `.env`.
  Vale trocar tambem as chaves do Groq e do Google criadas para o teste, se quiser garantir.
- `cloudflared.exe` (54 MB) e os modelos `.onnx` nao sobem (estao no `.gitignore`).
