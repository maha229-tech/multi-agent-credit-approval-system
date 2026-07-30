from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json

class FileAgent(Agent):
    class ForwardBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                payload = json.loads(msg.body)
                print(f"[File] Reçu de l'évaluateur: score={payload['score']}")

                decision_msg = Message(to="agent_decideur@mahasbk.mshome.net")
                decision_msg.set_metadata("performative", "inform")
                decision_msg.body = json.dumps(payload)
                await self.send(decision_msg)
                print(f"[File] Envoyé au décisionnaire: score={payload['score']}")

    async def setup(self):
        print("[File] Agent prêt.")
        self.add_behaviour(self.ForwardBehaviour())
