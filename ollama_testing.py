import ollama
contents = [
    # --- Fresher Tech (30) ---
    "We are hiring a Graduate Software Engineer with knowledge of Python and Java. Freshers encouraged to apply.",
    "Looking for an Entry Level Data Analyst to join our analytics team. No prior experience required.",
    "Junior Web Developer position available for new graduates with HTML, CSS, JavaScript skills.",
    "Hiring Fresher Backend Developer, knowledge of Node.js and MongoDB preferred.",
    "Graduate Engineer Trainee in Machine Learning. Candidates with 0-1 year of experience can apply.",
    "Associate Software Engineer role for campus hires. Training will be provided.",
    "Entry-level Full Stack Developer opportunity for fresh graduates skilled in MERN stack.",
    "We need a Junior Android Developer. Recent CS graduates are eligible.",
    "Looking for Fresher DevOps Engineer. Basic cloud knowledge required.",
    "Hiring Graduate QA Tester. Freshers with attention to detail can apply.",
    "Trainee Data Engineer role, suitable for recent graduates in computer science.",
    "Junior Security Analyst opening for candidates with 0-1 year experience.",
    "Entry-level Game Developer role for passionate freshers with Unity or Unreal knowledge.",
    "Graduate Trainee – Software Testing, ideal for freshers with basic programming knowledge.",
    "Junior Database Developer required. SQL knowledge must. Freshers eligible.",
    "Entry Level Python Developer with problem solving skills. Freshers can apply.",
    "Graduate Cloud Engineer Trainee for AWS and Azure. Recent grads welcome.",
    "Hiring Associate iOS Developer, 0-1 year experience preferred.",
    "Fresher Java Developer role with training program included.",
    "Junior ML Engineer position for CS freshers interested in AI/ML.",
    "Graduate Trainee – Business Intelligence Developer. Freshers with SQL and PowerBI preferred.",
    "Hiring Entry Level Automation Tester with scripting skills. Freshers encouraged.",
    "Junior Frontend Developer opening. Fresh graduates with React knowledge can apply.",
    "Graduate Cybersecurity Associate. Training program provided. Freshers only.",
    "Entry-level Blockchain Developer opportunity for motivated fresh graduates.",
    "Junior Embedded Systems Engineer role for fresh electronics/computer grads.",
    "Graduate Software Support Engineer with exposure to Linux. Fresher role.",
    "Hiring Trainee Big Data Engineer. Recent graduates in IT/CS preferred.",
    "Junior UI Developer for graduates skilled in design and HTML/CSS/JS.",
    "Entry-level Site Reliability Engineer role for tech freshers."
    
    # --- Experienced Tech (20) ---
    , "We are hiring a Senior Data Scientist with 6+ years of experience in ML and AI solutions.",
    "Principal Software Engineer required with expertise in distributed systems and 10 years of coding experience.",
    "Hiring a Lead DevOps Engineer with 8 years of cloud automation experience.",
    "Looking for a Technical Architect with 12 years in enterprise software solutions.",
    "Senior Backend Developer role requiring 7 years of Node.js and database expertise.",
    "Data Engineering Manager with at least 9 years of industry experience.",
    "Hiring a Senior Full Stack Developer with 6-8 years of experience.",
    "Lead iOS Developer role for candidates with over 7 years of mobile app experience.",
    "Technical Program Manager with 10 years in software delivery projects.",
    "Senior Security Consultant required with 8+ years in cybersecurity audits.",
    "Cloud Solutions Architect with minimum 12 years of IT experience.",
    "Lead QA Automation Engineer, 7 years of experience required.",
    "Hiring Senior AI Engineer with 6+ years of applied ML research experience.",
    "Principal Frontend Engineer role, 10 years in React/Angular ecosystems.",
    "Senior Database Administrator with at least 9 years of SQL and NoSQL expertise.",
    "Hiring Senior DevOps Specialist with 7 years of infrastructure automation experience.",
    "Lead Data Scientist position requiring 8 years in predictive analytics.",
    "Technical Lead Software Engineer with 10 years of system design background.",
    "Engineering Director role with 15 years in product development.",
    "Senior Software Engineering Manager with 12+ years of experience."
    
    # --- Fresher Non-Tech (25) ---
    , "We are hiring an HR Intern. Fresh graduates in management or psychology can apply.",
    "Looking for a Business Analyst Intern to assist with reports. Fresher role.",
    "Junior Operations Associate position for recent graduates in any discipline.",
    "Graduate Management Trainee role in Finance and Operations.",
    "Hiring Fresher Sales Associate with strong communication skills.",
    "Trainee Customer Support Executive, no prior experience required.",
    "Entry-level HR Coordinator role. Fresh graduates welcome.",
    "We are hiring a Marketing Intern for digital campaigns. Fresher opportunity.",
    "Graduate Trainee – Supply Chain Management. Freshers encouraged.",
    "Hiring Junior Recruiter role for campus graduates.",
    "Entry-level Business Operations Analyst. Suitable for freshers.",
    "Graduate Admin Associate with strong organizational skills. Fresher job.",
    "We are hiring a Junior Data Entry Executive. Fresh graduates can apply.",
    "Trainee Finance Analyst position. 0-1 year experience accepted.",
    "Entry-level Market Research Intern role. Fresh graduates encouraged.",
    "Junior HR Associate for recent MBA/HR graduates.",
    "Hiring Fresher Content Writer for social media campaigns.",
    "Graduate Trainee – Procurement Operations. Freshers welcome.",
    "Entry-level Customer Relationship Associate. Fresher profile accepted.",
    "Hiring a Junior Logistics Coordinator role. Freshers eligible.",
    "Graduate Event Coordinator trainee program for freshers.",
    "Entry-level Sales Trainee position. Suitable for new graduates.",
    "Junior HR Trainee required for recruitment support. Fresher opportunity.",
    "Graduate Trainee – Business Process Associate. Freshers accepted.",
    "Hiring Entry-level Operations Executive role for recent graduates."
    
    # --- Experienced Non-Tech (25) ---
    , "We are hiring an HR Manager with 7+ years of experience in employee relations.",
    "Senior Business Consultant role with 10 years of experience.",
    "Looking for an Operations Lead with 8 years in supply chain management.",
    "Hiring Senior Financial Analyst with at least 6 years of corporate finance experience.",
    "Marketing Manager position requiring 7 years of digital marketing expertise.",
    "HR Business Partner role, 8+ years of talent management experience required.",
    "Looking for a Senior Customer Success Manager with 9 years in client management.",
    "Hiring Senior Recruiter with 7 years of hiring experience.",
    "We are hiring a Supply Chain Manager with 10+ years of logistics experience.",
    "Senior Project Manager role requiring 12 years of experience.",
    "HR Director position, 15 years of experience mandatory.",
    "Hiring Senior Operations Consultant with 8 years of domain expertise.",
    "Looking for a Principal Financial Consultant with 12 years of experience.",
    "Senior Marketing Strategist with 7 years of branding experience.",
    "Business Process Manager role requiring 9 years of management experience.",
    "Senior HR Consultant with at least 10 years of experience.",
    "Hiring a Senior Policy Analyst with 6 years in government advisory.",
    "Senior Operations Manager role with 12+ years of experience.",
    "Looking for an Experienced Compliance Manager with 9 years background.",
    "Hiring Senior Business Analyst with 8 years of experience.",
    "HR Operations Head role requiring 15 years of experience.",
    "Principal Management Consultant with 12+ years in corporate advisory.",
    "Senior Procurement Manager with at least 8 years of experience.",
    "Looking for a Senior Event Manager with 7 years of professional experience.",
    "Hiring Senior Sales Director with 15 years in global markets."
]

fresh_keywords = [
"fresher", "0-1 year", "graduate", "entry level",
"trainee", "junior", "associate", "new grad", "campus hire"
]

tech_keywords = [
"developer", "engineer", "data analyst", "scientist",
"software", "frontend", "backend", "full stack", "machine learning","B.Tech", "B.E","data science", "AI", "artificial intelligence", "ML", "machine learning", "C++", "Java", "Python", "JavaScript", "Node.js", "React", "Angular", "SQL", "NoSQL", "DevOps", "cloud computing", "cybersecurity", "blockchain", "embedded systems"
]

def classify_job(description: str) -> str:
    text = description.lower()
    
    is_tech = any(word in text for word in tech_keywords)
    is_fresh = any(word in text for word in fresh_keywords)

    if is_tech and is_fresh:
        return "Yes"
    return "No"


for i, content in enumerate(contents):
    print(i,': ',classify_job(content),'\n')
