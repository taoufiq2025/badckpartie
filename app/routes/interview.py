from flask import Blueprint, request, jsonify, current_app

interview_bp = Blueprint("interview", __name__)

# Données simulées pour les tests sans base de données
INTERVIEWS = [
    {
        "id": "int-0001",
        "candidate_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "recruiter_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "job_id": "0ea26df1-efe3-4fd9-8d86-4ccedd175786",
        "date": "2025-06-24T10:00:00",
        "link": "https://meet.example.com/meet1",
        "message": "Entretien technique",
        "status": "prévu",
        "created_at": "2025-06-20T09:00:00"
    },
    {
        "id": "int-0002",
        "candidate_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "recruiter_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "job_id": "0ea26df1-efe3-4fd9-8d86-4ccedd175786",
        "date": "2025-06-25T11:00:00",
        "link": "https://meet.example.com/meet2",
        "message": "Entretien RH",
        "status": "terminé",
        "created_at": "2025-06-20T10:00:00"
    },
    {
        "id": "int-0003",
        "candidate_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "recruiter_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "job_id": "0ea26df1-efe3-4fd9-8d86-4ccedd175786",
        "date": "2025-06-26T12:00:00",
        "link": "https://meet.example.com/meet3",
        "message": "Entretien final",
        "status": "annulé",
        "created_at": "2025-06-20T11:00:00"
    },
    {
        "id": "int-0004",
        "candidate_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "recruiter_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "job_id": "0ea26df1-efe3-4fd9-8d86-4ccedd175786",
        "date": "2025-06-27T13:00:00",
        "link": "https://meet.example.com/meet4",
        "message": "Entretien motivation",
        "status": "prévu",
        "created_at": "2025-06-20T12:00:00"
    },
    {
        "id": "int-0005",
        "candidate_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "recruiter_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "job_id": "0ea26df1-efe3-4fd9-8d86-4ccedd175786",
        "date": "2025-06-28T14:00:00",
        "link": "https://meet.example.com/meet5",
        "message": "Entretien projet",
        "status": "prévu",
        "created_at": "2025-06-20T13:00:00"
    },
    {
        "id": "int-0006",
        "candidate_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "recruiter_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "job_id": "0ea26df1-efe3-4fd9-8d86-4ccedd175786",
        "date": "2025-06-29T15:00:00",
        "link": "https://meet.example.com/meet6",
        "message": "Entretien soft skills",
        "status": "prévu",
        "created_at": "2025-06-20T14:00:00"
    },
    {
        "id": "int-0007",
        "candidate_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "recruiter_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "job_id": "0ea26df1-efe3-4fd9-8d86-4ccedd175786",
        "date": "2025-06-30T16:00:00",
        "link": "https://meet.example.com/meet7",
        "message": "Entretien anglais",
        "status": "prévu",
        "created_at": "2025-06-20T15:00:00"
    },
    {
        "id": "int-0008",
        "candidate_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "recruiter_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "job_id": "0ea26df1-efe3-4fd9-8d86-4ccedd175786",
        "date": "2025-07-01T17:00:00",
        "link": "https://meet.example.com/meet8",
        "message": "Entretien culture d'entreprise",
        "status": "prévu",
        "created_at": "2025-06-20T16:00:00"
    },
    {
        "id": "int-0009",
        "candidate_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "recruiter_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "job_id": "0ea26df1-efe3-4fd9-8d86-4ccedd175786",
        "date": "2025-07-02T18:00:00",
        "link": "https://meet.example.com/meet9",
        "message": "Entretien technique avancé",
        "status": "prévu",
        "created_at": "2025-06-20T17:00:00"
    },
    {
        "id": "int-0010",
        "candidate_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "recruiter_id": "3823eb09-f9f6-4bc7-a8f3-49e9aea76e1a",
        "job_id": "0ea26df1-efe3-4fd9-8d86-4ccedd175786",
        "date": "2025-07-03T19:00:00",
        "link": "https://meet.example.com/meet10",
        "message": "Entretien final RH",
        "status": "prévu",
        "created_at": "2025-06-20T18:00:00"
    }
]
"""*
*
*   GET
*
"""
# 🔹 GET /interviews — Tous les entretiens (option : filtre, pagination)
@interview_bp.route("/", methods=["GET"])
def get_interviews():
    # Filtres optionnels
    candidate_id = request.args.get("candidate_id")
    recruiter_id = request.args.get("recruiter_id")
    job_id = request.args.get("job_id")
    # Pagination params facultatifs
    page = request.args.get("page", type=int, default=None)
    page_size = request.args.get("page_size", type=int, default=None)

    results = INTERVIEWS
    if candidate_id:
        results = [i for i in results if i["candidate_id"] == candidate_id]
    if recruiter_id:
        results = [i for i in results if i["recruiter_id"] == recruiter_id]
    if job_id:
        results = [i for i in results if i["job_id"] == job_id]

    if page is not None and page_size is not None:
        if page < 1 or page_size < 1:
            return jsonify({"error": "Paramètres de pagination invalides"}), 400
        total = len(results)
        total_pages = (total + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = start + page_size
        paginated = results[start:end]
        return jsonify({
            "results": paginated,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }), 200
    else:
        return jsonify(results), 200


"""*
*
*   ADD
*
"""
# 🔹 Planifier (créer) un entretien
@interview_bp.route("/", methods=["POST"])
def create_interview():
    data = request.get_json()
    required_fields = ["candidate_id", "recruiter_id", "job_id", "date", "link", "message", "status"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Champs requis manquants"}), 400
    new_interview = {
        "id": f'int-{len(INTERVIEWS) + 1:04d}',
        **{k: data[k] for k in required_fields},
        "created_at": data.get("created_at", "2025-06-20T18:00:00")
    }
    INTERVIEWS.append(new_interview)
    return jsonify(new_interview), 201
"""*
*
*   UPDATE
*
"""

# Helper to find interview by id or triplet

def find_interview(interview_id=None, recruiter_id=None, job_id=None, candidate_id=None):
    if interview_id:
        return next((i for i in INTERVIEWS if i["id"] == f"int-{interview_id}"), None)
    elif recruiter_id and job_id and candidate_id:
        return next((i for i in INTERVIEWS if i["recruiter_id"] == recruiter_id and i["job_id"] == job_id and i["candidate_id"] == candidate_id), None)
    return None

# 🔹 Mettre à jour un entretien (par id ou triplet)
@interview_bp.route("/<recruiter_id>/<job_id>/<candidate_id>", methods=["PUT"])
def update_interview(interview_id=None, recruiter_id=None, job_id=None, candidate_id=None):
    data = request.get_json()
    interview = find_interview(interview_id, recruiter_id, job_id, candidate_id)
    if not interview:
        return jsonify({"error": "Entretien non trouvé"}), 404
    for key in ["date", "link", "message", "status"]:
        if key in data:
            interview[key] = data[key]
    return jsonify(interview), 200

"""*
*
*   DELETE
*
"""
# 🔹 Supprimer un entretien (par id ou triplet)
@interview_bp.route("/<recruiter_id>/<job_id>/<candidate_id>", methods=["DELETE"])
def delete_interview(interview_id=None, recruiter_id=None, job_id=None, candidate_id=None):
    # Find index for removal
    idx = None
    if interview_id:
        idx = next((i for i, x in enumerate(INTERVIEWS) if x["id"] == f"int-{interview_id}"), None)
    elif recruiter_id and job_id and candidate_id:
        idx = next((i for i, x in enumerate(INTERVIEWS) if x["recruiter_id"] == recruiter_id and x["job_id"] == job_id and x["candidate_id"] == candidate_id), None)
    if idx is None:
        return jsonify({"error": "Entretien non trouvé"}), 404
    INTERVIEWS.pop(idx)
    return jsonify({"message": "Entretien supprimé"}), 200
