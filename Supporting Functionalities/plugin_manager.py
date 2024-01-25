import os
import importlib
import logging

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.plugin_directory = "plugins"
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_plugin(self, plugin):
        plugin_name = plugin.__class__.__name__
        self.plugins[plugin_name] = plugin
        logging.info(f"Plugin {plugin_name} loaded")

    def remove_plugin(self, plugin_name):
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            logging.info(f"Plugin {plugin_name} removed")

    def update_plugin(self, plugin):
        plugin_name = plugin.__class__.__name__
        self.plugins[plugin_name] = plugin
        logging.info(f"Plugin {plugin_name} updated")

    def execute_plugins(self, query):
        responses = []
        for plugin_name, plugin in self.plugins.items():
            response = plugin.process(query)
            responses.append((plugin_name, response))
        return responses

    def load_plugins_from_directory(self):
        for filename in os.listdir(self.plugin_directory):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                module = importlib.import_module(f"{self.plugin_directory}.{module_name}")
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if callable(attribute) and attribute is not attribute.__class__:
                        self.load_plugin(attribute())
                logging.info(f"Plugins from directory {self.plugin_directory} loaded")

# Example usage
# plugin_manager = PluginManager()
# plugin_manager.load_plugins_from_directory()
# responses = plugin_manager.execute_plugins("Sample query")
# for plugin_name, response in responses:
#     print(f"Response from {plugin_name}: {response}")
