from datetime import datetime, timedelta
from models.schemas import Contact, Category

def format_date(dt: datetime) -> str:
    """Format a datetime for display"""
    return dt.strftime("%B %d, %Y")

def get_next_outreach_date(contact: Contact) -> datetime:
    """Calculate the next outreach date based on cadence"""
    if contact.cadence_frequency == "weekly":
        return datetime.now() + timedelta(days=7)
    elif contact.cadence_frequency == "monthly":
        return datetime.now() + timedelta(days=30)
    elif contact.cadence_frequency == "quarterly":
        return datetime.now() + timedelta(days=90)
    else:  # custom - default to monthly
        return datetime.now() + timedelta(days=30)

def get_category_by_id(categories: list[Category], category_id: str) -> Category | None:
    """Get a category by its ID"""
    for category in categories:
        if category.id == category_id:
            return category
    return None

def get_contact_categories(contact: Contact, all_categories: list[Category]) -> list[Category]:
    """Get the full category objects for a contact"""
    return [cat for cat in all_categories if cat.id in contact.categories]

def generate_mock_email_draft(contact: Contact, categories: list[Category]) -> str:
    """Generate a mock email draft for demonstration"""
    category_names = [cat.name for cat in get_contact_categories(contact, categories)]
    category_str = ", ".join(category_names)
    
    return f"""
Subject: Draft for {contact.name} - {format_date(datetime.now())}

Hi {contact.name},

I hope this email finds you well! [AI would generate personalized content based on {category_str} categories]

{contact.personal_instructions or '[No personal instructions specified]'}

Best regards,
[Your name]

PS: [AI would generate category-specific postscripts]
""" 