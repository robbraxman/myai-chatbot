---

## Prerequisites

1. **Install Ollama**
   - Download from [Ollama.com](https://ollama.com/download)
   - Pull your desired models from the Ollama library

2. **Edit my-ai.py**
   - Open `my-ai.py` and update the `model_list` with the models you want to use
   - Set your preferred `multimodal_model` (for image processing)
   - Update the `basepath` to your desired folders for logs, images, text, and context files

---

## Installation

### System Dependencies

```bash
sudo apt install python3-pip
```

### Python Dependencies

```bash
pip install ollama
pip install textwrap
pip install time
```

### Download Ollama Models

To use the models configured in this project, download them with:

```bash
ollama pull llama3
ollama pull llava
ollama pull gemma2
ollama pull qwen2
ollama pull phi3:medium
ollama pull codellama
ollama pull dolphin-llama3
```

---

## Running MyAI

```bash
python3 my-ai.py
```

### Features

- **Multi-model support** - Choose from multiple AI models
- **Multi-line input** - Enter multiple lines by pressing Enter twice
- **Image processing** - Upload images with `/i` command (requires multimodal model)
- **Context/RAG** - Upload text context with `/c` command
- **Session customization** - Fine-tune the AI role and behavior
- **Conversation history** - Automatic logging and context management

### Commands

| Command | Function |
|---------|----------|
| `/i` | Upload an image (multimodal models only) |
| `/c` | Upload context text file |
| `/x` | Clear context and start fresh |
| `/r` | Redo current entry |
| `/?` | Show help information |
| `/bye` | Exit and optionally save context |

---

## Configuration

Edit the following variables in `my-ai.py`:

- `model_list` - Add or remove your preferred models
- `multimodal_model` - Set which model to use for image processing
- `basepath` - Change to your desired working directory

Default folder structure created:
- `images/` - For image uploads
- `logs/` - For query logs
- `text/` - For text files
- `context/` - For context summaries

---

## Notes

- The program uses local Ollama models running on `http://localhost:11434`
- Context is maintained throughout your session and can be saved upon exit
- Query logs are automatically saved with timestamps
- Multiline input requires hitting Enter twice to send
