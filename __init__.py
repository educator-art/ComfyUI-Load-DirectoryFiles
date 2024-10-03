from .nodes.nodes import *
from .nodes.nodes_advanced import *

NODE_CLASS_MAPPINGS = {
    "Load Images and Prompts from Directory": LoadImageAndPromptsFromDirectory,
    "Load Images and Prompts from Directory(Advanced)": LoadImageAndPromptsFromDirectory_Advanced,
}

print("Load Class: LoadImageAndPromptsFromDirectory")
print("Load Class: LoadImageAndPromptsFromDirectory_Advanced")
