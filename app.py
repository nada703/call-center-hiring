
from flask import Flask, request, redirect, render_template_string
from urllib.parse import quote
import os

app = Flask(__name__)

HOME_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Call Center Opportunities</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; }
        body { background: #f5f5f5; color: #111; }
        .hero {
            min-height: 100vh; background: #000; color: white;
            display: flex; align-items: center; justify-content: center;
            text-align: center; padding: 30px;
        }
        .content { max-width: 800px; }
        .badge {
            display: inline-block; border: 1px solid white; padding: 8px 16px;
            border-radius: 30px; font-size: 13px; letter-spacing: 1px; margin-bottom: 25px;
        }
        h1 { font-size: 55px; line-height: 1.1; margin-bottom: 20px; }
        .hero p { color: #ccc; font-size: 18px; line-height: 1.6; margin-bottom: 30px; }
        .companies { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-bottom: 35px; }
        .company { border: 1px solid #333; background: #111; padding: 10px 16px; border-radius: 8px; color: white; font-size: 14px; }
        .apply-btn {
            display: inline-block; background: white; color: black; padding: 16px 35px;
            border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 16px; transition: .3s;
        }
        .apply-btn:hover { transform: translateY(-2px); background: #ddd; }
        .footer-text { margin-top: 25px; font-size: 13px; color: #777; }
        @media (max-width: 600px) { h1 { font-size: 38px; } .hero p { font-size: 16px; } }
    </style>
</head>
<body>
<section class="hero">
    <div class="content">
        <div class="badge">NOW HIRING</div>
        <h1>Call Center Opportunities</h1>
        <p>
            Interested in Call Center jobs?
            Tell us what you're looking for and we'll contact you regarding suitable opportunities.
        </p>
        <div class="companies">
            <div class="company">Teleperformance</div>
            <div class="company">Concentrix</div>
            <div class="company">eClerx</div>
            <div class="company">TTEC</div>
        </div>
        <a href="/apply" class="apply-btn">Apply Now →</a>
        <div class="footer-text">Fast recruitment • Multiple locations • Call Center opportunities</div>
    </div>
</section>
</body>
</html>
"""

APPLY_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apply Now</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; }
        body { background: #f5f5f5; color: #111; }
        .header { background: #000; color: white; text-align: center; padding: 45px 20px; }
        .header h1 { font-size: 38px; margin-bottom: 10px; }
        .header p { color: #ccc; }
        .container { max-width: 750px; margin: 45px auto; padding: 0 20px; }
        .card { background: white; padding: 40px; border-radius: 18px; box-shadow: 0 10px 35px rgba(0,0,0,.08); }
        .card h2 { font-size: 28px; margin-bottom: 8px; }
        .subtitle { color: #777; margin-bottom: 30px; line-height: 1.6; }
        .form-group { margin-bottom: 25px; }
        label.main-label { display:block; font-size:14px; font-weight:bold; margin-bottom:10px; }
        input[type="text"], input[type="tel"], select {
            width:100%; padding:14px; border:1px solid #ddd; border-radius:10px;
            font-size:15px; outline:none; background:white;
        }
        input:focus, select:focus { border-color:#000; }
        .company-options, .radio-options { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
        .company-option, .radio-option {
            border:1px solid #ddd; padding:15px; border-radius:10px; cursor:pointer;
        }
        .company-option:hover, .radio-option:hover { border-color:#000; background:#fafafa; }
        .company-option input, .radio-option input { margin-right:8px; }
        .submit-btn {
            width:100%; padding:16px; border:none; border-radius:10px;
            background:#000; color:white; font-size:16px; font-weight:bold; cursor:pointer;
        }
        .submit-btn:hover { background:#222; }
        .back { display:block; text-align:center; margin-top:20px; color:#555; text-decoration:none; font-size:14px; }
        .note { text-align:center; color:#888; font-size:13px; margin-top:15px; line-height:1.5; }
        @media (max-width:600px) {
            .card { padding:25px 20px; }
            .company-options, .radio-options { grid-template-columns:1fr; }
            .header h1 { font-size:32px; }
        }
    </style>
</head>
<body>
<div class="header">
    <h1>Apply Now</h1>
    <p>Call Center Recruitment Form</p>
</div>

<div class="container">
    <div class="card">
        <h2>Tell Us About Yourself</h2>
        <p class="subtitle">
            Fill in your details and select the opportunities you're interested in.
        </p>

        <form method="POST" onsubmit="return validateForm()">
            <div class="form-group">
                <label class="main-label">Full Name *</label>
                <input type="text" name="name" placeholder="Enter your full name" required>
            </div>

            <div class="form-group">
                <label class="main-label">Mobile Number *</label>
                <input type="tel" name="phone" placeholder="01XXXXXXXXX"
                       pattern="[0-9]{11}" maxlength="11" inputmode="numeric" required>
            </div>

            <div class="form-group">
                <label class="main-label">Which companies are you interested in? *</label>
                <div class="company-options">
                    <label class="company-option"><input type="checkbox" name="companies" value="Teleperformance">Teleperformance</label>
                    <label class="company-option"><input type="checkbox" name="companies" value="Concentrix">Concentrix</label>
                    <label class="company-option"><input type="checkbox" name="companies" value="eClerx">eClerx</label>
                    <label class="company-option"><input type="checkbox" name="companies" value="TTEC">TTEC</label>
                </div>
            </div>

            <div class="form-group">
                <label class="main-label">Are you a graduate? *</label>
                <div class="radio-options">
                    <label class="radio-option"><input type="radio" name="graduation" value="Graduate" required>Yes, I'm a graduate</label>
                    <label class="radio-option"><input type="radio" name="graduation" value="Not Graduate">No, I'm not a graduate</label>
                </div>
            </div>

            <div class="form-group">
                <label class="main-label">Preferred Location *</label>
                <select name="location" required>
                    <option value="">Select location</option>
                    <option value="6 October">6 October</option>
                    <option value="New Cairo">New Cairo</option>
                    <option value="5th Settlement">5th Settlement</option>
                    <option value="Maadi">Maadi</option>
                    <option value="Nasr City">Nasr City</option>
                </select>
            </div>

            <button type="submit" class="submit-btn">Submit & Continue to WhatsApp</button>

            <p class="note">
                After submitting, WhatsApp will open with your information prepared in a message.
            </p>

            <a href="/" class="back">← Back to Home</a>
        </form>
    </div>
</div>

<script>
function validateForm() {
    const companies = document.querySelectorAll('input[name="companies"]:checked');
    if (companies.length === 0) {
        alert("Please select at least one company.");
        return false;
    }
    return true;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_PAGE)

@app.route("/apply", methods=["GET", "POST"])
def apply():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        companies = request.form.getlist("companies")
        graduation = request.form.get("graduation", "").strip()
        location = request.form.get("location", "").strip()

        companies_text = ", ".join(companies)

        message = f"""🚨 NEW CALL CENTER APPLICANT

━━━━━━━━━━━━━━━━━━

👤 Name:
{name}

📱 Phone:
{phone}

🏢 Interested Companies:
{companies_text}

🎓 Graduation Status:
{graduation}

📍 Preferred Location:
{location}

━━━━━━━━━━━━━━━━━━
New applicant from the hiring form.
"""

        whatsapp_number = "2010909466660"
        whatsapp_url = (
            f"https://wa.me/{whatsapp_number}"
            f"?text={quote(message)}"
        )

        return redirect(whatsapp_url)

    return render_template_string(APPLY_PAGE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
