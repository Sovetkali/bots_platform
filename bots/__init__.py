import importlib
from pathlib import Path

current_dir = Path(__file__).parent

for item in current_dir.iterdir():
    if item.is_dir() and not item.name.startswith('_') and (item / '__init__.py').exists():
        module_name = f"{__name__}.{item.name}"
        importlib.import_module(f'bots.{item.name}')
