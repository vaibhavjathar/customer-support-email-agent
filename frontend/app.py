"""Streamlit Frontend for Customer Support Email Agent - Premium SaaS UI."""
import streamlit as st
import requests
import json
import plotly.express as px
import pandas as pd
from datetime import datetime
from typing import Optional

# Configure page layout
st.set_page_config(
    page_title="Customer Support Email Agent",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Color Palette for Classifications
COLOR_PALETTE = {
    "billing": "#0066FF",      # Electric Blue
    "technical": "#DC143C",    # Crimson Red
    "account": "#FFA500",      # Amber/Gold
    "complaint": "#DC143C",    # Crimson Red
    "refund": "#9370DB",       # Purple/Amethyst
    "general": "#708090",      # Slate/Grey
}

EMOJI_PALETTE = {
    "billing": "💳",
    "technical": "⚙️",
    "account": "👤",
    "complaint": "😠",
    "refund": "💰",
    "general": "📝",
}

# Dark Mode & Glassmorphism CSS Styling
def apply_theme():
    """Apply dark mode and premium styling."""
    st.markdown("""
    <style>
    /* Root Color Variables */
    :root {
        --primary: #0066FF;
        --secondary: #DC143C;
        --accent: #FFA500;
        --success: #22C55E;
        --warning: #F59E0B;
        --error: #EF4444;
        --bg-dark: #0F172A;
        --bg-card: #1E293B;
        --bg-hover: #334155;
        --text-primary: #F1F5F9;
        --text-secondary: #CBD5E1;
        --border: #334155;
        --glass-blur: rgba(30, 41, 59, 0.7);
    }

    /* Overall Page Styling */
    html, body, .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: var(--text-primary);
    }

    /* Main Content Area */
    .main {
        background: transparent;
        padding: 2rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border-right: 1px solid var(--border);
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #0066FF, #00D4FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    h2 {
        font-size: 1.75rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--primary);
        padding-bottom: 0.5rem;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: var(--glass-blur);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        background: var(--glass-blur);
        border-color: rgba(148, 163, 184, 0.3);
        box-shadow: 0 12px 48px rgba(0, 102, 255, 0.15);
        transform: translateY(-2px);
    }

    /* Metrics */
    .metric-card {
        background: var(--glass-blur);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 1.25rem;
        backdrop-filter: blur(10px);
    }

    [data-testid="metric-container"] {
        background: transparent !important;
        border: none !important;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background: var(--glass-blur);
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 8px;
        margin: 0.5rem 0;
    }

    [data-testid="stExpanderDetails"] {
        background: rgba(15, 23, 42, 0.5) !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), #0052CC);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.875rem;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #0052CC, #0040A0);
        box-shadow: 0 8px 20px rgba(0, 102, 255, 0.3);
        transform: translateY(-2px);
    }

    /* Radio & Selectbox */
    .stRadio > label, .stMultiSelect > label {
        color: var(--text-secondary);
        font-weight: 500;
    }

    /* Info/Warning/Error Boxes */
    .stInfo, .stWarning, .stError, .stSuccess {
        background: var(--glass-blur) !important;
        border-left: 4px solid var(--primary) !important;
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }

    .stWarning {
        border-left-color: var(--warning) !important;
    }

    .stError {
        border-left-color: var(--error) !important;
    }

    .stSuccess {
        border-left-color: var(--success) !important;
    }

    /* Code Blocks */
    pre {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 8px;
        padding: 1rem !important;
        font-family: 'Courier New', monospace !important;
    }

    code {
        color: #22D3EE;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
    }

    /* Tables */
    table {
        color: var(--text-primary) !important;
    }

    thead {
        background: rgba(148, 163, 184, 0.1) !important;
    }

    /* Text Areas */
    .stTextArea textarea {
        background: rgba(30, 41, 59, 0.8) !important;
        color: var(--text-primary) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
    }

    /* Text Input */
    .stTextInput input {
        background: rgba(30, 41, 59, 0.8) !important;
        color: var(--text-primary) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 6px;
    }

    /* Dividers */
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.3), transparent);
        margin: 1.5rem 0;
    }

    /* Spinner */
    .stSpinner > div {
        color: var(--primary) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        border-bottom: 2px solid rgba(148, 163, 184, 0.2);
    }

    .stTabs [data-testid="stTab"] {
        padding: 0.75rem 1.5rem;
        color: var(--text-secondary);
        border-radius: 6px 6px 0 0;
        transition: all 0.3s ease;
    }

    .stTabs [data-testid="stTab"][aria-selected="true"] {
        color: var(--primary);
        border-bottom: 3px solid var(--primary);
        background: transparent;
    }

    /* Checkbox */
    .stCheckbox > label {
        color: var(--text-secondary);
    }

    /* Link Button */
    .stLinkButton > a {
        background: linear-gradient(135deg, var(--primary), #0052CC);
        color: white !important;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        text-decoration: none;
        font-weight: 600;
    }

    .stLinkButton > a:hover {
        box-shadow: 0 8px 20px rgba(0, 102, 255, 0.3);
    }

    /* Plotly Chart Container */
    .js-plotly-plot {
        background: var(--glass-blur) !important;
        border-radius: 12px;
        padding: 1rem;
    }

    /* Form */
    .stForm {
        background: var(--glass-blur);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }

    /* Email Card Styling */
    .email-card {
        background: var(--glass-blur);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .email-card:hover {
        border-color: rgba(148, 163, 184, 0.3);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
        transform: translateX(4px);
    }

    .email-badge {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Status Badge */
    .badge-auto {
        background: rgba(34, 197, 94, 0.2);
        border: 1px solid rgba(34, 197, 94, 0.5);
        color: #86EFAC;
    }

    .badge-review {
        background: rgba(245, 158, 11, 0.2);
        border: 1px solid rgba(245, 158, 11, 0.5);
        color: #FCD34D;
    }

    /* Classification Badges */
    .badge-billing {
        background: rgba(0, 102, 255, 0.2);
        border: 1px solid rgba(0, 102, 255, 0.5);
        color: #60A5FA;
    }

    .badge-technical {
        background: rgba(220, 20, 60, 0.2);
        border: 1px solid rgba(220, 20, 60, 0.5);
        color: #F87171;
    }

    .badge-account {
        background: rgba(255, 165, 0, 0.2);
        border: 1px solid rgba(255, 165, 0, 0.5);
        color: #FDBA74;
    }

    .badge-refund {
        background: rgba(147, 112, 219, 0.2);
        border: 1px solid rgba(147, 112, 219, 0.5);
        color: #D8B4FE;
    }

    .badge-general {
        background: rgba(112, 128, 144, 0.2);
        border: 1px solid rgba(112, 128, 144, 0.5);
        color: #CBD5E1;
    }

    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary), #00D4FF);
        border-radius: 10px;
    }

    /* Monospace font for tech feel */
    .mono {
        font-family: 'Courier New', 'Courier', monospace;
        color: #22D3EE;
    }
    </style>
    """, unsafe_allow_html=True)


# Initialize theme
apply_theme()


def get_classification_badge(classification: str) -> str:
    """Return badge HTML for classification."""
    emoji = EMOJI_PALETTE.get(classification, "📝")
    class_name = f"badge-{classification}"
    return f'<span class="email-badge {class_name}">{emoji} {classification.upper()}</span>'


def get_status_badge(requires_review: bool) -> str:
    """Return badge HTML for review status."""
    if requires_review:
        return '<span class="email-badge badge-review">⚠️ NEEDS REVIEW</span>'
    return '<span class="email-badge badge-auto">✅ AUTO-HANDLED</span>'


def page_send_email():
    """Page 1: Send Mock Email with step-by-step progress."""
    st.header("✉️ Send Mock Email")
    st.markdown("Submit an email to the AI agent and watch it process in real-time.")

    with st.form(key="email_form", border=False):
        col1, col2 = st.columns(2)

        with col1:
            email_from = st.text_input(
                "Email From",
                value="customer@example.com",
                placeholder="sender@example.com",
            )
            email_to = st.text_input(
                "Email To",
                value="support@company.com",
                placeholder="support@company.com",
            )

        with col2:
            customer_name = st.text_input(
                "Customer Name (Optional)",
                value="John Doe",
                placeholder="Customer Name",
            )

        email_subject = st.text_input(
            "Subject",
            value="Billing issue with my account",
            placeholder="Email subject...",
        )
        email_body = st.text_area(
            "Body",
            value="I was charged twice for my last invoice. Can you help me resolve this?",
            placeholder="Email content...",
            height=150,
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button(
                label="⚡ Process Email",
                use_container_width=True,
                type="primary",
            )

    if submit_button:
        if not email_from or not email_to or not email_subject or not email_body:
            st.error("❌ Please fill in all required fields.")
        else:
            st.divider()

            # Step-by-step progress
            processing_steps = [
                ("📋", "Validating Email", "Checking format and fields..."),
                ("🏷️", "Classifying Email", "Determining email category..."),
                ("🔍", "Searching Knowledge Base", "Finding relevant articles..."),
                ("✍️", "Drafting Response", "Generating AI response..."),
                ("✅", "Processing Complete", "Ready to display results!"),
            ]

            progress_container = st.container(border=True)

            try:
                payload = {
                    "email_from": email_from,
                    "email_to": email_to,
                    "email_subject": email_subject,
                    "email_body": email_body,
                    "customer_name": customer_name if customer_name else None,
                }

                # Show progress visualization
                progress_cols = st.columns(len(processing_steps))

                with progress_container:
                    st.write("### 🤖 Agent Processing Pipeline")
                    for i, (emoji, step_name, step_desc) in enumerate(processing_steps):
                        with progress_cols[i]:
                            if i < 3:
                                st.spinner(f"{emoji} {step_name}")
                            else:
                                st.success(f"{emoji} {step_name}")
                        if i < len(processing_steps) - 1:
                            progress_cols[i].write("→")

                with st.spinner("🔄 Sending request to backend..."):
                    response = requests.post(
                        f"{API_BASE_URL}/process-email",
                        json=payload,
                        timeout=30,
                    )

                if response.status_code == 200:
                    result = response.json()

                    # Update progress
                    progress_container.success("✅ Email Processed Successfully!")

                    st.divider()

                    # Create tabs for results
                    tab1, tab2, tab3, tab4 = st.tabs(
                        ["📊 Analysis", "📝 Response", "📚 Knowledge", "📋 Details"]
                    )

                    with tab1:
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            classification = result.get("email_classification", "general")
                            st.markdown(
                                f"""
                                <div class="glass-card">
                                    <h4 style="margin-top: 0;">Classification</h4>
                                    {get_classification_badge(classification)}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        with col2:
                            confidence = result.get("confidence_score", 0.85)
                            st.markdown(
                                f"""
                                <div class="glass-card">
                                    <h4 style="margin-top: 0;">Confidence</h4>
                                    <h3 style="margin: 0.5rem 0; color: #0066FF;">{confidence:.0%}</h3>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        with col3:
                            review = result.get("requires_human_review", False)
                            st.markdown(
                                f"""
                                <div class="glass-card">
                                    <h4 style="margin-top: 0;">Review Status</h4>
                                    {'⚠️ Needs Review' if review else '✅ Auto-Handled'}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    with tab2:
                        st.subheader("🤖 AI Generated Response")
                        st.markdown(
                            f"""
                            <div class="glass-card" style="padding: 1.5rem; border-left: 4px solid #0066FF;">
                                {result.get('generated_response', '').replace(chr(10), '<br>')}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        col1, col2 = st.columns(2)
                        with col1:
                            st.button("📋 Copy Response", use_container_width=True)
                        with col2:
                            st.button("📤 Email to Sender", use_container_width=True)

                    with tab3:
                        knowledge = result.get("retrieved_knowledge", [])
                        if knowledge:
                            st.subheader("📚 Retrieved Knowledge Base Articles")
                            for i, article in enumerate(knowledge, 1):
                                st.markdown(
                                    f"""
                                    <div class="glass-card" style="margin: 0.5rem 0;">
                                        <span class="mono"><strong>Article {i}:</strong></span> {article}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.info("📭 No relevant knowledge articles retrieved.")

                    with tab4:
                        st.subheader("📋 Full Response Data")
                        st.json(result)

                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Cannot connect to the API. Make sure the backend server is running at "
                    f"`{API_BASE_URL}`"
                )
            except requests.exceptions.Timeout:
                st.error("❌ Request timeout. The server took too long to respond.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def page_inbox():
    """Page 2: Agent Inbox Dashboard with analytics."""
    st.header("📥 Agent Inbox Dashboard")
    st.markdown("View all processed emails with advanced analytics and insights.")

    # Refresh button
    col1, col2, col3 = st.columns([0.88, 0.06, 0.06])
    with col2:
        if st.button("🔄", help="Refresh inbox", use_container_width=True):
            st.rerun()

    try:
        with st.spinner("📬 Loading inbox..."):
            response = requests.get(
                f"{API_BASE_URL}/emails",
                params={"limit": 100, "offset": 0},
                timeout=10,
            )

        if response.status_code == 200:
            data = response.json()
            emails = data.get("emails", [])
            count = data.get("count", 0)

            if count == 0:
                st.info("📭 No emails in inbox yet. Send one using the 'Send Mock Email' page.")
            else:
                # Analytics Row
                st.subheader("📊 Visual Insights")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(
                        f"""
                        <div class="metric-card" style="text-align: center;">
                            <h3 style="margin: 0; color: #0066FF; font-size: 2.5rem;">{count}</h3>
                            <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">Total Emails</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col2:
                    human_review_count = sum(
                        1 for email in emails if email.get("requires_human_review", False)
                    )
                    st.markdown(
                        f"""
                        <div class="metric-card" style="text-align: center;">
                            <h3 style="margin: 0; color: #FFA500; font-size: 2.5rem;">{human_review_count}</h3>
                            <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">Needs Review</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col3:
                    auto_count = count - human_review_count
                    st.markdown(
                        f"""
                        <div class="metric-card" style="text-align: center;">
                            <h3 style="margin: 0; color: #22C55E; font-size: 2.5rem;">{auto_count}</h3>
                            <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">Auto-Handled</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col4:
                    resolve_rate = (auto_count / count * 100) if count > 0 else 0
                    st.markdown(
                        f"""
                        <div class="metric-card" style="text-align: center;">
                            <h3 style="margin: 0; color: #00D4FF; font-size: 2.5rem;">{resolve_rate:.0f}%</h3>
                            <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">Resolution Rate</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.divider()

                # Charts Row
                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    st.subheader("📊 Email Classification Distribution")
                    classifications = [email.get("classification", "general") for email in emails]
                    classification_counts = pd.Series(classifications).value_counts()

                    fig = px.pie(
                        values=classification_counts.values,
                        names=classification_counts.index,
                        color=classification_counts.index,
                        color_discrete_map=COLOR_PALETTE,
                        hole=0.4,
                    )
                    fig.update_layout(
                        paper_bgcolor="rgba(30, 41, 59, 0.5)",
                        plot_bgcolor="rgba(30, 41, 59, 0.5)",
                        font=dict(color="var(--text-primary)", family="Arial"),
                        showlegend=True,
                        height=400,
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with chart_col2:
                    st.subheader("✅ Resolution Status")
                    status_data = pd.DataFrame({
                        "Status": ["Auto-Handled", "Needs Review"],
                        "Count": [auto_count, human_review_count]
                    })

                    fig = px.bar(
                        status_data,
                        x="Status",
                        y="Count",
                        color="Status",
                        color_discrete_map={"Auto-Handled": "#22C55E", "Needs Review": "#FFA500"},
                    )
                    fig.update_layout(
                        paper_bgcolor="rgba(30, 41, 59, 0.5)",
                        plot_bgcolor="rgba(30, 41, 59, 0.5)",
                        font=dict(color="var(--text-primary)", family="Arial"),
                        showlegend=False,
                        height=400,
                    )
                    st.plotly_chart(fig, use_container_width=True)

                st.divider()

                # Email List
                st.subheader("📧 Email Queue")

                # Filters
                col1, col2 = st.columns(2)
                with col1:
                    filter_classification = st.multiselect(
                        "Filter by Classification",
                        options=["billing", "technical", "account", "complaint", "refund", "general"],
                        default=[],
                    )

                with col2:
                    filter_review = st.checkbox("Show only emails needing review")

                # Filter emails
                filtered_emails = emails
                if filter_classification:
                    filtered_emails = [
                        e for e in filtered_emails
                        if e.get("classification") in filter_classification
                    ]
                if filter_review:
                    filtered_emails = [
                        e for e in filtered_emails
                        if e.get("requires_human_review", False)
                    ]

                st.write(f"**Showing {len(filtered_emails)} email(s)**")
                st.write("")

                # Display emails in glass cards
                for idx, email in enumerate(filtered_emails, 1):
                    email_id = email.get("id", "")
                    subject = email.get("email_subject", "No Subject")
                    classification = email.get("classification", "general")
                    requires_review = email.get("requires_human_review", False)
                    created_at = email.get("created_at", "Unknown")[:10]

                    # Email card with glassmorphism
                    col1, col2 = st.columns([0.9, 0.1])

                    with col1:
                        st.markdown(
                            f"""
                            <div class="email-card">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.75rem;">
                                    <div>
                                        <h4 style="margin: 0 0 0.5rem 0;">[{idx}] {subject[:60]}</h4>
                                        <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
                                            {get_classification_badge(classification)}
                                            {get_status_badge(requires_review)}
                                        </div>
                                    </div>
                                    <small style="color: var(--text-secondary);">{created_at}</small>
                                </div>
                                <hr style="margin: 0.75rem 0;">
                                <div style="font-size: 0.9rem; color: var(--text-secondary);">
                                    <strong>From:</strong> {email.get('email_from')}<br>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        # Expandable email details
                        with st.expander("📖 View Full Email", expanded=False):
                            col_body, col_response = st.columns(2)

                            with col_body:
                                st.write("**Original Email Body:**")
                                st.markdown(
                                    f"""
                                    <div class="glass-card mono" style="white-space: pre-wrap;">
                                        {email.get("email_body", "")}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                            with col_response:
                                st.write("**AI Generated Response:**")
                                st.markdown(
                                    f"""
                                    <div class="glass-card" style="border-left: 4px solid #0066FF;">
                                        {email.get("generated_response", "")}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                            # Action buttons
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.button("✅ Mark as Resolved", key=f"resolve_{email_id}", use_container_width=True)
                            with col_b:
                                st.button("📋 Copy Response", key=f"copy_{email_id}", use_container_width=True)
                            with col_c:
                                st.button("📤 Email to Sender", key=f"send_{email_id}", use_container_width=True)

        else:
            st.error(f"Error fetching emails: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error(
            "❌ Cannot connect to the API. Make sure the backend server is running at "
            f"`{API_BASE_URL}`"
        )
    except requests.exceptions.Timeout:
        st.error("❌ Request timeout. The server took too long to respond.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


def page_api_reference():
    """Page 3: API Reference Documentation."""
    st.header("🔌 API Reference")
    st.markdown("Complete documentation for the Customer Support Email Agent API.")

    # Interactive Docs Section
    st.info(
        "📚 **Full Interactive Swagger UI** available at "
        "[http://localhost:8000/docs](http://localhost:8000/docs) - "
        "Try out all endpoints interactively with automatic request/response generation."
    )

    st.divider()

    # POST Endpoint
    st.subheader("📤 POST /api/v1/process-email")
    st.markdown("Submit an email for processing and get AI-generated response.")

    with st.expander("📋 Request Schema", expanded=True):
        st.code(
            """{
  "email_from": "customer@example.com",
  "email_to": "support@company.com",
  "email_subject": "Billing issue with my account",
  "email_body": "I was charged twice for my last invoice.",
  "customer_name": "John Doe",  // Optional
  "customer_id": "cust_123"      // Optional
}""",
            language="json",
        )

    with st.expander("🐍 Python Example", expanded=False):
        st.code(
            """import requests

# API endpoint
url = "http://localhost:8000/api/v1/process-email"

# Prepare payload
payload = {
    "email_from": "customer@example.com",
    "email_to": "support@company.com",
    "email_subject": "I need help with my billing",
    "email_body": "I was charged twice this month. Can you help?",
    "customer_name": "John Doe"
}

# Send request
response = requests.post(url, json=payload)

# Handle response
if response.status_code == 200:
    result = response.json()
    print(f"Classification: {result['email_classification']}")
    print(f"Response: {result['generated_response']}")
    print(f"Needs Review: {result['requires_human_review']}")
else:
    print(f"Error: {response.status_code}")""",
            language="python",
        )

    with st.expander("✅ Response Schema", expanded=False):
        st.code(
            """{
  "email_id": "550e8400-e29b-41d4-a716-446655440000",
  "email_subject": "Re: Billing issue with my account",
  "generated_response": "Thank you for contacting us...",
  "confidence_score": 0.92,
  "email_classification": "billing",
  "requires_human_review": false,
  "retrieved_knowledge": [
    "Billing Information Update",
    "Invoice Explanation"
  ],
  "suggested_actions": [...],
  "processing_steps": [...],
  "errors": null
}""",
            language="json",
        )

    st.divider()

    # GET Endpoint
    st.subheader("📥 GET /api/v1/emails")
    st.markdown("Retrieve all processed emails from the audit trail with pagination.")

    with st.expander("📋 Query Parameters", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**limit** (integer)")
            st.caption("Maximum emails to return. Default: 100")
        with col2:
            st.write("**offset** (integer)")
            st.caption("Number of records to skip. Default: 0")

    with st.expander("🐍 Python Example", expanded=False):
        st.code(
            """import requests

# API endpoint
url = "http://localhost:8000/api/v1/emails"

# Pagination parameters
params = {
    "limit": 50,
    "offset": 0
}

# Fetch emails
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    emails = data['emails']
    count = data['count']

    print(f"Retrieved {count} emails")
    for email in emails:
        print(f"- {email['email_subject']} "
              f"({email['classification']}) "
              f"[{'Needs Review' if email['requires_human_review'] else 'Auto-handled'}]")
else:
    print(f"Error: {response.status_code}")""",
            language="python",
        )

    with st.expander("✅ Response Schema", expanded=False):
        st.code(
            """{
  "emails": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email_from": "customer@example.com",
      "email_subject": "Billing issue",
      "email_body": "I was charged twice...",
      "classification": "billing",
      "generated_response": "Thank you for contacting us...",
      "requires_human_review": false,
      "created_at": "2026-03-12T10:30:45.123456"
    },
    ...
  ],
  "count": 42
}""",
            language="json",
        )

    st.divider()

    # Response Schemas Section
    st.subheader("📊 Response Schemas")

    with st.expander("EmailResponse Fields", expanded=True):
        st.markdown("""
        | Field | Type | Description |
        |-------|------|-------------|
        | `email_id` | string | Unique identifier for the email |
        | `email_subject` | string | Subject line (prefixed with "Re:") |
        | `generated_response` | string | AI-generated email response |
        | `confidence_score` | float | Confidence in response (0-1) |
        | `email_classification` | string | Category: billing, technical, account, complaint, refund, general |
        | `requires_human_review` | boolean | Whether email needs human intervention |
        | `retrieved_knowledge` | array | List of relevant knowledge base articles |
        | `suggested_actions` | array | Recommended next steps |
        | `processing_steps` | array | Workflow steps completed |
        | `errors` | array | Any errors encountered during processing |
        """)

    with st.expander("Classification Categories", expanded=False):
        st.markdown("""
        - **Billing** 💳 - Invoice, payment, refund, duplicate charge issues
        - **Technical** ⚙️ - API errors, integration, authentication, rate limiting
        - **Account** 👤 - Password reset, 2FA, login issues, security
        - **Complaint** 😠 - Customer complaints and issues
        - **Refund** 💰 - Refund requests and processing
        - **General** 📝 - Onboarding, pricing, support, general inquiries
        """)

    st.divider()

    # Error Handling Section
    st.subheader("⚠️ Error Handling")

    with st.expander("HTTP Status Codes", expanded=True):
        st.markdown("""
        | Code | Meaning | Solution |
        |------|---------|----------|
        | 200 | Success | Request processed successfully |
        | 400 | Bad Request | Invalid JSON or missing required fields |
        | 404 | Not Found | Email ID doesn't exist |
        | 500 | Server Error | Internal server error - check logs |
        """)

    st.divider()

    # Embed Swagger UI
    st.subheader("🎮 Interactive Swagger UI")
    st.markdown(
        "Click below to open the Swagger UI where you can test all endpoints directly:"
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.link_button(
            "🔗 Open Swagger UI",
            "http://localhost:8000/docs",
            use_container_width=True,
        )


def main():
    """Main application."""
    # Sidebar navigation
    st.sidebar.image(
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect fill='%230066FF' width='100' height='100' rx='20'/%3E%3Ctext x='50' y='55' font-size='60' fill='white' text-anchor='middle' dominant-baseline='middle'%3E✉️%3C/text%3E%3C/svg%3E",
        width=80,
    )

    st.sidebar.title("Support Agent")
    st.sidebar.markdown("**Premium Command Center**")
    st.sidebar.markdown("---")

    # Page selection
    page = st.sidebar.radio(
        "Navigation",
        options=["✉️ Send Email", "📥 Inbox", "🔌 API Docs"],
        index=0,
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        ### System Status
        **Backend:** 🟢 Online
        **Database:** 🟢 Connected
        **AI Model:** Groq LLM

        ### Features
        - 🤖 AI Email Classification
        - 📚 FAISS RAG Pipeline
        - 💾 Persistent Audit Trail
        - 📊 Real-time Analytics
        """
    )

    # Route to appropriate page
    if page == "✉️ Send Email":
        page_send_email()
    elif page == "📥 Inbox":
        page_inbox()
    else:
        page_api_reference()


if __name__ == "__main__":
    main()
