import os
import json
import requests
from pathlib import Path

print("=" * 60)
print(" DOWNLOADING IEEE SB VIT PUNE CHATBOT DATASET")
print("=" * 60)

# Create data directory if not exists
os.makedirs('data', exist_ok=True)

# Option 1: Download from Hugging Face (Recommended)
def download_from_huggingface():
    try:
        from datasets import load_dataset
        print("\n Loading dataset from Hugging Face...")
        
        # Load dataset
        dataset = load_dataset("IEEEVITPune-AI-Team/chatbotAlpha")
        
        # Convert to list
        data = []
        for split in dataset.keys():
            for item in dataset[split]:
                data.append({
                    "instruction": item.get("instruction", ""),
                    "response": item.get("response", ""),
                    "category": item.get("category", "general")
                })
        
        print(f" Downloaded {len(data)} QA pairs")
        return data
        
    except Exception as e:
        print(f" Hugging Face download failed: {e}")
        return None

# Option 2: Manual dataset (if Hugging Face fails)
def create_sample_dataset():
    """Create a larger sample dataset with college-related Q&A"""
    
    print("\n Creating enhanced sample dataset...")
    
    # College-specific Q&A
    sample_data = [
        {
            "instruction": "What courses are available in college?",
            "response": "We offer B.Tech in Computer Science, Information Technology, Electronics & Communication, and M.Tech programs. We also have MBA and MCA courses.",
            "category": "academics"
        },
        {
            "instruction": "How is the placement record?",
            "response": "Our placement cell has achieved 90% placement record with top companies like Google, Amazon, Microsoft, TCS, Infosys, and Wipro. The highest package offered was ₹45 LPA.",
            "category": "placements"
        },
        {
            "instruction": "What is the admission process?",
            "response": "Admission is based on entrance exam scores (JEE Main for B.Tech) and academic performance. You need to register online, submit documents, and attend counseling.",
            "category": "admissions"
        },
        {
            "instruction": "What are the hostel facilities?",
            "response": "We have separate hostels for boys and girls with 24/7 security, Wi-Fi, mess facility, gym, and recreational areas. Hostel fees range from ₹80,000 to ₹1,20,000 per year.",
            "category": "facilities"
        },
        {
            "instruction": "What is the fee structure?",
            "response": "B.Tech annual fee is ₹1,50,000. Scholarships are available for meritorious students based on entrance exam rank and academic performance.",
            "category": "fees"
        },
        {
            "instruction": "Tell me about the campus facilities",
            "response": "Our campus has a library with 50,000+ books, sports complex with indoor and outdoor facilities, cafeteria, medical center, and 24/7 internet connectivity.",
            "category": "facilities"
        },
        {
            "instruction": "What research opportunities are available?",
            "response": "We have research centers in AI, Data Science, IoT, and Cybersecurity. Students can work on funded projects and publish papers in reputed journals.",
            "category": "research"
        },
        {
            "instruction": "How to apply for scholarships?",
            "response": "Scholarship applications are available online. Eligibility is based on academic performance and family income. The last date is usually March 31st.",
            "category": "admissions"
        },
        {
            "instruction": "What is the college ranking?",
            "response": "Our college is ranked among the top 50 engineering colleges in India by NIRF. We are also accredited by NAAC with A+ grade.",
            "category": "academics"
        },
        {
            "instruction": "Are there any exchange programs?",
            "response": "Yes, we have student exchange programs with universities in USA, UK, Germany, and Singapore. Applications open in December each year.",
            "category": "academics"
        },
        # Add more categories
        {
            "instruction": "What are the library timings?",
            "response": "Library is open from 8:00 AM to 10:00 PM on weekdays and 9:00 AM to 6:00 PM on weekends.",
            "category": "facilities"
        },
        {
            "instruction": "What sports facilities are available?",
            "response": "We have cricket ground, football field, basketball court, tennis court, swimming pool, and gymnasium.",
            "category": "facilities"
        },
        {
            "instruction": "How can I contact the admission office?",
            "response": "Admission office contact: +91-XXXXXXXXXX, email: admission@college.edu, or visit between 10 AM to 5 PM on weekdays.",
            "category": "contact"
        },
        {
            "instruction": "What companies come for placement?",
            "response": "Top recruiters include Google, Amazon, Microsoft, TCS, Infosys, Wipro, Cognizant, Accenture, and many more.",
            "category": "placements"
        },
        {
            "instruction": "Is there a campus interview process?",
            "response": "Yes, campus placements include pre-placement talks, aptitude tests, group discussions, technical interviews, and HR interviews.",
            "category": "placements"
        },
        {
            "instruction": "What is the student-teacher ratio?",
            "response": "Our college maintains a 15:1 student-teacher ratio to ensure personalized attention and quality education.",
            "category": "academics"
        },
        {
            "instruction": "Are there any clubs and societies?",
            "response": "We have technical clubs (Coding Club, Robotics Club), cultural clubs, sports clubs, and entrepreneurship cell. Students can join multiple clubs.",
            "category": "student_life"
        },
        {
            "instruction": "What events are organized in college?",
            "response": "We organize annual tech fest, cultural fest, sports meet, hackathons, workshops, and guest lectures throughout the year.",
            "category": "events"
        },
        {
            "instruction": "How is the faculty at this college?",
            "response": "Our faculty includes Ph.D. holders from IITs and NITs with years of teaching and research experience. Many have published in top journals.",
            "category": "academics"
        },
        {
            "instruction": "What is the attendance policy?",
            "response": "Students must maintain a minimum of 75% attendance in each subject to be eligible for semester examinations.",
            "category": "academics"
        }
    ]
    
    print(f" Created {len(sample_data)} enhanced sample QA pairs")
    return sample_data

def save_dataset(data, filename='data/ieee_dataset.json'):
    """Save dataset to file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f" Saved dataset to {filename}")
    return filename

def main():
    print("\n Downloading IEEE Chatbot Dataset...")
    
    # Try Hugging Face first
    data = download_from_huggingface()
    
    if data is None:
        print("\n Creating enhanced sample dataset instead...")
        data = create_sample_dataset()
    
    if data:
        save_dataset(data)
        print(f"\n Dataset Statistics:")
        print(f"   - Total QA Pairs: {len(data)}")
        
        # Count categories if available
        categories = {}
        for item in data:
            cat = item.get('category', 'general')
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"   - Categories: {len(categories)}")
        for cat, count in categories.items():
            print(f"      - {cat}: {count} pairs")
    
    print("\n" + "=" * 60)
    print(" DATASET DOWNLOAD COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    main()