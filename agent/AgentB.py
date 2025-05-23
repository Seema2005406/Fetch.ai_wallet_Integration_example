from uagents import Agent, Context, Model
from models import Payment

AGENT_B_SEED = "agent b unique wallet seed"

agent_b = Agent(name="agent_b",port=8002, seed=AGENT_B_SEED, endpoint=["http://localhost:8002/submit"])

@agent_b.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"✅ Agent B Ready. Wallet: {agent_b.wallet.address()}")

@agent_b.on_message(model=Payment)
async def receive(ctx: Context, sender: str, msg: Payment):
    ctx.logger.info(f"💰 Intent to transfer {msg.amount} FET from {sender} to {msg.receiver}")

if __name__ == "__main__":
    agent_b.run()
