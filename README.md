# FairPrep AI - Ethical Interview Coach v3.1

**Hackathon-Winning AI Product** - Practice interviews with transparent, bias-aware AI evaluation.

## Features

- **Bias Demonstration Mode** - Side-by-side comparison showing evaluation bias
- **Real-world Bias Simulation** - Demonstrates length bias in AI scoring
- **Ethical AI Banner** - Prominent fairness messaging and adjustments
- **Before vs After Metrics** - Shows fairness-adjusted scores
- **Enhanced Explainability** - Confidence reasoning and decision traces
- **Impact Section** - Compelling ethical AI messaging
- **Professional UI** - Modern design with proper typography
- **No External APIs** - All processing runs locally

## Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/isharak7m/FAIRPREP.git
cd FAIRPREP

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Deployment Options

#### 1. Streamlit Cloud (Recommended - Free)
1. Connect your GitHub repository to [Streamlit Cloud](https://cloud.streamlit.io)
2. Auto-deploys on every push
3. Free tier available

#### 2. Railway (Professional - $5-20/month)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway link
railway up
```

#### 3. Docker (Self-hosted)
```bash
# Build and run
docker build -t fairprep-ai .
docker run -p 8501:8501 fairprep-ai
```

## Architecture

- **Single-file application** (`app.py`) - 1,394 lines
- **Embedded CSS** - No external dependencies
- **Session state management** - User progress tracking
- **Local processing** - No external API calls
- **Bias detection engine** - Custom fairness algorithms

## Technical Stack

- **Framework**: Streamlit 1.28+
- **Language**: Python 3.9+
- **Dependencies**: Minimal (numpy, pandas, plotly, matplotlib)
- **Styling**: Custom CSS with Google Fonts
- **Deployment**: Docker-ready

## Ethical AI Features

- **Bias Detection**: Identifies length bias and content-form imbalance
- **Fairness Audit**: Simulates 3 alternate scoring philosophies
- **Transparency**: Every score explained with reasoning
- **Adjustments**: Automatic bias correction when detected
- **Education**: Users learn about AI evaluation pitfalls

## Demo Mode

Toggle **"Demo Bias Scenario"** to see how two answers of similar quality receive different scores due to evaluation bias - a powerful demonstration of AI fairness issues.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Contact

Created by [Ishara Kavinda](https://github.com/isharak7m)

---

**FairPrep AI** - Making AI evaluation transparent, fair, and educational.
