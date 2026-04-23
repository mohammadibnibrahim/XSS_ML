#!/usr/bin/env python3
"""
run_all.py — Master pipeline script for the XSS Detection project.

Executes the entire workflow end-to-end:
  1. Download dataset
  2. Preprocess and split data
  3. Train all models (with cross-validation)
  4. Evaluate and generate all figures

Usage:
    python run_all.py

Authors: Mohammad Ibrahim, Omar Adel, Mohamed Ahmed
Team: Blackhat — University of East London
Module: Level 4 Primers (Dr. Wael El Sersy)
"""

import time
import sys
from pathlib import Path

# Ensure project root is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.utils.helpers import load_config, setup_logging
from src.preprocessing.preprocess import (
    download_dataset, load_dataset, explore_dataset,
    preprocess_and_split, save_processed_data,
)
from src.training.train import train_all_models
from src.evaluation.evaluate import evaluate_all_models


def main():
    """Run the complete XSS detection pipeline."""
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("XSS Detection Project — Team Blackhat")
    logger.info("University of East London")
    logger.info("=" * 60)

    overall_start = time.time()

    # ── Step 1: Load configuration ──────────────────────────────────
    logger.info("\n>> Step 1: Loading configuration ...")
    config = load_config()

    # ── Step 2: Download & load dataset ─────────────────────────────
    logger.info("\n>> Step 2: Downloading and loading dataset ...")
    filepath = download_dataset(config)
    df = load_dataset(filepath)

    # ── Step 3: Exploratory analysis ────────────────────────────────
    logger.info("\n>> Step 3: Exploring dataset ...")
    stats = explore_dataset(df)

    # ── Step 4: Preprocess & split ──────────────────────────────────
    logger.info("\n>> Step 4: Preprocessing and splitting data ...")
    data = preprocess_and_split(df, config)
    save_processed_data(data, config)

    # ── Step 5: Train all models ────────────────────────────────────
    logger.info("\n>> Step 5: Training models ...")
    model_results = train_all_models(data, config)

    # ── Step 6: Evaluate & generate figures ─────────────────────────
    logger.info("\n>> Step 6: Evaluating models and generating figures ...")
    all_metrics = evaluate_all_models(model_results, data, config)

    # ── Summary ─────────────────────────────────────────────────────
    elapsed = time.time() - overall_start
    logger.info(f"\n{'=' * 60}")
    logger.info(f"Pipeline completed in {elapsed:.1f}s")
    logger.info(f"Models saved to: models/")
    logger.info(f"Figures saved to: figures/")
    logger.info(f"Processed data saved to: data/processed/")
    logger.info(f"{'=' * 60}")

    return all_metrics


if __name__ == "__main__":
    main()
