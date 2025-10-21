"""
# Plugin System

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/plugin_system.py #domain/plugin-system #layer/plugin-infrastructure #pattern/plugin-architecture #pattern/dependency-injection #pattern/observer

## Purpose
Provides hot-reloadable plugin infrastructure for extending calculator operations.
Plugins can be loaded, unloaded, and reloaded at runtime without restarting the calculator.

## Related Documentation
- Pattern: [[../obsidian/plugin-architecture|Plugin Architecture]]
- Pattern: [[../obsidian/strategy-pattern|Strategy Pattern]]

## Used By
- [[calculator.py|Calculator Class]]
"""
from typing import Dict, Callable, List, Optional, Any
import importlib
import importlib.util
import sys
from pathlib import Path


class PluginMetadata:  # ^PluginMetadata
    """
    Metadata about a loaded plugin.

    Related: [[../obsidian/plugin-architecture|Plugin Architecture]]
    """
    def __init__(self, name: str, module_path: str, operations: Dict[str, Callable]):  # ^PluginMetadata-__init__
        self.name = name
        self.module_path = module_path
        self.operations = operations
        self.enabled = True


class PluginSystem:  # ^PluginSystem
    """
    Manages the lifecycle of calculator plugins.

    Implements hot-reloading by tracking module state and supporting
    runtime load/unload operations.

    Related: [[../obsidian/plugin-architecture|Plugin Architecture]]
    Related: [[../obsidian/strategy-pattern|Strategy Pattern]]
    """

    def __init__(self):  # ^PluginSystem-__init__
        """Initialize the plugin system."""
        self.plugins: Dict[str, PluginMetadata] = {}
        self._observers: List[Callable] = []

    def register_observer(self, callback: Callable) -> None:  # ^PluginSystem-register_observer
        """
        Register a callback to be notified when plugins change.

        Implements: [[../obsidian/plugin-architecture|Observer Pattern]]
        """
        self._observers.append(callback)

    def _notify_observers(self, event: str, plugin_name: str) -> None:  # ^PluginSystem-_notify_observers
        """
        Notify all observers of a plugin event.

        Related: [[../obsidian/plugin-architecture|Observer Pattern]]
        """
        for callback in self._observers:
            callback(event, plugin_name)

    def load_plugin(self, plugin_name: str, plugin_path: Optional[str] = None) -> bool:  # ^PluginSystem-load_plugin
        """
        Load a plugin from the plugins directory.

        Args:
            plugin_name: Name of the plugin module (e.g., 'statistics')
            plugin_path: Optional custom path to plugin file

        Returns:
            True if loaded successfully, False otherwise

        Related: [[../obsidian/plugin-architecture|Plugin Architecture]]
        """
        try:
            # Determine plugin path
            if plugin_path is None:
                # Default: look in plugins/ subdirectory
                plugins_dir = Path(__file__).parent / "plugins"
                plugin_path = str(plugins_dir / f"{plugin_name}.py")

            # Load the module
            spec = importlib.util.spec_from_file_location(
                f"plugins.{plugin_name}",
                plugin_path
            )

            if spec is None or spec.loader is None:
                return False

            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)

            # Extract operations from module
            operations = {}
            if hasattr(module, 'PLUGIN_OPERATIONS'):
                operations = module.PLUGIN_OPERATIONS

            # Store plugin metadata
            metadata = PluginMetadata(plugin_name, plugin_path, operations)
            self.plugins[plugin_name] = metadata

            self._notify_observers('loaded', plugin_name)
            return True

        except Exception as e:
            print(f"Failed to load plugin '{plugin_name}': {e}")
            return False

    def unload_plugin(self, plugin_name: str) -> bool:  # ^PluginSystem-unload_plugin
        """
        Unload a plugin.

        Args:
            plugin_name: Name of the plugin to unload

        Returns:
            True if unloaded successfully, False otherwise

        Related: [[../obsidian/plugin-architecture|Plugin Architecture]]
        """
        if plugin_name not in self.plugins:
            return False

        # Remove from sys.modules
        module_name = f"plugins.{plugin_name}"
        if module_name in sys.modules:
            del sys.modules[module_name]

        # Remove plugin metadata
        del self.plugins[plugin_name]

        self._notify_observers('unloaded', plugin_name)
        return True

    def reload_plugin(self, plugin_name: str) -> bool:  # ^PluginSystem-reload_plugin
        """
        Reload a plugin (unload then load).

        Args:
            plugin_name: Name of the plugin to reload

        Returns:
            True if reloaded successfully, False otherwise

        Related: [[../obsidian/plugin-architecture|Plugin Architecture]]
        """
        if plugin_name not in self.plugins:
            return False

        plugin_path = self.plugins[plugin_name].module_path
        self.unload_plugin(plugin_name)
        return self.load_plugin(plugin_name, plugin_path)

    def get_all_operations(self) -> Dict[str, Callable]:  # ^PluginSystem-get_all_operations
        """
        Get all operations from all enabled plugins.

        Returns:
            Dictionary mapping operation names to functions

        Related: [[../obsidian/strategy-pattern|Strategy Pattern]]
        Related: [[../obsidian/plugin-architecture|Plugin Architecture]]
        """
        operations = {}
        for plugin in self.plugins.values():
            if plugin.enabled:
                operations.update(plugin.operations)
        return operations

    def get_plugin_operations(self, plugin_name: str) -> Dict[str, Callable]:  # ^PluginSystem-get_plugin_operations
        """
        Get operations from a specific plugin.

        Args:
            plugin_name: Name of the plugin

        Returns:
            Dictionary mapping operation names to functions

        Related: [[../obsidian/plugin-architecture|Plugin Architecture]]
        """
        if plugin_name not in self.plugins:
            return {}
        return self.plugins[plugin_name].operations.copy()

    def list_plugins(self) -> List[str]:  # ^PluginSystem-list_plugins
        """
        List all loaded plugins.

        Returns:
            List of plugin names
        """
        return list(self.plugins.keys())

    def enable_plugin(self, plugin_name: str) -> bool:  # ^PluginSystem-enable_plugin
        """
        Enable a previously disabled plugin.

        Args:
            plugin_name: Name of the plugin to enable

        Returns:
            True if enabled successfully, False otherwise
        """
        if plugin_name not in self.plugins:
            return False

        self.plugins[plugin_name].enabled = True
        self._notify_observers('enabled', plugin_name)
        return True

    def disable_plugin(self, plugin_name: str) -> bool:  # ^PluginSystem-disable_plugin
        """
        Disable a plugin without unloading it.

        Args:
            plugin_name: Name of the plugin to disable

        Returns:
            True if disabled successfully, False otherwise
        """
        if plugin_name not in self.plugins:
            return False

        self.plugins[plugin_name].enabled = False
        self._notify_observers('disabled', plugin_name)
        return True

    def auto_discover_plugins(self) -> int:  # ^PluginSystem-auto_discover_plugins
        """
        Automatically discover and load all plugins in the plugins/ directory.

        Returns:
            Number of plugins successfully loaded

        Related: [[../obsidian/plugin-architecture|Plugin Architecture]]
        """
        plugins_dir = Path(__file__).parent / "plugins"

        if not plugins_dir.exists():
            return 0

        loaded_count = 0
        for plugin_file in plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue  # Skip __init__.py and private modules

            plugin_name = plugin_file.stem
            if self.load_plugin(plugin_name):
                loaded_count += 1

        return loaded_count
