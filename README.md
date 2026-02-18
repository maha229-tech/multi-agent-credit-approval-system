# multi-agent-credit-approval-system
Conception et développement d'un système intelligent distribué pour l'évaluation automatisée des demandes de crédit bancaire basé sur une architecture multi-agents avec SPADE. Le système repose sur quatre agents collaboratifs : l'agent Demandeur, l'agent Évaluateur, l'agent File d'attente et l'agent Décisionnaire .


## 🚀 How to Run

1. Install dependencies:
pip install -r requirements.txt

2. Train the model:
python train_model.py

3. Run the multi-agent system:
python main.py


## Important: SPADE Configuration

This project requires a running XMPP server for SPADE agents communication.

You can use:

- localhost XMPP server
- Prosody server
- Or SPADE built-in configuration

Each agent must have:
- JID (e.g., agent1@localhost)
- Password

---

## 👩‍💻 Author

Developed as part of a Master’s project in Big Data & Cloud Computing.
