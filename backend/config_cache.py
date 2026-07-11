import os

os.environ["XDG_CACHE_HOME"] = "/tmp/.cache"
os.environ["HF_HOME"] = "/tmp/.cache/huggingface"
os.environ["HUGGINGFACE_HUB_CACHE"] = "/tmp/.cache/huggingface/hub"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/.cache/huggingface/transformers"
os.environ["TORCH_HOME"] = "/tmp/.cache/torch"