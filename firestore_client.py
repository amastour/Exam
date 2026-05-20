"""
Firestore client — singleton initialisé une seule fois.

Méthodes de credentials (priorité décroissante) :
  1. GOOGLE_CREDENTIALS_JSON='{"type":"service_account",...}'  (contenu JSON brut)
  2. GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json          (chemin vers fichier)
  3. Application Default Credentials (gcloud auth, GCE, Cloud Run…)

Optionnel :
  - FIRESTORE_PROJECT_ID=mon-projet   (détecté auto si non fourni)
  - FIRESTORE_EMULATOR_HOST=localhost:8080  (dev local avec émulateur)
"""

import json
import os
import firebase_admin
from firebase_admin import credentials, firestore

_app = None
_client = None


def get_firestore_client():
    """
    Retourne le client Firestore initialisé (singleton).
    Appeler cette fonction au lieu de recréer le client à chaque requête.
    """
    global _app, _client

    if _client is not None:
        return _client

    if not firebase_admin._apps:
        cred_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
        key_path  = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        if cred_json:
            # Méthode 1 : contenu JSON directement dans la variable d'env
            try:
                cred_dict = json.loads(cred_json)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"[FIRESTORE] GOOGLE_CREDENTIALS_JSON is not valid JSON: {e}")
            cred = credentials.Certificate(cred_dict)
            print("[FIRESTORE] Using credentials from GOOGLE_CREDENTIALS_JSON (env content)")
        elif key_path and os.path.exists(key_path):
            # Méthode 2 : chemin vers fichier
            cred = credentials.Certificate(key_path)
            print(f"[FIRESTORE] Using credentials from GOOGLE_APPLICATION_CREDENTIALS (file: {key_path})")
        else:
            # Méthode 3 : Application Default Credentials
            cred = credentials.ApplicationDefault()
            print("[FIRESTORE] Using Application Default Credentials")

        project_id = os.environ.get("FIRESTORE_PROJECT_ID")
        _app = firebase_admin.initialize_app(cred, {"projectId": project_id} if project_id else {})
    else:
        _app = firebase_admin.get_app()

    _client = firestore.client()
    return _client
