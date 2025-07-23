def apply_custom_css():
    css ="""
        <style>
            .main-header {
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 1rem;
            }
            .chat-message {
                padding: 1rem;
                border-radius: 0.5rem;
                margin-bottom: 1rem;
                display: flex;
                align-items: flex-start;
            }
            .user-message {
                background-color: #10b981;
                color: white;
            }
            .bot-message {
                background-color: #1e1e1e;
                border: 1px solid #333;
                color: white;
            }
            .message-content {
                margin-left: 1rem;
            }
            .block-container {
                padding-top: 2rem;
            }
            .stFileUploader {
                padding: 2rem;
                border: 2px dashed #10b981;
                border-radius: 0.5rem;
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 1rem;
            }
            .stTabs [data-baseweb="tab"] {
                height: 3rem;
                white-space: pre-wrap;
                background-color: #1e1e1e;
                border-radius: 0.5rem;
            }
            .stTabs [aria-selected="true"] {
                background-color: #10b981 !important;
                color: white !important;
            }
            .card {
                border-radius: 0.5rem;
                padding: 1.5rem;
                margin-bottom: 1rem;
                background-color: #1e1e1e;
                border: 1px solid #333;
            }
        </style>
        """
    return css