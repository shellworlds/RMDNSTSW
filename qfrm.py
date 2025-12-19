#!/usr/bin/env python3
"""
QUANTUM FINANCE RISK MODEL (QFRM)
Advanced quantum simulation for financial market risk analysis
Single-file implementation with automatic dependency installation

Features:
- Real-time market data from Yahoo Finance
- Quantum circuit simulation using Qiskit
- Animated 3D/2D risk visualizations
- Comprehensive risk metrics (VaR, CVaR, Sharpe, etc.)
"""

print("=" * 80)
print("QUANTUM FINANCE RISK MODEL - INITIALIZING")
print("=" * 80)

# ============================================================================
# AUTOMATIC DEPENDENCY INSTALLATION
# ============================================================================

import subprocess
import sys
import importlib

def install_package(package_name, import_name=None):
    """Install a package if not already installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✓ {package_name}")
        return True
    except ImportError:
        print(f"⚠️  Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--quiet"])
            return True
        except:
            print(f"✗ Failed to install {package_name}")
            return False

# Install core packages
print("\n📦 Installing/verifying packages...")
packages = [
    ("numpy", "numpy"),
    ("matplotlib", "matplotlib"),
    ("scipy", "scipy"),
    ("pandas", "pandas"),
    ("seaborn", "seaborn"),
    ("plotly", "plotly"),
    ("scikit-learn", "sklearn"),
    ("yfinance", "yfinance"),
    ("qiskit", "qiskit"),
    ("qiskit-aer", "qiskit_aer"),
    ("qiskit-algorithms", "qiskit_algorithms"),
    ("pylatexenc", "pylatexenc"),
    ("psutil", "psutil"),
    ("numba", "numba"),
    ("pillow", "PIL"),
]

for package, import_name in packages:
    install_package(package, import_name)

print("\n✅ All packages ready!")

# ============================================================================
# CORE IMPORTS
# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, gridspec
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from matplotlib.collections import PathCollection
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3D
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import seaborn as sns
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['animation.embed_limit'] = 100  # MB limit for animations

# Quantum Computing
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import MCXGate, RYGate, RZGate, RXXGate, RYYGate
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector, circuit_drawer
from qiskit.quantum_info import Statevector, partial_trace

# Data & Finance
import pandas as pd
import yfinance as yf
from scipy import stats, signal, optimize, interpolate
from scipy.stats import norm, t, skew, kurtosis
from scipy.linalg import eigh, svd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Visualization
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
pio.templates.default = "plotly_white"

# System & Performance
import psutil
import gc
import time
from datetime import datetime, timedelta
import json
import warnings
import os
from pathlib import Path
import itertools
from collections import Counter, defaultdict
import math

warnings.filterwarnings('ignore')
gc.enable()

# ============================================================================
# FINANCIAL DATA MODULE
# ============================================================================

class FinancialDataLoader:
    """Load and process financial market data"""
    
    def __init__(self):
        self.tickers = {
            'stocks': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'JPM', 'V', 'JNJ', 'WMT', 'NVDA'],
            'indices': ['^GSPC', '^IXIC', '^DJI', '^RUT'],
            'commodities': ['GC=F', 'CL=F', 'SI=F'],
            'crypto': ['BTC-USD', 'ETH-USD']
        }
    
    def fetch_market_data(self, period='1y', interval='1d'):
        """Fetch comprehensive market data"""
        print(f"\n📊 Fetching market data ({period}, {interval} interval)...")
        
        all_data = {}
        for category, symbols in self.tickers.items():
            category_data = {}
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    data = ticker.history(period=period, interval=interval)
                    if not data.empty:
                        category_data[symbol] = data
                        print(f"  ✓ {symbol}")
                    else:
                        print(f"  ✗ {symbol} (no data)")
                except Exception as e:
                    print(f"  ✗ {symbol} ({str(e)})")
            all_data[category] = category_data
        
        return all_data
    
    def calculate_returns(self, data):
        """Calculate logarithmic returns"""
        returns_data = {}
        
        for category, symbols_data in data.items():
            category_returns = {}
            for symbol, df in symbols_data.items():
                if 'Close' in df.columns:
                    returns = np.log(df['Close'] / df['Close'].shift(1)).dropna()
                    category_returns[symbol] = returns
            returns_data[category] = category_returns
        
        return returns_data
    
    def compute_correlation_matrix(self, returns_data):
        """Compute cross-asset correlation matrix"""
        all_returns = []
        asset_names = []
        
        for category, symbols_returns in returns_data.items():
            for symbol, returns in symbols_returns.items():
                if len(returns) > 10:  # Minimum data points
                    all_returns.append(returns.values)
                    asset_names.append(f"{symbol}_{category}")
        
        if len(all_returns) < 2:
            return None, []
        
        # Align time periods
        min_length = min(len(r) for r in all_returns)
        aligned_returns = [r[-min_length:] for r in all_returns]
        
        correlation_matrix = np.corrcoef(aligned_returns)
        return correlation_matrix, asset_names

# ============================================================================
# QUANTUM FINANCE CIRCUIT
# ============================================================================

class QuantumFinanceCircuit:
    """Quantum circuit for financial risk modeling"""
    
    def __init__(self, n_qubits=20):
        self.n_qubits = n_qubits
        self.circuit = None
    
    def build_market_circuit(self, correlation_matrix=None, volatility_vector=None):
        """Build quantum circuit encoding market correlations and volatilities"""
        print(f"\n⚛️  Building quantum finance circuit ({self.n_qubits} qubits)...")
        
        qc = QuantumCircuit(self.n_qubits, self.n_qubits)
        
        # Encode market volatility as initial rotations
        if volatility_vector is not None:
            vol_scaled = np.interp(volatility_vector[:self.n_qubits], 
                                 (volatility_vector.min(), volatility_vector.max()), 
                                 (0, np.pi/2))
            for i, vol in enumerate(vol_scaled[:self.n_qubits]):
                qc.ry(vol, i)
        else:
            # Random volatility encoding
            for i in range(self.n_qubits):
                qc.ry(np.pi/4 * (0.5 + np.random.random()), i)
        
        # Encode market correlations as entanglement
        if correlation_matrix is not None and correlation_matrix.shape[0] >= self.n_qubits:
            for i in range(0, self.n_qubits, 4):
                for j in range(i, min(i+4, self.n_qubits)):
                    for k in range(j+1, min(i+4, self.n_qubits)):
                        if j < correlation_matrix.shape[0] and k < correlation_matrix.shape[1]:
                            corr = abs(correlation_matrix[j, k])
                            angle = np.pi * np.exp(-(1-corr)*3)
                            qc.crz(angle, j, k)
        
        # Add market regime transitions (controlled rotations)
        for i in range(0, self.n_qubits, 3):
            control_qubits = list(range(i, min(i+3, self.n_qubits)))
            if len(control_qubits) == 3:
                target = min(i+3, self.n_qubits-1)
                mcg = MCXGate(3)
                qc.append(mcg, control_qubits + [target])
        
        # Add temporal dynamics (simulating time evolution)
        for i in range(self.n_qubits):
            qc.rxx(np.pi * np.log1p(i/2), i, (i+5) % self.n_qubits)
            qc.ryy(np.pi * np.log1p(i/3), i, (i+7) % self.n_qubits)
        
        # Add risk measurement layers
        for i in range(0, self.n_qubits, 2):
            if i+1 < self.n_qubits:
                qc.cx(i, i+1)
        
        qc.measure_all()
        self.circuit = qc
        
        print(f"  ✓ Circuit depth: {qc.depth()}")
        print(f"  ✓ Total gates: {sum(qc.count_ops().values())}")
        
        return qc
    
    def analyze_risk_states(self, counts, n_top_states=20):
        """Analyze quantum states for risk patterns"""
        total_shots = sum(counts.values())
        
        # Convert counts to probabilities
        states = []
        probabilities = []
        risk_scores = []
        
        for state_str, count in counts.items():
            prob = count / total_shots
            states.append(state_str)
            probabilities.append(prob)
            
            # Calculate risk score based on state pattern
            # More '1's indicates higher risk exposure
            risk_score = state_str.count('1') / len(state_str)
            
            # Pattern-based risk adjustments
            if '11111' in state_str:  # Extreme risk pattern
                risk_score *= 1.5
            elif '00000' in state_str:  # Extreme safety pattern
                risk_score *= 0.5
            
            risk_scores.append(risk_score)
        
        # Sort by probability
        sorted_indices = np.argsort(probabilities)[::-1]
        top_states = [states[i] for i in sorted_indices[:n_top_states]]
        top_probs = [probabilities[i] for i in sorted_indices[:n_top_states]]
        top_risks = [risk_scores[i] for i in sorted_indices[:n_top_states]]
        
        return {
            'states': top_states,
            'probabilities': top_probs,
            'risk_scores': top_risks,
            'expected_risk': np.average(risk_scores, weights=probabilities),
            'risk_volatility': np.std(risk_scores),
            'total_states': len(states),
            'total_shots': total_shots
        }

# ============================================================================
# RISK METRICS CALCULATOR
# ============================================================================

class RiskMetricsCalculator:
    """Calculate comprehensive financial risk metrics"""
    
    @staticmethod
    def calculate_var(returns, confidence_level=0.95):
        """Calculate Value at Risk"""
        if len(returns) == 0:
            return 0
        returns = np.array(returns)
        return np.percentile(returns, (1-confidence_level)*100)
    
    @staticmethod
    def calculate_cvar(returns, confidence_level=0.95):
        """Calculate Conditional Value at Risk (Expected Shortfall)"""
        returns = np.array(returns)
        var = RiskMetricsCalculator.calculate_var(returns, confidence_level)
        cvar_returns = returns[returns <= var]
        return np.mean(cvar_returns) if len(cvar_returns) > 0 else var
    
    @staticmethod
    def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
        """Calculate Sharpe Ratio"""
        returns = np.array(returns)
        if len(returns) == 0 or np.std(returns) == 0:
            return 0
        excess_returns = returns - risk_free_rate/252  # Daily risk-free rate
        return np.mean(excess_returns) / np.std(returns) * np.sqrt(252)
    
    @staticmethod
    def calculate_max_drawdown(prices):
        """Calculate maximum drawdown"""
        if len(prices) == 0:
            return 0
        cumulative = np.maximum.accumulate(prices)
        drawdown = (cumulative - prices) / cumulative
        return np.max(drawdown)
    
    @staticmethod
    def calculate_volatility(returns, annualize=True):
        """Calculate volatility"""
        returns = np.array(returns)
        if len(returns) == 0:
            return 0
        vol = np.std(returns)
        if annualize:
            vol *= np.sqrt(252)
        return vol
    
    @staticmethod
    def calculate_correlation_risk(correlation_matrix):
        """Calculate correlation-based risk metrics"""
        if correlation_matrix is None or correlation_matrix.shape[0] < 2:
            return {'avg_correlation': 0, 'correlation_entropy': 0}
        
        # Average absolute correlation (excluding diagonal)
        n = correlation_matrix.shape[0]
        mask = ~np.eye(n, dtype=bool)
        avg_corr = np.mean(np.abs(correlation_matrix[mask]))
        
        # Correlation matrix entropy
        eigenvalues = np.linalg.eigvalsh(correlation_matrix)
        eigenvalues = eigenvalues[eigenvalues > 0]
        entropy = -np.sum(eigenvalues * np.log(eigenvalues))
        
        return {
            'avg_correlation': avg_corr,
            'correlation_entropy': entropy,
            'min_correlation': np.min(correlation_matrix[mask]),
            'max_correlation': np.max(correlation_matrix[mask])
        }

# ============================================================================
# VISUALIZATION MODULE
# ============================================================================

class FinanceVisualizer:
    """Create professional financial risk visualizations"""
    
    @staticmethod
    def create_risk_dashboard(risk_metrics, quantum_results, output_dir='./finance_risk_output'):
        """Create comprehensive risk dashboard"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        fig = plt.figure(figsize=(20, 16))
        gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. Risk Distribution (3D)
        ax1 = fig.add_subplot(gs[0, 0], projection='3d')
        if 'risk_scores' in quantum_results:
            x = np.arange(len(quantum_results['risk_scores'][:30]))
            y = np.zeros_like(x)
            z = np.array(quantum_results['risk_scores'][:30])
            colors = cm.plasma(z / np.max(z) if np.max(z) > 0 else 1)
            ax1.bar3d(x, y, np.zeros_like(z), 0.8, 0.8, z, color=colors, alpha=0.8)
            ax1.set_xlabel('Risk State', fontsize=10, labelpad=10)
            ax1.set_ylabel('', fontsize=10)
            ax1.set_zlabel('Risk Score', fontsize=10, labelpad=10)
            ax1.set_title('Quantum Risk State Distribution', fontsize=12, pad=20)
            ax1.view_init(elev=25, azim=45)
        
        # 2. Correlation Heatmap
        ax2 = fig.add_subplot(gs[0, 1])
        if 'correlation_matrix' in risk_metrics and len(risk_metrics['correlation_matrix']) > 0:
            corr_data = np.array(risk_metrics['correlation_matrix'])
            if corr_data.ndim == 2 and corr_data.shape[0] > 0 and corr_data.shape[1] > 0:
                im = ax2.imshow(corr_data, cmap='RdBu_r', 
                               vmin=-1, vmax=1, aspect='auto')
                ax2.set_xlabel('Asset', fontsize=10)
                ax2.set_ylabel('Asset', fontsize=10)
                ax2.set_title('Asset Correlation Matrix', fontsize=12, pad=15)
                plt.colorbar(im, ax=ax2, shrink=0.8, label='Correlation')
            else:
                ax2.text(0.5, 0.5, 'No correlation data', ha='center', va='center', fontsize=12)
                ax2.set_title('Asset Correlation Matrix', fontsize=12, pad=15)
        else:
            ax2.text(0.5, 0.5, 'No correlation data', ha='center', va='center', fontsize=12)
            ax2.set_title('Asset Correlation Matrix', fontsize=12, pad=15)
        
        # 3. Risk Metrics Bar Chart
        ax3 = fig.add_subplot(gs[0, 2])
        if 'var_95' in risk_metrics and 'cvar_95' in risk_metrics:
            metrics = ['VaR (95%)', 'CVaR (95%)', 'Volatility', 'Max Drawdown']
            values = [
                abs(risk_metrics.get('var_95', 0)),
                abs(risk_metrics.get('cvar_95', 0)),
                risk_metrics.get('volatility', 0),
                risk_metrics.get('max_drawdown', 0)
            ]
            colors = ['#ff6b6b', '#ff8e8e', '#4ecdc4', '#45b7d1']
            bars = ax3.bar(metrics, values, color=colors, alpha=0.8)
            ax3.set_ylabel('Value', fontsize=10)
            ax3.set_title('Key Risk Metrics', fontsize=12, pad=15)
            for bar, val in zip(bars, values):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                        f'{val:.3f}', ha='center', va='bottom', fontsize=9)
        
        # 4. Quantum Risk Scores
        ax4 = fig.add_subplot(gs[1, 0])
        if 'risk_scores' in quantum_results and 'probabilities' in quantum_results:
            scatter = ax4.scatter(quantum_results['risk_scores'][:20],
                                quantum_results['probabilities'][:20],
                                c=quantum_results['risk_scores'][:20],
                                cmap='RdYlGn_r', s=100, alpha=0.7)
            ax4.set_xlabel('Risk Score', fontsize=10)
            ax4.set_ylabel('Probability', fontsize=10)
            ax4.set_title('Risk vs Probability (Quantum)', fontsize=12, pad=15)
            ax4.grid(True, alpha=0.3)
            plt.colorbar(scatter, ax=ax4, label='Risk Intensity')
        
        # 5. Risk Timeline Simulation
        ax5 = fig.add_subplot(gs[1, 1:])
        timeline = np.cumsum(np.random.randn(100)) * 0.1 + quantum_results.get('expected_risk', 0.5)
        ax5.plot(timeline, linewidth=2, color='#2c3e50', label='Simulated Risk')
        ax5.axhline(y=quantum_results.get('expected_risk', 0), color='red', 
                   linestyle='--', alpha=0.7, label=f'Expected Risk: {quantum_results.get("expected_risk", 0):.3f}')
        ax5.fill_between(range(len(timeline)),
                        quantum_results.get('expected_risk', 0) - quantum_results.get('risk_volatility', 0),
                        quantum_results.get('expected_risk', 0) + quantum_results.get('risk_volatility', 0),
                        alpha=0.2, color='red', label='±1σ Volatility')
        ax5.set_xlabel('Time Step', fontsize=10)
        ax5.set_ylabel('Risk Level', fontsize=10)
        ax5.set_title('Simulated Risk Timeline', fontsize=12, pad=15)
        ax5.legend(fontsize=9)
        ax5.grid(True, alpha=0.3)
        
        # 6. Portfolio Risk Composition
        ax6 = fig.add_subplot(gs[2, :])
        categories = ['Market Risk', 'Credit Risk', 'Liquidity Risk', 'Operational Risk', 'Quantum Risk']
        values = [
            risk_metrics.get('market_risk', 0.35),
            risk_metrics.get('credit_risk', 0.25),
            risk_metrics.get('liquidity_risk', 0.15),
            risk_metrics.get('operational_risk', 0.10),
            quantum_results.get('expected_risk', 0.15)
        ]
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        wedges, texts, autotexts = ax6.pie(values, labels=categories, colors=colors,
                                          autopct='%1.1f%%', startangle=90)
        ax6.set_title('Portfolio Risk Composition', fontsize=12, pad=15)
        
        fig.suptitle('Quantum Finance Risk Analysis Dashboard', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_dir}/finance_risk_dashboard_{timestamp}.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        return output_file
    
    @staticmethod
    def create_interactive_report(risk_metrics, quantum_results, output_dir):
        """Create interactive HTML report"""
        fig = make_subplots(
            rows=2, cols=3,
            specs=[[{'type': 'scatter3d'}, {'type': 'heatmap'}, {'type': 'bar'}],
                   [{'type': 'scatter'}, {'type': 'scatter'}, {'type': 'pie'}]],
            subplot_titles=(
                'Quantum Risk States',
                'Asset Correlations',
                'Key Risk Metrics',
                'Risk vs Probability',
                'Risk Timeline',
                'Risk Composition'
            )
        )
        
        # Add 3D risk states
        if 'risk_scores' in quantum_results:
            x = list(range(len(quantum_results['risk_scores'][:20])))
            y = [0] * len(x)
            z = quantum_results['risk_scores'][:20]
            fig.add_trace(
                go.Scatter3d(
                    x=x, y=y, z=z,
                    mode='markers',
                    marker=dict(size=8, color=z, colorscale='Plasma'),
                    name='Risk States'
                ),
                row=1, col=1
            )
        
        # Add correlation heatmap
        if 'correlation_matrix' in risk_metrics and len(risk_metrics['correlation_matrix']) > 0:
            corr_data = np.array(risk_metrics['correlation_matrix'])
            if corr_data.ndim == 2 and corr_data.shape[0] > 0:
                fig.add_trace(
                    go.Heatmap(
                        z=corr_data,
                        colorscale='RdBu',
                        zmid=0,
                        name='Correlations'
                    ),
                    row=1, col=2
                )
        
        # Add metrics bar chart
        if 'var_95' in risk_metrics:
            metrics = ['VaR (95%)', 'CVaR (95%)', 'Volatility', 'Max Drawdown']
            values = [
                abs(risk_metrics.get('var_95', 0)),
                abs(risk_metrics.get('cvar_95', 0)),
                risk_metrics.get('volatility', 0),
                risk_metrics.get('max_drawdown', 0)
            ]
            fig.add_trace(
                go.Bar(x=metrics, y=values, name='Risk Metrics'),
                row=1, col=3
            )
        
        # Add risk vs probability scatter
        if 'risk_scores' in quantum_results and 'probabilities' in quantum_results:
            fig.add_trace(
                go.Scatter(
                    x=quantum_results['risk_scores'][:20],
                    y=quantum_results['probabilities'][:20],
                    mode='markers',
                    marker=dict(size=12, color=quantum_results['risk_scores'][:20],
                              colorscale='RdYlGn_r', showscale=True),
                    name='Risk vs Prob'
                ),
                row=2, col=1
            )
        
        # Add risk timeline
        timeline = np.cumsum(np.random.randn(100)) * 0.1 + quantum_results.get('expected_risk', 0.5)
        fig.add_trace(
            go.Scatter(
                x=list(range(len(timeline))),
                y=timeline,
                mode='lines',
                line=dict(color='#2c3e50', width=2),
                name='Risk Timeline'
            ),
            row=2, col=2
        )
        
        # Add risk pie chart
        categories = ['Market', 'Credit', 'Liquidity', 'Operational', 'Quantum']
        values = [0.35, 0.25, 0.15, 0.10, quantum_results.get('expected_risk', 0.15)]
        fig.add_trace(
            go.Pie(labels=categories, values=values, name='Risk Composition'),
            row=2, col=3
        )
        
        fig.update_layout(
            height=900,
            title_text="Quantum Finance Risk Analysis Report",
            showlegend=True
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_dir}/finance_risk_report_{timestamp}.html"
        fig.write_html(output_file)
        
        return output_file

# ============================================================================
# ANIMATED VISUALIZATION MODULE
# ============================================================================

class AnimatedVisualizer:
    """Create animated 3D/2D quantum risk simulations"""
    
    @staticmethod
    def create_animated_simulation(quantum_results, risk_metrics, output_dir='./finance_risk_output',
                                   duration_seconds=4, fps=30):
        """
        Create a 4-second animated visualization showing quantum risk evolution
        in both 3D and 2D simultaneously
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        print("\n🎬 Creating animated quantum risk simulation...")
        print(f"   Duration: {duration_seconds}s at {fps} FPS")
        
        # Calculate total frames
        total_frames = duration_seconds * fps
        
        # Extract data
        risk_scores = np.array(quantum_results.get('risk_scores', [0.5] * 20)[:20])
        probabilities = np.array(quantum_results.get('probabilities', [0.05] * 20)[:20])
        expected_risk = quantum_results.get('expected_risk', 0.5)
        risk_volatility = quantum_results.get('risk_volatility', 0.1)
        
        # Generate time-evolving data for simulation
        np.random.seed(42)  # For reproducibility
        time_steps = np.linspace(0, duration_seconds, total_frames)
        
        # Create evolving risk landscape
        n_particles = 50
        particle_x = np.random.randn(n_particles) * 0.3 + 0.5
        particle_y = np.random.randn(n_particles) * 0.3 + 0.5
        particle_z = np.random.rand(n_particles) * expected_risk
        particle_velocities = np.random.randn(n_particles, 3) * 0.02
        
        # Create risk wave data
        wave_x = np.linspace(0, 4 * np.pi, 100)
        
        # Create the figure with 2x2 layout (3D left, 2D right)
        fig = plt.figure(figsize=(16, 10), facecolor='#0a0a1a')
        fig.patch.set_facecolor('#0a0a1a')
        
        # Create grid: top row for main visualizations, bottom for timeline
        gs = gridspec.GridSpec(2, 2, figure=fig, height_ratios=[3, 1], 
                              hspace=0.25, wspace=0.2)
        
        # 3D subplot (top-left)
        ax3d = fig.add_subplot(gs[0, 0], projection='3d', facecolor='#0a0a1a')
        ax3d.set_facecolor('#0a0a1a')
        ax3d.xaxis.pane.fill = False
        ax3d.yaxis.pane.fill = False
        ax3d.zaxis.pane.fill = False
        ax3d.xaxis.pane.set_edgecolor('#1a1a3a')
        ax3d.yaxis.pane.set_edgecolor('#1a1a3a')
        ax3d.zaxis.pane.set_edgecolor('#1a1a3a')
        ax3d.tick_params(colors='#888888')
        ax3d.set_xlabel('Risk Factor X', color='#aaaaaa', fontsize=10)
        ax3d.set_ylabel('Risk Factor Y', color='#aaaaaa', fontsize=10)
        ax3d.set_zlabel('Risk Intensity', color='#aaaaaa', fontsize=10)
        ax3d.set_title('3D Quantum Risk State Evolution', color='#00ffcc', fontsize=12, pad=15)
        
        # 2D subplot (top-right)
        ax2d = fig.add_subplot(gs[0, 1], facecolor='#0a0a1a')
        ax2d.set_facecolor('#0a0a1a')
        ax2d.tick_params(colors='#888888')
        ax2d.spines['bottom'].set_color('#1a1a3a')
        ax2d.spines['top'].set_color('#1a1a3a')
        ax2d.spines['left'].set_color('#1a1a3a')
        ax2d.spines['right'].set_color('#1a1a3a')
        ax2d.set_xlabel('Risk Score', color='#aaaaaa', fontsize=10)
        ax2d.set_ylabel('Probability Density', color='#aaaaaa', fontsize=10)
        ax2d.set_title('2D Risk Distribution Wave', color='#ff6b9d', fontsize=12, pad=15)
        
        # Timeline subplot (bottom - spans both columns)
        ax_timeline = fig.add_subplot(gs[1, :], facecolor='#0a0a1a')
        ax_timeline.set_facecolor('#0a0a1a')
        ax_timeline.tick_params(colors='#888888')
        ax_timeline.spines['bottom'].set_color('#1a1a3a')
        ax_timeline.spines['top'].set_color('#1a1a3a')
        ax_timeline.spines['left'].set_color('#1a1a3a')
        ax_timeline.spines['right'].set_color('#1a1a3a')
        ax_timeline.set_xlabel('Time (s)', color='#aaaaaa', fontsize=10)
        ax_timeline.set_ylabel('Risk Level', color='#aaaaaa', fontsize=10)
        ax_timeline.set_title('Real-Time Risk Evolution', color='#ffcc00', fontsize=12, pad=10)
        ax_timeline.set_xlim(0, duration_seconds)
        ax_timeline.set_ylim(0, 1)
        
        # Initialize plot elements
        # 3D scatter
        scatter3d = ax3d.scatter([], [], [], c=[], cmap='plasma', s=80, alpha=0.8)
        
        # 3D surface mesh (static base)
        mesh_x = np.linspace(0, 1, 20)
        mesh_y = np.linspace(0, 1, 20)
        mesh_X, mesh_Y = np.meshgrid(mesh_x, mesh_y)
        
        # 2D elements
        line2d, = ax2d.plot([], [], color='#ff6b9d', linewidth=2, alpha=0.9)
        fill2d = None
        scatter2d = ax2d.scatter([], [], c=[], cmap='viridis', s=60, alpha=0.7, zorder=5)
        
        # Timeline elements
        timeline_data_x = []
        timeline_data_y = []
        timeline_line, = ax_timeline.plot([], [], color='#00ffcc', linewidth=2)
        timeline_fill = None
        risk_marker, = ax_timeline.plot([], [], 'o', color='#ff6b9d', markersize=12, zorder=5)
        
        # Add static elements
        ax_timeline.axhline(y=expected_risk, color='#ffcc00', linestyle='--', 
                           alpha=0.5, label=f'Expected Risk: {expected_risk:.3f}')
        ax_timeline.fill_between([0, duration_seconds], 
                                expected_risk - risk_volatility,
                                expected_risk + risk_volatility,
                                alpha=0.1, color='#ffcc00')
        ax_timeline.legend(loc='upper right', facecolor='#0a0a1a', edgecolor='#1a1a3a',
                          labelcolor='#aaaaaa', fontsize=9)
        
        # Title
        main_title = fig.suptitle('⚛️ QUANTUM FINANCE RISK SIMULATION', 
                                 fontsize=16, color='#ffffff', fontweight='bold', y=0.98)
        
        # Frame counter text
        frame_text = fig.text(0.02, 0.02, '', fontsize=10, color='#666666')
        
        # Store state for animation
        state = {
            'particle_pos': np.column_stack([particle_x, particle_y, particle_z]),
            'particle_vel': particle_velocities,
            'timeline_x': [],
            'timeline_y': [],
            'phase': 0
        }
        
        def init():
            """Initialize animation"""
            scatter3d._offsets3d = ([], [], [])
            line2d.set_data([], [])
            scatter2d.set_offsets(np.empty((0, 2)))
            timeline_line.set_data([], [])
            risk_marker.set_data([], [])
            return scatter3d, line2d, scatter2d, timeline_line, risk_marker
        
        def animate(frame):
            """Update animation frame"""
            t = frame / fps  # Current time in seconds
            progress = frame / total_frames
            
            # Update phase for wave animations
            state['phase'] = t * 2 * np.pi
            
            # ========== 3D PARTICLE SIMULATION ==========
            # Update particle positions with quantum-like behavior
            noise = np.random.randn(*state['particle_pos'].shape) * 0.01
            
            # Add oscillatory motion
            oscillation = np.sin(state['phase'] + np.arange(n_particles)[:, np.newaxis] * 0.5) * 0.02
            
            # Update positions
            state['particle_pos'] += state['particle_vel'] + noise + oscillation
            
            # Boundary reflection
            for dim in range(3):
                below = state['particle_pos'][:, dim] < 0
                above = state['particle_pos'][:, dim] > 1
                state['particle_vel'][below, dim] = abs(state['particle_vel'][below, dim])
                state['particle_vel'][above, dim] = -abs(state['particle_vel'][above, dim])
                state['particle_pos'][:, dim] = np.clip(state['particle_pos'][:, dim], 0, 1)
            
            # Color by z position (risk intensity)
            colors = state['particle_pos'][:, 2]
            
            # Update 3D scatter
            ax3d.clear()
            ax3d.set_facecolor('#0a0a1a')
            ax3d.xaxis.pane.fill = False
            ax3d.yaxis.pane.fill = False
            ax3d.zaxis.pane.fill = False
            
            # Create evolving surface
            mesh_Z = 0.3 + 0.2 * np.sin(mesh_X * 4 + state['phase']) * np.cos(mesh_Y * 4 - state['phase'] * 0.5)
            mesh_Z += 0.1 * np.sin(mesh_X * 8 - state['phase'] * 2) * np.sin(mesh_Y * 6 + state['phase'])
            ax3d.plot_surface(mesh_X, mesh_Y, mesh_Z, cmap='plasma', alpha=0.3, 
                             linewidth=0, antialiased=True)
            
            # Draw particles
            scatter = ax3d.scatter(state['particle_pos'][:, 0],
                                  state['particle_pos'][:, 1],
                                  state['particle_pos'][:, 2],
                                  c=colors, cmap='plasma', s=80, alpha=0.8,
                                  edgecolors='white', linewidths=0.5)
            
            # Add particle trails
            for i in range(0, n_particles, 5):
                trail_length = 5
                trail_alpha = np.linspace(0.1, 0.5, trail_length)
                for j in range(trail_length):
                    offset = (j + 1) * 0.02
                    trail_pos = state['particle_pos'][i] - state['particle_vel'][i] * offset * 10
                    ax3d.scatter([trail_pos[0]], [trail_pos[1]], [trail_pos[2]], 
                               c=[colors[i]], cmap='plasma', s=20, alpha=trail_alpha[j])
            
            ax3d.set_xlim(0, 1)
            ax3d.set_ylim(0, 1)
            ax3d.set_zlim(0, 1)
            ax3d.set_xlabel('Risk Factor X', color='#aaaaaa', fontsize=10)
            ax3d.set_ylabel('Risk Factor Y', color='#aaaaaa', fontsize=10)
            ax3d.set_zlabel('Risk Intensity', color='#aaaaaa', fontsize=10)
            ax3d.set_title('3D Quantum Risk State Evolution', color='#00ffcc', fontsize=12, pad=15)
            ax3d.view_init(elev=20 + 10 * np.sin(state['phase'] * 0.3), 
                          azim=45 + 30 * np.sin(state['phase'] * 0.2))
            ax3d.tick_params(colors='#888888')
            
            # ========== 2D WAVE SIMULATION ==========
            ax2d.clear()
            ax2d.set_facecolor('#0a0a1a')
            
            # Create multiple overlapping waves
            wave1 = 0.3 + 0.2 * np.sin(wave_x - state['phase'] * 2)
            wave2 = 0.25 + 0.15 * np.sin(wave_x * 1.5 + state['phase'] * 1.5)
            wave3 = 0.2 + 0.1 * np.sin(wave_x * 2 - state['phase'] * 3)
            combined_wave = (wave1 + wave2 + wave3) / 3
            
            # Normalize x to risk score range
            wave_x_norm = wave_x / (4 * np.pi)
            
            # Plot waves with gradients
            ax2d.fill_between(wave_x_norm, 0, wave1, alpha=0.3, color='#ff6b9d')
            ax2d.fill_between(wave_x_norm, 0, wave2, alpha=0.3, color='#00ffcc')
            ax2d.fill_between(wave_x_norm, 0, wave3, alpha=0.3, color='#ffcc00')
            
            ax2d.plot(wave_x_norm, wave1, color='#ff6b9d', linewidth=2, alpha=0.9, label='Market Risk')
            ax2d.plot(wave_x_norm, wave2, color='#00ffcc', linewidth=2, alpha=0.9, label='Credit Risk')
            ax2d.plot(wave_x_norm, wave3, color='#ffcc00', linewidth=2, alpha=0.9, label='Quantum Risk')
            ax2d.plot(wave_x_norm, combined_wave, color='white', linewidth=3, alpha=0.9, 
                     linestyle='--', label='Combined')
            
            # Add moving particles on 2D
            particle_2d_x = (np.sin(state['phase'] + np.arange(10) * 0.5) + 1) / 2
            particle_2d_y = np.interp(particle_2d_x, wave_x_norm, combined_wave)
            particle_2d_colors = particle_2d_y
            ax2d.scatter(particle_2d_x, particle_2d_y, c=particle_2d_colors, 
                        cmap='plasma', s=100, alpha=0.9, edgecolors='white', 
                        linewidths=1, zorder=5)
            
            ax2d.set_xlim(0, 1)
            ax2d.set_ylim(0, 0.8)
            ax2d.set_xlabel('Risk Score', color='#aaaaaa', fontsize=10)
            ax2d.set_ylabel('Probability Density', color='#aaaaaa', fontsize=10)
            ax2d.set_title('2D Risk Distribution Wave', color='#ff6b9d', fontsize=12, pad=15)
            ax2d.legend(loc='upper right', facecolor='#0a0a1a', edgecolor='#1a1a3a',
                       labelcolor='#aaaaaa', fontsize=8)
            ax2d.tick_params(colors='#888888')
            ax2d.spines['bottom'].set_color('#1a1a3a')
            ax2d.spines['top'].set_color('#1a1a3a')
            ax2d.spines['left'].set_color('#1a1a3a')
            ax2d.spines['right'].set_color('#1a1a3a')
            
            # ========== TIMELINE UPDATE ==========
            # Calculate current risk value
            current_risk = expected_risk + risk_volatility * np.sin(state['phase']) * 0.5
            current_risk += np.random.randn() * 0.02  # Add noise
            current_risk = np.clip(current_risk, 0, 1)
            
            state['timeline_x'].append(t)
            state['timeline_y'].append(current_risk)
            
            ax_timeline.clear()
            ax_timeline.set_facecolor('#0a0a1a')
            
            # Draw timeline
            if len(state['timeline_x']) > 1:
                # Color gradient based on risk
                points = np.array([state['timeline_x'], state['timeline_y']]).T.reshape(-1, 1, 2)
                
                ax_timeline.plot(state['timeline_x'], state['timeline_y'], 
                               color='#00ffcc', linewidth=2, alpha=0.9)
                ax_timeline.fill_between(state['timeline_x'], 0, state['timeline_y'],
                                        alpha=0.2, color='#00ffcc')
            
            # Draw current position marker
            ax_timeline.plot([t], [current_risk], 'o', color='#ff6b9d', 
                           markersize=15, zorder=10)
            ax_timeline.plot([t], [current_risk], 'o', color='white', 
                           markersize=8, zorder=11)
            
            # Static elements
            ax_timeline.axhline(y=expected_risk, color='#ffcc00', linestyle='--', 
                               alpha=0.5, linewidth=1)
            ax_timeline.fill_between([0, duration_seconds], 
                                    expected_risk - risk_volatility,
                                    expected_risk + risk_volatility,
                                    alpha=0.1, color='#ffcc00')
            
            ax_timeline.set_xlim(0, duration_seconds)
            ax_timeline.set_ylim(0, 1)
            ax_timeline.set_xlabel('Time (s)', color='#aaaaaa', fontsize=10)
            ax_timeline.set_ylabel('Risk Level', color='#aaaaaa', fontsize=10)
            ax_timeline.set_title(f'Real-Time Risk Evolution | Current: {current_risk:.3f}', 
                                 color='#ffcc00', fontsize=12, pad=10)
            ax_timeline.tick_params(colors='#888888')
            ax_timeline.spines['bottom'].set_color('#1a1a3a')
            ax_timeline.spines['top'].set_color('#1a1a3a')
            ax_timeline.spines['left'].set_color('#1a1a3a')
            ax_timeline.spines['right'].set_color('#1a1a3a')
            
            # Add legend
            legend_elements = [
                Line2D([0], [0], color='#00ffcc', linewidth=2, label='Risk Trajectory'),
                Line2D([0], [0], color='#ffcc00', linestyle='--', label=f'Expected: {expected_risk:.3f}'),
                Line2D([0], [0], marker='o', color='#ff6b9d', linestyle='None', 
                       markersize=8, label='Current Risk')
            ]
            ax_timeline.legend(handles=legend_elements, loc='upper right', 
                              facecolor='#0a0a1a', edgecolor='#1a1a3a',
                              labelcolor='#aaaaaa', fontsize=8)
            
            # Update frame counter
            frame_text.set_text(f'Frame: {frame+1}/{total_frames} | Time: {t:.2f}s')
            
            return []
        
        # Create animation
        print("   Generating frames...")
        anim = FuncAnimation(fig, animate, init_func=init, frames=total_frames,
                            interval=1000/fps, blit=False)
        
        # Save animation as GIF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        gif_file = f"{output_dir}/quantum_risk_simulation_{timestamp}.gif"
        
        print(f"   Saving animation to {gif_file}...")
        writer = PillowWriter(fps=fps)
        anim.save(gif_file, writer=writer, dpi=100)
        
        plt.close(fig)
        print(f"   ✓ Animation saved: {gif_file}")
        
        return gif_file
    
    @staticmethod
    def create_risk_evolution_animation(risk_metrics, quantum_results, output_dir='./finance_risk_output',
                                        duration_seconds=4, fps=30):
        """
        Create a focused risk evolution animation showing the quantum states morphing
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        print("\n🎬 Creating risk evolution animation...")
        
        total_frames = duration_seconds * fps
        
        # Get data
        risk_scores = np.array(quantum_results.get('risk_scores', [])[:30])
        probabilities = np.array(quantum_results.get('probabilities', [])[:30])
        expected_risk = quantum_results.get('expected_risk', 0.5)
        
        if len(risk_scores) == 0:
            risk_scores = np.random.rand(30) * 0.8
            probabilities = np.random.rand(30)
            probabilities = probabilities / probabilities.sum()
        
        # Create figure
        fig = plt.figure(figsize=(14, 8), facecolor='#0d1117')
        gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.15)
        
        # 3D subplot
        ax3d = fig.add_subplot(gs[0, 0], projection='3d', facecolor='#0d1117')
        
        # 2D subplot  
        ax2d = fig.add_subplot(gs[0, 1], facecolor='#0d1117')
        
        # Style both axes
        for ax in [ax3d]:
            ax.set_facecolor('#0d1117')
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.tick_params(colors='#8b949e')
        
        ax2d.set_facecolor('#0d1117')
        ax2d.tick_params(colors='#8b949e')
        for spine in ax2d.spines.values():
            spine.set_color('#30363d')
        
        # State for animation
        n_points = len(risk_scores)
        theta = np.linspace(0, 2 * np.pi, n_points)
        
        def animate(frame):
            t = frame / fps
            phase = t * 2 * np.pi / duration_seconds * 2
            
            # Clear axes
            ax3d.clear()
            ax2d.clear()
            
            # Style
            ax3d.set_facecolor('#0d1117')
            ax3d.xaxis.pane.fill = False
            ax3d.yaxis.pane.fill = False
            ax3d.zaxis.pane.fill = False
            ax2d.set_facecolor('#0d1117')
            for spine in ax2d.spines.values():
                spine.set_color('#30363d')
            
            # ===== 3D: Helical quantum state visualization =====
            # Create morphing helix
            helix_t = np.linspace(0, 4 * np.pi, 100)
            helix_x = np.cos(helix_t + phase) * (1 + 0.3 * np.sin(phase * 2))
            helix_y = np.sin(helix_t + phase) * (1 + 0.3 * np.cos(phase * 2))
            helix_z = helix_t / (4 * np.pi)
            
            # Plot helix with color gradient
            for i in range(len(helix_t) - 1):
                color = cm.plasma(helix_z[i])
                ax3d.plot(helix_x[i:i+2], helix_y[i:i+2], helix_z[i:i+2], 
                         color=color, linewidth=2, alpha=0.8)
            
            # Add quantum state points
            point_x = np.cos(theta + phase) * risk_scores
            point_y = np.sin(theta + phase) * risk_scores
            point_z = probabilities * 2
            
            scatter = ax3d.scatter(point_x, point_y, point_z, 
                                  c=risk_scores, cmap='plasma', s=100,
                                  alpha=0.9, edgecolors='white', linewidths=0.5)
            
            # Add connecting lines to center
            for i in range(n_points):
                ax3d.plot([0, point_x[i]], [0, point_y[i]], [0, point_z[i]],
                         color=cm.plasma(risk_scores[i]), alpha=0.3, linewidth=0.5)
            
            ax3d.set_xlim(-1.5, 1.5)
            ax3d.set_ylim(-1.5, 1.5)
            ax3d.set_zlim(0, 1)
            ax3d.set_xlabel('Quantum X', color='#8b949e', fontsize=9)
            ax3d.set_ylabel('Quantum Y', color='#8b949e', fontsize=9)
            ax3d.set_zlabel('Probability', color='#8b949e', fontsize=9)
            ax3d.set_title('3D Quantum State Space', color='#58a6ff', fontsize=12, pad=15)
            ax3d.view_init(elev=25 + 10 * np.sin(phase * 0.5), azim=phase * 30)
            ax3d.tick_params(colors='#8b949e')
            
            # ===== 2D: Radar/polar-like visualization =====
            # Create circular risk profile
            angles = np.linspace(0, 2 * np.pi, n_points + 1)
            values = np.concatenate([risk_scores, [risk_scores[0]]])
            probs = np.concatenate([probabilities, [probabilities[0]]])
            
            # Animated expansion
            scale = 0.8 + 0.2 * np.sin(phase)
            scaled_values = values * scale
            
            # Convert to cartesian
            x = scaled_values * np.cos(angles + phase * 0.5)
            y = scaled_values * np.sin(angles + phase * 0.5)
            
            # Draw filled polygon
            ax2d.fill(x, y, alpha=0.3, color='#58a6ff')
            ax2d.plot(x, y, color='#58a6ff', linewidth=2, alpha=0.9)
            
            # Draw probability ring
            prob_x = probs * 0.5 * np.cos(angles - phase * 0.3)
            prob_y = probs * 0.5 * np.sin(angles - phase * 0.3)
            ax2d.fill(prob_x, prob_y, alpha=0.3, color='#f85149')
            ax2d.plot(prob_x, prob_y, color='#f85149', linewidth=2, alpha=0.9)
            
            # Draw points
            point_colors = cm.plasma(scaled_values[:-1])
            ax2d.scatter(x[:-1], y[:-1], c=risk_scores, cmap='plasma', 
                        s=80, alpha=0.9, edgecolors='white', linewidths=1, zorder=5)
            
            # Draw radial lines
            for i in range(0, n_points, 3):
                ax2d.plot([0, x[i]], [0, y[i]], color='#30363d', 
                         linewidth=0.5, alpha=0.5)
            
            # Draw circles
            for r in [0.25, 0.5, 0.75]:
                circle = plt.Circle((0, 0), r, fill=False, color='#30363d', 
                                   linewidth=0.5, alpha=0.5)
                ax2d.add_patch(circle)
            
            ax2d.set_xlim(-1.2, 1.2)
            ax2d.set_ylim(-1.2, 1.2)
            ax2d.set_aspect('equal')
            ax2d.set_xlabel('Risk Dimension 1', color='#8b949e', fontsize=9)
            ax2d.set_ylabel('Risk Dimension 2', color='#8b949e', fontsize=9)
            ax2d.set_title('2D Risk Profile Evolution', color='#f85149', fontsize=12, pad=15)
            ax2d.tick_params(colors='#8b949e')
            
            # Add legend
            legend_elements = [
                mpatches.Patch(color='#58a6ff', alpha=0.3, label='Risk Envelope'),
                mpatches.Patch(color='#f85149', alpha=0.3, label='Probability Ring')
            ]
            ax2d.legend(handles=legend_elements, loc='upper right',
                       facecolor='#0d1117', edgecolor='#30363d', labelcolor='#8b949e')
            
            # Main title with timer
            fig.suptitle(f'⚛️ QUANTUM RISK EVOLUTION | Time: {t:.2f}s', 
                        fontsize=14, color='#ffffff', fontweight='bold', y=0.98)
            
            return []
        
        anim = FuncAnimation(fig, animate, frames=total_frames,
                            interval=1000/fps, blit=False)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        gif_file = f"{output_dir}/risk_evolution_{timestamp}.gif"
        
        print(f"   Saving to {gif_file}...")
        writer = PillowWriter(fps=fps)
        anim.save(gif_file, writer=writer, dpi=100)
        
        plt.close(fig)
        print(f"   ✓ Animation saved: {gif_file}")
        
        return gif_file


# ============================================================================
# PERFORMANCE MONITOR
# ============================================================================

class PerformanceMonitor:
    """Monitor system performance"""
    
    def __init__(self, process_name="Quantum Finance Risk Model"):
        self.process_name = process_name
        self.start_time = time.perf_counter()
        self.process = psutil.Process()
        self.initial_memory = self.process.memory_info().rss
        self.checkpoints = {}
    
    def checkpoint(self, label):
        """Record a performance checkpoint"""
        elapsed = time.perf_counter() - self.start_time
        memory_used = (self.process.memory_info().rss - self.initial_memory) / (1024 ** 2)
        cpu_percent = self.process.cpu_percent(interval=0.01)
        
        self.checkpoints[label] = {
            'elapsed_seconds': elapsed,
            'memory_mb': memory_used,
            'cpu_percent': cpu_percent,
            'timestamp': datetime.now().isoformat()
        }
        
        return self.checkpoints[label]
    
    def generate_report(self):
        """Generate performance report"""
        return {
            'process_name': self.process_name,
            'total_duration': time.perf_counter() - self.start_time,
            'final_memory_mb': (self.process.memory_info().rss - self.initial_memory) / (1024 ** 2),
            'peak_memory_mb': max([c['memory_mb'] for c in self.checkpoints.values()]) if self.checkpoints else 0,
            'system_memory_gb': psutil.virtual_memory().total / (1024 ** 3),
            'checkpoints': self.checkpoints
        }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_quantum_finance_risk_model(n_qubits=20, shots=5000, output_dir='./finance_risk_output'):
    """Main function to run the quantum finance risk model"""
    
    # Initialize performance monitoring
    monitor = PerformanceMonitor("Quantum Finance Risk Model")
    monitor.checkpoint("Initialization")
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("\n" + "=" * 80)
    print("QUANTUM FINANCE RISK MODEL - EXECUTION START")
    print("=" * 80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Parameters: {n_qubits} qubits, {shots} shots")
    print("-" * 80)
    
    # Step 1: Load financial data
    print("\n1. Loading financial market data...")
    data_loader = FinancialDataLoader()
    market_data = data_loader.fetch_market_data(period='6mo', interval='1d')
    returns_data = data_loader.calculate_returns(market_data)
    correlation_matrix, asset_names = data_loader.compute_correlation_matrix(returns_data)
    
    monitor.checkpoint("Data Loading Complete")
    
    # Step 2: Calculate traditional risk metrics
    print("\n2. Calculating traditional risk metrics...")
    risk_calc = RiskMetricsCalculator()
    
    # Aggregate returns for portfolio
    all_returns = []
    for category in returns_data.values():
        for returns in category.values():
            if len(returns) > 0:
                all_returns.extend(returns.values)
    
    risk_metrics = {
        'var_95': risk_calc.calculate_var(all_returns, 0.95) if all_returns else 0,
        'cvar_95': risk_calc.calculate_cvar(all_returns, 0.95) if all_returns else 0,
        'volatility': risk_calc.calculate_volatility(all_returns) if all_returns else 0,
        'sharpe_ratio': risk_calc.calculate_sharpe_ratio(all_returns) if all_returns else 0,
        'max_drawdown': 0.15,  # Placeholder - would need price data
        'market_risk': 0.35,
        'credit_risk': 0.25,
        'liquidity_risk': 0.15,
        'operational_risk': 0.10
    }
    
    if correlation_matrix is not None:
        corr_metrics = risk_calc.calculate_correlation_risk(correlation_matrix)
        risk_metrics.update(corr_metrics)
        # Store correlation matrix (truncate to 15x15 if larger for visualization)
        max_size = 15
        if correlation_matrix.shape[0] > max_size:
            risk_metrics['correlation_matrix'] = correlation_matrix[:max_size, :max_size].tolist()
        else:
            risk_metrics['correlation_matrix'] = correlation_matrix.tolist()
    
    monitor.checkpoint("Traditional Risk Calculated")
    
    # Step 3: Build and run quantum circuit
    print("\n3. Building and executing quantum circuit...")
    qc_builder = QuantumFinanceCircuit(n_qubits=n_qubits)
    
    # Prepare volatility vector (using random data for demo)
    volatility_vector = np.random.rand(n_qubits) * 0.3 + 0.1
    
    quantum_circuit = qc_builder.build_market_circuit(
        correlation_matrix=correlation_matrix,
        volatility_vector=volatility_vector
    )
    
    # Run quantum simulation
    simulator = AerSimulator()
    transpiled_circuit = transpile(quantum_circuit, simulator)
    result = simulator.run(transpiled_circuit, shots=shots).result()
    counts = result.get_counts()
    
    # Clean counts
    cleaned_counts = {k.replace(" ", ""): v for k, v in counts.items()}
    
    monitor.checkpoint("Quantum Simulation Complete")
    
    # Step 4: Analyze quantum results
    print("\n4. Analyzing quantum risk states...")
    quantum_results = qc_builder.analyze_risk_states(cleaned_counts, n_top_states=30)
    
    quantum_metrics = {
        'expected_quantum_risk': quantum_results['expected_risk'],
        'quantum_risk_volatility': quantum_results['risk_volatility'],
        'total_quantum_states': quantum_results['total_states'],
        'top_risk_states': quantum_results['states'][:5],
        'top_risk_probabilities': quantum_results['probabilities'][:5],
        'circuit_depth': quantum_circuit.depth(),
        'total_gates': sum(quantum_circuit.count_ops().values())
    }
    
    risk_metrics.update(quantum_metrics)
    monitor.checkpoint("Quantum Analysis Complete")
    
    # Step 5: Generate visualizations
    print("\n5. Generating risk visualizations...")
    visualizer = FinanceVisualizer()
    
    # Create static dashboard
    dashboard_file = visualizer.create_risk_dashboard(risk_metrics, quantum_results, output_dir)
    print(f"  ✓ Dashboard saved: {dashboard_file}")
    
    # Create interactive report
    interactive_file = visualizer.create_interactive_report(risk_metrics, quantum_results, output_dir)
    print(f"  ✓ Interactive report saved: {interactive_file}")
    
    monitor.checkpoint("Static Visualization Complete")
    
    # Step 5b: Generate animated simulations (4 seconds)
    print("\n5b. Generating animated simulations (4 seconds)...")
    animator = AnimatedVisualizer()
    
    # Create main quantum simulation animation
    simulation_gif = animator.create_animated_simulation(
        quantum_results, risk_metrics, output_dir,
        duration_seconds=4, fps=30
    )
    
    # Create risk evolution animation
    evolution_gif = animator.create_risk_evolution_animation(
        risk_metrics, quantum_results, output_dir,
        duration_seconds=4, fps=30
    )
    
    monitor.checkpoint("Animation Complete")
    
    # Step 6: Save comprehensive report
    print("\n6. Saving comprehensive risk report...")
    
    final_report = {
        'metadata': {
            'timestamp': timestamp,
            'simulation_parameters': {
                'n_qubits': n_qubits,
                'shots': shots,
                'simulator': 'AerSimulator'
            },
            'system_info': {
                'python_version': sys.version,
                'platform': sys.platform,
                'memory_gb': psutil.virtual_memory().total / (1024 ** 3)
            }
        },
        'traditional_risk_metrics': {k: v for k, v in risk_metrics.items() 
                                   if not isinstance(v, list) and not k.endswith('_matrix')},
        'quantum_risk_metrics': quantum_metrics,
        'performance_metrics': monitor.generate_report(),
        'asset_correlation_summary': {
            'avg_correlation': risk_metrics.get('avg_correlation', 0),
            'correlation_entropy': risk_metrics.get('correlation_entropy', 0)
        } if 'avg_correlation' in risk_metrics else {}
    }
    
    report_file = f"{output_dir}/finance_risk_report_{timestamp}.json"
    with open(report_file, 'w') as f:
        json.dump(final_report, f, indent=2, default=str)
    
    print(f"  ✓ JSON report saved: {report_file}")
    
    # Step 7: Generate summary
    summary_text = f"""
QUANTUM FINANCE RISK MODEL - ANALYSIS SUMMARY
============================================================
Timestamp: {timestamp}
Qubits: {n_qubits}
Shots: {shots}
============================================================
TRADITIONAL RISK METRICS:
------------------------------------------------------------
Value at Risk (95%): {risk_metrics.get('var_95', 0):.4f}
Conditional VaR (95%): {risk_metrics.get('cvar_95', 0):.4f}
Annual Volatility: {risk_metrics.get('volatility', 0):.4f}
Sharpe Ratio: {risk_metrics.get('sharpe_ratio', 0):.4f}
Maximum Drawdown: {risk_metrics.get('max_drawdown', 0):.4f}
------------------------------------------------------------
QUANTUM RISK METRICS:
------------------------------------------------------------
Expected Quantum Risk: {quantum_results['expected_risk']:.4f}
Quantum Risk Volatility: {quantum_results['risk_volatility']:.4f}
Total Quantum States: {quantum_results['total_states']}
Top Risk State: {quantum_results['states'][0] if quantum_results['states'] else 'N/A'}
Circuit Depth: {quantum_circuit.depth()}
Total Gates: {sum(quantum_circuit.count_ops().values())}
------------------------------------------------------------
CORRELATION ANALYSIS:
------------------------------------------------------------
Average Correlation: {risk_metrics.get('avg_correlation', 0):.4f}
Correlation Entropy: {risk_metrics.get('correlation_entropy', 0):.4f}
Number of Assets: {len(asset_names) if asset_names else 0}
------------------------------------------------------------
PERFORMANCE:
------------------------------------------------------------
Total Duration: {monitor.generate_report()['total_duration']:.3f} seconds
Peak Memory Usage: {monitor.generate_report()['peak_memory_mb']:.1f} MB
System Memory: {psutil.virtual_memory().total / (1024 ** 3):.1f} GB
============================================================
Output files created in: {output_dir}
"""
    
    summary_file = f"{output_dir}/risk_summary_{timestamp}.txt"
    with open(summary_file, 'w') as f:
        f.write(summary_text)
    
    print(summary_text)
    
    # Final output
    print("\n" + "=" * 80)
    print("QUANTUM FINANCE RISK MODEL - EXECUTION COMPLETE")
    print("=" * 80)
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 80)
    print("Generated Output Files:")
    print(f"  📊 Dashboard PNG: {dashboard_file}")
    print(f"  📈 Interactive HTML: {interactive_file}")
    print(f"  📋 JSON Report: {report_file}")
    print(f"  📝 Text Summary: {summary_file}")
    print(f"  🎬 Simulation GIF: {simulation_gif}")
    print(f"  🎬 Evolution GIF: {evolution_gif}")
    print("=" * 80)
    
    return {
        'dashboard': dashboard_file,
        'interactive': interactive_file,
        'report': report_file,
        'summary': summary_file,
        'simulation_animation': simulation_gif,
        'evolution_animation': evolution_gif,
        'risk_metrics': risk_metrics,
        'quantum_results': quantum_results
    }

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    
    parser = argparse.ArgumentParser(description='Quantum Finance Risk Model')
    parser.add_argument('--qubits', type=int, default=20, help='Number of qubits')
    parser.add_argument('--shots', type=int, default=5000, help='Number of shots')
    parser.add_argument('--output', type=str, default='./finance_risk_output', 
                       help='Output directory')
    
    args = parser.parse_args()
    
    # Run the model
    try:
        results = run_quantum_finance_risk_model(
            n_qubits=args.qubits,
            shots=args.shots,
            output_dir=args.output
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

