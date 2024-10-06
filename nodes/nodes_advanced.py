"""
2024.10.02 Created
Automatic1111 WebUIのBreak文、ComfyUIへPromptをSplitして出力する対応
"""
import numpy as np
import torch
from PIL import Image
import os
import glob

class LoadImageAndPromptsFromDirectory_Advanced:

    def __init__(self):

        self.max_len = 0
        self.text_files_path = []
        self.text_negative_files_path = []
        self.image_files_path = []

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "dir": (
                    "STRING",
                    {"multiline": False, "default": "Please input Directory Path"},
                ),
                "files_index": (
                    "INT",
                    {"default": 0, "min": 0, "max": 4096},
                ),
            }
        }

    # Automatic 1111 Web UIのPromptのBreak文に対応（Break文：5件対応なので最大、6件のプロンプト文）
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "STRING", "IMAGE")
    RETURN_NAMES = ("1st prompt", "2nd prompt", "3rd prompt","4th prompt","5th prompt" , "6th prompt", "negative prompt", "image")
    FUNCTION = "load_data"
    OUTPUT_NODE = True
    CATEGORY = "Load Images and Prompts from Directory"

    def check_directory(self, dir):

        if not os.path.isdir(dir):
            raise ValueError(f"指定されたディレクトリが存在しません: {dir}")

        image_files = sorted(glob.glob(os.path.join(dir, "*.png")))
        text_files = sorted(glob.glob(os.path.join(dir, "*.txt")))
        text_files = [f for f in text_files if not f.endswith('_n.txt')]
        text_files_negative=sorted(glob.glob(os.path.join(dir, "*_n.txt")))

        if image_files == 0 or text_files == 0:
            raise RuntimeError("テキストファイルか画像ファイルが存在しません。")

        if len(image_files) != len(text_files):
            raise ValueError("テキストファイルと画像ファイルの数が一致しません。")

        self.text_files_path = text_files
        self.text_negative_files_path=text_files_negative
        self.image_files_path = image_files
        self.max_len = len(image_files)


    def pil_to_tensor(self, image: Image.Image) -> torch.Tensor:
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

    def load_data(self, dir, files_index):
        
        # 2024/10/06 毎回、読み込むように修正する
        self.check_directory(dir)

        text_name = os.path.splitext(
            os.path.basename(self.text_files_path[files_index])
        )[0]
        image_name = os.path.splitext(
            os.path.basename(self.image_files_path[files_index])
        )[0]

        if text_name != image_name:
            raise ValueError("プロンプトと画像のファイル名が一致しません。")

        with open(self.text_files_path[files_index], "r", encoding="utf-8") as file:
            prompt_string = file.read()

        # 追記
        prompt_split_string = ["", "", "", "", "", ""]
        prompt_string = prompt_string.replace("\n", "").strip()
        segments = [segment for segment in prompt_string.split("BREAK,")]
        for i in range(min(len(segments), len(prompt_split_string))):
            prompt_split_string[i] = segments[i]
        
        with open(self.text_negative_files_path[files_index], "r", encoding="utf-8") as file:
            prompt_negative_string = file.read()

        image = Image.open(self.image_files_path[files_index]).convert("RGB")
        image_tensor = self.pil_to_tensor(image)

        # 修正
        return (prompt_split_string[0],prompt_split_string[1],prompt_split_string[2],prompt_split_string[3],prompt_split_string[4],prompt_split_string[5], prompt_negative_string, image_tensor)
    