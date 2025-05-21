import asyncio
import os 
from dotenv import load_dotenv
from agents import Agent,OpenAIChatCompletionsModel, Runner,set_tracing_disabled
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
import rich


load_dotenv()

set_tracing_disabled(disabled=True)

OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
#----------------------------------------

client = AsyncOpenAI(
    api_key=OPEN_ROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
)

agent = Agent(
     model = OpenAIChatCompletionsModel(model="deepseek/deepseek-r1:free", openai_client=client),
     name = "my_agent",
     instructions = "you are a helpful assistant",
                        #  --------- system prompt-------
)

# ----------------------------------------------
# ------------------- streaming ----------------------
#                                             ---- user prompt-------
async def main():
    jawab = Runner.run_streamed(starting_agent=agent, input="write a 10 lines of easy") #agentic loop
    async for event in jawab.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data , ResponseTextDeltaEvent):
         rich.print(event.data.delta,end="",flush=True)


if __name__ == "__main__":
    asyncio.run(main())    