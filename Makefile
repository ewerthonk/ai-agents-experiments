# Makefile for LaTeX dissertation formatting
# Author: Ewerthon José Kutz

# Variables
ESSAY_DIR = essay
MAIN_TEX = $(ESSAY_DIR)/main.tex
INDENT_CONFIG = $(ESSAY_DIR)/latexindent.yaml
LATEXINDENT = /Library/TeX/texbin/latexindent

# Phony targets
.PHONY: help format

# Default target
help:
	@echo "Available targets:"
	@echo "  make format - Format theTeX file with latexindent"
	@echo "  make help   - Show this help message"

# Format the LaTeX file
format:
	@echo "Formatting $(MAIN_TEX)..."
	@$(LATEXINDENT) -l=$(INDENT_CONFIG) -w $(MAIN_TEX)
	@echo "✓ Formatting complete!"
