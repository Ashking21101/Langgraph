FOR UV = 
1. curl -LsSf https://astral.sh/uv/install.sh | sh
2. uv --version
3. uv venv
4. source .venv/bin/activate
5. uv init
6. uv add -r requirements.txt
   

``` bash

Markdown op
from IPython.display import display, Markdown
display(Markdown(result))




Wht is structure op?
""".with_structured_output()
This method binds a schema (like a Pydantic model) to an LLM, ensuring the output strictly follows the defined structure. It works with models that support native structured output (e.g., OpenAI’s json_mode, Anthropic, Cohere)."""

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

class Trivia(BaseModel):
    question: str = Field(description="The trivia question")
    answer: str = Field(description="The correct answer")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = model.with_structured_output(Trivia, method="json_mode")   


-------------------------------------

"""PydanticOutputParser
Use this when your LLM doesn’t support native structured output. It parses raw model output into a Pydantic object, enforcing type safety and validation."""

from langchain_core.output_parsers import PydanticOutputParser
parser = PydanticOutputParser(pydantic_object=Library)