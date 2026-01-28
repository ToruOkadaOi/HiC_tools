#!/usr/bin/env bash
# Quick start script for running the Hi-C Tools Dashboard with uv
# This script demonstrates the fastest way to get started with uv

set -e

echo "🧬 Hi-C Tools Dashboard - Quick Start with uv"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "⚠️  uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv installed successfully!"
    echo ""
    echo "Please restart your shell or run: source ~/.bashrc"
    echo "Then run this script again."
    exit 0
fi

echo "✅ uv found: $(uv --version)"
echo ""
echo "📦 Installing dependencies..."
uv pip install -r requirements.txt

echo ""
echo "🚀 Starting dashboard..."
echo "   The dashboard will open in your browser at http://localhost:8501"
echo ""

streamlit run dashboard.py
