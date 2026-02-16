(base) miked@Johns-iMac ai-rag-labs %  cd /Users/miked/Documents/Code_Louisville_Project/CY_Data_AI/ai-rag-labs ; /usr/bin/env /opt
/anaconda3/bin/python /Users/miked/.vscode/extensions/ms-python.debugpy-2025.18.0-darwin-x64/bundled/libs/debugpy/adapter/../../deb
ugpy/launcher 59455 -- /Users/miked/Documents/Code_Louisville_Project/CY_Data_AI/ai-rag-labs/app.py 
python-dotenv could not parse statement starting at line 1
python-dotenv could not parse statement starting at line 2
🤖 Python LangChain Agent Starting...

=== Loading Documents into Vector Database ===

✓ Successfully loaded 'HealthInsuranceBrochure.md' (4631 characters, 1176 tokens)
✓ Document successfully stored with ID: 2f490254-d76d-4778-ade7-c0dd8d3845c2

📑 Markdown Structure-Based Chunking Statistics for 'EmployeeHandbook.md':
   - Number of chunks: 11
   - Average chunk size: 2685 characters
   - Smallest chunk: 658 characters
   - Largest chunk: 4502 characters
   - Chunk overlap: 200 characters
   - Chunks with header metadata: 11
   - Total content size: 29537 characters

📦 Loading 11 chunks from 'EmployeeHandbook.md'...

   ✓ Chunk 1/11 processed (658 characters)
   ✓ Chunk 2/11 processed (1993 characters)
   ✓ Chunk 3/11 processed (4453 characters)
   ✓ Chunk 4/11 processed (4502 characters)
   ✓ Chunk 5/11 processed (2299 characters)
   ✓ Chunk 6/11 processed (1990 characters)
   ✓ Chunk 7/11 processed (2203 characters)
   ✓ Chunk 8/11 processed (3424 characters)
   ✓ Chunk 9/11 processed (2324 characters)
   ✓ Chunk 10/11 processed (2359 characters)
   ✓ Chunk 11/11 processed (3332 characters)

✓ Successfully loaded all 11 chunks from 'EmployeeHandbook.md'

✓ Successfully stored 11 chunks from EmployeeHandbook

=== Setting Up ReAct Agent ===

✓ Agent successfully initialized

============================================================
🤖 Company Document Assistant
============================================================
Welcome! I'm an AI assistant trained on company policies, benefits, and procedures.
I can help answer your questions about:
  • Employee benefits and insurance
  • Company policies and procedures
  • HR guidelines and requirements

Type 'quit' or 'exit' to end the conversation.
============================================================

You: What health insurance benefits does the company offer?

Agent: The company offers a comprehensive range of health insurance benefits to support employees and their families. Here’s a detailed breakdown of the available options:

### **Medical Insurance Plans**
Employees can choose from three medical insurance plans provided by Aetna:

1. **PPO High Plan (Maximum Coverage)**:
   - Low deductible: $500 (individual) / $1,000 (family)
   - $20 copay for primary care visits
   - The company covers **85% of premiums**
   - Employee cost: **$95/month** (individual)

2. **PPO Standard Plan (Balanced Value)**:
   - Deductible: $1,500 (individual) / $3,000 (family)
   - Nationwide network access
   - The company covers **80% of premiums**
   - Employee cost: **$75/month** (individual)

3. **High Deductible Health Plan (HDHP) with HSA**:
   - Best for healthy employees who want to save
   - The company covers **90% of premiums**
   - Lowest cost: **$50/month** (individual)
   - Includes **$1,000-$2,000 employer contribution** to a Health Savings Account (HSA)

### **Dental Insurance**
1. **Dental PPO**:
   - 100% coverage for preventive care (e.g., cleanings, exams)
   - $2,000 annual maximum
   - Orthodontia coverage available

2. **Dental HMO**:
   - **100% free for employees** (no monthly cost)
   - Fixed low copays (e.g., $5 for cleanings)
   - No deductibles or annual maximum

### **Vision Insurance**
- Fully paid by the company (no cost to employees)
- $10 copay for eye exams
- $130 annual allowance for frames
- Contact lens option available
- 15% discount on laser vision correction

### **Tax-Advantaged Accounts**
1. **Health Savings Account (HSA)** (for HDHP participants):
   - Employer contribution: $1,000 (individual) or $2,000 (family) annually
   - Employee contributions are pre-tax
   - Funds roll over year to year and can be invested for retirement

2. **Flexible Spending Accounts (FSA)** (for PPO plans):
   - Healthcare FSA: Contribute up to $3,200/year pre-tax
   - Dependent Care FSA: Contribute up to $5,000/year for childcare or eldercare expenses

### **Life and Disability Insurance**
1. **Basic Life Insurance**:
   - Fully paid by the company
   - Coverage equal to your annual salary (up to $250,000)
   - Includes Accidental Death & Dismemberment (AD&D)

2. **Disability Insurance**:
   - **Short-term disability**: 60% salary replacement for up to 26 weeks
   - **Long-term disability**: 60% salary replacement until age 65
   - Both are fully paid by the company

3. **Supplemental Life Insurance** (optional):
   - Additional coverage up to 5x your salary
   - Coverage available for spouse and children at affordable rates

### **Additional Wellness Perks**
- **24/7 Telemedicine**: Access to doctors anytime, anywhere
- **Free Annual Health Screenings** with wellness incentives
- **Employee Assistance Program (EAP)**: 6 free counseling sessions per year
- **Free Flu Shots** at the office
- **20% Gym Membership Discount**
- **Smoking Cessation Support**

### **Eligibility and Enrollment**
- **Full-time employees**: Coverage starts the first of the month after 30 days of employment
- **Part-time employees (30+ hours/week)**: Coverage starts the first of the month after 60 days
- Dependents, including spouses, domestic partners, and children up to age 26, are eligible for coverage.

### **Enrollment Periods**
- **New hires**: Must enroll within 30 days of hire
- **Annual Open Enrollment**: Held every November
- **Qualifying Life Events**: Changes allowed within 30 days of events like marriage, birth, or adoption

### **Monthly Premium Costs (Employee Portion)**

| Coverage Tier         | PPO High | PPO Standard | HDHP |
|------------------------|----------|--------------|------|
| Individual             | $95      | $75          | $50  |
| Employee + Spouse      | $210     | $170         | $125 |
| Employee + Child(ren)  | $185     | $150         | $110 |
| Family                 | $295     | $240         | $180 |

The company covers 80-90% of the total premium cost.

For more information or assistance with selecting the right plan, you can contact the **HR Benefits Team** at benefits@techcorpsolutions.com or call Ext. 5000.