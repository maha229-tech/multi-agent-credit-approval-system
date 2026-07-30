# train_model.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# Chargement du dataset
df = pd.read_csv("base_prete.csv")

# Colonnes à garder
features = [
    'age', 'occupation', 'annual_income', 'monthly_inhand_salary', 'num_bank_accounts',
    'num_credit_card', 'interest_rate', 'num_of_loan', 'delay_from_due_date',
    'num_of_delayed_payment', 'changed_credit_limit', 'num_credit_inquiries',
    'credit_mix', 'outstanding_debt', 'credit_utilization_ratio', 'credit_history_age',
    'payment_of_min_amount', 'total_emi_per_month', 'amount_invested_monthly',
    'payment_behaviour', 'monthly_balance'
]

# On garde uniquement les lignes sans valeurs manquantes sur ces colonnes + target
df = df[features + ['credit_score_numeric']].dropna()

# Encodage des colonnes catégorielles
label_encoders = {}
for col in df.select_dtypes(include='object').columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Séparation des données en train et test (80% train, 20% test)
X = df[features]
y = df['credit_score_numeric']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Création et entraînement du modèle RandomForest avec gestion du déséquilibre
model = RandomForestClassifier(class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Prédictions sur le test
y_pred = model.predict(X_test)

# Évaluation
print("=== Évaluation du modèle ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Rapport de classification:")
print(classification_report(y_test, y_pred))
print("Matrice de confusion:")
print(confusion_matrix(y_test, y_pred))

# Sauvegarde du modèle et des encodeurs
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

print("Modèle et encodeurs enregistrés.")
