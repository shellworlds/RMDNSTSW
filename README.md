# 🔮 Quantum Finance Risk Model (QFRM)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-6929C4?style=for-the-badge&logo=qiskit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Advanced quantum simulation for financial market risk analysis**

</div>

---

## 📋 Overview

QFRM is a cutting-edge financial risk analysis tool that combines **quantum computing simulations** with **traditional risk metrics** to provide comprehensive portfolio risk assessment. The model leverages IBM's Qiskit framework to simulate quantum circuits that encode market correlations and volatilities.

### ✨ Key Features

- 🔄 **Real-time Market Data** — Fetches live data from Yahoo Finance (stocks, indices, commodities, crypto)
- ⚛️ **Quantum Risk Simulation** — 20-qubit quantum circuit for risk state analysis
- 📊 **Traditional Metrics** — VaR, CVaR, Sharpe Ratio, Maximum Drawdown, Volatility
- 📈 **Interactive Visualizations** — 3D risk distributions, correlation heatmaps, risk timelines
- 🎬 **Animated Simulations** — 4-second 3D/2D quantum risk evolution animations (GIF)
- 🎯 **Correlation Analysis** — Cross-asset correlation matrices with entropy calculations
- 📋 **Comprehensive Reports** — JSON, PNG, HTML, GIF, and TXT output formats

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/shellworlds/RMDNSTSW.git
cd RMDNSTSW

# Install dependencies
pip install -r requirements.txt

# Run the model
python qfrm.py
```

### Command Line Options

```bash
python qfrm.py --qubits 20 --shots 5000 --output ./finance_risk_output
```

| Option | Description | Default |
|--------|-------------|---------|
| `--qubits` | Number of qubits in quantum circuit | 20 |
| `--shots` | Number of quantum measurement shots | 5000 |
| `--output` | Output directory for reports | ./finance_risk_output |

---

## 📊 Output Files

After execution, the model generates:

| File | Description |
|------|-------------|
| `finance_risk_dashboard_*.png` | Visual risk dashboard with 6 panels |
| `finance_risk_report_*.html` | Interactive Plotly report |
| `finance_risk_report_*.json` | Comprehensive JSON data |
| `risk_summary_*.txt` | Text summary of key metrics |
| `quantum_risk_simulation_*.gif` | 🎬 4-second animated 3D/2D quantum simulation |
| `risk_evolution_*.gif` | 🎬 4-second risk evolution animation |

### 🎬 Animation Features

The model generates two animated GIF simulations:

1. **Quantum Risk Simulation** (`quantum_risk_simulation_*.gif`)
   - 3D particle system showing quantum risk states
   - Evolving risk surface mesh
   - 2D overlapping risk waves (Market, Credit, Quantum)
   - Real-time risk timeline with trajectory

2. **Risk Evolution** (`risk_evolution_*.gif`)
   - 3D helical quantum state visualization
   - 2D polar risk profile with rotating envelope
   - Probability ring animation
   - Synchronized 4-second duration at 30 FPS

---

## 🔬 How It Works

### 1. Data Collection
Fetches 6 months of daily price data for:
- **Stocks**: AAPL, MSFT, GOOGL, AMZN, TSLA, JPM, V, JNJ, WMT, NVDA
- **Indices**: S&P 500, NASDAQ, Dow Jones, Russell 2000
- **Commodities**: Gold, Crude Oil, Silver
- **Crypto**: Bitcoin, Ethereum

### 2. Traditional Risk Metrics
- **Value at Risk (VaR)** — Maximum expected loss at 95% confidence
- **Conditional VaR (CVaR)** — Expected loss beyond VaR threshold
- **Volatility** — Annualized standard deviation of returns
- **Sharpe Ratio** — Risk-adjusted return metric
- **Correlation Entropy** — Portfolio diversification measure

### 3. Quantum Circuit Design

```
┌──────────────────────────────────────────────────────────┐
│ Quantum Finance Circuit (20 qubits)                      │
├──────────────────────────────────────────────────────────┤
│ Layer 1: RY gates (volatility encoding)                  │
│ Layer 2: CRZ gates (correlation entanglement)            │
│ Layer 3: MCX gates (market regime transitions)           │
│ Layer 4: RXX/RYY gates (temporal dynamics)               │
│ Layer 5: CX gates (risk measurement)                     │
│ Layer 6: Measurement                                     │
└──────────────────────────────────────────────────────────┘
```

### 4. Risk State Analysis
Quantum measurement results are analyzed to extract:
- Expected quantum risk score
- Risk volatility
- Pattern-based risk adjustments
- State probability distributions

---

## 📈 Sample Output

```
QUANTUM FINANCE RISK MODEL - ANALYSIS SUMMARY
============================================================
TRADITIONAL RISK METRICS:
------------------------------------------------------------
Value at Risk (95%): -0.0234
Conditional VaR (95%): -0.0412
Annual Volatility: 0.3156
Sharpe Ratio: 0.8421
Maximum Drawdown: 0.1500
------------------------------------------------------------
QUANTUM RISK METRICS:
------------------------------------------------------------
Expected Quantum Risk: 0.4523
Quantum Risk Volatility: 0.1234
Total Quantum States: 4096
Circuit Depth: 127
Total Gates: 312
============================================================
```

---

## 🛠️ Requirements

- Python 3.9+
- Internet connection (for market data)
- ~2GB RAM minimum
- ~500MB disk space

---

## 📁 Project Structure

```
RMDNSTSW/
├── qfrm.py              # Main application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .gitignore          # Git ignore rules
└── finance_risk_output/ # Generated reports (created at runtime)
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [IBM Qiskit](https://qiskit.org/) for quantum computing framework
- [Yahoo Finance](https://finance.yahoo.com/) for market data
- [Plotly](https://plotly.com/) for interactive visualizations

---

<div align="center">

**Built with ❤️ for quantitative finance research**

</div>

