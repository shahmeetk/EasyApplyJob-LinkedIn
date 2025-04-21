default_resume_path = "all resumes/default/NewResume.pdf"      # (In Development)

# What do you want to answer for questions that ask about years of experience you have, this is different from current_experience?
years_of_experience = "15"         # A number in quotes Eg: "0","1","2","3","4", etc.

# Do you need visa sponsorship now or in future?
require_visa = "No"               # "Yes" or "No"

# What is the link to your portfolio website, leave it empty as "", if you want to leave this question unanswered
website = "https://shahmeetk.github.io"                        # "www.example.bio" or "" and so on....

# Please provide the link to your LinkedIn profile.
linkedIn = "https://www.linkedin.com/in/meetshah10290/"       # "https://www.linkedin.com/in/example" or "" and so on...

# What is the status of your citizenship? # If left empty as "", tool will not answer the question. However, note that some companies make it compulsory to be answered
# Valid options are: "U.S. Citizen/Permanent Resident", "Non-citizen allowed to work for any employer", "Non-citizen allowed to work for current employer", "Non-citizen seeking work authorization", "Canadian Citizen/Permanent Resident" or "Other"
us_citizenship = "Other"


## SOME ANNOYING QUESTIONS BY COMPANIES 🫠 ##

# What to enter in your desired salary question (AED), What is your expected CTC?, only enter in numbers as some companies only allow numbers,
desired_salary = 55000          # 200000, 240000, 300000 or 360000 and so on... Do NOT use quotes
'''
Note: If question has the word "thousands" in it (Example: What is your expected CTC in thousands),
then it will divide by 1000 and answer. Examples:
* 240000 will be answered as "240.00"
* 85000 will be answered as "85.00"
And if asked in months, then it will divide by 12 and answer. Examples:
* 240000 will be answered as "20000"
* 85000 will be answered as "7083"
'''

# What is your current CTC? Some companies make it compulsory to be answered in numbers...
current_ctc = 45000            # 800000, 900000, 1000000 or 1200000 and so on... Do NOT use quotes
'''
Note: If question has the word "lakhs" in it (Example: What is your current CTC in lakhs),
then it will add '.' before last 5 digits and answer. Examples:
* 2400000 will be answered as "24.00"
* 850000 will be answered as "8.50"
# And if asked in months, then it will divide by 12 and answer. Examples:
# * 2400000 will be answered as "200000"
# * 850000 will be answered as "70833"
'''

# (In Development) # Currency of salaries you mentioned. Companies that allow string inputs will add this tag to the end of numbers. Eg:
currency = "AED"                 # "USD", "INR", "EUR", etc.

# What is your notice period in days?
notice_period = 60                   # Any number >= 0 without quotes. Eg: 0, 7, 15, 30, 45, etc.
'''
Note: If question has 'month' or 'week' in it (Example: What is your notice period in months),
then it will divide by 30 or 7 and answer respectively. Examples:
* For notice_period = 66:
  - "66" OR "2" if asked in months OR "9" if asked in weeks
* For notice_period = 15:"
  - "15" OR "0" if asked in months OR "2" if asked in weeks
* For notice_period = 0:
  - "0" OR "0" if asked in months OR "0" if asked in weeks
'''

# Your LinkedIn headline in quotes Eg: "Software Engineer @ Google, Masters in Computer Science", "Recent Grad Student @ MIT, Computer Science"
linkedin_headline = "Cloud & AI Practice Lead | AIOps | DevSecOps | Multi-Cloud Architect" # "Headline" or "" to leave this question unanswered

# Your summary in quotes, use \n to add line breaks if using single quotes "Summary".You can skip \n if using triple quotes """Summary"""
linkedin_summary = """
Cloud Transformation Leader with 15+ years of experience architecting secure, scalable infrastructure and driving enterprise digital transformations. Proven track record in implementing AiOps & full-stack DevSecOps pipelines, cloud-native platforms (AWS, Azure, GCP), and leading multi-cloud strategies across fintech and payment solutions. Evolved responsibilities into AI-enhanced operations (AIOps) — applying machine learning to observability, cost optimization, workflow automation, and merchant onboarding. Passionate about simplifying complexity through automation, mentoring high-performance teams, and building secure, compliant, high-availability systems across international markets. Expert in optimising and automating testing and release cycles, significantly accelerating time-to-market.
"""

'''
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
'''

# Your cover letter in quotes, use \n to add line breaks if using single quotes "Cover Letter".You can skip \n if using triple quotes """Cover Letter""" (This question makes sense though)
cover_letter = """
Dear Hiring Manager,

I am writing to express my interest in the given position at your organization. With over 15 years of experience in AI Engineering, multi-cloud transformation, DevSecOps implementation, and AI-enhanced operations, I believe my skills and experience align perfectly with your requirements.

As the Cloud & AI Practice Lead at Network International LLC, I've driven end-to-end AI-based Digital Transformation for Payment Gateway Platforms, architected hybrid cloud programs across Azure, AWS, and Oracle Cloud, and implemented AI-based automation that enabled 60% faster merchant onboarding.

I am particularly interested in bringing my expertise in cloud architecture, AI implementation, and security compliance to your team. My experience with Kubernetes, Terraform, and implementing zero-trust security architectures would be valuable assets to your organization.

Thank you for considering my application. I look forward to the opportunity to discuss how my skills and experience can contribute to your team's success.

Sincerely,
Meet Shah
"""

# Your user_information_all letter in quotes, use \n to add line breaks if using single quotes "user_information_all".You can skip \n if using triple quotes """user_information_all""" (This question makes sense though)
# We use this to pass to AI to generate answer from information , Assuing Information contians eg: resume  all the information like name, experience, skills, Country, any illness etc.
user_information_all ="""
Name: Meet Shah
Email: shahmeetk@gmail.com
Phone: +971562201306
Location: Dubai, UAE
Website: https://shahmeetk.github.io
LinkedIn: https://www.linkedin.com/in/meetshah10290/
Github: https://github.com/shahmeetk

Headline: Cloud & AI Practice Lead | AIOps | DevSecOps | Multi-Cloud Architect

Summary: Cloud Transformation Leader with 15+ years of experience architecting secure, scalable infrastructure and driving enterprise digital transformations. Proven track record in implementing AiOps & full-stack DevSecOps pipelines, cloud-native platforms (AWS, Azure, GCP), and leading multi-cloud strategies across fintech and payment solutions.

Experience:
- Cloud & AI Practice Lead at Network International LLC (Oct 2020 – Present)
- Lead Site Reliability Engineer, DevSecOps Role at Emirates Group IT (April 2019 – Oct 2020)
- Sr. Software Engineer, Lead DevOps Role at eInfochips (Oct 2016 – Apr 2019)
- Sr. Software Engineer, CloudOps Role at Sophos (Dec 2015 – Oct 2016)

Education:
- Ph.D., Computer Science (Ongoing) - Gujarat University
- M.Tech., Networking & Cloud Technology - Gujarat University (2014)
- B.E., Electronics & Telecommunication Engineering - Sardar Patel University (2011)

Skills:
- AI/ML & AIOps: AI Flow Builder, Agent Creation, OpenTelemetry, Grafana, Azure ML, Databricks
- DevSecOps & CI/CD: Jenkins, GitHub Actions, Terraform, Kubernetes, Docker, OpenShift
- Cloud Platforms: AWS, Azure, GCP, Oracle Cloud
- Security: Prisma Cloud, Veracode, Snyk, CrowdStrike, Azure Defender

Certifications:
- AI Certifications: ISO 42001 Lead AI Auditor, Azure AI Fundamentals, AWS AI Certified Engineer
- Microsoft Certified: DevOps Engineer Expert, Azure Architect Technologies
- AWS: Certified DevOps Engineer - Professional, Solutions Architect – Associate
- GCP: Big Data and Machine Learning Fundamentals, DevOps Architect Expert
"""
##<
'''
Note: If left empty as "", the tool will not answer the question. However, note that some companies make it compulsory to be answered. Use \n to add line breaks.
'''

# Name of your most recent employer
recent_employer = "Network International LLC" # "", "Lala Company", "Google", "Snowflake", "Databricks"

# Example question: "On a scale of 1-10 how much experience do you have building web or mobile applications? 1 being very little or only in school, 10 being that you have built and launched applications to real users"
confidence_level = "8"             # Any number between "1" to "10" including 1 and 10, put it in quotes ""
##

run_in_background = True

# >>>>>>>>>>> RELATED SETTINGS <<<<<<<<<<<

## Allow Manual Inputs
# Should the tool pause before every submit application during easy apply to let you check the information?
pause_before_submit = True         # True or False, Note: True or False are case-sensitive
'''
Note: Will be treated as False if `run_in_background = True`
'''

# Should the tool pause if it needs help in answering questions during easy apply?
# Note: If set as False will answer randomly...
pause_at_failed_question = True    # True or False, Note: True or False are case-sensitive
'''
Note: Will be treated as False if `run_in_background = True`
'''
##

# Do you want to overwrite previous answers?
overwrite_previous_answers = False # True or False, Note: True or False are case-sensitive
