import os
import subprocess
import sys
from pathlib import Path
from urllib import response

def setup_llama(base_dir):
    base_dir = Path(base_dir).resolve()
    base_dir.mkdir(exist_ok=True, parents=True)
    os.chdir(base_dir)

    print(f"Setting up Llama in {base_dir}")

    subprocess.check_call([sys.executable, "-m", "pip", "install", "llama-cpp-python"])
    model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7B-chat.Q4_K_M.gguf"
    model_path = base_dir / "llama-2-7B-chat.gguf"


    if not model_path.exists():
        print(f"Downloading model to {model_path}")
        subprocess.check_call(["curl", "-L", model_url, "-o", str(model_path)])
    
    return model_path


def chat_with_llama(model_path, prompt):
    from llama_cpp import Llama

    llama = Llama(model_path=str(model_path), n_ctx=2048, n_threads=8, chat_format='llama-2')
    print("\nLlama chat interface")
    print("Type 'exit' to quit\n")
    print("-"*50)

    messages = []

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Exiting chat.")
            break
        
        messages.append({"role": "user", "content": user_input})
        response = llama.create_chat_completion(messages=messages)
        assistant_messages = response['choices'][0]['message']['content']
        print("\nAssistant:")
        print(assistant_messages)
        print("-"*50)

    return response['choices'][0]['text']


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            custom_dir = sys.argv[1]
        else:
            custom_dir = "."

        model_path = setup_llama(custom_dir)
        chat_with_llama(model_path)
    except Exception as e:
        print(f"An error occurred: {e}")