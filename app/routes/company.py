from flask import Blueprint, jsonify, current_app, request
import uuid

company_bp = Blueprint("company", __name__)

# 🔹 Récupérer toutes les entreprises
@company_bp.route("/", methods=["GET"])
def get_companies():
    try:
        supabase = current_app.supabase
        result = supabase.table("companies").select("*").execute()
        return jsonify(result.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""
# 🔹 Récupérer une entreprise par ID
@company_bp.route('/company/<company_id>', methods=['GET'])
def get_company(company_id):
    try:
        supabase = current_app.supabase
        result = supabase.table("companies").select("*").eq("id", company_id).single().execute()
        if result.data:
            return jsonify(result.data), 200
        return jsonify({"error": "Company not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Mettre à jour une entreprise par ID
@company_bp.route('/company/<company_id>', methods=['PUT'])
def update_company(company_id):
    try:
        supabase = current_app.supabase
        data = request.json

        update_data = {
            "name": data.get("name"),
            "website": data.get("website"),
            "email": data.get("email"),
            "logo_url": data.get("logo_url"),
            "description": data.get("description"),
            "social_links": data.get("social_links", {})
        }

        response = supabase.table("companies").update(update_data).eq("id", company_id).execute()
        return jsonify({"message": "Company updated successfully", "data": response.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@company_bp.route('/upload-logo', methods=['POST'])
def upload_logo():
    try:
        recruiter_id = request.headers.get("X-Recruiter-ID")
        if not recruiter_id:
            return jsonify({"error": "Missing X-Recruiter-ID header"}), 400

        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Générer un nom de fichier unique
        filename = f"{uuid.uuid4()}.png"

        # Lire le contenu du fichier en bytes
        file_content = file.read()

        supabase = current_app.supabase

        # Récupérer le bucket "logos"
        bucket = supabase.storage.from_('logos')

        print("Upload fichier vers Supabase Storage…")
        bucket.upload(filename, file_content, {"content-type": file.mimetype})
        public_url = bucket.get_public_url(filename)

        print("Logo uploadé, URL publique :", public_url)

        # Trouver l'entreprise liée au recruteur
        company_result = supabase.table("companies").select("id").eq("recruiter_id", recruiter_id).single().execute()
        if not company_result.data:
            return jsonify({"error": "Company not found for recruiter"}), 404

        company_id = company_result.data["id"]

        # Mettre à jour l'URL du logo dans la table companies
        supabase.table("companies").update({"logo_url": public_url}).eq("id", company_id).execute()

        return jsonify({"logo_url": public_url}), 200

    except Exception as e:
        print("Exception lors de l'upload :", e)
        return jsonify({"error": str(e)}), 500
"""    
# 🔹 Récupérer une entreprise par recruiter_id
@company_bp.route('/company/recruiter/<recruiter_id>', methods=['GET'])
def get_company_by_recruiter(recruiter_id):
    try:
        supabase = current_app.supabase
        result = supabase.table("companies").select("*").eq("recruiter_id", recruiter_id).single().execute()
        if result.data:
            return jsonify(result.data), 200
        return jsonify({"error": "Company not found for this recruiter"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔹 Mettre à jour une entreprise par recruiter_id
@company_bp.route('/company/recruiter/<recruiter_id>', methods=['PUT'])
def update_company_by_recruiter(recruiter_id):
    try:
        supabase = current_app.supabase
        data = request.json

        update_data = {
            "name": data.get("name"),
            "website": data.get("website"),
            "email": data.get("email"),
            "logo_url": data.get("logo_url"),
            "description": data.get("description"),
            "social_links": data.get("social_links", {})
        }

        # Update the company where recruiter_id matches
        response = supabase.table("companies").update(update_data).eq("recruiter_id", recruiter_id).execute()
        return jsonify({"message": "Company updated successfully", "data": response.data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
