from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI()

class text(BaseModel):
    message: str
    language: str


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing from environment variables.")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
model = ChatOpenAI(model="gpt-3.5-turbo")

#output parser
parser = StrOutputParser()

system_template = "Translate the following into {language}:"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
     
chain = prompt_template | model | parser


@app.get("/by_name/{name}")
def index(name):
    return (f"Welcome {name}!")


@app.post("/translator")
def mess_translator(info:text):
    lang = info.language
    data = info.message

    translated_message = chain.invoke({"language":lang, "text": data})

    return translated_message


