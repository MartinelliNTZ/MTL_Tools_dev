# -*- coding: utf-8 -*-
"""Compatibility shim for legacy imports of `MTL_Tools.utils.core`.

Some older versions of the plugin (or external integrations) may attempt to
import `MTL_Tools.utils.core`. That module path no longer exists in the
current architecture, so this shim forwards key submodules from the real
`MTL_Tools.core` package.

If you are seeing this import, please consider updating the calling code to
import directly from `MTL_Tools.core` (or the specific submodule) instead.
"""

# NOTE: We keep this file intentionally lightweight to minimize side effects.
# It exists solely to prevent ModuleNotFoundError for `MTL_Tools.utils.core`.

# Expose the core package (namespace package) for legacy imports.
from .. import core  # noqa: F401

# Optionally expose frequently used components for backwards compatibility
# (uncomment if needed):
# from ..core.config.LogUtilsNew import LogUtilsNew
# from ..core.config.LogUtils import LogUtils
# from ..core.config.LogCleanupUtils import LogCleanupUtils
