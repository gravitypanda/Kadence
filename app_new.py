import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.sample_data import generate_sample_categories, generate_sample_contacts
from utils.helpers import format_date, get_contact_categories, generate_mock_email_draft
