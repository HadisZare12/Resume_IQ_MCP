import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_linkedin_jobs, fetch_xing_jobs

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeIQ · Career Intelligence",
    page_icon="⬡",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,700&family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: #12121a !important;
    color: #e8e4dc !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"]    { display: none; }
[data-testid="stToolbar"]    { display: none; }
[data-testid="stDecoration"] { display: none; }

/* ── Center the whole layout ── */
.main .block-container {
    max-width: 780px !important;
    padding: 2rem 1.5rem 5rem !important;
    margin: 0 auto !important;
}

/* ── Hero ── */
.riq-hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
}
.riq-badge { font-family: 'DM Sans' !important;
    display: inline-block;
    font-family: 'Playfair Display';
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #d4c06a;
    border: 1px solid rgba(212,192,106,0.3);
    border-radius: 100px;
    padding: 0.35rem 1.1rem;
    margin-bottom: 1.5rem;
}
.riq-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.8rem, 6vw, 4.5rem) !important;
    font-weight: 800 !important;
    line-height: 1.05 !important;
    letter-spacing: -0.03em !important;
    color: #f0ece2 !important;
    margin-bottom: 1rem !important;
}
.riq-title span { color: #d4c06a; }
.riq-sub p {
    font-size: 1rem;
    font-weight: 300;
    color: #a09a90;
    max-width: 400px;
    margin: 0 auto 2rem; 
    line-height: 1.65;
}
.riq-divider {
    width: 36px;
    height: 2px;
    background: #d4c06a;
    margin: 0 auto 2.5rem;
    border-radius: 2px;
}

/* ── File uploader ── */
[data-testid="stFileUploaderDropzone"] {
    background: #1c1c28 !important;
    border: 1.5px dashed #3a3a50 !important;
    border-radius: 14px !important;
    transition: border-color 0.25s, background 0.25s !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(212,192,106,0.5) !important;
    background: #20202e !important;
}
[data-testid="stFileUploaderDropzone"] svg { color: #d4c06a !important; }
[data-testid="stFileUploaderDropzoneInstructions"] p {
    color: #8a8680 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    color: #a09a90 !important;
    font-size: 0.88rem;
}

/* ── Success ── */
[data-testid="stAlert"] {
    background: #162016 !important;
    border: 1px solid #2e5a2e !important;
    border-radius: 10px !important;
    color: #80d080 !important;
}

/* ── Cards ── */
.riq-card {
    background: #1e1e2e;
    border: 1px solid #2e2e42;
    border-radius: 18px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.riq-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 18px 18px 0 0;
}
.riq-card.summary::before { background: linear-gradient(90deg, #d4c06a, #ead880); }
.riq-card.gaps::before    { background: linear-gradient(90deg, #e07a5a, #d4614a); }
.riq-card.roadmap::before { background: linear-gradient(90deg, #6a9fe0, #5a8fd4); }
.riq-card.jobs::before    { background: linear-gradient(90deg, #6abf7a, #50af62); }

.riq-card-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.2rem;
}
.riq-icon {
    width: 36px; height: 36px;
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.icon-gold  { background: rgba(212,192,106,0.15); color: #d4c06a; }
.icon-red   { background: rgba(224,122, 90,0.15); color: #e07a5a; }
.icon-blue  { background: rgba(106,159,224,0.15); color: #6a9fe0; }
.icon-green { background: rgba(106,191,122,0.15); color: #6abf7a; }

.riq-card-meta { line-height: 1.3; }
.riq-card-label {
    font-family: 'Playfair Display', serif;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7a7670;
    margin-bottom: 0.15rem;
}
.riq-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #f0ece2;
}
.riq-card-body {
    font-size: 0.94rem;
    line-height: 1.78;
    color: #ccc8be;
    font-weight: 300;
}
.riq-card-body strong { color: #e8e4dc; font-weight: 500; }

/* ── Button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #d4c06a, #ead880) !important;
    color: #0a0a10 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 100px !important;
    padding: 0.8rem 2.2rem !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 0 24px rgba(212,192,106,0.2) !important;
}
div[data-testid="stButton"] > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}

/* ── Platform badges ── */
.riq-platform-row {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.2rem;
}
.riq-badge-pill {
    font-family: 'Playfair Display', serif;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.28rem 0.8rem;
    border-radius: 100px;
    border: 1px solid;
}
.pill-li { color: #6aaee0; border-color: rgba(106,174,224,0.4); background: rgba(106,174,224,0.1); }
.pill-xi { color: #6abf7a; border-color: rgba(106,191,122,0.4); background: rgba(106,191,122,0.1); }

/* ── Job rows ── */
.riq-job-list { display: flex; flex-direction: column; gap: 0.65rem; }
.riq-job-row {
    background: #181826;
    border: 1px solid #28283a;
    border-radius: 11px;
    padding: 0.85rem 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.9rem;
    transition: border-color 0.2s;
}
.riq-job-row:hover { border-color: #3a3a52; }
.riq-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
}
.dot-li { background: #6aaee0; }
.dot-xi { background: #6abf7a; }
.riq-job-info { flex: 1; min-width: 0; }
.riq-job-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.88rem;
    font-weight: 700;
    color: #f0ece2;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.riq-job-sub {
    font-size: 0.76rem;
    color: #8a8680;
    margin-top: 0.12rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.riq-job-btn {
    font-family: 'Playfair Display', serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-decoration: none;
    padding: 0.3rem 0.75rem;
    border-radius: 100px;
    border: 1px solid;
    white-space: nowrap;
    flex-shrink: 0;
    transition: opacity 0.2s;
}
.riq-job-btn:hover { opacity: 0.65; }
.btn-li { color: #6aaee0; border-color: rgba(106,174,224,0.45); }
.btn-xi { color: #6abf7a; border-color: rgba(106,191,122,0.45); }

/* ── Footer ── */
.riq-footer {
    text-align: center;
    padding: 3rem 0 1rem;
    font-size: 0.75rem;
    color: #4a4845;
    letter-spacing: 0.06em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: result card ───────────────────────────────────────────────────────
def result_card(variant, icon, icon_cls, label, title, content):
    st.markdown(f"""
    <div class="riq-card {variant}">
        <div class="riq-card-header">
            <div class="riq-icon {icon_cls}">{icon}</div>
            <div class="riq-card-meta">
                <div class="riq-card-label">{label}</div>
                <div class="riq-card-title">{title}</div>
            </div>
        </div>
        <div class="riq-card-body">{content}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="riq-hero">
    <div class="riq-badge">⬡ &nbsp; Career Intelligence Platform</div>
    <!-- <h1 class="riq-title">Your Resume,<br><span>Decoded.</span></h1> -->
            <h1 class="riq-title">Resume<span>IQ</span></h1>
    <div class="riq-sub"><p>Upload your CV and get an instant AI-powered breakdown — skills, gaps, and a personalised career roadmap.</p></div>
    <div class="riq-divider"></div>
</div>
""", unsafe_allow_html=True)


# ── Upload ────────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Drop your resume here",
    type=["pdf"],
    label_visibility="collapsed",
)


# ── Processing ────────────────────────────────────────────────────────────────
if uploaded_file:

    with st.spinner("Extracting text from your resume…"):
        resume_text = extract_text_from_pdf(uploaded_file)
    st.success("✓  Text extracted successfully.")

    with st.spinner("Summarising your profile…"):
        summary = ask_openai(
            f"Summarize this resume highlighting the skills, education and experiences: {resume_text}",
            max_tokens=500,
        )

    with st.spinner("Identifying skill gaps…"):
        analyze = ask_openai(
            f"Analyze this resume and highlight missing skills, certifications and experiences needed for better job opportunities: {resume_text}",
            max_tokens=400,
        )

    with st.spinner("Charting your roadmap…"):
        roadmap = ask_openai(
            f"Based on this resume, suggest the future roadmap to improve this person's chances to get the job (skills to learn, certifications needed): {resume_text}",
            max_tokens=500,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    result_card("summary", "◈", "icon-gold",  "Profile Overview",   "Resume Summary",                  content=summary.replace("\n", "<br>"))
    result_card("gaps",    "◉", "icon-red",   "Gap Analysis",       "Missing Skills & Certifications", content=analyze.replace("\n", "<br>"))
    result_card("roadmap", "◎", "icon-blue",  "Action Plan",        "Your Career Roadmap",             content=roadmap.replace("\n", "<br>"))

    # ── Job Recommendation ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬡  Get Job Recommendations", use_container_width=True):

        with st.spinner("Identifying best-fit job title…"):
            keyword = ask_openai(
                f"Based on this resume, reply with ONLY a short job title keyword (2-4 words) for a LinkedIn search. No explanation, no punctuation: {resume_text}",
                max_tokens=20,
            ).strip().strip('"').strip("'")

        with st.spinner(f'Searching LinkedIn for "{keyword}"…'):
            linkedin_raw = fetch_linkedin_jobs(search_query=keyword, location="germany", rows=60) or []

        with st.spinner("Fetching Technology roles from Xing Germany…"):
            xing_raw = fetch_xing_jobs(location="germany") or []

        st.markdown("<br>", unsafe_allow_html=True)

        def li_html(job):
            title   = job.get("title")       or job.get("jobTitle")    or "Untitled Role"
            company = job.get("companyName") or job.get("company")     or ""
            loc     = job.get("location")    or job.get("jobLocation") or ""
            url     = job.get("jobUrl")      or job.get("url")         or "#"
            sub     = " · ".join(filter(None, [company, loc]))
            sub_row = f'<div class="riq-job-sub">{sub}</div>' if sub else ""
            return f"""<div class="riq-job-row">
                <div class="riq-dot dot-li"></div>
                <div class="riq-job-info">
                    <div class="riq-job-title">{title}</div>{sub_row}
                </div>
                <a class="riq-job-btn btn-li" href="{url}" target="_blank">View ↗</a>
            </div>"""

        def xi_html(job):
            title   = job.get("title")    or job.get("job_title")    or "Untitled Role"
            company = job.get("company")  or job.get("company_name") or ""
            loc     = job.get("location") or job.get("city")         or "Germany"
            url     = job.get("url")      or job.get("job_url")      or "#"
            sub     = " · ".join(filter(None, [company, loc]))
            sub_row = f'<div class="riq-job-sub">{sub}</div>' if sub else ""
            return f"""<div class="riq-job-row">
                <div class="riq-dot dot-xi"></div>
                <div class="riq-job-info">
                    <div class="riq-job-title">{title}</div>{sub_row}
                </div>
                <a class="riq-job-btn btn-xi" href="{url}" target="_blank">View ↗</a>
            </div>"""

        li_block = "".join(li_html(j) for j in linkedin_raw) if linkedin_raw else \
            '<p style="color:#6a6865;font-size:0.84rem;padding:0.4rem 0">No LinkedIn results found.</p>'
        xi_block = "".join(xi_html(j) for j in xing_raw) if xing_raw else \
            '<p style="color:#6a6865;font-size:0.84rem;padding:0.4rem 0">No Xing results found.</p>'

        total = len(linkedin_raw) + len(xing_raw)

        st.markdown(f"""
        <div class="riq-card jobs">
            <div class="riq-card-header">
                <div class="riq-icon icon-green">◐</div>
                <div class="riq-card-meta">
                    <div class="riq-card-label">Live listings · {total} found</div>
                    <div class="riq-card-title">Jobs matching "{keyword}"</div>
                </div>
            </div>
            <div class="riq-platform-row">
                <span class="riq-badge-pill pill-li">⬡ LinkedIn · {len(linkedin_raw)}</span>
                <span class="riq-badge-pill pill-xi">⬡ Xing · {len(xing_raw)}</span>
            </div>
            <div class="riq-job-list">
                {li_block}
                {xi_block}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="riq-footer">ResumeIQ · Powered by Groq Llama 3 &nbsp;·&nbsp; Your data is never stored</div>',
    unsafe_allow_html=True,
)