# Full working ContractAI Streamlit app

import streamlit as st
import requests
import os
import tempfile


# CONFIGURATION
API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

CONTRACT_TYPES = {
    "NDA (Non-Disclosure Agreement)": "Draft a detailed, mutual NDA...",
    "Service Agreement": "Draft a Service Agreement...",
    "Employment Agreement": "Draft an Employment Agreement...",
    "Founder Agreement": "Draft a Founder Agreement...",
    "Consultancy Agreement": "Draft a Consultancy Agreement..."
}

TEMPLATES = {
    "NDA (Non-Disclosure Agreement)": ("Mob Makers Pvt. Ltd.", "Cartel Clothing Co.", "Both Companies", "India", 
        "1. Confidential Information includes all disclosed data.\n2. Parties agree to protect it for 3 years."),
    "Service Agreement": ("Alpha Design Studio", "Zed Tech Ltd.", "Freelancer & Client", "United States", 
        "1. Scope includes design and branding.\n2. Payment in two milestones.")
}

CLAUSE_EXPLANATIONS = {
    "Include IP Ownership Clause": "Ensures IP ownership.",
    "Include Arbitration/Dispute Clause": "Dispute resolution via arbitration.",
    "Include Termination Clause": "Grounds to end the agreement.",
    "Include Confidentiality Clause": "Protects sensitive information.",
    "Add Signature Section": "Adds signatory section."
}

# STREAMLIT UI
st.set_page_config(page_title="ContractAI - GPT for Contracts", layout="centered")
st.title("📜 ContractAI: GPT-Powered Contract Generator")

st.markdown("""
### 🪄 Step 1: Select Contract & Parties
Choose contract type, parties & jurisdiction.

### ⚙️ Step 2: Customize Clauses
Select and edit optional clauses.

### 📩 Step 3: Generate & Download
Generate your contract with risk analysis and PDF export.
""")

with st.form("contract_form"):
    contract_type = st.selectbox("Contract type:", list(CONTRACT_TYPES.keys()))
    use_template = st.checkbox("Use pre-filled template")

    if use_template:
        default_a, default_b, default_party_type, default_jurisdiction, clause_preview = TEMPLATES.get(contract_type, ("", "", "Both Companies", "India", ""))
        st.text_area("📑 Template preview", clause_preview, height=100, disabled=True)
    else:
        default_a, default_b, default_party_type, default_jurisdiction, clause_preview = ("", "", "Both Companies", "India", "")

    party_a = st.text_input("Party A", value=default_a)
    party_b = st.text_input("Party B", value=default_b)
    party_type = st.selectbox("Relationship Type:", ["Both Companies", "One Company & One Individual", "Freelancer & Client", "Partnership", "Other"],
                              index=["Both Companies", "One Company & One Individual", "Freelancer & Client", "Partnership", "Other"].index(default_party_type))
    if party_type == "Other":
        party_type = st.text_input("Custom Relationship Type")

    jurisdiction = st.selectbox(
    "Jurisdiction:",
    ["United States", "India", "United Kingdom", "Singapore", "Germany", "Other"],
    index=["United States", "India", "United Kingdom", "Singapore", "Germany", "Other"].index(default_jurisdiction)
    )

    if jurisdiction == "Other":
        jurisdiction = st.text_input("Custom Jurisdiction")


    term = st.number_input("Contract Duration (years)", min_value=1, max_value=10, value=1)

    st.subheader("Optional Clauses")
    include_ip = st.checkbox("Include IP Ownership Clause")
    ip_text = st.text_area("Custom IP Clause", "", height=80) if include_ip else ""

    include_dispute = st.checkbox("Include Arbitration/Dispute Clause")
    dispute_text = st.text_area("Custom Dispute Clause", "", height=80) if include_dispute else ""

    include_termination = st.checkbox("Include Termination Clause")
    termination_text = st.text_area("Custom Termination Clause", "", height=80) if include_termination else ""

    include_confidentiality = st.checkbox("Include Confidentiality Clause")
    confidentiality_text = st.text_area("Custom Confidentiality Clause", "", height=80) if include_confidentiality else ""

    include_signature = st.checkbox("Add Signature Section")

    submit = st.form_submit_button("⚖️ Generate Contract")

# GENERATE
if submit:
    st.info("⏳ Generating contract...")

    clause_list = ""
    if include_ip: clause_list += f"- IP Ownership Clause: {ip_text}\n" if ip_text else "- IP Ownership Clause\n"
    if include_dispute: clause_list += f"- Arbitration/Dispute Clause: {dispute_text}\n" if dispute_text else "- Arbitration/Dispute Clause\n"
    if include_termination: clause_list += f"- Termination Clause: {termination_text}\n" if termination_text else "- Termination Clause\n"
    if include_confidentiality: clause_list += f"- Confidentiality Clause: {confidentiality_text}\n" if confidentiality_text else "- Confidentiality Clause\n"
    if include_signature: clause_list += "- Signature Section\n"

    prompt = f"""You are a senior legal contract drafter specializing in startup, technology, and creative services agreements.

You are tasked with drafting a complete, enforceable **{contract_type}** between:

- **Party A**: {party_a}
- **Party B**: {party_b}
- **Relationship Type**: {party_type}
- **Jurisdiction**: {jurisdiction}
- **Contract Term**: {term} year(s)

The final agreement must follow a clear **clause-by-clause legal structure** using professional formatting and enforceable legal language. Use defined clause headings and maintain legal precision.

### 🔐 Mandatory Clauses (Structure)
Include the following *at a minimum* (based on agreement type): 1. Title and Introduction
2. Definitions and Interpretation
3. Scope of Work / Employment / Services
4. Duties and Obligations of Parties
5. Compensation and Payment Terms
6. Intellectual Property (if applicable)
7. Confidentiality
8. Term and Termination
9. Indemnity
10. Force Majeure
11. Non-Solicitation and Non-Compete (if applicable)
12. Dispute Resolution and Governing Law
13. Miscellaneous Clauses (Entire Agreement, Severability, Notices, Waiver)
14. Signature Blocks

Include clause examples from these templates where relevant:

---

### 📌 CLAUSE EXAMPLES TO FOLLOW

**Confidentiality Clause**:
> Both Parties agree to maintain strict confidentiality of all proprietary, technical, or business information disclosed. Neither Party shall disclose such information to third parties without prior written consent.

**Indemnity Clause**:
> The [Client/Employee] shall indemnify and hold harmless the [Agency/Employer] from all losses arising due to breach, misrepresentation, or third-party claims arising from the performance of this agreement.

**Force Majeure**:
> Neither Party shall be liable for delay or failure to perform obligations due to events beyond their control including acts of God, pandemic, governmental orders, or natural calamities.

Termination:
> This agreement may be terminated by giving [30] days written notice after the lock-in period. Immediate termination may occur in case of breach or non-payment.

Non-Compete Clause:
> For a period of [1 year] post-termination, the [Receiving Party/Employee] shall not engage in any business competing directly or indirectly with the [Disclosing Party/Employer].

Assignment of IP (Employment/Service):
> Any intellectual property created during the course of the engagement shall be the sole and exclusive property of the Employer/Client, and the other party agrees to execute any necessary documents to assign such rights.

---

### 🧠 ANALYSIS & COMPLIANCE

After drafting the agreement, provide a structured **Clause Risk Analysis**:

- Highlight risky, one-sided, or ambiguous phrases.
- Use bullet points to explain risks for each major clause.
- Suggest improvements for missing standard clauses.
- Use **bold** for clause names and **red text** to flag risky terms (like "indemnify", "terminate", "waive").

---

### OUTPUT FORMAT

Return output as:
--- CONTRACT TEXT ---
<full draft here with clauses>

--- RISK ANALYSIS ---
<bullet points>

Keep language jurisdiction-appropriate (e.g., Indian law: Arbitration & Conciliation Act, Companies Act 2013, etc.)

Avoid vague placeholders like [insert here]. Fill all with default legal language when blank.
"""

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "You are a legal assistant."},
                {"role": "user", "content": prompt}
            ]
        })

        response_data = res.json()
        if "choices" not in response_data:
            st.error(f"❌ API Error: {response_data}")
        else:
            content = response_data["choices"][0]["message"]["content"]
            contract_part, analysis_part = content.split("RISK/CLAUSE ANALYSIS", 1) if "RISK/CLAUSE ANALYSIS" in content else (content, "")

            # === Contract Output ===
            st.subheader("📄 Contract Text")
            st.text_area("Generated Contract", value=contract_part.strip(), height=400)

            # === Risk & Clause Analysis ===
            st.subheader("🛡️ Risk & Clause Analysis")

            if analysis_part.strip().startswith("---"):
                analysis_part = analysis_part.split("---")[-1].strip()

            risky_keywords = ["indemnify", "liability", "terminate", "breach", "waive", "exclusive", "discretion"]
            for word in risky_keywords:
                analysis_part = analysis_part.replace(word, f"**:red[{word}]**")

            st.markdown(analysis_part, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Error generating contract: {e}")
