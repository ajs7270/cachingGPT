import json
from dataclasses import dataclass
from pathlib import Path
from time import sleep

from langchain import OpenAI, ConversationChain
from datetime import datetime

from datasets import Dataset
from core import PoT, PoT_original

# Load SVAMP dataset
svamp = Dataset(Path("data/SVAMP.json"))

# Load LlamaCpp
llm = OpenAI(temperature=0.7)

@dataclass
class Result:
    passage: str
    question: str
    answer: float
    cache: str
    openai: str


def dataclass_to_dict(obj):
    if isinstance(obj, list):
        return [dataclass_to_dict(value) for value in obj]
    elif isinstance(obj, dict):
        return {key: dataclass_to_dict(value) for key, value in obj.items()}
    elif isinstance(obj, Result):
        return {"passage": obj.passage, "question": obj.question, "answer": obj.answer,
                "cache": obj.cache, "openai": obj.openai}
    else:
        return obj


try:
    outputs = []
    for i, problem in enumerate(svamp):
        sleep(1)
        pot_cache, pot_output = PoT_original(llm=llm, problem=problem)

        print(f"Question {i+1}---")
        outputs.append(Result(passage=problem.passage, question=problem.question,
                              answer=problem.answer, cache=pot_cache, openai=pot_output))

finally:
    # Convert dataclass objects to dictionaries
    outputs = dataclass_to_dict(outputs)

    # Get current date and time
    now = datetime.now()

    # Save result json
    with open(Path(f"result_{now.strftime('%m%d_%H%M')}.json"), 'w') as f:
        json.dump({
            "Results": outputs,
        }, f, indent=4)
