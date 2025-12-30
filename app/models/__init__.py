import importlib
import pkgutil
from pathlib import Path

# ensure Base is imported
from app.db.database import Base  # noqa: F401

package_dir = Path(__file__).resolve().parent
package_name = __name__

for module in pkgutil.iter_modules([str(package_dir)]):
    if module.ispkg:
        continue

    importlib.import_module(f"{package_name}.{module.name}")

