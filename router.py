import json
import os

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        config = {
            "google": {
                "api_keys": []
            },
            "groq": {
                "api_keys": []
            }
        }

        with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)

        return config

    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


config = load_config()

print("AI Router")
print("\nConfigured providers:")

for provider, details in config.items():
    key_count = len(details["api_keys"])
    print(f"- {provider}: {key_count} API key(s)")
