from flask import Blueprint, jsonify, current_app,request

recruiter_bp = Blueprint("recruiter", __name__)



@recruiter_bp.route("/offers/by-recruiter", methods=["GET"])
def get_offers_by_recruiter():
    supabase = current_app.supabase
    recruiter_id = request.args.get("recruiter_id")
    if not recruiter_id:
        return jsonify({"error": "recruiter_id is required"}), 400
    
    # Trouver la company associée au recruiter_id
    company = supabase.table("companies").select("id").eq("recruiter_id", recruiter_id).execute()
    if not company.data:
        return jsonify([]), 200  # Pas d'entreprise = pas d'offres
    
    company_id = company.data[0]["id"]
    
    # Récupérer les jobs liés à la company
    jobs = supabase.table("jobs").select("*").eq("company_id", company_id).execute()
    
    return jsonify(jobs.data), 200



@recruiter_bp.route("/company/by-recruiter", methods=["GET"])
def get_company_by_recruiter():
    supabase = current_app.supabase
    recruiter_id = request.args.get("recruiter_id")
    
    if not recruiter_id:
        return jsonify({"error": "recruiter_id is required"}), 400
    
    # Trouver la company associée au recruiter_id
    company = supabase.table("companies").select("*").eq("recruiter_id", recruiter_id).execute()
    
    if not company.data:
        return jsonify({"error": "No company found for this recruiter"}), 404
    
    # Retourner les informations de la company
    return jsonify(company.data[0]), 200













