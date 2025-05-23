from uagents import Agent, Context, Model
from pydantic import Field
from models import Payment

AGENT_A_SEED = "praise frost bubble arrest vital drill option never permit extend tragic valve"
AGENT_B_ADDRESS = "agent1qdzg73y99qyhfl8ps4nkup8970ymnxjzv0esuw2ra7te77c3vhfhwwkxzhj"
AGENT_B_WALLET_ADDRESS = "fetch16vstnzcew34zlxenagse7s8l4rc6mkp6fxkjyr"

agent_a = Agent(name="agent_a", port=8003, seed=AGENT_A_SEED, endpoint=["http://localhost:8003/submit"])

@agent_a.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Agent A Ready. Sending token intent to {AGENT_B_ADDRESS}")
    await ctx.send(AGENT_B_ADDRESS, Payment(amount=1, receiver=AGENT_B_WALLET_ADDRESS))

if __name__ == "__main__":
    agent_a.run()
