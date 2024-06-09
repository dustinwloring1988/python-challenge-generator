import os
import json
import yaml
from typing import List
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Groq with API key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not found")
groq = Groq(api_key=groq_api_key)

class Test(BaseModel):
    input: str
    expected: str

class Challenge(BaseModel):
    title: str
    difficulty: str
    description: str
    example: str
    template: str
    solution: str
    tests: List[Test]

def get_challenges(num_challenges: int) -> List[Challenge]:
    example = "- title: Reverse String\n  difficulty: medium\n  description: \"Write a function called 'reverse_string' that returns the reverse of the input string `s`.\"\n  example: \"Example: reverse_string('hello') should return 'olleh'.\"\n  template: \"def reverse_string(s):\\n    # Write your code here\\n    pass\\n\"\n  solution: \"def reverse_string(s):\\n    return s[::-1]\\n\"\n  tests:\n    - input: 'reverse_string(\"hello\")'\n      expected: 'olleh'\n    - input: 'reverse_string(\"world\")'\n      expected: 'dlrow'\n    - input: 'reverse_string(\"\")'\n      expected: ''"
    challenges = []
    for _ in range(num_challenges):
        chat_completion = groq.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a coding challenge database that outputs challenges in JSON.\n"
                    f" The JSON object must use the schema: {json.dumps(Challenge.schema(), indent=2)}",
                },
                {
                    "role": "user",
                    "content": f"Generate a challenge from the following example: '{example}'.\nPlease ensure that the solution and template are not the same. The template should provide a boilerplate code with the function definition and should include a placeholder (e.g., 'pass') for the implementation.",
                },
            ],
            model="llama3-8b-8192",
            temperature=0,
            stream=False,
            response_format={"type": "json_object"},
        )

        response_content = chat_completion.choices[0].message.content
        response_json = json.loads(response_content)

        challenge_data = {
            "title": response_json["properties"]["title"],
            "difficulty": response_json["properties"]["difficulty"],
            "description": response_json["properties"]["description"],
            "example": response_json["properties"]["example"],
            "template": response_json["properties"]["template"],
            "solution": response_json["properties"]["solution"],
            "tests": response_json["properties"]["tests"],
        }

        challenges.append(Challenge(**challenge_data))

    return challenges

def save_challenges_to_yaml(challenges: List[Challenge], filename: str):
    formatted_data = [{
        "title": challenge.title,
        "difficulty": challenge.difficulty.lower(),
        "description": challenge.description,
        "example": challenge.example,
        "template": challenge.template,
        "solution": challenge.solution,
        "tests": [{"input": test.input, "expected": int(test.expected)} if test.expected.isdigit() else {"input": test.input, "expected": test.expected} for test in challenge.tests],
    } for challenge in challenges]

    with open(filename, 'w') as file:
        yaml.dump(formatted_data, file, default_flow_style=False)
    print(f"Challenges saved to {filename}")

def print_challenges(challenges: List[Challenge]):
    for i, challenge in enumerate(challenges, start=1):
        print(f"Challenge {i}:")
        print("Title:", challenge.title)
        print("Difficulty:", challenge.difficulty)
        print("Description:", challenge.description)
        print("Example:", challenge.example)
        print("Template:\n", challenge.template)
        print("Solution:\n", challenge.solution)
        print("\nTests:")
        for test in challenge.tests:
            print(f"- Input: {test.input}, Expected: {test.expected}")
        print()

if __name__ == "__main__":
    num_challenges = 5
    challenges = get_challenges(num_challenges)
    print_challenges(challenges)
    save_challenges_to_yaml(challenges, "test.yaml")
