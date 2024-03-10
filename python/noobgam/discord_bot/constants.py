import os

CLIENT_ID = 223097750416392192
if os.environ.get("CLIENT_ID_OVERRIDE"):
    CLIENT_ID = int(os.environ["CLIENT_ID_OVERRIDE"])

MODEL_NAME = os.getenv("MODEL_NAME_OVERRIDE") or "NoobGPT"
