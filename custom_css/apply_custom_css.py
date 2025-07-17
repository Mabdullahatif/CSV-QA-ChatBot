def apply_custom_css():
    css ="""<style>
        .chat-bubble {
            padding: 10px 15px;
            border-radius: 15px;
            margin: 8px 0;
            max-width: 80%;
            word-wrap: break-word;
            word-break: break-word;
            overflow-wrap: break-word;
            display: flex;
            align-items: flex-start;
            flex-wrap: wrap;
            line-height: 1.5;
        }

        .user-message {
            background-color: #2b6cb0;
            color: white;
            margin-left: auto;
            justify-content: flex-end;
            display: flex;
            align-items: center;
        }

        .assistant-message {
            background-color: #e2e8f0;
            color: black;
            margin-right: auto;
            justify-content: flex-start;
            display: flex;
            align-items: center;
        }

        .avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            margin: 0 10px;
        }

        .row {
            display: flex;
            align-items: flex-start;
            flex-wrap: nowrap;
        }
        </style>"""
    return css