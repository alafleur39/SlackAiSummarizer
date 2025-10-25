from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
parser = StrOutputParser()

template = """
You are a helpful Slack AI assistant.
Summarize the following Slack messages into a concise, professional daily update.
Make it sound human, short, and clear.

Messages:
{messages}

Output format:
### Team Summary
...
"""

prompt = PromptTemplate.from_template(template)
chain = prompt | llm | parser

def summarize_messages(messages: list[str]) -> str:
    combined = "\n".join(messages)
    return chain.invoke({"messages": combined})
