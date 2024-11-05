import streamlit as st
import pandas as pd
import plotly.express as px

# Set up Streamlit app with a wider layout and custom title
st.set_page_config(page_title='Churn Analysis Dashboard', page_icon=":bar_chart:", layout='wide')
st.title('Churn Analysis Dashboard')

# Load the dataset
df = pd.read_csv('Customer_Data.csv')

# Sidebar for downloading data
st.sidebar.download_button(
    label="Download Raw Data", 
    data=df.to_csv(index=False).encode('utf-8'),
    file_name="Customer_Data.csv",
    mime="text/csv"
)

# Add custom CSS for styling
st.markdown("""
<style>
    .title {
        font-size: 2.5em;
        text-align: center;
        color: #4B0082;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f5;
        padding: 20px;
    }
    .stButton > button {
        background-color: #4CAF50; /* Green */
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 10px;
    }
    .stButton > button:hover {
        background-color: #45a049; /* Darker Green */
    }
    .section-title {
        color: white; /* Changed to white for better visibility */
        background-color: #005782; /* Dark violet background */
        padding: 10px;
        border-radius: 5px;
        font-size: 1.5em;
        margin-top: 40px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Define color themes for better aesthetics
age_colors = px.colors.qualitative.Pastel
tenure_colors = px.colors.qualitative.Pastel1
contract_colors = px.colors.qualitative.Set2
payment_colors = px.colors.qualitative.Dark2

# Create a function to get selected values with Select/Deselect All buttons
def multi_select_with_all_option(label, options):
    selected = st.sidebar.multiselect(label, options, default=options)
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button(f'Select All {label}'):
            selected = options
    with col2:
        if st.button(f'Deselect All {label}'):
            selected = []
    return selected

# Create filters for the data with buttons
st.sidebar.header("Filters")
gender_filter = multi_select_with_all_option('Gender', options=df['Gender'].unique())
age_bins = [0, 20, 35, 50, 100]
age_labels = ['<20', '20-35', '35-50', '>50']
df['Age_Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)
age_group_filter = multi_select_with_all_option('Age Group', options=age_labels)
state_filter = multi_select_with_all_option('State', options=df['State'].unique())
contract_filter = multi_select_with_all_option('Contract Type', options=df['Contract'].unique())
payment_filter = multi_select_with_all_option('Payment Method', options=df['Payment_Method'].unique())

# Filter the dataframe based on user input
filtered_df = df[
    (df['Gender'].isin(gender_filter)) &
    (df['Age_Group'].isin(age_group_filter)) &
    (df['State'].isin(state_filter)) &
    (df['Contract'].isin(contract_filter)) &
    (df['Payment_Method'].isin(payment_filter))
]

# Function to plot gender distribution as a pie chart
def plot_gender_distribution(df):
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    fig = px.pie(gender_counts, names='Gender', values='Count', 
                 color_discrete_sequence=age_colors, title="Gender Distribution of Churners")
    st.plotly_chart(fig, use_container_width=True)

# Function to plot age group distribution as a bar chart
def plot_age_group_distribution(df):
    age_group_counts = df['Age_Group'].value_counts().reset_index()
    age_group_counts.columns = ['Age_Group', 'Count']
    fig = px.bar(age_group_counts, x='Age_Group', y='Count', color='Age_Group', 
                 color_discrete_sequence=age_colors, title="Age Group Distribution of Churners")
    fig.update_layout(margin=dict(t=30, b=0), height=400)
    st.plotly_chart(fig, use_container_width=True)

# Function to plot tenure group distribution as a bar chart
def plot_tenure_group_distribution(df):
    tenure_bins = [0, 6, 12, 18, 24, 100]
    tenure_labels = ['<6 Months', '6-12 Months', '12-18 Months', '18-24 Months', '>= 24 Months']
    df['Tenure_Group'] = pd.cut(df['Tenure_in_Months'], bins=tenure_bins, labels=tenure_labels)
    tenure_group_counts = df['Tenure_Group'].value_counts().reset_index()
    tenure_group_counts.columns = ['Tenure_Group', 'Count']
    fig = px.bar(tenure_group_counts, x='Tenure_Group', y='Count', color='Tenure_Group', 
                 color_discrete_sequence=tenure_colors, title="Tenure Group Distribution of Churners")
    fig.update_layout(margin=dict(t=30, b=0), height=400)
    st.plotly_chart(fig, use_container_width=True)

# Function to plot contract type distribution as a bar chart
def plot_contract_distribution(df):
    contract_counts = df['Contract'].value_counts().reset_index()
    contract_counts.columns = ['Contract', 'Count']
    fig = px.bar(contract_counts, x='Contract', y='Count', color='Contract', 
                 color_discrete_sequence=contract_colors, title="Contract Type Distribution of Churners")
    fig.update_layout(margin=dict(t=30, b=0), height=400)
    st.plotly_chart(fig, use_container_width=True)

# Function to plot payment method distribution as a bar chart
def plot_payment_method_distribution(df):
    payment_counts = df['Payment_Method'].value_counts().reset_index()
    payment_counts.columns = ['Payment_Method', 'Count']
    fig = px.bar(payment_counts, x='Payment_Method', y='Count', color='Payment_Method', 
                 color_discrete_sequence=payment_colors, title="Payment Method Distribution of Churners")
    fig.update_layout(margin=dict(t=30, b=0), height=400)
    st.plotly_chart(fig, use_container_width=True)

# Function to plot churn count by state
def plot_churn_count_by_state(df):
    state_counts = df['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']
    fig = px.bar(state_counts, x='State', y='Count', color='Count', 
                 color_continuous_scale='Spectral', title="Churn Count by State")
    fig.update_layout(margin=dict(t=30, b=0), height=500)
    st.plotly_chart(fig, use_container_width=True)

# Layout the dashboard in sections for better readability and aesthetics
st.subheader("Overview of Churn Demographics", anchor="overview-demographics")
st.markdown('<div class="section-title">Demographics Charts</div>', unsafe_allow_html=True)

# Organize demographic charts in columns
col1, col2 = st.columns(2)
with col1:
    plot_gender_distribution(filtered_df)
    plot_age_group_distribution(filtered_df)
with col2:
    plot_tenure_group_distribution(filtered_df)
    plot_churn_count_by_state(filtered_df)

st.subheader("Churner Preferences in Contract and Payment Method", anchor="preferences")
st.markdown('<div class="section-title">Contract and Payment Method Charts</div>', unsafe_allow_html=True)
# Organize contract and payment method charts in columns
col3, col4 = st.columns(2)
with col3:
    plot_contract_distribution(filtered_df)
with col4:
    plot_payment_method_distribution(filtered_df)
