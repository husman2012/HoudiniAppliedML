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
    model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
    model_path = base_dir / "llama-2-7b-chat.gguf"

    if not model_path.exists():
        print(f"Downloading model to {model_path}")
        subprocess.check_call(["curl", "-L", model_url, "-o", str(model_path)])
    
    return model_path


def chat_with_llama(model_path):
    from llama_cpp import Llama

    llama = Llama(model_path=str(model_path), n_ctx=2048, n_threads=16, chat_format='llama-2')
    
    system_prompt = {
        "role" : "system",
        "content" : """You are a highly knoledgeable and helpful Houdini assistant with expertise in:
        - Houdini software
        - VEX and Python scripting
        - 3D graphics, topology and procedural generation
        - Visual effects and simulations
        - Shading and Lighting
        - Dynamics and particle systems
        - Animation and rigging
        - Rendering techniques and optimization
        - Node-based workflows and best practices
        - Troubleshooting and problem-solving in Houdini
        - Industry trends and updates related to Houdini and 3D graphics
        - USD Pipelining and integration with other software
        - Houdini Engine for integration with other 3D applications
        - Houdini's role in game development and real-time applications

        Provide clear, detailed and accurate responses to user queries, drawing from your extensive knowledge of Houdini and related fields. 
        Answer in a technical manner, suitable for users with a background in 3D graphics, programming and Houdini. Include:
        - Code snippets in VEX or Python where relevant
        - Step-by-step instructions for complex tasks
        - Best practices and tips for efficient workflows
        - References to official documentation or tutorials when applicable
        Avoid vague or generic responses. If you don't know the answer, admit it rather than guessing. When possible recommend a workflow using Houdini's Nodes system over scripting in VEX or Python.
        Use actual Node names and terminology from Houdini.
        """
    }

    print("\nLlama chat interface")
    print("Type 'exit' to quit\n")
    print("-"*50)

    messages = [system_prompt]

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Exiting chat.")
            break

        if user_input.lower() == 'reset':
            messages = [system_prompt]
            print("Chat history reset.")
            continue    
        
        messages.append({"role": "user", "content": user_input})
        response = llama.create_chat_completion(messages=messages)
        assistant_messages = response['choices'][0]['message']['content']
        print("\nAssistant:")
        print(assistant_messages)
        print("-"*50)


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