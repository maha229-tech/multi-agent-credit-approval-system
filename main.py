import asyncio
from demandeur import DemandeurAgent
from evaluateur import EvaluateurAgent
from file import FileAgent
from decisionnaire import DecisionnaireAgent

async def main():
    server_domain = "mahasbk.mshome.net"
    mot_de_passe = "maha2002"

    demandeur = DemandeurAgent(f"agent_demandeur@{server_domain}", mot_de_passe)
    evaluateur = EvaluateurAgent(f"agent_evaluateur@{server_domain}", mot_de_passe)
    file = FileAgent(f"agent_file@{server_domain}", mot_de_passe)
    decisionnaire = DecisionnaireAgent(f"agent_decideur@{server_domain}", mot_de_passe)  # ici agent_decideur

    await demandeur.start(auto_register=False)
    await evaluateur.start(auto_register=False)
    await file.start(auto_register=False)
    await decisionnaire.start(auto_register=False)

    print("[Main] Tous les agents ont été démarrés.")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("[Main] Arrêt demandé.")

    await demandeur.stop()
    await evaluateur.stop()
    await file.stop()
    await decisionnaire.stop()

if __name__ == "__main__":
    asyncio.run(main())
