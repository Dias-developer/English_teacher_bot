from groq import AsyncGroq
from os import getenv
from dotenv import load_dotenv
load_dotenv()
client = AsyncGroq(api_key=getenv('GROQ_API'))

