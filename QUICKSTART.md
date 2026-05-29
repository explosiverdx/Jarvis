# Jarvis Quick Start Guide

Get Jarvis up and running in 5 minutes!

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/explosiverdx/Jarvis.git
cd Jarvis
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Jarvis
```bash
cp config/settings.yaml config/settings.local.yaml
# Edit config/settings.local.yaml if needed
```

## Running Jarvis

### Start the Assistant
```bash
python -m jarvis.main
```

You should see:
```
"Hello! I'm Jarvis, your personal assistant. How can I help you?"
```

### Try Some Commands

Once Jarvis is running, try speaking:
- "What time is it?"
- "Hello"
- "Tell me today's date"
- "Help"
- "Goodbye"

## Basic Usage Examples

### Programmatic Usage

```python
from jarvis import VoiceEngine, NLPEngine, TaskExecutor

# Initialize components
voice = VoiceEngine()
nlp = NLPEngine()
executor = TaskExecutor()

# Listen and process
command = voice.listen()
intent, entities = nlp.process(command)
result = executor.execute(intent, entities)

# Respond
voice.speak(result)
```

### Creating Custom Tasks

```python
from jarvis.automation.task_executor import TaskExecutor

executor = TaskExecutor()

def my_custom_task(entities):
    return "Custom task executed!"

executor.register_handler("my_intent", my_custom_task)
```

## Common Issues

### PyAudio Installation Issues
If you have trouble installing PyAudio:

**On macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install python-dev portaudio19-dev
pip install pyaudio
```

**On Windows:**
Use pre-built wheels from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

### Microphone Not Detected
Try specifying the microphone index:
```python
voice = VoiceEngine(config)
voice.microphone = sr.Microphone(device_index=1)  # Change index as needed
```

## Next Steps

- Read the [README](README.md) for detailed documentation
- Check [API_REFERENCE.md](docs/API_REFERENCE.md) for API details
- Create [plugins](jarvis/automation/plugins/) for custom functionality
- Run tests: `pytest`

## Getting Help

- Check existing [Issues](https://github.com/explosiverdx/Jarvis/issues)
- Read [CONTRIBUTING.md](CONTRIBUTING.md)
- Open a new issue with details about your problem

## Useful Links

- [SpeechRecognition Documentation](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)
- [NLTK Documentation](https://www.nltk.org/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)

---

**Enjoy using Jarvis!** 🤖
