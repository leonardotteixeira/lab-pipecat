# pipecat-telefone

A Pipecat AI voice agent built with a cascade pipeline (STT → LLM → TTS).

## Configuration

- **Bot Type**: Telephony
- **Transport(s)**: Twilio, SmallWebRTC
- **Pipeline**: Cascade
  - **STT**: Groq (Whisper)
  - **LLM**: Groq
  - **TTS**: Piper

## Setup

### Setting Up Twilio

#### 1. Create a TwiML Bin

A TwiML Bin tells Twilio how to handle incoming calls. You'll create one that establishes a WebSocket connection to your bot.

1. Go to the [Twilio Console](https://console.twilio.com)
2. Navigate to **TwiML Bins** → **My TwiML Bins**
3. Click the **+** to create a new TwiML Bin
4. Name your bin and add the TwiML:

    **For Local Development:**

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
      <Connect>
        <Stream url="wss://your-url.ngrok.io/ws" />
      </Connect>
    </Response>
    ```

    Replace `your-url.ngrok.io` with your ngrok URL.

    **For Pipecat Cloud:**

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <Response>
      <Connect>
        <Stream url="wss://api.pipecat.daily.co/ws/twilio">
          <Parameter name="_pipecatCloudServiceHost"
            value="AGENT_NAME.ORGANIZATION_NAME"/>
        </Stream>
      </Connect>
    </Response>
    ```

    Replace:
    - `AGENT_NAME` with the name of the agent you deployed to Pipecat Cloud
    - `ORGANIZATION_NAME` with the name of your Pipecat Cloud organization

5. Click **Save**

#### 2. Assign TwiML Bin to Your Phone Number

1. Navigate to **Phone Numbers** → **Manage** → **Active Numbers**
2. Click on your Twilio phone number
3. In the "Voice Configuration" section:
   - Set "A call comes in" to **TwiML Bin**
   - Select the TwiML Bin you created
4. Click **Save configuration**

### Server

1. **Navigate to server directory**:

   ```bash
   cd server
   ```

2. **Install dependencies**:

   ```bash
   uv sync
   ```

3. **Configure environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. **Run the bot**:

   ```bash
   uv run bot.py
   ```

   The runner serves every transport; the caller selects which one (a web/mobile
   client picks its transport when it connects; a telephony provider connects to
   `/ws`).

   For telephony, expose the bot with a public tunnel and point your provider's
   webhook at it:

   ```bash
   ngrok http 7860
   # then set the provider's webhook to wss://<your-ngrok-host>/ws
   ```

## Project Structure

```
pipecat-telefone/
├── server/              # Python bot server
│   ├── bot.py           # Main bot implementation
│   ├── pyproject.toml   # Python dependencies
│   ├── .env.example     # Environment variables template
│   ├── .env             # Your API keys (git-ignored)
│   └── ...
├── .gitignore           # Git ignore patterns
└── README.md            # This file
```
## Building with an AI coding agent

Extending this bot with Claude Code, Codex, or another AI coding assistant? Give it live, accurate Pipecat context instead of stale training data with the **Pipecat Context Hub** — a local index of Pipecat docs, examples, and API source your agent queries over MCP:

```bash
# The Context Hub ships with the CLI
uv tool install "pipecat-ai[cli]"
pipecat context-hub install
```

`install` registers the MCP server with each coding agent it finds and builds the index — a few minutes and about 900 MB the first time. MCP servers load at session start, so do this before opening your coding session, and note the server won't start against an empty index. See the [Pipecat Context Hub docs](https://docs.pipecat.ai/api-reference/context-hub) for the full setup.

## Learn More

- [Pipecat Documentation](https://docs.pipecat.ai/)
- [Pipecat GitHub](https://github.com/pipecat-ai/pipecat)
- [Pipecat Examples](https://github.com/pipecat-ai/pipecat-examples)
- [Discord Community](https://discord.gg/pipecat)