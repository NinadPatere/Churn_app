import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp

# Title of the web app
st.title('Churn Analysis Dashboard')

# Load your dataset
df = pd.read_csv('Customer_Data.csv')

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a Chart", [
    "Gender Distribution", 
    "Age Group Distribution", 
    "Tenure Group Distribution",
    "Contract & Payment Method", 
    "Churn Count by State"
])

# Function to plot gender distribution
def plot_gender_distribution(df, fig):
    # Count gender distribution
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    
    # Create a bar chart
    fig1 = px.bar(gender_counts, x='Gender', y='Count', color='Gender', color_continuous_scale='viridis')

    # Add the bar chart to the first subplot
    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)

# Function to plot age group distribution
def plot_age_group_distribution(df, fig):
    # Define age bins and labels
    age_bins = [0, 20, 35, 50, 100]
    age_labels = ['<20', '20-35', '35-50', '>50']
    
    # Create age groups
    df['Age_Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)

    # Count the number of entries in each age group
    age_group_counts = df['Age_Group'].value_counts().reset_index()
    age_group_counts.columns = ['Age_Group', 'Count']
    
    # Create a bar chart
    fig2 = px.bar(age_group_counts, x='Age_Group', y='Count', color='Age_Group', color_continuous_scale='Reds')

    # Add the bar chart to the second subplot
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)

# Function to plot tenure group distribution
def plot_tenure_group_distribution(df):
    # Binning tenure data
    tenure_bins = [0, 6, 12, 18, 24, 100]
    tenure_labels = ['<6 Months', '6-12 Months', '12-18 Months', '18-24 Months', '>= 24 Months']
    df['Tenure_Group'] = pd.cut(df['Tenure_in_Months'], bins=tenure_bins, labels=tenure_labels)

    # Counting Tenure Group Distribution
    tenure_group_counts = df['Tenure_Group'].value_counts().reset_index()
    tenure_group_counts.columns = ['Tenure_Group', 'Count']

    # Create bar chart using Plotly
    fig = px.bar(tenure_group_counts, x='Tenure_Group', y='Count', color='Tenure_Group', color_continuous_scale='Spectral')

    # Update layout for better presentation
    fig.update_layout(
        title="Tenure Group Distribution of Churners",
        xaxis_title="Tenure Group",
        yaxis_title="Count",
        xaxis_tickangle=-30,
        height=400,
        width=600
    )

    # Show the figure in Streamlit
    st.plotly_chart(fig)

# Function to plot contract and payment method distribution
def plot_contract_payment_method_distribution(df):
    # Create subplots
    fig = sp.make_subplots(
        rows=1, 
        cols=2, 
        subplot_titles=("Contract Type Distribution of Churners", "Payment Method Distribution of Churners")
    )

    # Contract Type Distribution
    contract_counts = df['Contract'].value_counts().reset_index()
    contract_counts.columns = ['Contract', 'Count']
    fig1 = px.bar(contract_counts, x='Contract', y='Count', color='Contract', color_continuous_scale='Reds')

    # Add to first subplot
    for trace in fig1.data:
        fig.add_trace(trace, row=1, col=1)

    # Payment Method Distribution
    payment_counts = df['Payment_Method'].value_counts().reset_index()
    payment_counts.columns = ['Payment_Method', 'Count']
    fig2 = px.bar(payment_counts, x='Payment_Method', y='Count', color='Payment_Method', color_continuous_scale='magma')

    # Add to second subplot
    for trace in fig2.data:
        fig.add_trace(trace, row=1, col=2)

    # Update layout and show the figure
    fig.update_layout(
        showlegend=False,
        title_text="Contract & Payment Method Distribution of Churners",
        height=500,
        width=900
    )
    st.plotly_chart(fig)

# Function to plot churn count by state
def plot_churn_count_by_state(df):
    # Counting churners by state
    state_counts = df['State'].value_counts().reset_index()
    state_counts.columns = ['State', 'Count']

    # Create a bar chart using Plotly
    fig = px.bar(state_counts, x='State', y='Count', color='Count', color_continuous_scale='Spectral')

    # Update layout for better presentation
    fig.update_layout(
        title="Churn Count by State",
        xaxis_title="State",
        yaxis_title="Count of Churners",
        height=600,
        width=800
    )

    # Show the figure in Streamlit
    st.plotly_chart(fig)

# Create subplots for Gender and Age Group distributions
fig = sp.make_subplots(rows=1, cols=2, subplot_titles=("Gender Distribution of Churners", "Age Group Distribution of Churners"))

# Display charts based on user selection
if options == "Gender Distribution":
    plot_gender_distribution(df, fig)
elif options == "Age Group Distribution":
    plot_age_group_distribution(df, fig)
elif options == "Tenure Group Distribution":
    plot_tenure_group_distribution(df)
elif options == "Contract & Payment Method":
    plot_contract_payment_method_distribution(df)
elif options == "Churn Count by State":
    plot_churn_count_by_state(df)

# Show the figure for Gender and Age distributions
if options in ["Gender Distribution", "Age Group Distribution"]:
    fig.update_layout(showlegend=False, title_text="Churners Distribution", height=400, width=900)
    st.plotly_chart(fig)
