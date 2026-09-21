import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import *
from call_function import *
import argparse
import json

load_dotenv()
api_key = os.environ.get("DEEPSEEK_API_KEY")

if api_key is None:
    raise RuntimeError("No API Key")

def main():
        
    client = OpenAI(
        base_url="https://api.deepseek.com",
        api_key=api_key
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):

        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,  # type: ignore
            tools=available_functions, # type: ignore
            temperature=0.2,
        )



        if response.usage is None:
            raise RuntimeError("No response")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for item in message.tool_calls:
                result_message = call_function(item, args.verbose)

                messages.append(result_message)

                if result_message["content"] == "":
                    raise Exception

                if args.verbose:
                    print(f"-> {result_message['content']}")
                continue
        else:
            print(f"Response:\n {message.content}")
            break
    else:
        print(f"Maximum number of iterations reached, no final response produced.")
        exit(1)
        
if __name__ == "__main__":
    main()
