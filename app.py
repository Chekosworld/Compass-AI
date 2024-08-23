import streamlit as st
from datetime import datetime, timedelta
import requests
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


# Groq API configuration
GROQ_API_KEY = st.secrets["API_KEY"]

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_marketing_content(instruction, input_context, is_strategy=False):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_message = "You are a helpful AI assistant specializing in marketing and content creation."
    if is_strategy:
        system_message += " For strategy, provide a day-by-day breakdown."
    else:
        system_message += " For content, focus on creating a single cohesive piece without day-by-day breakdown."
    
    system_message += " Avoid generating any external links or off-topic content."
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Instruction: {instruction}\nInput: {input_context}\nPlease format your response in markdown, excluding any links."}
        ],
        "max_tokens": 1000
    }
    
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: Unable to generate content. Status code: {response.status_code}"

def create_pdf(content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                            rightMargin=72, leftMargin=72, 
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    
    story = []
    
    # Split content into paragraphs
    paragraphs = content.split('\n\n')
    for para in paragraphs:
        p = Paragraph(para, style)
        story.append(p)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

import streamlit as st
from PIL import Image, ImageOps
import io

def remove_background(image):
    # Convert the logo to RGBA mode to handle transparency
    image = image.convert('RGBA')

    # Get the image data
    datas = image.getdata()
    new_data = []

    # Iterate through each pixel and check if it's dark enough to be background
    for item in datas:
        if item[0] < 50 and item[1] < 50 and item[2] < 50:  # Dark pixels
            new_data.append((255, 255, 255, 0))  # Make it transparent
        else:
            new_data.append(item)

    # Update the image data
    image.putdata(new_data)
    return image

def main():
    # Load the logo
    logo = Image.open("Compassai.png")

    # Remove background from logo
    logo = remove_background(logo)

  

    # Convert the image to bytes
    img_byte_arr = io.BytesIO()
    logo.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    # Set page config with the logo as favicon
    st.set_page_config(
        page_title="Compass AI",
        page_icon=img_byte_arr,
        layout="centered"  # Adjusted for center alignment
        )

    # Custom CSS to style the banner
    st.markdown("""
    <style>
    .banner-container {
        width: 100%;  /* Make it span the entire width */
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 5px 0;
    }
    .banner-container img {
        width: 100%;  /* Banner stretches across the page */
        height: auto;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display the banner at the top of the app
    st.markdown('<div class="banner-container">', unsafe_allow_html=True)
    st.image(logo, use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Sidebar for navigation
    page = st.sidebar.selectbox("Choose a page", ["Home", "Campaign Creation", "Strategy", "Scheduling", "Analytics"])

    # Handle page selection
    if page == "Home":
        show_home()
    elif page == "Campaign Creation":
        show_campaign_creation()
    elif page == "Strategy":
        show_strategy()
    elif page == "Scheduling":
        show_scheduling()
    elif page == "Analytics":
        show_analytics()




def show_home():
    st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        font-weight: bold;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-font {
        font-size:25px !important;
        color: #4682B4;
        text-align: center;
        margin-bottom: 30px;
    }
    .feature-font {
        font-size:30px !important;
        color: #4169E1;
        text-align: center;
        margin-bottom: 30px;
    }
    .feature-card {
        background-color: #F0F8FF;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 2px solid #1E90FF;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .feature-title {
        font-size: 24px !important;
        font-weight: bold;
        color: #1E90FF;
        margin-bottom: 10px;
    }
    .feature-list {
        color: #333;
        font-size: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Welcome to AI Marketing Campaign Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-font">Your intelligent assistant for creating, managing, and analyzing marketing campaigns</p>', unsafe_allow_html=True)

    st.markdown('<p class="feature-font">🚀 Key Features</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
        <div class="feature-card">
        <p class="feature-title">Campaign Creation</p>
        <ul class="feature-list">
            <li>AI-powered content generation</li>
            <li>Customized for your brand</li>
            <li>Multiple content types</li>
        </ul>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <div class="feature-card">
        <p class="feature-title">Strategy Planning</p>
        <ul class="feature-list">
            <li>Comprehensive marketing strategies</li>
            <li>Day-by-day breakdown</li>
            <li>Tailored to your objectives</li>
        </ul>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="feature-card">
        <p class="feature-title">Content Scheduling</p>
        <ul class="feature-list">
            <li>Multi-platform scheduling</li>
            <li>Optimize posting times</li>
            <li>Manage your content calendar</li>
        </ul>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <div class="feature-card">
        <p class="feature-title">Analytics (Coming Soon)</p>
        <ul class="feature-list">
            <li>Track campaign performance</li>
            <li>Gain actionable insights</li>
            <li>Improve your marketing ROI</li>
        </ul>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<p class="sub-font">Get started by selecting a feature from the sidebar!</p>', unsafe_allow_html=True)


def show_campaign_creation():
    st.header("Campaign Creation")
    
    # Brand Questionnaire
    st.subheader("Brand Questionnaire")
    brand_name = st.text_input("Brand Name")
    industry = st.selectbox("Industry", ["Technology", "Fashion", "Food & Beverage", "Other"])
    target_audience = st.text_area("Describe your target audience")
    campaign_objective = st.selectbox("Campaign Objective", ["Brand Awareness", "Lead Generation", "Sales", "Other"])

    # Content Generation
    st.subheader("Content Generation")
    content_type = st.selectbox("Content Type", ["Social Media Post", "Ad Copy", "Email"])
    content_prompt = st.text_area("Describe the content you want to generate")

    if st.button("Generate Content"):
        instruction = f"Create a single {content_type} for a {industry} company, focusing on {campaign_objective}"
        input_context = f"Brand: {brand_name}, Target Audience: {target_audience}, Objective: {campaign_objective}, Content Details: {content_prompt}"
        
        with st.spinner("Generating content..."):
            generated_content = generate_marketing_content(instruction, input_context)
        
        st.markdown(generated_content)
        
        # Download as PDF
        pdf = create_pdf(generated_content)
        st.download_button(
            label="Download Generated Content as PDF",
            data=pdf,
            file_name="generated_content.pdf",
            mime="application/pdf"
        )

def show_strategy():
    st.header("Marketing Strategy")
    
    start_date = st.date_input("Campaign Start Date")
    duration = st.number_input("Campaign Duration (days)", min_value=1, value=30)
    
    if st.button("Generate Strategy"):
        instruction = f"Generate a day-by-day marketing strategy for {duration} days"
        input_context = f"Start Date: {start_date}, Duration: {duration} days"
        
        with st.spinner("Generating strategy..."):
            strategy = generate_marketing_content(instruction, input_context, is_strategy=True)
        
        st.subheader("Generated Marketing Strategy")
        st.markdown(strategy)
        
        # Download as PDF
        pdf = create_pdf(strategy)
        st.download_button(
            label="Download Marketing Strategy as PDF",
            data=pdf,
            file_name="marketing_strategy.pdf",
            mime="application/pdf"
        )

def show_scheduling():
    st.header("Content Scheduling")
    
    platforms = st.multiselect("Select Platforms", ["Facebook", "Instagram", "Twitter"])
    post_content = st.text_area("Post Content")
    post_date = st.date_input("Post Date")
    post_time = st.time_input("Post Time")
    
    if st.button("Schedule Post"):
        scheduled_datetime = datetime.combine(post_date, post_time)
        for platform in platforms:
            st.success(f"Post scheduled for {platform} at {scheduled_datetime}")

def show_analytics():
    st.header("Campaign Analytics")
    st.write("This feature is under development. It will show campaign performance metrics and insights.")

if __name__ == "__main__":
    main()
