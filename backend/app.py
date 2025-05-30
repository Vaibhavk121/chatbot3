# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import joblib
import random
import re

app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication

# Load the trained NLP model
try:
    nlp_model = joblib.load('intent_model.joblib')
    print("NLP intent model loaded successfully.")
except FileNotFoundError:
    print("ERROR: intent_model.joblib not found. Please run train_model.py first. NLP capabilities will be limited.")
    nlp_model = None

# Career Map (Comprehensive data for different fields and interests)
# In backend/app.py or a data file it imports

career_map = {
    "science": {
        "coding": [
            "Software Engineer", "Web Developer", "AI/ML Engineer", "Full Stack Developer",
            "Data Scientist", "Blockchain Developer", "Cybersecurity Analyst", "Game Developer",
            "DevOps Engineer", "Cloud Architect", "Mobile App Developer", "Site Reliability Engineer"
        ],
        "physics": [
            "Physicist", "Aerospace Engineer", "Nuclear Scientist", "Astrophysicist",
            "Quantum Physicist", "Geophysicist", "Medical Physicist", "Acoustics Engineer",
            "Optical Physicist", "Laser Technologist"
        ],
        "biology": [
            "Biologist", "Biochemist", "Geneticist", "Medical Researcher", "Pharmacologist",
            "Marine Biologist", "Microbiologist", "Zoologist", "Botanist", "Ecologist", "Entomologist"
        ],
        "chemistry": [
            "Chemist", "Pharmaceutical Chemist", "Toxicologist", "Forensic Chemist",
            "Analytical Chemist", "Materials Scientist", "Polymer Chemist", "Nanochemist"
        ],
        "mathematics": [
            "Mathematician", "Statistician", "Data Analyst", "Actuary", "Cryptographer",
            "Operations Research Analyst", "Quantitative Researcher", "Mathematical Modeler"
        ],
        "earth science": [
            "Geologist", "Oceanographer", "Meteorologist", "Seismologist", "Climatologist"
        ]
    },
    
    "arts": {
        "design": [
            "UI/UX Designer", "Graphic Designer", "Product Designer", "Animator",
            "Fashion Designer", "Interior Designer", "Game Designer", "3D Modeler",
            "Textile Designer", "Exhibition Designer", "Visual Merchandiser"
        ],
        "writing": [
            "Content Writer", "Journalist", "Editor", "Copywriter", "Author",
            "Technical Writer", "Screenwriter", "Grant Writer", "Blogger", "Novelist"
        ],
        "music": [
            "Musician", "Composer", "Sound Engineer", "Music Teacher", "DJ",
            "Music Therapist", "Recording Engineer", "Choir Director", "Voice Coach"
        ],
        "film": [
            "Film Director", "Actor", "Cinematographer", "Editor", "Producer",
            "Storyboard Artist", "Lighting Technician", "Set Designer", "Film Critic"
        ],
        "performing arts": [
            "Dancer", "Choreographer", "Theatre Actor", "Stage Manager", "Circus Performer"
        ]
    },
    "business": {
        "marketing": [
            "Digital Marketer", "SEO Specialist", "Brand Manager", "PR Specialist",
            "Marketing Analyst", "Growth Hacker", "Affiliate Marketer", "Event Planner"
        ],
        "finance": [
            "Accountant", "Financial Analyst", "Investment Banker", "Auditor",
            "Risk Manager", "Credit Analyst", "Loan Officer", "Portfolio Manager"
        ],
        "entrepreneur": [
            "Startup Founder", "Business Consultant", "Product Manager", "Venture Capitalist",
            "Franchise Owner", "E-commerce Business Owner", "Startup Mentor"
        ],
        "management": [
            "HR Manager", "Operations Manager", "Project Manager", "Retail Manager",
            "Business Analyst", "Supply Chain Manager", "Logistics Coordinator"
        ],
        "sales": [
            "Sales Executive", "Business Development Manager", "Account Executive",
            "Inside Sales Representative", "Sales Operations Analyst"
        ]
    },
    "engineering": {
        "mechanical": [
            "Mechanical Engineer", "Automotive Engineer", "Robotics Engineer", "Product Designer",
            "Mechatronics Engineer", "HVAC Engineer", "Tool Designer", "CAD Engineer"
        ],
        "civil": [
            "Civil Engineer", "Structural Engineer", "Urban Planner", "Surveyor",
            "Construction Manager", "Environmental Engineer", "Geotechnical Engineer"
        ],
        "electrical": [
            "Electrical Engineer", "Electronics Engineer", "Embedded Systems Engineer",
            "Power Systems Engineer", "Control Systems Engineer", "Telecom Engineer"
        ],
        "computer": [ # Note: Some roles here overlap with science->coding. Ensure consistency in role_details.
            "Computer Engineer", "IoT Developer", "Hardware Engineer", "Network Architect",
            "Systems Engineer", "AR/VR Developer", "Software Engineer" # Added for consistency if navigated via Eng->Comp
        ],
        "chemical": [
            "Chemical Engineer", "Petroleum Engineer", "Process Engineer",
            "Materials Engineer", "Energy Engineer", "Biochemical Engineer"
        ],
        "aerospace": [ # Note: "Aerospace Engineer" also in science->physics.
            "Aerospace Engineer", "Avionics Engineer", "Flight Test Engineer", "Spacecraft Systems Engineer"
        ]
    },
    "healthcare": {
        "medicine": [
            "Doctor", "Surgeon", "Dermatologist", "Pediatrician", "Radiologist",
            "Anesthesiologist", "Cardiologist", "Psychiatrist"
        ],
        "allied health": [
            "Nurse", "Pharmacist", "Physiotherapist", "Lab Technician", "Optometrist",
            "Occupational Therapist", "Speech Therapist"
        ],
        "mental health": [
            "Psychologist", "Counselor", "Social Worker", "Therapist", "Clinical Psychologist"
        ],
        "veterinary": [
            "Veterinarian", "Vet Technician", "Animal Behaviorist"
        ]
    },
    "law": {
        "legal practice": [
            "Lawyer", "Legal Advisor", "Corporate Lawyer", "Litigation Attorney",
            "Criminal Lawyer", "Family Lawyer"
        ],
        "judiciary": [
            "Judge", "Court Clerk", "Judicial Assistant"
        ],
        "public service": [
            "Civil Rights Lawyer", "Public Prosecutor", "Legal Aid Worker"
        ]
    },
    "education": {
        "school": [
            "Primary School Teacher", "High School Teacher", "Special Education Teacher",
            "Physical Education Teacher", "Subject Matter Expert"
        ],
        "higher education": [
            "College Professor", "Academic Researcher", "Curriculum Developer",
            "Librarian", "Academic Dean"
        ],
        "training": [
            "Corporate Trainer", "Instructional Designer", "EdTech Consultant"
        ]
    },
    "environment": {
        "ecology": [
            "Environmental Scientist", "Ecologist", "Wildlife Biologist", "Marine Conservationist"
        ],
        "sustainability": [
            "Sustainability Consultant", "Environmental Policy Analyst", "Renewable Energy Specialist",
            "Climate Change Analyst"
        ]
    },
    "sports": {
        "athletics": [
            "Athlete", "Cricketer", "Footballer", "Tennis Player", "Swimmer"
        ],
        "support": [
            "Coach", "Physiotherapist", "Sports Psychologist", "Referee", "Sports Journalist"
        ],
        "fitness": [
            "Personal Trainer", "Fitness Instructor", "Gym Manager", "Yoga Instructor", "Nutritionist"
        ]
    },
    "social sciences": {
        "human behavior": [
            "Sociologist", "Anthropologist", "Political Scientist", "Historian", "Demographer"
        ],
        "public policy": [
            "Policy Analyst", "Urban Planner", "Development Officer", "NGO Manager", "Social Reformer"
        ]
    }
}

# Generate all_roles list (place this after career_map definition in your app.py)
all_roles_list = []
for field_key in career_map:
    for interest_key in career_map[field_key]:
        all_roles_list.extend(career_map[field_key][interest_key])
# Ensure unique roles, sorted by length (desc) for better matching in find_role_in_input
all_roles = sorted(list(set(all_roles_list)), key=len, reverse=True)

# General question templates for roles (used with NLP intent)
specific_role_questions = {
    "get_skills": "To succeed as a {role}, you'll typically need proficiency in {skills}. Key skills include {specific_skills}.",
    "get_daily_tasks": "A typical day for a {role} involves {daily_tasks}. You'll often collaborate with {collaborators} and work on {projects}.",
    "get_how_to_get_into": "To get into {role}, consider pursuing a degree in {degree_suggestion}, gaining practical experience through {experience_suggestion}, and networking with professionals in the field.",
    "get_salary": "The average salary for a {role} varies greatly based on location, experience, and specific company, but typically ranges from {min_salary} to {max_salary} annually in India.",
    "get_education_needed": "For a {role}, an educational background in {degree_suggestion} is usually required. Relevant coursework or certifications in {relevant_courses} would also be beneficial.",
    "get_job_outlook": "The job outlook for {role} is generally {outlook_status} over the next decade, driven by {outlook_reasons}. This suggests {outlook_advice}."
}

# Detailed information for specific roles (add more as needed)
role_details = {
    "Software Engineer": {
        "skills": "programming languages (Python, Java, C++, JavaScript), data structures, algorithms, problem-solving, software development methodologies, version control (Git)",
        "specific_skills": "Python, Java, C++, algorithms, data structures, Git, Agile/Scrum",
        "daily_tasks": "writing, testing, and debugging code; participating in code reviews; collaborating on system design; maintaining existing software",
        "collaborators": "other developers, product managers, QA testers, UI/UX designers",
        "projects": "developing new features, fixing bugs, optimizing performance, integrating APIs",
        "degree_suggestion": "Computer Science, Software Engineering, or a related technical field",
        "experience_suggestion": "internships, personal coding projects, open-source contributions, hackathons",
        "min_salary": "₹5,00,000",
        "max_salary": "₹20,00,000",
        "relevant_courses": "object-oriented programming, web development, database management, cloud computing",
        "outlook_status": "very strong",
        "outlook_reasons": "rapid technological advancements, increased demand for digital services, and ongoing innovation",
        "outlook_advice": "excellent long-term career prospects"
    },
    
  "Biologist": {
    "skills": "biology, lab techniques, data analysis, scientific writing, critical thinking",
    "specific_skills": "microscopy, experimental design, fieldwork, PCR, data interpretation",
    "daily_tasks": "conducting experiments, collecting and analyzing data, preparing reports, publishing research",
    "collaborators": "research assistants, lab technicians, fellow scientists, academic advisors",
    "projects": "studying living organisms, analyzing biological processes, environmental impact studies",
    "degree_suggestion": "Biology, Life Sciences",
    "experience_suggestion": "lab internships, undergraduate research, science fairs, fieldwork",
    "min_salary": "₹3,00,000",
    "max_salary": "₹12,00,000",
    "relevant_courses": "cell biology, genetics, ecology, biostatistics",
    "outlook_status": "strong",
    "outlook_reasons": "growth in environmental, medical, and biotech sectors",
    "outlook_advice": "broad career scope in research, education, and applied science"
  },
  "Biochemist": {
    "skills": "chemistry, biology, lab work, analytical techniques, molecular biology",
    "specific_skills": "chromatography, spectroscopy, protein purification, enzyme assays",
    "daily_tasks": "analyzing chemical processes in living organisms, designing experiments, compiling results",
    "collaborators": "chemists, lab techs, molecular biologists, healthcare researchers",
    "projects": "drug development, metabolic studies, disease mechanism research",
    "degree_suggestion": "Biochemistry, Molecular Biology",
    "experience_suggestion": "lab internships, biotech workshops, pharmaceutical research",
    "min_salary": "₹4,00,000",
    "max_salary": "₹15,00,000",
    "relevant_courses": "organic chemistry, molecular biology, biophysics",
    "outlook_status": "very strong",
    "outlook_reasons": "high demand in healthcare, pharmaceuticals, and research",
    "outlook_advice": "great opportunities in research, diagnostics, and pharma"
  },
  "Geneticist": {
    "skills": "genetics, bioinformatics, lab techniques, data analysis, precision research",
    "specific_skills": "DNA sequencing, PCR, CRISPR, genome editing, data interpretation",
    "daily_tasks": "studying genes and heredity, conducting lab experiments, analyzing genetic data",
    "collaborators": "medical researchers, lab technicians, data analysts, clinicians",
    "projects": "genetic disorder studies, gene therapy, personalized medicine research",
    "degree_suggestion": "Genetics, Biotechnology, Molecular Biology",
    "experience_suggestion": "research labs, genetic counseling internships, academic projects",
    "min_salary": "₹4,50,000",
    "max_salary": "₹18,00,000",
    "relevant_courses": "molecular genetics, genomics, bioinformatics",
    "outlook_status": "very strong",
    "outlook_reasons": "advancements in gene therapy, personalized medicine, and diagnostics",
    "outlook_advice": "excellent future in healthcare and research"
  },
  "Medical Researcher": {
    "skills": "medical knowledge, research methodology, statistics, lab techniques",
    "specific_skills": "clinical trials, literature review, statistical analysis, lab testing",
    "daily_tasks": "designing and conducting studies, analyzing results, writing research papers",
    "collaborators": "doctors, clinicians, biostatisticians, regulatory experts",
    "projects": "drug trials, disease studies, treatment effectiveness evaluations",
    "degree_suggestion": "Biomedical Science, Medicine, Public Health",
    "experience_suggestion": "hospital internships, research fellowships, thesis work",
    "min_salary": "₹5,00,000",
    "max_salary": "₹20,00,000",
    "relevant_courses": "clinical research, epidemiology, pharmacology",
    "outlook_status": "strong",
    "outlook_reasons": "increased healthcare demands and medical innovation",
    "outlook_advice": "highly rewarding for those interested in health advancements"
  },
  "Pharmacologist": {
    "skills": "pharmacology, chemistry, drug interaction knowledge, lab testing",
    "specific_skills": "drug mechanism studies, dose-response analysis, clinical trials",
    "daily_tasks": "studying drug effects, running experiments, analyzing therapeutic responses",
    "collaborators": "pharmacists, biochemists, doctors, regulatory authorities",
    "projects": "drug development, toxicology studies, dosage optimization",
    "degree_suggestion": "Pharmacy, Pharmacology, Biomedical Science",
    "experience_suggestion": "internships in pharma companies, lab projects, clinical research training",
    "min_salary": "₹4,50,000",
    "max_salary": "₹16,00,000",
    "relevant_courses": "toxicology, pharmaceutical chemistry, drug design",
    "outlook_status": "very strong",
    "outlook_reasons": "constant need for drug innovation and testing",
    "outlook_advice": "excellent for those interested in medicine and chemistry"
  },
  "Marine Biologist": {
    "skills": "marine ecosystems, diving, lab work, environmental science, data collection",
    "specific_skills": "SCUBA, water sampling, marine taxonomy, remote sensing",
    "daily_tasks": "studying marine life, conducting field research, analyzing oceanic data",
    "collaborators": "environmental scientists, oceanographers, research divers",
    "projects": "coral reef studies, marine species conservation, pollution impact analysis",
    "degree_suggestion": "Marine Biology, Oceanography, Environmental Science",
    "experience_suggestion": "underwater research programs, internships with marine institutes",
    "min_salary": "₹3,50,000",
    "max_salary": "₹12,00,000",
    "relevant_courses": "marine ecology, aquatic biology, conservation science",
    "outlook_status": "moderate",
    "outlook_reasons": "specialized field with limited positions but high impact",
    "outlook_advice": "ideal for those passionate about oceans and marine life"
  },
  "Microbiologist": {
    "skills": "microbiology, sterile techniques, lab instrumentation, report writing",
    "specific_skills": "culturing microbes, staining, microscopy, antibiotic testing",
    "daily_tasks": "examining microorganisms, performing lab tests, identifying pathogens",
    "collaborators": "doctors, lab techs, public health officers",
    "projects": "disease detection, food safety analysis, industrial microbiology",
    "degree_suggestion": "Microbiology, Biotechnology",
    "experience_suggestion": "lab internships, public health projects, food testing labs",
    "min_salary": "₹3,00,000",
    "max_salary": "₹10,00,000",
    "relevant_courses": "bacteriology, virology, immunology",
    "outlook_status": "strong",
    "outlook_reasons": "importance in healthcare, food, and research sectors",
    "outlook_advice": "solid path with roles in diagnostics, pharma, and research"
  },
  "Zoologist": {
    "skills": "animal biology, taxonomy, ecology, research techniques",
    "specific_skills": "habitat analysis, wildlife tracking, data logging, behavior observation",
    "daily_tasks": "studying animals, conducting fieldwork, analyzing ecological data",
    "collaborators": "ecologists, conservationists, wildlife officers",
    "projects": "animal behavior studies, species conservation, habitat restoration",
    "degree_suggestion": "Zoology, Wildlife Biology, Ecology",
    "experience_suggestion": "wildlife internships, research projects, zoo volunteering",
    "min_salary": "₹3,00,000",
    "max_salary": "₹10,00,000",
    "relevant_courses": "vertebrate biology, conservation science, environmental studies",
    "outlook_status": "moderate",
    "outlook_reasons": "valuable for conservation but fewer job openings",
    "outlook_advice": "best for those with a deep love for animals and nature"
  },
  "Botanist": {
    "skills": "plant science, taxonomy, ecology, greenhouse techniques",
    "specific_skills": "herbarium use, soil testing, plant identification, tissue culture",
    "daily_tasks": "researching plants, documenting species, analyzing plant interactions",
    "collaborators": "ecologists, agricultural scientists, conservationists",
    "projects": "crop improvement, plant disease study, forest conservation",
    "degree_suggestion": "Botany, Plant Science, Agricultural Science",
    "experience_suggestion": "herbarium work, nursery internships, agricultural labs",
    "min_salary": "₹3,00,000",
    "max_salary": "₹9,00,000",
    "relevant_courses": "plant physiology, taxonomy, agronomy",
    "outlook_status": "moderate",
    "outlook_reasons": "demand in agriculture, forestry, and conservation",
    "outlook_advice": "strong niche for those passionate about plants"
  },
  "Ecologist": {
    "skills": "ecosystem analysis, environmental science, statistics, GIS tools",
    "specific_skills": "biodiversity surveys, environmental impact assessments, data modeling",
    "daily_tasks": "monitoring ecosystems, fieldwork, studying human impacts",
    "collaborators": "environmental scientists, policy makers, NGOs",
    "projects": "habitat restoration, sustainability studies, climate change modeling",
    "degree_suggestion": "Ecology, Environmental Science, Biology",
    "experience_suggestion": "NGO volunteering, environmental internships, conservation projects",
    "min_salary": "₹3,50,000",
    "max_salary": "₹11,00,000",
    "relevant_courses": "climate science, ecosystem ecology, conservation biology",
    "outlook_status": "strong",
    "outlook_reasons": "increasing awareness of climate change and biodiversity",
    "outlook_advice": "excellent for green careers and sustainability initiatives"
  },
  "Entomologist": {
    "skills": "insect biology, lab techniques, taxonomy, field surveys",
    "specific_skills": "trap setting, specimen preservation, pest analysis, microscopy",
    "daily_tasks": "studying insects, identifying species, researching pest control methods",
    "collaborators": "agricultural scientists, ecologists, public health officials",
    "projects": "crop protection, insect biodiversity, disease vector analysis",
    "degree_suggestion": "Entomology, Zoology, Agricultural Science",
    "experience_suggestion": "research projects, insect collection work, agro research internships",
    "min_salary": "₹3,00,000",
    "max_salary": "₹10,00,000",
    "relevant_courses": "insect physiology, agricultural entomology, pest control",
    "outlook_status": "moderate",
    "outlook_reasons": "important role in agriculture and pest management",
    "outlook_advice": "great niche for insect lovers and agriculture researchers"
  },

     "Physicist": {
    "skills": "analytical thinking, mathematical modeling, experimental techniques, data analysis, research writing",
    "specific_skills": "MATLAB, Python, LaTeX, simulations, lab instruments",
    "daily_tasks": "designing and conducting experiments, analyzing data, publishing research papers, presenting findings",
    "collaborators": "researchers, lab assistants, university staff, government agencies",
    "projects": "particle research, material studies, physical simulations",
    "degree_suggestion": "Physics, Applied Physics, or a related science field",
    "experience_suggestion": "research internships, academic projects, science fairs, publications",
    "min_salary": "₹4,00,000",
    "max_salary": "₹15,00,000",
    "relevant_courses": "classical mechanics, quantum physics, thermodynamics, electromagnetism",
    "outlook_status": "stable",
    "outlook_reasons": "ongoing scientific research and need for theoretical expertise",
    "outlook_advice": "good for those passionate about pure science and academia"
  },
  "Aerospace Engineer": {
    "skills": "aerodynamics, fluid mechanics, propulsion systems, systems design, CAD software",
    "specific_skills": "ANSYS, CATIA, MATLAB, C++, Simulink",
    "daily_tasks": "designing aircraft or spacecraft, testing prototypes, analyzing flight data, ensuring compliance with safety standards",
    "collaborators": "mechanical engineers, pilots, government officials, manufacturing teams",
    "projects": "design of satellites, rockets, aircraft systems",
    "degree_suggestion": "Aerospace Engineering or Aeronautical Engineering",
    "experience_suggestion": "internships with aerospace companies, model rocket clubs, research assistantships",
    "min_salary": "₹6,00,000",
    "max_salary": "₹20,00,000",
    "relevant_courses": "fluid dynamics, aerospace structures, propulsion, control systems",
    "outlook_status": "strong",
    "outlook_reasons": "growth in defense, commercial aviation, and space exploration",
    "outlook_advice": "excellent opportunities in both private and government sectors"
  },
  "Nuclear Scientist": {
    "skills": "nuclear physics, radiation safety, reactor design, critical thinking, lab experimentation",
    "specific_skills": "radiation detectors, nuclear simulation tools, C++, FORTRAN",
    "daily_tasks": "studying nuclear reactions, monitoring radiation levels, developing nuclear technologies, conducting safety assessments",
    "collaborators": "health physicists, reactor engineers, safety officers, research scientists",
    "projects": "nuclear energy development, medical isotopes, fusion research",
    "degree_suggestion": "Nuclear Physics, Nuclear Engineering, or Physics",
    "experience_suggestion": "nuclear lab internships, research projects, university labs",
    "min_salary": "₹5,50,000",
    "max_salary": "₹18,00,000",
    "relevant_courses": "nuclear physics, reactor engineering, radiation protection",
    "outlook_status": "moderate",
    "outlook_reasons": "nuclear power remains a key energy source in many countries",
    "outlook_advice": "niche but rewarding field for those interested in atomic science"
  },
  "Astrophysicist": {
    "skills": "astronomical data analysis, theoretical modeling, programming, strong math foundation",
    "specific_skills": "Python, R, MATLAB, telescope operation, image processing",
    "daily_tasks": "analyzing celestial phenomena, simulating models, publishing research, working with observatory data",
    "collaborators": "astronomers, physicists, data scientists, observatory staff",
    "projects": "galaxy formation, black hole research, cosmology simulations",
    "degree_suggestion": "Astrophysics, Physics, or Astronomy",
    "experience_suggestion": "internships with research centers, amateur astronomy clubs, telescope work",
    "min_salary": "₹4,50,000",
    "max_salary": "₹16,00,000",
    "relevant_courses": "astrophysics, general relativity, observational astronomy",
    "outlook_status": "stable",
    "outlook_reasons": "scientific curiosity and space research funding",
    "outlook_advice": "ideal for research-oriented individuals fascinated by space"
  },
  "Quantum Physicist": {
    "skills": "quantum mechanics, linear algebra, theoretical modeling, simulation, problem-solving",
    "specific_skills": "Qiskit, Python, quantum simulators, LaTeX",
    "daily_tasks": "studying quantum systems, developing quantum algorithms, conducting experiments, writing papers",
    "collaborators": "quantum engineers, computer scientists, mathematicians",
    "projects": "quantum computing, entanglement studies, particle-wave duality research",
    "degree_suggestion": "Physics with specialization in Quantum Mechanics or Quantum Computing",
    "experience_suggestion": "quantum research labs, online quantum programming challenges, academic projects",
    "min_salary": "₹6,00,000",
    "max_salary": "₹22,00,000",
    "relevant_courses": "quantum mechanics, quantum information theory, computational physics",
    "outlook_status": "very strong",
    "outlook_reasons": "rising interest in quantum computing and next-gen technologies",
    "outlook_advice": "emerging and highly promising field with global demand"
  },
  "Geophysicist": {
    "skills": "earth sciences, seismic interpretation, data logging, geospatial analysis, research",
    "specific_skills": "GIS tools, Python, MATLAB, field instruments",
    "daily_tasks": "studying Earth's physical structure, analyzing seismic data, field surveys, creating geological models",
    "collaborators": "geologists, mining engineers, environmental scientists, oil companies",
    "projects": "earthquake studies, oil exploration, geothermal analysis",
    "degree_suggestion": "Geophysics, Earth Sciences, or Physics",
    "experience_suggestion": "field trips, internships in mining or oil companies, university labs",
    "min_salary": "₹4,80,000",
    "max_salary": "₹14,00,000",
    "relevant_courses": "geophysics, mineralogy, seismic data analysis",
    "outlook_status": "strong",
    "outlook_reasons": "exploration and environmental monitoring needs",
    "outlook_advice": "great for those who enjoy a mix of outdoor and lab work"
  },
  "Medical Physicist": {
    "skills": "radiation physics, human anatomy, treatment planning, calibration, safety compliance",
    "specific_skills": "LINAC machines, MRI/CT safety, radiation therapy software",
    "daily_tasks": "calibrating machines, ensuring patient safety, assisting in treatment plans, performing QA checks",
    "collaborators": "oncologists, radiologists, radiologic technologists",
    "projects": "radiation treatment planning, medical imaging QA, dosimetry studies",
    "degree_suggestion": "Medical Physics or Physics with a specialization in healthcare",
    "experience_suggestion": "internships in hospitals, certified medical physics programs",
    "min_salary": "₹6,00,000",
    "max_salary": "₹20,00,000",
    "relevant_courses": "radiation physics, anatomy, medical imaging",
    "outlook_status": "very strong",
    "outlook_reasons": "growing need for cancer treatment and imaging technologies",
    "outlook_advice": "excellent choice for physics lovers wanting to work in healthcare"
  },
  "Acoustics Engineer": {
    "skills": "sound wave physics, vibration analysis, signal processing, measurement techniques",
    "specific_skills": "MATLAB, LabVIEW, audio analysis software, sensors",
    "daily_tasks": "designing soundproof systems, testing acoustics, improving product sound quality",
    "collaborators": "architects, product designers, construction teams",
    "projects": "concert hall design, consumer electronics audio, noise cancellation",
    "degree_suggestion": "Acoustical Engineering, Physics, or Mechanical Engineering",
    "experience_suggestion": "internships in audio tech companies, DIY acoustic projects, labs",
    "min_salary": "₹3,50,000",
    "max_salary": "₹12,00,000",
    "relevant_courses": "acoustics, vibrations, signal processing",
    "outlook_status": "moderate",
    "outlook_reasons": "specialized demand in construction, entertainment, and manufacturing",
    "outlook_advice": "great niche for sound-tech enthusiasts"
  },
  "Optical Physicist": {
    "skills": "optics, wave theory, light-matter interaction, precision measurement",
    "specific_skills": "Zemax, LabVIEW, optical benches, interferometers",
    "daily_tasks": "designing lenses, studying light behavior, working on lasers and fiber optics",
    "collaborators": "electronics engineers, photonics experts, material scientists",
    "projects": "laser systems, fiber optic communications, imaging technologies",
    "degree_suggestion": "Optical Physics, Photonics, or Applied Physics",
    "experience_suggestion": "optical lab work, telescope building, laser workshops",
    "min_salary": "₹5,00,000",
    "max_salary": "₹18,00,000",
    "relevant_courses": "geometrical optics, quantum optics, photonics",
    "outlook_status": "strong",
    "outlook_reasons": "increased use in telecom, medicine, and defense",
    "outlook_advice": "valuable for tech-oriented physics grads"
  },
  "Laser Technologist": {
    "skills": "laser theory, safety procedures, alignment techniques, optics integration",
    "specific_skills": "laser tuning, CAD for optics, laser spectrometry tools",
    "daily_tasks": "calibrating laser systems, testing components, ensuring beam quality, integrating lasers into devices",
    "collaborators": "engineers, physicists, medical teams, manufacturing teams",
    "projects": "laser cutting machines, medical lasers, optical instruments",
    "degree_suggestion": "Laser Technology, Photonics, Applied Physics",
    "experience_suggestion": "laser research labs, industry training programs, workshops",
    "min_salary": "₹4,00,000",
    "max_salary": "₹14,00,000",
    "relevant_courses": "laser physics, electronics, optical design",
    "outlook_status": "moderate",
    "outlook_reasons": "use in various sectors from healthcare to defense",
    "outlook_advice": "excellent for hands-on physics applications"
  },
  "Geologist": {
    "skills": "earth sciences, rock and mineral analysis, geological mapping, field research",
    "specific_skills": "GIS, stratigraphy, remote sensing, drilling techniques",
    "daily_tasks": "studying rock formations, conducting field surveys, analyzing soil samples",
    "collaborators": "environmental scientists, mining engineers, geophysicists",
    "projects": "mineral exploration, environmental assessments, natural disaster studies",
    "degree_suggestion": "Geology, Earth Science, or Environmental Science",
    "experience_suggestion": "field internships, research in geological labs, mapping projects",
    "min_salary": "₹3,50,000",
    "max_salary": "₹12,00,000",
    "relevant_courses": "mineralogy, petrology, structural geology, GIS",
    "outlook_status": "steady",
    "outlook_reasons": "demand in natural resource extraction and environmental planning",
    "outlook_advice": "strong field for those who enjoy outdoor scientific work"
  },

  "Oceanographer": {
    "skills": "marine science, hydrodynamics, data analysis, remote sensing",
    "specific_skills": "CTD sensors, sonar mapping, water sampling, modeling software",
    "daily_tasks": "studying ocean currents, analyzing marine ecosystems, conducting ocean expeditions",
    "collaborators": "marine biologists, climate scientists, naval researchers",
    "projects": "climate impact studies, marine pollution analysis, ocean current modeling",
    "degree_suggestion": "Oceanography, Marine Science, or Environmental Science",
    "experience_suggestion": "marine internships, research cruises, water quality labs",
    "min_salary": "₹4,00,000",
    "max_salary": "₹14,00,000",
    "relevant_courses": "physical oceanography, marine chemistry, aquatic ecosystems",
    "outlook_status": "growing",
    "outlook_reasons": "increasing climate research and ocean resource exploration",
    "outlook_advice": "ideal for those interested in marine environments and climate"
  },

  "Meteorologist": {
    "skills": "weather forecasting, atmospheric science, data interpretation, communication",
    "specific_skills": "radar systems, satellite imagery, weather modeling, Python/R",
    "daily_tasks": "analyzing weather data, predicting forecasts, reporting severe weather conditions",
    "collaborators": "climatologists, broadcasters, aviation and disaster teams",
    "projects": "weather predictions, storm tracking, climate monitoring",
    "degree_suggestion": "Meteorology, Atmospheric Science, or Physics",
    "experience_suggestion": "weather station internships, forecasting labs, research roles",
    "min_salary": "₹4,00,000",
    "max_salary": "₹15,00,000",
    "relevant_courses": "synoptic meteorology, climatology, atmospheric physics",
    "outlook_status": "strong",
    "outlook_reasons": "essential for public safety, agriculture, and aviation",
    "outlook_advice": "great for those passionate about weather and environmental science"
  },

  "Seismologist": {
    "skills": "geophysics, earthquake analysis, seismic wave studies, instrumentation",
    "specific_skills": "seismographs, GPS, data modeling, signal processing",
    "daily_tasks": "monitoring seismic activity, analyzing earthquake data, preparing risk assessments",
    "collaborators": "geologists, civil engineers, emergency response teams",
    "projects": "earthquake prediction models, building safety codes, seismic hazard mapping",
    "degree_suggestion": "Geophysics, Earth Science, or Seismology",
    "experience_suggestion": "earthquake research labs, seismic data analysis projects",
    "min_salary": "₹4,50,000",
    "max_salary": "₹16,00,000",
    "relevant_courses": "seismology, geodynamics, wave mechanics",
    "outlook_status": "growing",
    "outlook_reasons": "increasing need for earthquake preparedness and disaster resilience",
    "outlook_advice": "important field for natural disaster risk reduction"
  },

  "Climatologist": {
    "skills": "climate science, statistical modeling, long-term data analysis, environmental systems",
    "specific_skills": "climate modeling tools, GIS, remote sensing, paleoclimate methods",
    "daily_tasks": "analyzing historical climate data, building future climate models, writing reports",
    "collaborators": "policy makers, environmental scientists, data scientists",
    "projects": "global warming impact studies, regional climate forecasts, sustainability research",
    "degree_suggestion": "Climatology, Environmental Science, or Meteorology",
    "experience_suggestion": "climate research internships, work with NGOs, environmental monitoring roles",
    "min_salary": "₹4,50,000",
    "max_salary": "₹18,00,000",
    "relevant_courses": "climate change, environmental modeling, data analysis",
    "outlook_status": "very strong",
    "outlook_reasons": "growing global focus on climate change and sustainability",
    "outlook_advice": "critical role in addressing future environmental challenges"
  },


    "UI/UX Designer": {
        "skills": "design tools (Figma, Sketch, Adobe XD), user psychology, wireframing, prototyping, usability testing, user research, information architecture, visual design principles",
        "specific_skills": "Figma, Sketch, Adobe XD, user research, wireframing, prototyping, design systems",
        "daily_tasks": "creating user flows and wireframes; designing high-fidelity prototypes; conducting user research and usability testing; iterating on designs based on feedback",
        "collaborators": "product managers, front-end developers, marketing teams, business analysts",
        "projects": "designing new app features, optimizing website layouts, improving user onboarding, creating design systems",
        "degree_suggestion": "Graphic Design, Human-Computer Interaction (HCI), Industrial Design, or a related design field",
        "experience_suggestion": "building a strong portfolio, internships, design challenges, freelance projects",
        "min_salary": "₹4,00,000",
        "max_salary": "₹15,00,000",
        "relevant_courses": "interaction design, user research methods, visual communication, front-end development basics",
        "outlook_status": "strong",
        "outlook_reasons": "the increasing focus on user-centered design in all industries and the growth of digital products",
        "outlook_advice": "good opportunities for those with a strong portfolio and understanding of user needs"
    },
    "Graphic Designer": {
        "skills": "Adobe Photoshop, Illustrator, InDesign, visual composition, typography, branding principles, creativity, communication",
        "specific_skills": "Adobe Creative Suite, layout design, branding, illustration, photo editing",
        "daily_tasks": "creating logos, brochures, website graphics, marketing collateral, advertisements; collaborating on design concepts; preparing files for print or digital use",
        "collaborators": "clients, marketing teams, content creators, web developers",
        "projects": "developing brand identities, designing advertising campaigns, creating social media graphics, producing print materials",
        "degree_suggestion": "Graphic Design, Fine Arts, Visual Communication, or a related design discipline",
        "experience_suggestion": "building a diverse portfolio, freelance projects, internships, participating in design contests",
        "min_salary": "₹3,00,000",
        "max_salary": "₹10,00,000",
        "relevant_courses": "design history, color theory, digital illustration, printing techniques",
        "outlook_status": "stable",
        "outlook_reasons": "continued need for visual content across all platforms, although automation might impact some tasks",
        "outlook_advice": "continuous learning and adapting to new tools is key for success"
    },
    "Data Scientist": {
        "skills": "statistical modeling, machine learning, programming (Python/R), data manipulation (SQL), data visualization, problem-solving, communication",
        "specific_skills": "Python, R, SQL, TensorFlow, scikit-learn, Tableau, predictive modeling, big data technologies",
        "daily_tasks": "collecting and cleaning data; building and testing predictive models; interpreting and presenting data insights; collaborating with business stakeholders",
        "collaborators": "data engineers, business analysts, domain experts, management",
        "projects": "developing recommendation systems, optimizing business processes, fraud detection, customer churn prediction",
        "degree_suggestion": "Data Science, Statistics, Computer Science, or Mathematics",
        "experience_suggestion": "data analysis projects, Kaggle competitions, internships, relevant certifications",
        "min_salary": "₹6,00,000",
        "max_salary": "₹25,00,000",
        "relevant_courses": "linear algebra, calculus, probability, machine learning, deep learning, big data analytics",
        "outlook_status": "excellent",
        "outlook_reasons": "the explosion of data and the growing need for data-driven decision-making in almost every industry",
        "outlook_advice": "a highly sought-after and rewarding career path"
    },
    "Doctor": {
        "skills": "medical knowledge, diagnostic skills, critical thinking, empathy, communication, decision-making under pressure",
        "specific_skills": "diagnosis, patient care, medical procedures, pharmacology, ethical practice",
        "daily_tasks": "diagnosing and treating illnesses, performing examinations, prescribing medications, advising on preventative care, maintaining patient records",
        "collaborators": "nurses, other doctors, specialists, medical assistants, administrative staff",
        "projects": "managing patient cases, medical research, continuous professional development, contributing to public health initiatives",
        "degree_suggestion": "MBBS (Bachelor of Medicine, Bachelor of Surgery) followed by MD/MS for specialization",
        "experience_suggestion": "internships, residency programs, clinical rotations, rural service bonds",
        "min_salary": "₹6,00,000",
        "max_salary": "₹30,00,000+", # Can be very high for specialists
        "relevant_courses": "Anatomy, Physiology, Pathology, Pharmacology, Surgery, Medicine, Pediatrics",
        "outlook_status": "consistently high",
        "outlook_reasons": "the universal and ongoing need for healthcare services, an aging population, and advances in medical technology",
        "outlook_advice": "a challenging but deeply rewarding career with high societal impact"
    },
    "Lawyer": {
        "skills": "legal research, analytical thinking, strong written and verbal communication, negotiation, persuasion, attention to detail, problem-solving",
        "specific_skills": "legal research databases, case law analysis, drafting legal documents (pleadings, contracts), courtroom advocacy, client counseling",
        "daily_tasks": "researching legal cases and precedents; preparing legal documents (briefs, contracts); advising clients; representing clients in court or negotiations; attending depositions",
        "collaborators": "clients, paralegals, other lawyers, court staff, expert witnesses",
        "projects": "litigation, corporate mergers and acquisitions, family law cases, criminal defense, public interest advocacy",
        "degree_suggestion": "LLB (Bachelor of Legislative Law) or BA LLB for integrated programs",
        "experience_suggestion": "internships at law firms/chambers, moot court participation, legal aid clinics, working as a junior advocate",
        "min_salary": "₹4,00,000",
        "max_salary": "₹25,00,000", # Can be much higher for senior corporate lawyers
        "relevant_courses": "Constitutional Law, Criminal Law, Civil Procedure Code, Contract Law, Corporate Law, Jurisprudence",
        "outlook_status": "stable with competition",
        "outlook_reasons": "the ongoing need for legal services in a complex society, but new graduates face strong competition for entry-level positions",
        "outlook_advice": "specialization and continuous professional development are key for career growth"
    },
    "Aerospace Engineer": {
        "skills": "fluid mechanics, thermodynamics, materials science, propulsion systems, CAD software, problem-solving, attention to detail",
        "specific_skills": "SolidWorks, AutoCAD, MATLAB, aerodynamics, structural analysis, flight dynamics",
        "daily_tasks": "designing aircraft, spacecraft, satellites, or missiles; testing prototypes; analyzing flight data; ensuring safety and efficiency of aerospace vehicles",
        "collaborators": "other engineers (mechanical, electrical, software), scientists, technicians, project managers",
        "projects": "developing new propulsion systems, improving aircraft fuel efficiency, designing spacecraft components, integrating avionics systems",
        "degree_suggestion": "Aerospace Engineering, Aeronautical Engineering, or Mechanical Engineering with an aerospace specialization",
        "experience_suggestion": "internships with aerospace companies (e.g., HAL, ISRO, Boeing), participation in aerospace clubs/competitions, research assistantships",
        "min_salary": "₹6,00,000",
        "max_salary": "₹20,00,000",
        "relevant_courses": "aerodynamics, flight mechanics, propulsion, aerospace structures, control systems",
        "outlook_status": "growing steadily",
        "outlook_reasons": "demand from defense, commercial aviation, and increasing space exploration initiatives",
        "outlook_advice": "a specialized field with high-tech challenges and significant contributions to innovation"
    },
    "Chemist": {
        "skills": "analytical skills, problem-solving, laboratory techniques, data analysis, scientific writing, safety protocols",
        "specific_skills": "spectroscopy, chromatography, organic synthesis, analytical instrumentation, quality control",
        "daily_tasks": "conducting experiments; analyzing substances; developing new materials or processes; interpreting results; writing reports",
        "collaborators": "other scientists, researchers, technicians, production teams",
        "projects": "developing new drugs, improving industrial processes, creating sustainable materials, forensic analysis",
        "degree_suggestion": "Chemistry, Chemical Engineering, or Biochemistry",
        "experience_suggestion": "research internships, laboratory assistant positions, industrial training",
        "min_salary": "₹3,50,000",
        "max_salary": "₹12,00,000",
        "relevant_courses": "organic chemistry, inorganic chemistry, physical chemistry, analytical chemistry, biochemistry",
        "outlook_status": "stable",
        "outlook_reasons": "essential in pharmaceuticals, materials science, environmental protection, and manufacturing",
        "outlook_advice": "specialization in emerging areas like nanotechnology or green chemistry can enhance prospects"
    },
    "Biologist": {
        "skills": "scientific method, observation, experimentation, data analysis, molecular biology techniques, critical thinking",
        "specific_skills": "PCR, gel electrophoresis, microscopy, statistical software, field research methods",
        "daily_tasks": "designing and conducting experiments; collecting and analyzing biological data; studying living organisms and their environments; preparing scientific reports",
        "collaborators": "other scientists, researchers, lab technicians, environmental specialists",
        "projects": "gene editing research, ecological impact assessments, drug discovery, biodiversity conservation",
        "degree_suggestion": "Biology, Biotechnology, Microbiology, or Environmental Science",
        "experience_suggestion": "laboratory internships, field research assistantships, volunteer work at conservation organizations",
        "min_salary": "₹3,00,000",
        "max_salary": "₹10,00,000",
        "relevant_courses": "genetics, ecology, cell biology, molecular biology, immunology",
        "outlook_status": "growing",
        "outlook_reasons": "advancements in biotechnology, increasing environmental concerns, and demand in healthcare and agriculture",
        "outlook_advice": "interdisciplinary skills and research experience are highly valued"
    },
    "Web Developer": {
    "skills": "HTML, CSS, JavaScript, responsive design, debugging, browser compatibility",
    "specific_skills": "React, Angular, Vue.js, Bootstrap, Git, REST APIs",
    "daily_tasks": "building and maintaining websites, fixing UI bugs, integrating frontend with backend APIs",
    "collaborators": "UI/UX designers, backend developers, content writers",
    "projects": "company websites, e-commerce sites, web apps, landing pages",
    "degree_suggestion": "Computer Science, Web Development, or related field",
    "experience_suggestion": "portfolio websites, freelance work, internships, personal projects",
    "min_salary": "₹3,00,000",
    "max_salary": "₹12,00,000",
    "relevant_courses": "web design, frontend development, JavaScript frameworks, responsive design",
    "outlook_status": "strong",
    "outlook_reasons": "growing demand for online presence",
    "outlook_advice": "strong skills in frameworks and design will boost opportunities"
  },
  "AI/ML Engineer": {
    "skills": "machine learning, deep learning, Python, statistics, data preprocessing, model evaluation",
    "specific_skills": "TensorFlow, PyTorch, Scikit-learn, NumPy, Pandas",
    "daily_tasks": "training models, tuning hyperparameters, analyzing datasets, deploying ML solutions",
    "collaborators": "data scientists, software engineers, product teams",
    "projects": "chatbots, recommendation systems, predictive analytics, computer vision apps",
    "degree_suggestion": "AI/ML, Data Science, Computer Science, or related field",
    "experience_suggestion": "Kaggle competitions, research projects, ML internships, GitHub projects",
    "min_salary": "₹6,00,000",
    "max_salary": "₹30,00,000",
    "relevant_courses": "machine learning, deep learning, statistics, data science",
    "outlook_status": "very strong",
    "outlook_reasons": "AI is transforming multiple industries",
    "outlook_advice": "solid math and programming background is essential"
  },
    "Full Stack Developer": {
    "skills": "frontend and backend development, databases, version control, RESTful APIs",
    "specific_skills": "Node.js, React, Express, MongoDB, MySQL, Git",
    "daily_tasks": "building full-featured applications, writing APIs, fixing bugs, integrating systems",
    "collaborators": "frontend developers, backend developers, UI/UX designers, DevOps",
    "projects": "web apps, admin dashboards, social platforms, SaaS products",
    "degree_suggestion": "Computer Science, Software Engineering",
    "experience_suggestion": "full-stack bootcamps, internships, personal web apps, team projects",
    "min_salary": "₹5,00,000",
    "max_salary": "₹25,00,000",
    "relevant_courses": "web development, databases, APIs, software architecture",
    "outlook_status": "very strong",
    "outlook_reasons": "companies want developers who can do both frontend and backend",
    "outlook_advice": "stay updated with both frontend and backend tech stacks"
  },
    "Data Scientist": {
    "skills": "data analysis, statistics, machine learning, data visualization, data cleaning",
    "specific_skills": "Python, R, SQL, Pandas, Matplotlib, Scikit-learn",
    "daily_tasks": "analyzing data, building models, presenting insights, working with big data",
    "collaborators": "business analysts, data engineers, product managers",
    "projects": "sales predictions, customer segmentation, business dashboards, anomaly detection",
    "degree_suggestion": "Data Science, Statistics, Mathematics, or Computer Science",
    "experience_suggestion": "Kaggle projects, data internships, business case studies",
    "min_salary": "₹6,00,000",
    "max_salary": "₹28,00,000",
    "relevant_courses": "data analytics, statistics, machine learning, Python for data science",
    "outlook_status": "very strong",
    "outlook_reasons": "data-driven decision making is essential everywhere",
    "outlook_advice": "communication skills and storytelling with data are key"
  },
 "Blockchain Developer": {
    "skills": "blockchain architecture, cryptography, smart contracts, distributed systems",
    "specific_skills": "Solidity, Ethereum, Hyperledger, Web3.js, Truffle, Metamask",
    "daily_tasks": "developing smart contracts, integrating blockchain with apps, testing decentralized systems",
    "collaborators": "backend developers, cryptographers, finance teams",
    "projects": "DeFi platforms, NFT apps, blockchain games, DAOs",
    "degree_suggestion": "Computer Science, Cryptography, Blockchain Technology",
    "experience_suggestion": "hackathons, blockchain courses, GitHub projects, testnets",
    "min_salary": "₹7,00,000",
    "max_salary": "₹35,00,000",
    "relevant_courses": "smart contracts, cryptography, Web3 development, decentralized systems",
    "outlook_status": "growing",
    "outlook_reasons": "decentralized finance and Web3 are gaining traction",
    "outlook_advice": "keep up with rapidly evolving blockchain standards"
  },
 "Cybersecurity Analyst": {
    "skills": "network security, threat detection, vulnerability assessment, risk analysis, encryption",
    "specific_skills": "Wireshark, Nessus, Nmap, Kali Linux, Metasploit, firewalls",
    "daily_tasks": "monitoring systems, responding to security incidents, conducting audits, updating policies",
    "collaborators": "IT administrators, security engineers, compliance officers",
    "projects": "penetration testing, security training, incident response plans, audit reports",
    "degree_suggestion": "Cybersecurity, Information Security, or Computer Science",
    "experience_suggestion": "CTF competitions, internships, security certifications (CEH, CompTIA Security+)",
    "min_salary": "₹4,50,000",
    "max_salary": "₹22,00,000",
    "relevant_courses": "ethical hacking, network security, digital forensics, cryptography",
    "outlook_status": "very strong",
    "outlook_reasons": "increasing cyber threats and data regulations",
    "outlook_advice": "certifications and practical skills matter more than just degrees"
  },
   "Game Developer": {
    "skills": "game mechanics, animation, physics, graphics programming, problem-solving",
    "specific_skills": "Unity, Unreal Engine, C#, C++, Blender, physics engines",
    "daily_tasks": "coding game logic, debugging, creating levels, optimizing performance, testing gameplay",
    "collaborators": "artists, designers, sound engineers, QA testers",
    "projects": "2D/3D games, mobile games, AR/VR games, multiplayer systems",
    "degree_suggestion": "Game Development, Computer Graphics, or Software Engineering",
    "experience_suggestion": "game jams, indie game projects, modding, internships in studios",
    "min_salary": "₹4,00,000",
    "max_salary": "₹18,00,000",
    "relevant_courses": "game design, 3D modeling, computer graphics, AI in games",
    "outlook_status": "strong",
    "outlook_reasons": "growing gaming industry in mobile and console markets",
    "outlook_advice": "a good portfolio speaks louder than a resume"
  },
  "DevOps Engineer": {
    "skills": "CI/CD pipelines, automation, scripting (Bash, Python), containerization (Docker), orchestration (Kubernetes)",
    "specific_skills": "Jenkins, Docker, Kubernetes, AWS, Git, Terraform",
    "daily_tasks": "maintaining CI/CD pipelines, automating infrastructure, monitoring systems, managing deployments",
    "collaborators": "developers, sysadmins, QA teams",
    "projects": "cloud automation, scalable deployments, container orchestration, infrastructure as code",
    "degree_suggestion": "Computer Science, IT, or DevOps certifications",
    "experience_suggestion": "Linux experience, cloud platforms, GitHub Actions, scripting",
    "min_salary": "₹6,00,000",
    "max_salary": "₹25,00,000",
    "relevant_courses": "DevOps fundamentals, cloud computing, automation tools",
    "outlook_status": "very strong",
    "outlook_reasons": "demand for fast, reliable software delivery",
    "outlook_advice": "strong automation mindset and scripting skills are key"
  },
  "Cloud Architect": {
    "skills": "cloud platforms (AWS, Azure, GCP), cloud security, cost optimization, architecture design",
    "specific_skills": "AWS Certified Architect, Kubernetes, Terraform, VPC, IAM",
    "daily_tasks": "designing scalable cloud systems, managing cloud budgets, securing environments, mentoring teams",
    "collaborators": "DevOps, software architects, CTOs",
    "projects": "multi-cloud strategies, serverless systems, cloud migrations, disaster recovery",
    "degree_suggestion": "Cloud Computing, Computer Science, IT",
    "experience_suggestion": "cloud certifications, enterprise IT projects, architectural documentation",
    "min_salary": "₹10,00,000",
    "max_salary": "₹35,00,000",
    "relevant_courses": "cloud architecture, network security, distributed computing",
    "outlook_status": "very strong",
    "outlook_reasons": "widespread cloud adoption across all sectors",
    "outlook_advice": "business understanding and scalability mindset are key"
  },
  "Mobile App Developer": {
    "skills": "mobile app frameworks, UI design, API integration, testing, app deployment",
    "specific_skills": "Flutter, React Native, Kotlin, Swift, Android Studio, Firebase",
    "daily_tasks": "writing and testing mobile apps, collaborating with UI/UX teams, publishing apps",
    "collaborators": "designers, backend developers, QA testers",
    "projects": "e-commerce apps, productivity tools, social apps, cross-platform apps",
    "degree_suggestion": "Mobile Computing, Computer Science, or Software Engineering",
    "experience_suggestion": "personal apps, published apps on Play Store/App Store, internships",
    "min_salary": "₹4,00,000",
    "max_salary": "₹18,00,000",
    "relevant_courses": "mobile development, UI/UX, cross-platform frameworks",
    "outlook_status": "strong",
    "outlook_reasons": "increasing mobile usage for all services",
    "outlook_advice": "know both Android and iOS ecosystems"
  },
  "Site Reliability Engineer": {
    "skills": "system monitoring, alerting, automation, incident response, reliability metrics",
    "specific_skills": "Prometheus, Grafana, Kubernetes, Python, Google SRE practices",
    "daily_tasks": "ensuring uptime, reducing system toil, automating maintenance, analyzing outages",
    "collaborators": "DevOps, software engineers, product teams",
    "projects": "SLAs/SLOs setup, fault tolerance, disaster recovery, monitoring dashboards",
    "degree_suggestion": "Computer Science, Systems Engineering, IT",
    "experience_suggestion": "Linux administration, cloud monitoring, scripting projects",
    "min_salary": "₹8,00,000",
    "max_salary": "₹30,00,000",
    "relevant_courses": "systems reliability, infrastructure monitoring, automation scripting",
    "outlook_status": "very strong",
    "outlook_reasons": "companies prioritize high availability and fault tolerance",
    "outlook_advice": "best suited for those who enjoy backend systems and automation"
  },
    "Mathematician": {
        "skills": "advanced mathematical concepts, logical reasoning, problem-solving, abstract thinking, computational tools (e.g., MATLAB, Python), data analysis",
        "specific_skills": "calculus, algebra, differential equations, numerical analysis, statistical modeling, LaTeX",
        "daily_tasks": "developing mathematical models; solving complex problems in various fields (science, engineering, finance); conducting research; teaching",
        "collaborators": "scientists, engineers, economists, statisticians, computer scientists",
        "projects": "financial modeling, cryptographic algorithm development, optimizing logistics, theoretical research in pure mathematics",
        "degree_suggestion": "Mathematics, Applied Mathematics, Statistics, or Quantitative Finance",
        "experience_suggestion": "research assistantships, internships in data analysis or finance, participation in math competitions",
        "min_salary": "₹4,00,000",
        "max_salary": "₹18,00,000",
        "relevant_courses": "real analysis, complex analysis, topology, numerical methods, probability theory, operations research",
        "outlook_status": "strong",
        "outlook_reasons": "increasing demand for quantitative skills in areas like data science, cybersecurity, and financial analysis",
        "outlook_advice": "combining mathematical expertise with computational or domain-specific skills is highly beneficial"
    },
  "Chemist": {
    "skills": "analytical chemistry, organic/inorganic chemistry, lab safety, spectroscopy, chromatography",
    "specific_skills": "GC-MS, HPLC, titration, lab reporting, chemical synthesis",
    "daily_tasks": "conducting experiments, analyzing substances, recording results, maintaining lab equipment",
    "collaborators": "lab technicians, fellow chemists, quality assurance teams, production managers",
    "projects": "developing new compounds, testing material properties, quality control",
    "degree_suggestion": "Chemistry, Applied Chemistry, or related field",
    "experience_suggestion": "internships in chemical industries, lab assistant roles, academic research",
    "min_salary": "₹3,00,000",
    "max_salary": "₹12,00,000",
    "relevant_courses": "organic chemistry, physical chemistry, analytical methods, instrumentation",
    "outlook_status": "steady",
    "outlook_reasons": "continued need in pharmaceuticals, materials, and manufacturing industries",
    "outlook_advice": "chemistry roles remain valuable across multiple industries"
  },

  "Pharmaceutical Chemist": {
    "skills": "medicinal chemistry, pharmacology, drug formulation, chemical analysis",
    "specific_skills": "tablet coating, HPLC, compound screening, stability testing",
    "daily_tasks": "designing and testing drug compounds, documenting trials, collaborating with biologists",
    "collaborators": "pharmacologists, clinical researchers, regulatory officers",
    "projects": "developing new drugs, improving existing medications, conducting clinical research",
    "degree_suggestion": "Pharmaceutical Chemistry, Pharmacy, or Chemistry",
    "experience_suggestion": "pharma internships, lab-based research, clinical trials involvement",
    "min_salary": "₹4,00,000",
    "max_salary": "₹15,00,000",
    "relevant_courses": "drug design, bioanalytical chemistry, toxicology, regulatory affairs",
    "outlook_status": "strong",
    "outlook_reasons": "growing demand for new medicines and COVID-era pharmaceutical expansion",
    "outlook_advice": "highly promising for those interested in medicine and chemistry"
  },

  "Toxicologist": {
    "skills": "toxicology, biochemistry, risk assessment, regulatory knowledge",
    "specific_skills": "dose-response analysis, LC-MS, toxicokinetics, report writing",
    "daily_tasks": "testing chemicals for toxicity, assessing exposure risks, preparing safety data",
    "collaborators": "environmental scientists, medical professionals, product developers",
    "projects": "chemical safety testing, product approval documentation, clinical trial monitoring",
    "degree_suggestion": "Toxicology, Pharmacology, or Biochemistry",
    "experience_suggestion": "labs specializing in environmental or product safety, research assistant roles",
    "min_salary": "₹4,00,000",
    "max_salary": "₹16,00,000",
    "relevant_courses": "toxicology, human physiology, environmental chemistry, bioethics",
    "outlook_status": "growing",
    "outlook_reasons": "increased focus on environmental and consumer product safety",
    "outlook_advice": "good path for combining chemistry and public safety interests"
  },

  "Forensic Chemist": {
    "skills": "forensic analysis, analytical chemistry, criminal law basics, evidence handling",
    "specific_skills": "FTIR, toxicology screening, fingerprint powder testing, forensic reporting",
    "daily_tasks": "analyzing crime scene evidence, documenting procedures, testifying in court",
    "collaborators": "law enforcement, forensic pathologists, legal teams",
    "projects": "drug analysis, trace material examination, fire debris testing",
    "degree_suggestion": "Forensic Science, Chemistry, or Biochemistry",
    "experience_suggestion": "crime lab internships, forensic science workshops, mock investigations",
    "min_salary": "₹4,50,000",
    "max_salary": "₹13,00,000",
    "relevant_courses": "forensic chemistry, criminalistics, analytical techniques, criminal law",
    "outlook_status": "strong",
    "outlook_reasons": "growing interest in forensic science and crime investigation",
    "outlook_advice": "excellent for analytical minds with a passion for justice"
  },

  "Analytical Chemist": {
    "skills": "instrumental analysis, chemical quantification, lab data interpretation",
    "specific_skills": "HPLC, UV-Vis spectroscopy, titration, precision measurement",
    "daily_tasks": "testing substances for quality, analyzing material components, producing reports",
    "collaborators": "R&D teams, quality control staff, manufacturing units",
    "projects": "product testing, method development, contamination detection",
    "degree_suggestion": "Chemistry or Analytical Chemistry",
    "experience_suggestion": "internships in QC/QA labs, certification in instrumentation",
    "min_salary": "₹3,50,000",
    "max_salary": "₹10,00,000",
    "relevant_courses": "instrumental methods, data analysis, quality control",
    "outlook_status": "steady",
    "outlook_reasons": "constant need in pharmaceuticals, food, and materials sectors",
    "outlook_advice": "solid and versatile chemistry career"
  },

  "Materials Scientist": {
    "skills": "materials engineering, nanotechnology, polymer science, microscopy",
    "specific_skills": "XRD, SEM, tensile testing, material synthesis",
    "daily_tasks": "researching material properties, developing new materials, writing reports",
    "collaborators": "engineers, physicists, product designers",
    "projects": "creating stronger/lighter materials, sustainable alternatives, coatings",
    "degree_suggestion": "Materials Science, Chemistry, or Physics",
    "experience_suggestion": "internships in R&D labs, academic research projects",
    "min_salary": "₹5,00,000",
    "max_salary": "₹18,00,000",
    "relevant_courses": "solid-state chemistry, nanomaterials, mechanical testing",
    "outlook_status": "very strong",
    "outlook_reasons": "key role in technological innovation, especially in electronics and aerospace",
    "outlook_advice": "excellent for innovation-focused chemists"
  },

  "Polymer Chemist": {
    "skills": "polymer science, thermoplastics, polymer synthesis, rheology",
    "specific_skills": "extrusion, injection molding, FTIR, DSC analysis",
    "daily_tasks": "designing polymers, testing plastic properties, optimizing production",
    "collaborators": "chemical engineers, product developers, manufacturing teams",
    "projects": "biodegradable plastics, packaging materials, high-performance rubbers",
    "degree_suggestion": "Polymer Science, Chemical Engineering, or Chemistry",
    "experience_suggestion": "plastics industry internships, research in material development",
    "min_salary": "₹4,00,000",
    "max_salary": "₹14,00,000",
    "relevant_courses": "polymer chemistry, materials processing, thermodynamics",
    "outlook_status": "growing",
    "outlook_reasons": "need for sustainable and high-performance materials",
    "outlook_advice": "great for those interested in plastics and sustainability"
  },

  "UI/UX Designer": {
    "skills": "user interface design, user experience principles, wireframing, prototyping, usability testing",
    "specific_skills": "Figma, Adobe XD, Sketch, user research, design thinking",
    "daily_tasks": "designing user interfaces, conducting user research, testing prototypes, collaborating with developers",
    "collaborators": "product managers, developers, graphic designers",
    "projects": "app UI redesigns, website user flow optimization, user testing",
    "degree_suggestion": "Interaction Design, Graphic Design, or related field",
    "experience_suggestion": "design internships, UX case studies, personal portfolio projects",
    "min_salary": "₹4,00,000",
    "max_salary": "₹18,00,000",
    "relevant_courses": "UI design, human-computer interaction, usability testing",
    "outlook_status": "very strong",
    "outlook_reasons": "growing need for digital products with great user experience",
    "outlook_advice": "strong career for creative and user-focused thinkers"
  },

  "Graphic Designer": {
    "skills": "visual communication, layout, typography, branding, digital illustration",
    "specific_skills": "Adobe Photoshop, Illustrator, InDesign, Canva",
    "daily_tasks": "creating visuals for marketing, branding materials, social media graphics",
    "collaborators": "marketing teams, art directors, web developers",
    "projects": "logo designs, brochures, social campaigns, branding kits",
    "degree_suggestion": "Graphic Design, Fine Arts, or Visual Communication",
    "experience_suggestion": "freelance work, internships, online portfolio",
    "min_salary": "₹3,00,000",
    "max_salary": "₹12,00,000",
    "relevant_courses": "visual design, branding, digital art tools",
    "outlook_status": "strong",
    "outlook_reasons": "demand in advertising, content creation, and branding",
    "outlook_advice": "ideal for creative individuals with strong visual sense"
  },

  "Product Designer": {
    "skills": "design strategy, UI/UX, product thinking, prototyping, usability",
    "specific_skills": "Figma, Adobe XD, prototyping tools, design systems",
    "daily_tasks": "creating product workflows, collaborating with teams, refining user experiences",
    "collaborators": "developers, product managers, business analysts",
    "projects": "app design, feature UX improvement, product branding",
    "degree_suggestion": "Product Design, UX Design, or Human-Centered Design",
    "experience_suggestion": "startup projects, internships, real-world product redesigns",
    "min_salary": "₹5,00,000",
    "max_salary": "₹22,00,000",
    "relevant_courses": "UX design, product thinking, digital prototyping",
    "outlook_status": "very strong",
    "outlook_reasons": "booming product-centric tech industry",
    "outlook_advice": "perfect for those who blend creativity with functionality"
  },

  "Animator": {
    "skills": "2D/3D animation, character design, storytelling, motion graphics",
    "specific_skills": "Blender, After Effects, Maya, Toon Boom",
    "daily_tasks": "creating animation sequences, editing frames, collaborating with creative teams",
    "collaborators": "illustrators, directors, sound designers",
    "projects": "animated videos, explainer content, films, game animations",
    "degree_suggestion": "Animation, Multimedia Design, or Fine Arts",
    "experience_suggestion": "animated short films, internships, YouTube channel, portfolio",
    "min_salary": "₹3,50,000",
    "max_salary": "₹15,00,000",
    "relevant_courses": "motion graphics, animation principles, rigging",
    "outlook_status": "strong",
    "outlook_reasons": "demand in media, gaming, and digital content",
    "outlook_advice": "great field for storytellers and visual artists"
  },

  "Fashion Designer": {
    "skills": "fashion illustration, fabric knowledge, garment construction, trend forecasting",
    "specific_skills": "Adobe Illustrator, CLO 3D, pattern making",
    "daily_tasks": "sketching designs, choosing fabrics, collaborating with tailors, managing collections",
    "collaborators": "models, stylists, fashion merchandisers",
    "projects": "fashion lines, seasonal collections, runway outfits",
    "degree_suggestion": "Fashion Design, Textile Design, or Apparel Production",
    "experience_suggestion": "fashion internships, student shows, design portfolio",
    "min_salary": "₹3,00,000",
    "max_salary": "₹18,00,000",
    "relevant_courses": "textiles, fashion illustration, draping",
    "outlook_status": "growing",
    "outlook_reasons": "rising fashion startups and e-commerce",
    "outlook_advice": "suits trendsetters with creative flair"
  },

  "Interior Designer": {
    "skills": "spatial planning, aesthetics, color theory, CAD software",
    "specific_skills": "AutoCAD, SketchUp, 3ds Max, V-Ray",
    "daily_tasks": "designing interiors, selecting materials and colors, consulting with clients",
    "collaborators": "architects, contractors, furniture designers",
    "projects": "home renovations, commercial spaces, hotel lobbies",
    "degree_suggestion": "Interior Design, Architecture, or Fine Arts",
    "experience_suggestion": "interior design internships, renovation projects, design portfolio",
    "min_salary": "₹3,50,000",
    "max_salary": "₹15,00,000",
    "relevant_courses": "space planning, lighting design, CAD tools",
    "outlook_status": "steady",
    "outlook_reasons": "demand in real estate and luxury sectors",
    "outlook_advice": "for those with a strong eye for aesthetics and space"
  },

  "Game Designer": {
    "skills": "game mechanics, storytelling, level design, user engagement",
    "specific_skills": "Unity, Unreal Engine, C#, game balancing",
    "daily_tasks": "designing gameplay systems, building prototypes, testing game loops",
    "collaborators": "game developers, artists, sound designers",
    "projects": "video games, mobile games, VR experiences",
    "degree_suggestion": "Game Design, Computer Science, or Interactive Media",
    "experience_suggestion": "game jams, indie projects, modding communities",
    "min_salary": "₹4,00,000",
    "max_salary": "₹20,00,000",
    "relevant_courses": "game development, 3D design, narrative writing",
    "outlook_status": "very strong",
    "outlook_reasons": "growing global game industry and mobile gaming boom",
    "outlook_advice": "best for gamers with creative and technical skills"
  },

  "3D Modeler": {
    "skills": "3D modeling, sculpting, texturing, UV mapping",
    "specific_skills": "Blender, Maya, ZBrush, Substance Painter",
    "daily_tasks": "creating 3D assets, working on game or movie visuals, optimizing models",
    "collaborators": "animators, game developers, VFX artists",
    "projects": "game characters, movie props, architectural visualization",
    "degree_suggestion": "Animation, Game Design, or 3D Art",
    "experience_suggestion": "personal models, 3D portfolios, freelance gigs",
    "min_salary": "₹3,00,000",
    "max_salary": "₹14,00,000",
    "relevant_courses": "3D modeling, digital sculpting, texturing",
    "outlook_status": "growing",
    "outlook_reasons": "demand in gaming, film, and AR/VR industries",
    "outlook_advice": "a top pick for detail-oriented digital artists"
  },

  "Textile Designer": {
    "skills": "pattern design, fabric knowledge, color theory, textile technology",
    "specific_skills": "Adobe Illustrator, textile CAD software, weaving/knitting methods",
    "daily_tasks": "creating patterns, experimenting with fabrics, collaborating with manufacturers",
    "collaborators": "fashion designers, fabric technologists, dyeing specialists",
    "projects": "print collections, fabric lines, fashion fabric R&D",
    "degree_suggestion": "Textile Design, Fashion Technology, or Fine Arts",
    "experience_suggestion": "fabric workshops, internships in mills or brands",
    "min_salary": "₹2,80,000",
    "max_salary": "₹10,00,000",
    "relevant_courses": "surface design, textile chemistry, color theory",
    "outlook_status": "steady",
    "outlook_reasons": "ongoing demand in fashion and home textiles",
    "outlook_advice": "great fit for those who love fabric art and design"
  },

  "Exhibition Designer": {
    "skills": "spatial design, storytelling, lighting, branding",
    "specific_skills": "SketchUp, Adobe Suite, AutoCAD, exhibition planning tools",
    "daily_tasks": "designing layouts, coordinating materials, ensuring theme alignment",
    "collaborators": "event planners, curators, construction teams",
    "projects": "museum exhibits, trade shows, gallery installations",
    "degree_suggestion": "Exhibition Design, Interior Design, or Communication Design",
    "experience_suggestion": "museum internships, event design freelancing",
    "min_salary": "₹3,00,000",
    "max_salary": "₹12,00,000",
    "relevant_courses": "exhibition planning, visual storytelling, lighting design",
    "outlook_status": "niche",
    "outlook_reasons": "demand tied to museum and event sectors",
    "outlook_advice": "excellent for creative spatial thinkers"
  },

  "Visual Merchandiser": {
    "skills": "retail design, customer behavior, visual storytelling, trend forecasting",
    "specific_skills": "store layout planning, POS displays, mannequins, color coordination",
    "daily_tasks": "setting up store displays, aligning branding visuals, analyzing sales data",
    "collaborators": "retail managers, fashion merchandisers, marketing teams",
    "projects": "window displays, seasonal themes, store rebranding",
    "degree_suggestion": "Visual Merchandising, Fashion Retail, or Design",
    "experience_suggestion": "retail internships, store styling, visual branding practice",
    "min_salary": "₹2,50,000",
    "max_salary": "₹10,00,000",
    "relevant_courses": "retail marketing, design principles, color theory",
    "outlook_status": "growing",
    "outlook_reasons": "retail innovation and competition",
    "outlook_advice": "perfect for creative minds in fashion and retail"
  },


  "Nanochemist": {
    "skills": "nanotechnology, quantum chemistry, surface science, lab techniques",
    "specific_skills": "AFM, TEM, nanoparticle synthesis, nanoscale characterization",
    "daily_tasks": "designing nanoscale materials, conducting experiments, analyzing results",
    "collaborators": "physicists, materials scientists, biomedical engineers",
    "projects": "drug delivery systems, nano-coatings, nanomaterials for electronics",
    "degree_suggestion": "Nanotechnology, Chemistry, or Materials Science",
    "experience_suggestion": "research internships in nanotech labs, interdisciplinary projects",
    "min_salary": "₹5,50,000",
    "max_salary": "₹20,00,000",
    "relevant_courses": "nanoscience, surface chemistry, molecular engineering",
    "outlook_status": "very strong",
    "outlook_reasons": "emerging applications in medicine, electronics, and energy",
    "outlook_advice": "excellent long-term growth potential in cutting-edge science"
  }



}

# Simulates typing delay for a more natural conversation flow
def simulate_typing_delay():
    time.sleep(0.5)

# Function to find a role mentioned in the user's input
def find_role_in_input(user_input):
    user_input_lower = user_input.lower()
    all_roles = []
    # Collect all role names from the career_map, preserving original capitalization
    for field_data in career_map.values():
        for interest_data in field_data.values():
            all_roles.extend(interest_data)

    # Sort roles by length (descending) to match longer phrases first (e.g., "Software Engineer" before "Engineer")
    all_roles_sorted = sorted(all_roles, key=len, reverse=True)

    for role in all_roles_sorted:
        # Use regex for whole word matching (\b) to avoid partial matches (e.g., "bio" in "biologist")
        # re.escape() handles special characters in role names if any
        if re.search(r'\b' + re.escape(role.lower()) + r'\b', user_input_lower):
            return role # Return the original capitalized role from the list
    return None


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_input_raw = data.get('message', '').lower()
    current_field = data.get('field')
    current_interest = data.get('interest')

    print(f"Received: message='{user_input_raw}', field='{current_field}', interest='{current_interest}'")

    response_answer = "I'm sorry, I couldn't understand your input. Could you please clarify or choose from the options?"
    response_choices = None # Default to no choices

    # Predict intent using the loaded NLP model
    predicted_intent = None
    if nlp_model:
        predicted_intent = nlp_model.predict([user_input_raw])[0]
        print(f"Predicted Intent: {predicted_intent}")

    # --- Conversation Flow Logic ---

    # PRIORITY 1: Handle Specific Questions about Roles (NLP-driven)
    # This comes first so direct queries like "salary of a data scientist" are handled immediately.
    target_role = find_role_in_input(user_input_raw)

    if target_role and predicted_intent in specific_role_questions:
        info_response = role_details.get(target_role)
        if info_response:
            try:
                # Format the answer using the template and role details
                formatted_answer = specific_role_questions[predicted_intent].format(role=target_role, **info_response)
                simulate_typing_delay()
                return jsonify({"answer": formatted_answer, "choices": response_choices})
            except KeyError as e:
                print(f"Missing data for intent '{predicted_intent}' and role '{target_role}': {e}")
                response_answer = f"I'm sorry, I don't have enough information for {target_role} regarding {predicted_intent.replace('get_', '').replace('_', ' ')}."
                simulate_typing_delay()
                return jsonify({"answer": response_answer, "choices": response_choices})
        else:
            # Role found, but no detailed info for it
            response_answer = f"I don't have detailed information for the role: {target_role} yet. Please ask about a different one, or choose from suggested options."
            simulate_typing_delay()
            return jsonify({"answer": response_answer, "choices": response_choices})
    elif target_role:
        # If a role is identified, but the intent is not a specific question about it
        # This handles cases like "Tell me about Software Engineer" after picking a field
        response_answer = f"What would you like to know about a {target_role} role? You can ask things like 'what skills do I need', 'what does a day look like', 'salary', 'education needed', or 'job outlook'."
        simulate_typing_delay()
        return jsonify({"answer": response_answer, "choices": response_choices})


    # PRIORITY 2: Handle Greetings (NLP-driven)
    if predicted_intent == "greet":
        response_answer = "Hey there! I'm here to help you explore career paths. What field are you interested in?"
        response_choices = list(career_map.keys()) # Provide main field options
        simulate_typing_delay()
        return jsonify({"answer": response_answer, "choices": response_choices})

    # PRIORITY 3: Handle User Selecting a Main Field (from button click or direct text match)
    # This condition also covers direct text input like "science" if current_field is None
    if user_input_raw in career_map and not current_field:
        response_answer = f"Great! Within {user_input_raw.capitalize()}, what specific area are you interested in? You can choose from: {', '.join([s.capitalize() for s in career_map[user_input_raw]])}."
        response_choices = list(career_map[user_input_raw].keys()) # Provide interest options
        simulate_typing_delay()
        return jsonify({"answer": response_answer, "choices": response_choices})
    

    # PRIORITY 4: Handle User Selecting an Interest (subfield) within an already chosen main field
    # This handles button clicks for interests or direct text input if current_interest is None
    if current_field and current_field in career_map:
        if user_input_raw in career_map[current_field] and not current_interest:
            suggested_careers = career_map[current_field][user_input_raw]
            response_answer = f"For {user_input_raw.capitalize()} within {current_field.capitalize()}, you might consider careers like: {', '.join(suggested_careers)}. Is there a specific role you'd like to know more about, or do you have another question?"
            response_choices = None # No choices here; user types a role or question
            simulate_typing_delay()
            return jsonify({"answer": response_answer, "choices": response_choices})
        # If current_field is set, but user input is not a recognized interest or a role,
        # it might still fall through to a fallback, but at least we tried to use context.


    # FINAL FALLBACK: For unhandled inputs, unknown intents, or when no specific field/interest/role is determined
    # If the predicted intent is 'fallback' from NLP, or if no context was built yet.
    if predicted_intent == "fallback" or (not current_field and not current_interest and not target_role):
        response_answer = "I'm here to guide you through career options! To start, please select a field from the list or type a greeting like 'Hi'."
        response_choices = list(career_map.keys()) # Re-suggest main fields
    else:
        # Generic fallback if a specific intent wasn't matched or role wasn't found in context
        response_answer = "I'm sorry, I couldn't find specific information for that. Could you try rephrasing your question, or ask about specific skills, daily tasks, or salary for a role?"
        response_choices = None # No choices for this generic fallback

    simulate_typing_delay()
    return jsonify({"answer": response_answer, "choices": response_choices})


if __name__ == '__main__':
    # For development, run on port 5000 and enable debug mode
    app.run(debug=True, port=5000)