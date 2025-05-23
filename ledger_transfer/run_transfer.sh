#!/bin/bash
echo "Starting Agent A..."
gnome-terminal -- bash -c "cd agent_uagents && source ../uagents_env/bin/activate && python AgentA.py"

echo "Starting Agent B..."
gnome-terminal -- bash -c "cd agent_uagents && source ../uagents_env/bin/activate && python AgentB.py"
