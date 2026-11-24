import json
import os, argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key is None:
    raise RuntimeError("API key not loaded from configuration file")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

# Now we can access `args.user_prompt`

finalReached = False

for i in range(5):


    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print("Prompt tokens: ", response.usage.prompt_tokens)
        print("Response tokens: ", response.usage.completion_tokens)

    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)

            if args.verbose:
                print(f"-> {result_message['content']}")

    else:
        print("Final response: ")
        finalReached = True
        print(message.content)
        break;

if not finalReached:
    print("Reached maximum amount of tool calls before finishing :(")