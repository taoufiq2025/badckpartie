from flask import Blueprint, jsonify, current_app
from datetime import datetime
from collections import defaultdict

dashboard_bp = Blueprint("dashboard", __name__) #*
#*
#**
@dashboard_bp.route("/dashboard/summary", methods=["GET"])#used
def dashboard_summary():
    supabase = current_app.supabase

    total_applied = supabase.table("applications").select("id").execute().data
    total_hired = supabase.table("applications").select("id").eq("status", "hired").execute().data
    open_positions = supabase.table("jobs").select("id").execute().data

    avg_cost_per_hire = 12

    return jsonify({
        "appliedCandidates": len(total_applied),
        "hiredCandidates": len(total_hired),
        "openPositions": len(open_positions),
        "avgCostPerHire": avg_cost_per_hire
    }), 200

@dashboard_bp.route("/dashboard/job-stats", methods=["GET"])#used
def job_stats():
    supabase = current_app.supabase
    apps = supabase.table("applications").select("created_at,status").execute().data

    stats = defaultdict(lambda: {"applications": 0, "hired": 0})

    for app in apps:
        month = datetime.strptime(app["created_at"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%b")
        stats[month]["applications"] += 1
        if app["status"] == "hired":
            stats[month]["hired"] += 1

    return jsonify([{"month": m, **v} for m, v in stats.items()]), 200

"""
@dashboard_bp.route("/dashboard/application-progression", methods=["GET"])
def application_progression():
    supabase = current_app.supabase
    apps = supabase.table("applications").select("status").execute().data

    counts = defaultdict(int)
    for app in apps:
        counts[app["status"]] += 1

    return jsonify({
        "applied": counts.get("applied", 0),
        "shortlisted_round1": counts.get("shortlisted_round1", 0),
        "shortlisted_round2": counts.get("shortlisted_round2", 0),
        "hired": counts.get("hired", 0)
    }), 200

"""



@dashboard_bp.route("/dashboard/offer-acceptance", methods=["GET"])#used
def offer_acceptance():
    supabase = current_app.supabase
    apps = supabase.table("applications").select("status").execute().data

    accepted = sum(1 for app in apps if app["status"] == "hired")
    rejected = sum(1 for app in apps if app["status"] == "rejected")
    pending=sum(1 for app in apps if app["status"] == "pending")
    total  =accepted+rejected+pending


    if(accepted==0 or rejected==0 or pending==0) :

       return jsonify({
           "accepted":100,
            "rejected":8 ,
            "pending":20,
            "total":128    
              })
    




    return jsonify({
        "accepted": round((accepted / len(apps)) * 100) if apps else 0,
        "rejected": round((rejected / len(apps)) * 100) if apps else 0,
         "pending": round((pending / len(apps)) * 100) if apps else 0,
        "total":round((total / len(apps)) * 100) if apps else 0,
    }), 200

@dashboard_bp.route("/dashboard/source-of-hire", methods=["GET"])#no usedc mais data not dynamic
def source_of_hire():
    # Données statiques basées sur l'image fournie (Total: 400)
    data = [
        {"source": "Company Website", "count": 100, "percentage": 30},
        {"source": "Job Boards", "count": 50, "percentage": 5},
        {"source": "Social Media", "count": 80, "percentage": 20},
        {"source": "Career Fair", "count": 100, "percentage": 30},
        {"source": "Referrals", "count": 70, "percentage": 15}
    ]
    return jsonify(data), 200

"""
@dashboard_bp.route("/dashboard/source-of-hire", methods=["GET"])
def source_of_hire():
    supabase = current_app.supabase
    profiles = supabase.table("candidate_profiles").select("source").execute().data

    counts = defaultdict(int)
    for profile in profiles:
        source = profile.get("source", "other")
        counts[source] += 1

    total = sum(counts.values())
    response = [
        {"source": k, "count": v, "percentage": round((v / total) * 100)} for k, v in counts.items()
    ]
    return jsonify(response), 200
"""
@dashboard_bp.route("/dashboard/lgbtq-inclusion", methods=["GET"])#used
def lgbtq_inclusion():
    return jsonify({
        "applied": 40,
        "interviewed": 24,
        "hired": 16
    }), 200

@dashboard_bp.route("/dashboard/candidates-by-location", methods=["GET"])
def candidates_by_location():
    supabase = current_app.supabase
    profiles = supabase.table("candidate_profiles").select("location").execute().data

    stats = defaultdict(int)
    for p in profiles:
        loc = p.get("location", "unknown")
        stats[loc] += 1

    return jsonify([{"location": k, "count": v} for k, v in stats.items()]), 200

@dashboard_bp.route("/dashboard/average-candidate-score", methods=["GET"])
def average_candidate_score():
    supabase = current_app.supabase
    profiles = supabase.table("candidate_profiles").select("skills_score", "context_score").execute().data

    total_skills = sum(p["skills_score"] or 0 for p in profiles)
    total_context = sum(p["context_score"] or 0 for p in profiles)
    count = len(profiles)

    return jsonify({
        "avgSkillsScore": round(total_skills / count, 2) if count else 0,
        "avgContextScore": round(total_context / count, 2) if count else 0
    }), 200

@dashboard_bp.route("/dashboard/jobs-by-company", methods=["GET"])
def jobs_by_company():
    supabase = current_app.supabase
    jobs = supabase.table("jobs").select("company_id").execute().data
    companies = supabase.table("companies").select("id", "name").execute().data

    company_map = {c["id"]: c["name"] for c in companies}
    stats = defaultdict(int)
    for job in jobs:
        name = company_map.get(job["company_id"], "unknown")
        stats[name] += 1

    return jsonify([{"company": k, "jobCount": v} for k, v in stats.items()]), 200

@dashboard_bp.route("/dashboard/top-skills", methods=["GET"])
def top_skills():
    supabase = current_app.supabase
    profiles = supabase.table("candidate_profiles").select("skills").execute().data

    skill_counts = defaultdict(int)
    for profile in profiles:
        skills = profile.get("skills", []) or []
        for skill in skills:
            skill_counts[skill.lower()] += 1

    sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return jsonify([{"skill": s, "count": c} for s, c in sorted_skills]), 200

@dashboard_bp.route("/dashboard/gender-diversity", methods=["GET"])
def gender_diversity():
    supabase = current_app.supabase
    try:
        profiles = supabase.table("candidate_profiles").select("gender").execute().data
    except Exception as e:
        return jsonify({
            "error": "Failed to fetch gender data. Ensure 'gender' column exists.",
            "details": str(e)
        }), 500

    counts = defaultdict(int)
    for profile in profiles:
        gender = profile.get("gender", "unknown")
        counts[gender] += 1
    total = sum(counts.values())
    response = [
        {"gender": g, "count": c, "percentage": round((c / total) * 100)} for g, c in counts.items()
    ]
    return jsonify(response), 200

@dashboard_bp.route("/dashboard/recruiter-performance", methods=["GET"])
def recruiter_performance():
    supabase = current_app.supabase
    recruiters = supabase.table("recruiters").select("id", "full_name").execute().data
    companies = supabase.table("companies").select("id", "recruiter_id").execute().data
    jobs = supabase.table("jobs").select("id", "company_id").execute().data
    apps = supabase.table("applications").select("job_id", "status").execute().data

    recruiter_map = {r["id"]: r["full_name"] for r in recruiters}
    company_to_recruiter = {c["id"]: c["recruiter_id"] for c in companies}
    job_to_company = {j["id"]: j["company_id"] for j in jobs}

    performance = defaultdict(lambda: {"applied": 0, "hired": 0})

    for app in apps:
        job_id = app["job_id"]
        company_id = job_to_company.get(job_id)
        recruiter_id = company_to_recruiter.get(company_id)
        if recruiter_id:
            performance[recruiter_id]["applied"] += 1
            if app["status"] == "hired":
                performance[recruiter_id]["hired"] += 1

    response = [
        {"recruiter": recruiter_map.get(rid, "unknown"), **stats}
        for rid, stats in performance.items()
    ]
    return jsonify(response), 200

@dashboard_bp.route("/dashboard/time-to-hire", methods=["GET"])
def time_to_hire():
    supabase = current_app.supabase
    apps = supabase.table("applications").select("created_at", "status").execute().data

    hire_durations = []
    for app in apps:
        if app["status"] == "hired":
            try:
                created = datetime.strptime(app["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                days = (datetime.now() - created).days
                hire_durations.append(days)
            except:
                continue

    if not hire_durations:
        return jsonify({"averageDays": 0, "minDays": 0, "maxDays": 0}), 200

    return jsonify({
        "averageDays": round(sum(hire_durations) / len(hire_durations), 1),
        "minDays": min(hire_durations),
        "maxDays": max(hire_durations)
    }), 200

@dashboard_bp.route("/dashboard/application-funnel", methods=["GET"])
def application_funnel():
    supabase = current_app.supabase
    apps = supabase.table("applications").select("status").execute().data

    total = len(apps)
    counts = defaultdict(int)
    for app in apps:
        counts[app["status"]] += 1

    funnel = {
        "applied": counts.get("applied", 0),
        "shortlisted_round1": counts.get("shortlisted_round1", 0),
        "shortlisted_round2": counts.get("shortlisted_round2", 0),
        "hired": counts.get("hired", 0)
    }

    for key in funnel:
        funnel[key + "_percent"] = round((funnel[key] / total) * 100) if total else 0

    return jsonify(funnel), 200

@dashboard_bp.route("/dashboard/job-popularity", methods=["GET"])
def job_popularity():
    supabase = current_app.supabase
    apps = supabase.table("applications").select("job_id").execute().data
    jobs = supabase.table("jobs").select("id", "title").execute().data

    job_titles = {job["id"]: job["title"] for job in jobs}
    counts = defaultdict(int)

    for app in apps:
        job_id = app.get("job_id")
        if job_id:
            counts[job_id] += 1

    result = [
        {"job": job_titles.get(jid, "Unknown"), "applications": count}
        for jid, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)
    ]

    return jsonify(result[:10]), 200


@dashboard_bp.route("/dashboard/application-progression", methods=["GET"])#used
def get_application_progression():
    result = {
        "applied": 100,
        "shortlisted_round1": 50,
        "shortlisted_round2": 62,
        "hired": 1
    }
    return jsonify(result), 200

@dashboard_bp.route("/offers/applications/by-recruiter/<recruiter_id>", methods=["GET"])
def get_offers_applications_by_recruiter(recruiter_id):
    offers = []
    for i in range(20):
        applications = []
        matched_count = 0
        for j in range(14):
            is_matched = j < 10
            status = "matched" if is_matched else "screened"
            if is_matched:
                matched_count += 1
            applications.append({
                "application_id": f"app-{i+1}-{j+1}",
                "appliedDate": f"2025-06-{(j%28)+1:02d}T10:00:00",
                "candidate": {
                    "created_at": f"2025-05-{10+(j%20):02d}T10:00:00",
                    "cv_url": f"cv{i+1}{j+1}.pdf",
                    "email": f"user{i+1}{j+1}@email.com",
                    "full_name": f"User {i+1}-{j+1}",
                    "id": f"candidate-{i+1}-{j+1}",
                    "phone": f"06{j+1:08d}"
                },
                "candidate_profile": {
                    "candidate_id": f"candidate-{i+1}-{j+1}",
                    "context_score": 90 if is_matched else 80,
                    "cv_path": f"cv{i+1}{j+1}.pdf",
                    "education": {
                        "degree": "Master" if is_matched else "Licence",
                        "institution": f"University {chr(65+i)}"
                    },
                    "experience": {
                        "level": "Senior" if is_matched else "Junior",
                        "years": 5 if is_matched else 2
                    },
                    "id": f"profile-{i+1}-{j+1}",
                    "location": "Paris" if is_matched else "Lyon",
                    "skills": ["Python", "Flask"] if is_matched else ["JavaScript", "React"],
                    "skills_score": 95 if is_matched else 80,
                    "source": "platform",
                    "updated_at": f"2025-06-{(j%28)+1:02d}T10:00:00"
                },
                "score": 95 if is_matched else 80,
                "status": status,
                "interviewDate": f"2025-06-{10+(j%20):02d}T14:00:00" if is_matched else None
            })
        offer = {
            "applicants": 14,
            "applications": applications,
            "company_id": f"company-{i+1}",
            "contract_type": "Temps plein",
            "created_at": "2025-06-17T14:03:15.723719",
            "deadline": "2025-07-17",
            "description": f"Développeur Backend Senior {i+1}...",
            "education": "Licence",
            "experience": "2 ans",
            "file_url": None,
            "id": f"job-{i+1}",
            "location": "À distance",
            "matched": matched_count,
            "requirements": [
                "Emplacement : Paris",
                "France",
                "Exigences :",
                "Python",
                "Flask"
            ],
            "salary": 48000 + i * 1000,
            "title": f"Développeur Backend Senior {i+1}"
        }
        offers.append(offer)
    return jsonify(offers)