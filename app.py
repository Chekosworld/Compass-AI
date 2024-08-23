import streamlit as st
from datetime import datetime, timedelta
import requests
import json
import uuid
import os
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# Groq API configuration
GROQ_API_KEY = st.secrets["API_KEY"]

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Error handling decorator
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None
    return wrapper

@handle_errors
def generate_marketing_content(instruction, input_context, is_strategy=False):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_message = "You are a helpful AI assistant specializing in marketing and content creation."
    if is_strategy:
        system_message += " For strategy, provide a unique day-by-day breakdown tailored to the specific input."
    else:
        system_message += " For content, focus on creating a single cohesive piece without day-by-day breakdown."
    
    system_message += " Avoid generating any external links or off-topic content."
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Instruction: {instruction}\nInput: {input_context}\nPlease format your response in markdown, excluding any links."}
        ],
        "max_tokens": 1000,
        "temperature": 0.7  # Adjust this value to increase randomness and uniqueness
    }
    
    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Unable to generate content. Status code: {response.status_code}")
 

def create_pdf(content):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, 
                            rightMargin=inch, leftMargin=inch, 
                            topMargin=inch, bottomMargin=inch)
    
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=6
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=11,
        spaceBefore=6,
        spaceAfter=6
    )
    
    story = []
    
    # Split content into paragraphs
    paragraphs = content.split('\n\n')
    
    # Process paragraphs and apply appropriate styling
    for i, para in enumerate(paragraphs):
        if i == 0:  # First paragraph as title
            p = Paragraph(para, title_style)
        elif para.startswith('#'):  # Headings
            level = para.count('#')
            text = para.lstrip('#').strip()
            if level == 2:
                p = Paragraph(text, heading_style)
            else:
                p = Paragraph(text, normal_style)
        else:  # Normal paragraphs
            p = Paragraph(para, normal_style)
        
        story.append(p)
        story.append(Spacer(1, 6))  # Add space between paragraphs
    
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
        padding: 10px 0;
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
    page = st.sidebar.selectbox("Choose a page", ["Home", "Post Creation", "Marketing Strategy", "Scheduling", "Analytics"])

    # Handle page selection
    if page == "Home":
        show_home()
    elif page == "Post Creation":
        show_post_creation()
    elif page == "Marketing Strategy":
        show_marketing_strategy()
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


@handle_errors
def show_post_creation():
    st.header("Post Creation")
    
    content_type = st.selectbox("Content Type", ["Social Media Post", "Ad Copy", "Email"])
    content_prompt = st.text_area("Describe the content you want to generate")

    if st.button("Generate Content"):
        if not content_prompt:
            st.warning("Please provide a content description.")
        else:
            instruction = f"Create a single {content_type}"
            
            with st.spinner("Generating content..."):
                generated_content = generate_marketing_content(instruction, content_prompt)
            
            st.markdown(generated_content)
            
            # Download as PDF
            pdf = create_pdf(generated_content)
            st.download_button(
                label="Download Generated Content as PDF",
                data=pdf,file_name="generated_content.pdf",
                mime="application/pdf"
            )

@handle_errors
def show_marketing_strategy():
    st.header("Marketing Strategy")
    
    # Brand Questionnaire
    st.subheader("Brand Questionnaire")
    brand_name = st.text_input("Brand Name")
    industry = st.selectbox("Industry", ["Technology", "Fashion", "Food & Beverage", "Other"])
    target_audience = st.text_area("Describe your target audience")
    campaign_objective = st.selectbox("Campaign Objective", ["Brand Awareness", "Lead Generation", "Sales", "Other"])
    
    start_date = st.date_input("Campaign Start Date")
    duration = st.number_input("Campaign Duration (days)", min_value=1, value=30)
    
    if st.button("Generate Strategy"):
        if not all([brand_name, industry, target_audience, campaign_objective]):
            st.warning("Please fill in all the fields in the Brand Questionnaire.")
        else:
            instruction = f"Generate a unique day-by-day marketing strategy for {duration} days"
            input_context = f"Brand: {brand_name}, Industry: {industry}, Target Audience: {target_audience}, Objective: {campaign_objective}, Start Date: {start_date}, Duration: {duration} days"
            
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
import streamlit as st
import requests
import json
from datetime import datetime, timedelta
from PIL import Image
import io
import os
import uuid
ACCESS_TOKEN = st.secrets["META_ACCESS_TOKEN"]
PAGE_ID = st.secrets["META_PAGE_ID"]

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def post_to_facebook(message, image_url=None, scheduled_time=None):
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
    data = {
        "message": message,
        "published": "false" if scheduled_time else "true",
    }
    if image_url:
        data["link"] = image_url
    if scheduled_time:
        data["scheduled_publish_time"] = int(scheduled_time.timestamp())
    
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()



def save_scheduled_post(platform, content, image_path, scheduled_time):
    # Create a unique ID for the scheduled post
    post_id = str(uuid.uuid4())
    
    # Save post details to a JSON file
    scheduled_posts = load_scheduled_posts()
    scheduled_posts[post_id] = {
        "platform": platform,
        "content": content,
        "image_path": image_path,
        "scheduled_time": scheduled_time.isoformat()
    }
    
    with open("scheduled_posts.json", "w") as f:
        json.dump(scheduled_posts, f)

def load_scheduled_posts():
    if os.path.exists("scheduled_posts.json"):
        with open("scheduled_posts.json", "r") as f:
            return json.load(f)
    return {}

import streamlit as st
import requests
import json
from datetime import datetime
from PIL import Image
import os
import uuid

# Meta API configuration
ACCESS_TOKEN = st.secrets["META_ACCESS_TOKEN"]
PAGE_ID = st.secrets["META_PAGE_ID"]


HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def post_to_facebook(message, image_url=None, scheduled_time=None):
    url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
    data = {
        "message": message,
        "published": "false" if scheduled_time else "true",
    }
    if image_url:
        data["link"] = image_url
    if scheduled_time:
        data["scheduled_publish_time"] = int(scheduled_time.timestamp())
    
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()


def show_scheduling():
    st.header("Content Scheduling")
    
    platforms = ["Facebook"]  # Remove Instagram option
    
    post_content = st.text_area("Post Content", key="schedule_post_content")
    
    uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="schedule_image_upload")
    
    post_date = st.date_input("Post Date", key="schedule_post_date")
    post_time = st.time_input("Post Time", key="schedule_post_time")
    
    if post_content or uploaded_image:
        st.subheader("Preview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if post_content:
                st.text_area("Content Preview", post_content, height=150, disabled=True, key="schedule_content_preview")
        
        with col2:
            if uploaded_image:
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Schedule Post", key="schedule_post_button"):
        if not post_content and not uploaded_image:
            st.warning("Please add content or upload an image.")
        else:
            scheduled_datetime = datetime.combine(post_date, post_time)
            
            # Save image temporarily if uploaded
            image_path = None
            if uploaded_image:
                image_path = f"temp_image_{uuid.uuid4()}.jpg"
                Image.open(uploaded_image).save(image_path)
            
            response = post_to_facebook(post_content, image_path, scheduled_datetime)
            if "id" in response:
                st.success(f"Post scheduled for Facebook at {scheduled_datetime}")
                # Save scheduled post
                save_scheduled_post("Facebook", post_content, image_path, scheduled_datetime)
            else:
                st.error(f"Error scheduling Facebook post: {response.get('error', {}).get('message', 'Unknown error')}")
            
            # Display scheduled post details
            st.subheader("Scheduled Post Details")
            st.write(f"Date and Time: {scheduled_datetime}")
            st.write("Platform: Facebook")
            if post_content:
                st.write("Content:")
                st.text_area("Scheduled Content", post_content, height=150, disabled=True, key="scheduled_content_display")
            if uploaded_image:
                st.write("Image:")
                st.image(image, caption="Scheduled Image", use_column_width=True)

    # Display scheduled posts
    st.subheader("Scheduled Posts")
    scheduled_posts = load_scheduled_posts()
    for post_id, post_data in scheduled_posts.items():
        st.write(f"Platform: {post_data['platform']}")
        st.write(f"Scheduled Time: {post_data['scheduled_time']}")
        st.text_area(f"Content for post {post_id}", post_data['content'], height=100, disabled=True, key=f"scheduled_post_{post_id}")
        if post_data['image_path']:
            st.image(post_data['image_path'], caption="Scheduled Image", width=200)
        st.write("---")

def show_analytics():
    st.header("Campaign Analytics")
    st.write("This feature is under development. It will show campaign performance metrics and insights.")

if __name__ == "__main__":
    main()
