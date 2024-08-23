# 📊 Compass AI Marketing Campaign Agent

Compass AI is a powerful, AI-driven marketing tool that helps you create, strategize, schedule, and analyze marketing campaigns seamlessly. With built-in AI capabilities, it automates content generation, strategy planning, and scheduling to help you focus on scaling your business.

## ✨ Key Features
- **🚀 Campaign Creation**: AI-powered content generation tailored for various platforms.
- **📅 Strategy Planning**: Generate a day-by-day marketing strategy for your campaigns.
- **🕒 Content Scheduling**: Schedule posts across multiple platforms and optimize posting times.
- **📈 Analytics (Coming Soon)**: Track your campaign’s performance and get actionable insights.

## 🔧 Tech Stack
- **Streamlit**: Frontend framework for building web apps.
- **Groq API**: AI engine for generating content and strategies.
- **Pillow**: Image processing library to handle logo modifications.
- **ReportLab**: PDF generation library for creating downloadable content.

## 🚀 Getting Started

### Prerequisites
Ensure that you have the following installed:
- **Python 3.9+**
- **Pip** (Python package installer)

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/muhammad-farhan67/CompassAI.git
    cd CompassAi
    ```

2. **Install Dependencies**:
    Install the necessary dependencies from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up API Key**:
    Create a `secrets.toml` file in the `.streamlit/` directory with your Groq API key.
    ```toml
    [default]
    API_KEY = "your_groq_api_key"
    ```

4. **Run Locally**:
    Start the Streamlit app by running the following command:
    ```bash
    streamlit run app.py
    ```

5. **Access the App**:
    The app will be accessible at `http://localhost:8501` in your browser.

## ☁️ Deployment on Streamlit Cloud

1. **Fork the Repository**:
    Go to the [CompassAI GitHub repo](https://github.com/muhammad-farhan67/CompassAI) and fork it to your account.

2. **Set Up Streamlit Cloud**:
    - Go to [Streamlit Cloud](https://share.streamlit.io/) and sign in.
    - Create a new app and connect it to your GitHub repository.
  
3. **Configure Secrets**:
    Add your `API_KEY` directly in the Streamlit Cloud app settings under `Secrets` with the following format:
    ```
    API_KEY = "your_groq_api_key"
    ```

4. **Deploy**:
    Once the app is linked and secrets are set, Streamlit Cloud will automatically deploy your app.

## 🛠 Usage

Once the app is running, you can:

1. **Create Campaigns**:
   - Go to the "Campaign Creation" section.
   - Fill out your brand details and content requirements.
   - Generate content and download it as a PDF.
   
2. **Generate Strategies**:
   - Navigate to the "Strategy" section.
   - Input your campaign start date and duration.
   - Generate and download a comprehensive strategy for your marketing efforts.

3. **Schedule Posts**:
   - Use the "Scheduling" section to plan content for multiple platforms and schedule posts with a single click.

4. **Analytics**:
   - The "Analytics" section will soon allow you to track your campaigns and get valuable insights.
  
## 📚 Additional Resources

- **Compass_Model**: We have created a model named "Compass_Model." The reason we haven't used it extensively was due to a lack of GPU resources. The model was deployed but lacked the necessary computational power. It was generated using data from Llama 3.1 405B and was pre-trained on Llama 3.1 8B with fine-tuning applied.
  
  - **Model on Hugging Face**: [Compass_Model](https://huggingface.co/RafaM97/Compass_Model)

- **Marketing Social Media Dataset**: This dataset is designed to support AI-driven marketing tools, providing data essential for content generation, strategy planning, and more. It includes a comprehensive collection of marketing campaigns focused on various industries, channels, and objectives.
  
  - **Dataset on Hugging Face**: [Marketing Social Media Dataset](https://huggingface.co/datasets/RafaM97/marketing_social_media)
     

## 💡 Future Features
- **Campaign Analytics**: Analyze the success of your campaigns and track metrics like engagement and reach.
- **Integration with More Platforms**: Expand scheduling and analytics to more social media platforms.

## 🤝 Contributing
Contributions are welcome! Please fork the repository and create a pull request with your feature enhancements or bug fixes.
