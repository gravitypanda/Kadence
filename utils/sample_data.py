from faker import Faker
from datetime import datetime, timedelta, date
import random
import uuid
from models.schemas import Contact, Category, CadenceFrequency

fake = Faker()

def generate_sample_categories() -> list[Category]:
    categories = [
        Category(
            id=str(uuid.uuid4()),
            name="Real Estate Client",
            description="Past and potential real estate clients",
            rule_text="Include local market updates and property value trends. End with 'Looking forward to helping you with your next real estate journey!'",
            precedence_order=1
        ),
        Category(
            id=str(uuid.uuid4()),
            name="Pickleball",
            description="Pickleball playing partners",
            rule_text="Always include a PS about playing soon. Reference recent games or tournaments.",
            precedence_order=2
        ),
        Category(
            id=str(uuid.uuid4()),
            name="Business Referral",
            description="Professional network and referral partners",
            rule_text="Maintain professional tone. Include recent business wins or industry news.",
            precedence_order=3
        ),
        Category(
            id=str(uuid.uuid4()),
            name="Local Business",
            description="Local business owners and partners",
            rule_text="Reference local events and community news. Keep it community-focused.",
            precedence_order=4
        )
    ]
    return categories

def generate_sample_contacts(categories: list[Category], num_contacts: int = 10) -> list[Contact]:
    contacts = []
    
    for _ in range(num_contacts):
        # Randomly select 1-3 categories
        contact_categories = random.sample([cat.id for cat in categories], k=random.randint(1, 3))
        
        # Generate a random next outreach date between now and 30 days from now
        next_outreach = datetime.now() + timedelta(days=random.randint(1, 30))
        
        contact = Contact(
            id=str(uuid.uuid4()),
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            special_dates={"birthday": fake.date_of_birth(minimum_age=25, maximum_age=80)},
            categories=contact_categories,
            personal_instructions=random.choice([None, "Always mention our shared love of coffee", "Reference our last golf game", "Ask about their kids"]),
            cadence_frequency=random.choice(list(CadenceFrequency)),
            next_outreach_date=next_outreach,
            relevant_websites=[fake.url() for _ in range(random.randint(0, 2))],
            keywords=random.sample(["real estate", "local news", "pickleball", "business", "technology"], k=random.randint(0, 3)),
            last_contact=datetime.now() - timedelta(days=random.randint(7, 90))
        )
        contacts.append(contact)
    
    return contacts 