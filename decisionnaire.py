from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import json

class DecisionnaireAgent(Agent):
    class DecisionnaireBehaviour(CyclicBehaviour):
        async def on_start(self):
            self.lignes_traitees = 0
            self.total_lignes_traitees = 0
            self.batch_size = 50
            self.batch_start_time = None
            self.timeout_batch = 60  # secondes
            print("[Décisionnaire] Prêt à recevoir.")

        async def run(self):
            if self.lignes_traitees == 0:
                self.batch_start_time = self.agent.loop.time()

            elapsed = self.agent.loop.time() - self.batch_start_time
            remaining_time = max(0, self.timeout_batch - elapsed)

            print("[Décisionnaire] 🔄 En attente de message...")
            msg = await self.receive(timeout=remaining_time)

            if msg:
                try:
                    payload = json.loads(msg.body)
                    score = payload.get('score')
                    data = payload.get('data', {})
                    customer_id = data.get('customer_id', "unknown")

                    decision_map = {
                        0: "Refusé (Profil Poor : risque élevé)",
                        1: "Accepté sous conditions (Profil Standard : risque modéré)",
                        2: "Accepté (Profil Good : faible risque)"
                    }

                    delay = data.get('delay_from_due_date', 0)
                    utilization = data.get('credit_utilization_ratio', 0.0)

                    decision = decision_map.get(score, "Score inconnu")

                    if score == 1 and delay > 30:
                        decision = "Refusé (Retard important malgré score standard)"
                    elif score == 1 and utilization > 0.8:
                        decision = "Refusé (Ratio d'utilisation élevé malgré score standard)"

                    print(f"[Décisionnaire] Crédit {decision} pour client ID : {customer_id} (score : {score})")

                    self.lignes_traitees += 1
                    self.total_lignes_traitees += 1
                    print(f"[Décisionnaire] Lignes traitées dans ce lot : {self.lignes_traitees}, Total : {self.total_lignes_traitees}")

                    if self.lignes_traitees >= self.batch_size:
                        confirm_msg = Message(to="agent_demandeur@mahasbk.mshome.net")
                        confirm_msg.set_metadata("performative", "inform")
                        confirm_msg.body = "Lot traité"
                        await self.send(confirm_msg)
                        print("[Décisionnaire] Confirmation envoyée au Demandeur.")
                        self.lignes_traitees = 0
                        self.batch_start_time = None

                except Exception as e:
                    print(f"[Décisionnaire] ERREUR lors de la décision: {e}")

            else:
                # Timeout expiré
                if self.lignes_traitees > 0:
                    perdues = self.batch_size - self.lignes_traitees
                    print(f"[Décisionnaire] Timeout batch atteint. Lignes traitées : {self.lignes_traitees}, perdues : {perdues}")
                    confirm_msg = Message(to="agent_demandeur@mahasbk.mshome.net")
                    confirm_msg.set_metadata("performative", "inform")
                    confirm_msg.body = "Lot traité"
                    await self.send(confirm_msg)
                    print("[Décisionnaire] Confirmation envoyée malgré pertes.")
                    self.lignes_traitees = 0
                    self.batch_start_time = None
                else:
                    print("[Décisionnaire] Aucun message reçu dans le délai.")

    async def setup(self):
        b = self.DecisionnaireBehaviour()
        self.add_behaviour(b)
