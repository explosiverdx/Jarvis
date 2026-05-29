# Jarvis - AI Voice Assistant & Automation System

An intelligent AI-powered voice assistant and automation system built with Python. Jarvis can listen to voice commands, process natural language, and execute various automation tasks.

## Features

- 🎤 **Voice Recognition**: Convert speech to text using multiple engines
- 🧠 **Natural Language Processing**: Understand and process user commands
- 🤖 **AI Responses**: Generate intelligent responses using NLP
- ⚙️ **Task Automation**: Execute scheduled tasks and automations
- 📅 **Calendar Integration**: Manage events and reminders
- 🌐 **Web Integration**: Fetch information from the web
- 🔌 **Extensible Plugin System**: Easy to add new capabilities
- 💾 **Persistent Memory**: Remember user preferences and history
- 🔐 **Secure**: Private and secure command execution

## Project Structure

```
Jarvis/
├── jarvis/
│   ├── __init__.py
│   ├── main.py                 # Main entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── voice_engine.py     # Voice recognition and synthesis
│   │   ├── nlp_engine.py       # Natural language processing
│   │   └── command_parser.py   # Command parsing and routing
│   ├── automation/
│   │   ├── __init__.py
│   │   ├── task_scheduler.py   # Task scheduling
│   │   ├── task_executor.py    # Execute automation tasks
│   │   └── plugins/
│   │       ├── __init__.py
│   │       ├── weather.py
│   │       ├── calendar.py
│   │       └── web_search.py
│   ├── memory/
│   │   ├── __init__.py
│   │   └── storage.py          # Persistent storage
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # Configuration management
│       └── logger.py           # Logging utility
├── tests/
│   ├── __init__.py
│   ├── test_voice_engine.py
│   ├── test_nlp_engine.py
│   └── test_automation.py
├── config/
│   ├── settings.yaml           # Configuration file
│   └── commands.json           # Command definitions
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
├── .gitignore
└── LICENSE
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/explosiverdx/Jarvis.git
cd Jarvis
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure settings:
```bash
cp config/settings.yaml.example config/settings.yaml
# Edit config/settings.yaml with your preferences
```

5. Run Jarvis:
```bash
python -m jarvis.main
```

## Usage

### Voice Commands

Start Jarvis and speak naturally:

```
"Hey Jarvis, what's the weather?"
"Schedule a meeting for tomorrow at 2 PM"
"Search for Python tutorials"
"Set a reminder for lunch at noon"
"What time is it?"
```

### Programmatic Usage

```python
from jarvis.core.voice_engine import VoiceEngine
from jarvis.core.nlp_engine import NLPEngine
from jarvis.automation.task_executor import TaskExecutor

# Initialize components
voice = VoiceEngine()
nlp = NLPEngine()
executor = TaskExecutor()

# Listen for voice command
command = voice.listen()

# Process command
intent, entities = nlp.process(command)

# Execute task
result = executor.execute(intent, entities)

# Respond with voice
voice.speak(result)
```

## Configuration

Edit `config/settings.yaml` to customize:

- Voice engine (Google Speech-to-Text, Azure, etc.)
- TTS voice (male/female, accent)
- Language and region
- Automation tasks
- Plugin settings

## Plugins

Jarvis supports a plugin system for extending functionality:

```python
from jarvis.automation.plugins.base import Plugin

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__("my_plugin")
    
    def can_handle(self, intent):
        return intent == "my_custom_intent"
    
    def execute(self, entities):
        # Your automation logic here
        return "Result"
```

## API Reference

See [API_REFERENCE.md](./docs/API_REFERENCE.md) for detailed documentation.

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) file for details.

## Roadmap

- [ ] Machine learning model for custom intents
- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] Smart home automation
- [ ] Advanced scheduling
- [ ] User authentication
- [ ] Web dashboard

## Support

For issues and feature requests, please open an issue on GitHub.

## Author

**explosiverdx** - *AI Assistant & Automation Enthusiast*

---

**Built with ❤️ for automation and AI**
