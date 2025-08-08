# Voice Conversion System

A modular voice conversion system with FastAPI backend for real-time voice transformation.

## 🚀 Quick Start

### What is this?
This system allows you to convert one person's voice to sound like another person while preserving the original speech content. It uses modern deep learning techniques for speaker embedding extraction and voice synthesis.

### Current Status
- ✅ **Architecture**: Complete modular design with FastAPI backend
- ✅ **Pipeline**: Voice conversion pipeline with chunking support  
- ✅ **API**: REST endpoints for conversion and voice library management
- ⚠️ **Models**: Core models need implementation (currently placeholder)
- ⚠️ **Testing**: No tests yet - needs test infrastructure

### Get Started in 2 Minutes

1. **Setup Environment**:
   ```bash
   # Run the setup script
   python setup.py
   
   # Or manually install dependencies
   pip install -r voice_conversion_system/requirements.txt
   ```

2. **Check Current Status**:
   ```bash
   cd voice_conversion_system
   python -c "from src.api.main import app; print('✓ API setup successful')"
   ```

3. **What to Do Next**:
   - 📖 **Read the roadmap**: Check `NEXT_STEPS.md` for detailed development plan
   - 🔧 **Start developing**: Follow the priority order in the next steps guide
   - 🧪 **Run tests**: Create your first test audio conversion

## 📁 Project Structure

```
voice_conversion_system/
├── src/
│   ├── api/           # FastAPI REST endpoints
│   ├── core/          # Configuration and logging
│   ├── models/        # ML models (speaker encoder, voice converter, etc.)
│   ├── pipeline/      # Voice conversion pipeline
│   ├── preprocessing/ # Audio processing utilities
│   └── storage/       # Voice library and cache management
├── config/            # YAML configuration files
├── requirements.txt   # Python dependencies
└── NEXT_STEPS.md      # Detailed development roadmap
```

## 🎯 Current Priority: What Do Next?

**The #1 question: "What should we implement next?"**

👉 **Answer**: See `NEXT_STEPS.md` for the complete roadmap!

**Quick summary**:
1. **Setup Environment** (30 min) - Get dependencies working
2. **Implement Core Models** (4-6 hours) - Make placeholders functional  
3. **Basic Voice Conversion** (8-12 hours) - Replace placeholder with real conversion
4. **Add Tests** (3-4 hours) - Ensure reliability
5. **Development Tools** (2-3 hours) - CLI, Docker, examples

## 🔧 Technical Stack

- **Backend**: FastAPI, Python 3.8+
- **ML Framework**: PyTorch, Transformers
- **Audio**: LibROSA, SoundFile, torchaudio
- **Models**: Resemblyzer (speaker), Wav2Vec2 (content), AutoVC (conversion)
- **Config**: YAML with dataclasses

## 📖 Documentation

- `NEXT_STEPS.md` - Complete development roadmap and priorities
- `config/` - Configuration file examples and documentation
- API docs: Start server and visit `http://localhost:8000/docs`

## 🤝 Contributing

This is an active development project. Check `NEXT_STEPS.md` for current priorities and how to contribute.

## 🆘 Need Help?

1. **Can't get started?** Run `python setup.py` 
2. **Don't know what to do next?** Read `NEXT_STEPS.md`
3. **Want to understand the code?** Start with `src/api/main.py` and `src/pipeline/conversion_pipeline.py`

---

**🎯 Current Goal**: Make the system functional with basic voice conversion capabilities!