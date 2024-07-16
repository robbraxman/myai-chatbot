
# How to Use Your Local AI
1. Pre-install Ollama from Ollama.ai and pre-load your desired models.
2. Then edit the my-ai.py file to include the models you want to use.
3. Run the software on your terminal

## Pre-installing Ollama
Install these from the command line.
```bash
# Installing Python and Ollama and other project dependencies:
sudo apt install python3-pip
pip install ollama
pip install textwrap

# or for Python3
pip install textwrap3
```

## Pre-Load Desired Models
After installing Ollama, to load the match the pre-defeined modesl in the my-ai.py file, download the models as follows:
```bash
ollama pull llama3
ollama pull llava
ollama pull phi3:medium
ollama pull codellama
ollama pull dolphin-llama3
```

You can browse [the Ollama library](https://ollama.com/library) for more models.

## Running the program
```bash
python3 my-ai.py
```

And proceed to follow instructions.
