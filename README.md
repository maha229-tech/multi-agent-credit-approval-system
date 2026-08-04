# multi-agent-credit-approval-system
Design and development of a distributed intelligent system for automated bank credit application evaluation, based on a multi-agent architecture using SPADE. The system relies on four collaborative agents: the Applicant agent, the Evaluator agent, the Queue agent, and the Decision-Maker agent.


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
