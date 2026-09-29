# Pipecat

- **Repo:** https://github.com/pipecat-ai/pipecat
- **O que e:** framework Python open source para agentes de voz e multimodais em tempo real.
- **Licenca:** BSD-2-Clause (uso comercial permitido)
- **Stack:** Python 3.11+ (recomendado 3.12+), `uv`
- **Analisado em:** 2026-09-29
- **Veredito:** **Testado e aprovado.** Bom candidato para qualquer projeto com voz.

## Como funciona
Um **pipeline** de processadores por onde passam "frames":

```
transporte (entrada) -> STT -> LLM -> TTS -> transporte (saida)
```

Cada etapa e trocavel por configuracao (Groq, Gemini, OpenAI, Piper, Deepgram...).
O Pipecat trata interrupcoes (o usuario fala por cima do bot) e turnos de fala.

## O que testamos (ver README.md)
| Projeto | Resultado |
|---|---|
| `pipecat-teste` | Funciona. Voz no navegador: Groq (STT+LLM) + Piper (TTS local, pt-BR). |
| `pipecat-gemini` | Funciona, mas o TTS do Gemini (gratis) limita a 3 req/min. Beco sem saida para conversa. |
| `pipecat-telefone` | Bot pronto e o servidor responde a Twilio, mas o **trial da Twilio nao conectou o audio**. |

## Pontos fortes
- Quickstart rapido; trocar de provedor e mudar poucas linhas.
- Muitos provedores prontos (STT, LLM, TTS, telefonia, video).
- Ecossistema: SDKs de cliente (JS, React, Swift, Kotlin...), Flows para conversas em etapas, evals.
- Ha modo 100% local (Whisper, Ollama, Piper) sem contas.

## Pontos de atencao
- **Custo por minuto** sempre envolve varios servicos (telefonia + STT + LLM + TTS).
  Estimativa grosseira: ~US$ 0,05 a 0,30 por minuto. Conferir precos atuais.
- **Camadas gratuitas tem limites baixos**, principalmente TTS (Gemini: 3 req/min no modelo testado).
  O LLM gratuito do Gemini tambem estourou (5 req/min).
- **Windows + Smart App Control:** os `.exe` gerados pelo `uv` (`pipecat.exe`) sao bloqueados por nao
  terem assinatura. Chamar o modulo pelo Python assinado funciona (ver README.md).
- **Telefonia real** exige plano pago no provedor (no teste, o trial da Twilio nao serviu).
- `piper-tts` e GPL: ok para estudo, conferir antes de usar em produto fechado.
- O `pipecat init` registra por padrao um servidor MCP nos agentes de codigo; usamos `--no-context-hub`.

## Quando usar / quando evitar
- **Usar:** assistente de voz, atendimento, agendamento, companion, bot de reuniao.
- **Evitar:** so chat de texto (exagero); quem quer solucao sem codigo.

## Alternativas a comparar
LiveKit Agents (parecido, ecossistema proprio).
