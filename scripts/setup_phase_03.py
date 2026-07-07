from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

directories = [
    "src/replay_engine",
    "src/utils",
    "logs",
]

files = [
    "src/replay_engine/__init__.py",
    "src/replay_engine/replay.py",
    "src/replay_engine/producer.py",
    "src/replay_engine/validator.py",
    "src/replay_engine/replay_controller.py",
    "src/replay_engine/metrics.py",
    "src/replay_engine/schemas.py",

    "src/utils/__init__.py",
    "src/utils/config.py",
    "src/utils/logger.py",

    "configs/settings.yaml",

    "logs/.gitkeep",

    "docs/implementation/PHASE_03_SUMMARY.md",
]

print("=" * 60)
print("Setting up Phase 3 - Replay Engine")
print("=" * 60)

for directory in directories:
    path = PROJECT_ROOT / directory
    path.mkdir(parents=True, exist_ok=True)
    print(f"[DIR ] {directory}")

for file in files:
    path = PROJECT_ROOT / file
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.touch()
        print(f"[FILE] {file}")
    else:
        print(f"[SKIP] {file}")

print("\nPhase 3 folder structure created successfully.")