from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import pandas as pd
import json
import asyncio

class DemandeurAgent(Agent):
    class DemandeurBehaviour(CyclicBehaviour):
        async def on_start(self):
            print("[Demandeur] Chargement des données...")
            self.dataset = pd.read_csv("base_prete.csv")
            self.important_fields = [
                'customer_id','age', 'occupation', 'annual_income', 'monthly_inhand_salary', 'num_bank_accounts',
                'num_credit_card', 'interest_rate', 'num_of_loan', 'delay_from_due_date',
                'num_of_delayed_payment', 'changed_credit_limit', 'num_credit_inquiries',
                'credit_mix', 'outstanding_debt', 'credit_utilization_ratio', 'credit_history_age',
                'payment_of_min_amount', 'total_emi_per_month', 'amount_invested_monthly',
                'payment_behaviour', 'monthly_balance'
            ]
            self.current_index = 0
            self.batch_size = 50
            self.waiting_for_confirmation = False

        async def run(self):
            if not self.waiting_for_confirmation:
                if self.current_index >= len(self.dataset):
                    print("[Demandeur] Fin du dataset.")
                    await self.agent.stop()
                    return

                batch = self.dataset.iloc[self.current_index:self.current_index + self.batch_size]
                self.current_index += self.batch_size

                for index, row in batch.iterrows():
                    credit_data = {key: row[key] for key in self.important_fields}
                    credit_data["customer_id"] = int(index)
                    msg = Message(to="agent_evaluateur@mahasbk.mshome.net")
                    msg.set_metadata("performative", "inform")
                    msg.body = json.dumps(credit_data)
                    await self.send(msg)
                    await asyncio.sleep(0.1)

                print(f"[Demandeur] Lot de {len(batch)} demandes envoyé.")
                self.waiting_for_confirmation = True
            else:
                msg = await self.receive(timeout=30)
                if msg and msg.body == "Lot traité":
                    print("[Demandeur] Confirmation reçue, envoi du lot suivant.")
                    self.waiting_for_confirmation = False

    async def setup(self):
        print("[Demandeur] Agent initialisé.")
        b = self.DemandeurBehaviour()
        self.add_behaviour(b)    
