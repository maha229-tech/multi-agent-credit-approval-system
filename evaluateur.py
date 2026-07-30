import pickle
import numpy as np
import pandas as pd
import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class EvaluateurAgent(Agent):
    class EvaluationBehaviour(CyclicBehaviour):
        async def on_start(self):
            print("[Évaluateur] Initialisation : chargement du modèle…")
            try:
                with open("model.pkl", "rb") as f:
                    self.model = pickle.load(f)
                with open("encoders.pkl", "rb") as f:
                    self.label_encoders = pickle.load(f)
                self.features = [
                    'age', 'occupation', 'annual_income', 'monthly_inhand_salary',
                    'num_bank_accounts', 'num_credit_card', 'interest_rate',
                    'num_of_loan', 'delay_from_due_date', 'num_of_delayed_payment',
                    'changed_credit_limit', 'num_credit_inquiries', 'credit_mix',
                    'outstanding_debt', 'credit_utilization_ratio', 'credit_history_age',
                    'payment_of_min_amount', 'total_emi_per_month',
                    'amount_invested_monthly', 'payment_behaviour', 'monthly_balance'
                ]
                print("[Évaluateur] ✅ Modèle et encodeurs chargés avec succès.")
            except Exception as e:
                print(f"[Évaluateur] ❌ Erreur au chargement du modèle/encodeurs : {e}")

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print("[Évaluateur] 📩 Message reçu.")
                try:
                    data = json.loads(msg.body)

                    for col, le in self.label_encoders.items():
                        if col in data:
                            try:
                                data[col] = int(le.transform([data[col]])[0])
                            except ValueError:
                                print(f"[Évaluateur] ⚠ Valeur inconnue pour '{col}': {data[col]}, encodée à 0")
                                data[col] = 0
                        else:
                            data[col] = 0

                    for feat in self.features:
                        if feat not in data or data[feat] in [None, "", "nan", np.nan]:
                            data[feat] = 0

                    df = pd.DataFrame([data], columns=self.features)
                    if df.isnull().any().any():
                        df.fillna(0, inplace=True)

                    prediction = self.model.predict(df)[0]

                    payload = {
                        "score": int(prediction),
                        "customer_id": data.get("customer_id", "unknown"),
                        "data": data
                    }
                    result_msg = Message(to="agent_file@mahasbk.mshome.net")
                    result_msg.set_metadata("performative", "inform")
                    result_msg.set_metadata("type", "evaluation_result")
                    result_msg.body = json.dumps(payload)
                    await self.send(result_msg)

                    print(f"[Évaluateur] Score {prediction} envoyé au FileAgent.")

                except Exception as e:
                    print(f"[Évaluateur] ERREUR de traitement : {e}")

    async def setup(self):
        print("[Évaluateur] Démarrage en cours…")
        b = self.EvaluationBehaviour()
        self.add_behaviour(b)
        await b.on_start()   
