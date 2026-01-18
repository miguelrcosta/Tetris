# Tetris AI

Project developed in an academic context that combines **Tetris gameplay (Pygame)** with **computer vision using YOLOv8** to detect pieces (current and next) and support automated decision-making.

This repository includes:

- A playable Tetris version (human mode) with AI-assisted piece detection
- An automated mode that simulates a human by choosing moves based on detected pieces
- Scripts to train YOLOv8 models using annotated datasets (with and without augmentation)

---

## Libraries Required

Install these libraries:

```bash
pip install ultralytics pygame torch mss numpy
```

---

## How to run

### Play as a Human

In this mode, you play normally and the AI component is used only to detect the next piece.

```bash
python jogarTetris.py
```

---

### Play with Automated Behavior

This mode simulates a human player by automatically selecting the best moves based on detection of the current and next pieces.

```bash
python tetrisAutoRotacao.py
```

---

### Training YOLOv8 Models

This script trains two YOLOv8 models:

- One with data augmentation
- One without data augmentation

The datasets were annotated using Roboflow.

```bash
python treinarModelos.py
```

---

## Notes

- This project was developed for academic and experimental purposes, focusing on the application of computer vision techniques to game automation.
- Model training and inference performance may vary depending on hardware capabilities.
- The YOLOv8 models were trained using custom datasets annotated with Roboflow.
- Screen resolution and window positioning may affect piece detection accuracy during gameplay.
- The codebase prioritizes clarity and experimentation over production-level optimization.
