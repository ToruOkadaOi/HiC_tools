#!/usr/bin/env bash
# Quick start script for running the Hi-C Tools Dashboard with uv
# This script demonstrates the fastest way to get started with uv

set -e

echo "🧬 Hi-C Tools Dashboard - Quick Start with uv"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv is not installed."
    echo ""
    echo "Please install uv first using one of these methods:"
    echo "  - pip install uv"
    echo "  - curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  - brew install uv  (macOS)"
    echo ""
    exit 1
fi

echo "✅ uv found: $(uv --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
fi

echo "📦 Installing dependencies..."
source .venv/bin/activate
uv pip install -r requirements.txt

echo ""
echo "🚀 Starting dashboard..."
echo "   The dashboard will open in your browser at http://localhost:8501"
echo ""

streamlit run dashboard.py
