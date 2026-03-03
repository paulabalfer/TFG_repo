# Artistic Swimming Position Classifier

A vision-language model (vLLM) classifier for artistic swimming body positions, built using Claude's multimodal capabilities and structured prompt engineering ("skills").

## Overview

This project classifies pool photographs of an artistic swimmer into one of 5 body positions defined by the World Aquatics Figures Manual. Rather than training a traditional ML model, it uses **carefully engineered classification prompts** (Claude Code skills) that encode expert judging knowledge, decision trees, contrastive examples, and scoring rubrics.

## The 5 Positions

| # | Position | BP Code | Key Feature |
|---|----------|---------|-------------|
| 1 | Double Leg Vertical | BP6 | Both legs together, straight, vertical |
| 2 | Fishtail | BP8 | One leg vertical + one leg straight FORWARD, trunk straight |
| 3 | Bent Knee Vertical | BP14c | One leg vertical + one leg BENT at knee, thigh horizontal, trunk straight |
| 4 | Bent Knee Surface Arch | BP14d | ARCHED back + one leg BENT at knee, thigh perpendicular, near surface |
| 5 | Knight | BP17 | ARCHED back + one leg vertical + one leg straight BACKWARD |

### Decision Tree

```
1. How many distinct leg directions?
   +-- ONE (both legs together) --> Double Leg Vertical (BP6)
   +-- TWO (legs split) ----------> Go to step 2

2. Is either knee BENT?
   +-- YES --> Go to step 3
   +-- NO  --> Go to step 4

3. Is the back ARCHED?
   +-- YES --> Bent Knee Surface Arch (BP14d)
   +-- NO  --> Bent Knee Vertical (BP14c)

4. Is the back ARCHED?
   +-- YES --> Knight (BP17)
   +-- NO  --> Fishtail (BP8)
```

## Architecture

### Skills Structure

The classifier is implemented as 6 Claude Code skills in `.claude/skills/`:

```
.claude/skills/
  natacion-classifier/SKILL.md        # Orchestrator - evaluates all 5 positions
  natacion-bp06-double-leg-vertical/   # BP6 position-specific scorer
  natacion-bp08-fishtail/              # BP8 position-specific scorer
  natacion-bp14c-bent-knee-vertical/   # BP14c position-specific scorer
  natacion-bp14d-bent-knee-surface-arch/ # BP14d position-specific scorer
  natacion-bp17-knight/                # BP17 position-specific scorer
```

### Each Skill Contains

1. **Official Definition** - World Aquatics Figures Manual specification
2. **Visual Scratchpad** - 7-step evaluation procedure forcing systematic observation
3. **Exclusion Checklist** - Hard disqualifiers (any triggered = score 0)
4. **Contrastive Learning** - Side-by-side comparison tables for every confusable pair
5. **Scoring Rubric** - 0-5 scale with precise criteria per score level
6. **Text Shots** - Detailed text descriptions of verified training images (serve as few-shot examples without consuming vision tokens)

### Orchestrator

The master skill (`natacion-classifier/SKILL.md`) scores against ALL 5 positions and applies aggregation rules:
- **Rule 1**: All scores <= 1 -> UNCERTAIN
- **Rule 2**: Clear winner (>= 2 points ahead) -> classify
- **Rule 3**: Moderate winner (>= 1 point ahead) -> classify
- **Rule 4**: Tie-breaking via exclusion counts, confusion-pair heuristics, and anti-Fishtail bias

## Reference Documents

The skills were built by studying these documents in the project root:

- `Figures-Manual-2022-2025-ALL.pdf` - Official World Aquatics Figures Manual
- `JUDGES SUPPORT_Height Chart Jan 2025.pdf` - Judge support materials
- `Sistema Multimodal para Natacion Artistica_Paula Ballesteros.pdf` - Research thesis on multimodal artistic swimming analysis

## Dataset

- **30 total images** in `resources/`, organized by position (6 per class)
- Each image is a pool photograph of a swimmer performing a specific body position
- Images include augmented variants (e.g., `_aug8`, `_aug21`)

### Train/Test Split

A deterministic 50/50 split was created (`data/train_test_split.json`):
- **Train (dev) set**: 15 images (3 per class) - used to build and refine skills
- **Test set**: 15 images (3 per class) - held out for final evaluation

## Results

### Development Set (Train) - Used for Skill Refinement

| Class | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| Double Leg Vertical | 3 | 3 | 100% |
| Fishtail | 3 | 3 | 100% |
| Bent Knee Vertical | 3 | 3 | 100% |
| Bent Knee Surface Arch | 3 | 3 | 100% |
| Knight | 3 | 3 | 100% |
| **Total** | **15** | **15** | **100%** |

### Test Set (Held-Out) - Final Evaluation

| Class | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| Double Leg Vertical | 3 | 3 | 100% |
| Fishtail | 3 | 3 | 100% |
| Bent Knee Vertical | 3 | 3 | 100% |
| Bent Knee Surface Arch | 3 | 3 | 100% |
| Knight | 2 | 3 | 66.7% |
| **Total** | **14** | **15** | **93.3%** |

### Confusion Matrix (Test Set)

```
                    Predicted
                DLV  Fish  BKV  BKSA  Knight
True  DLV      [ 3    0     0    0     0   ]
      Fish     [ 0    3     0    0     0   ]
      BKV      [ 0    0     3    0     0   ]
      BKSA     [ 0    0     0    3     0   ]
      Knight   [ 0    0     0    1     2   ]
```

### Error Analysis

**1 misclassification**: `IMG_1379_aug8.jpg` (Knight) was classified as Bent Knee Surface Arch.

Both Knight and BKSA share an **arched back** — the discriminating feature is whether the non-vertical leg is **straight** (Knight) or **bent at the knee** (BKSA). The model perceived a knee bend where the leg was actually straight, triggering the BKSA classification. This Knight/BKSA boundary is the hardest confusion pair in the dataset.

No further iteration was performed after the test set evaluation, per proper evaluation protocol.

## Methodology

1. **Study reference materials** - Read World Aquatics manuals and research thesis to understand each position's biomechanics
2. **Create skills with text shots** - Build structured prompts encoding domain expertise, using text descriptions of training images as few-shot examples
3. **Evaluate on dev set** - Run all 15 training images through the classifier using parallel Claude Sonnet 4.5 agents
4. **Iterate on skills** - Refine prompts until dev set accuracy is satisfactory (achieved 100%)
5. **Final test evaluation** - Run held-out test set once, report results without further iteration (achieved 93.3%)

## Model

- **Classification model**: Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) via multimodal vision
- **Evaluation method**: Each image read via Claude's Read tool (vision), then classified using the orchestrator skill's structured evaluation procedure
- **Parallelization**: 5 concurrent subagents (one per class) for efficient batch evaluation

## File Structure

```
natacion_paula/
  README.md                    # This file
  data/
    train_test_split.json      # Deterministic 50/50 split definition
  resources/
    Double Leg Vertical/       # 6 images
    Fishtail/                  # 6 images
    Bent Knee Vertical/        # 6 images
    Bent Knee Surface Arch Position/  # 6 images
    Knight/                    # 6 images
  results/
    dev_set_results.json       # Full dev set evaluation results
    test_set_results.json      # Full test set evaluation results + confusion matrix
  .claude/skills/
    natacion-classifier/       # Master orchestrator skill
    natacion-bp06-*/           # BP6 position scorer
    natacion-bp08-*/           # BP8 position scorer
    natacion-bp14c-*/          # BP14c position scorer
    natacion-bp14d-*/          # BP14d position scorer
    natacion-bp17-*/           # BP17 position scorer
```
