from flask import Flask, request, render_template_string, session
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure Gemini API
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    messages = session.get('messages', [])
    if not messages:
        # Add welcome message
        messages.append({"sender": "Bot", "text": "Hi! I'm your Smart Product Assistant. Ask me anything about products, reviews, or just say hi!"})
        session['messages'] = messages
        
    if request.method == 'POST':
        user_message = request.form.get('message', '').strip()
        if user_message:
            try:
                # Format prompt to ensure tabular and pointwise response for product queries while behaving normally otherwise
                prompt = f"""You are an advanced AI assistant. You answer exactly like Gemini would. 
If the user asks for product information or product reviews, ALWAYS present the information using Markdown tables and point-wise lists. 
CRITICAL RULE: Whenever mentioning any price or cost, ALWAYS provide the value in Indian Rupees (INR) format (e.g., ₹80,000). Convert the price to INR if necessary.
For other casual conversation, just answer normally.

User: {user_message}"""
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                bot_text = response.text
            except Exception as e:
                import traceback
                traceback.print_exc()
                bot_text = f"I'm having trouble connecting right now. Error: {str(e)}"
                
            messages.append({"sender": "User", "text": user_message})
            messages.append({"sender": "Bot", "text": bot_text})
            session['messages'] = messages
            session.modified = True

    # Use marked.js to render Markdown on the frontend
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Product Review & Info Chatbot</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <!-- Include Marked.js for Markdown parsing -->
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <!-- Include DOMPurify to sanitize markdown output -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.0.6/purify.min.js"></script>
        
        <style>
            :root {
                --primary: #6366f1;
                --primary-dark: #4f46e5;
                --bot-bg: rgba(255, 255, 255, 0.85);
                --user-bg: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                --text-dark: #1e293b;
                --text-light: #f8fafc;
            }
            
            body { 
                font-family: 'Inter', sans-serif; 
                margin: 0; 
                padding: 20px; 
                color: var(--text-dark);
                background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                box-sizing: border-box;
            }

            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            .container { 
                width: 100%;
                max-width: 1000px; 
                background: rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 24px; 
                box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25); 
                overflow: hidden; 
                display: flex;
                flex-direction: column;
            }

            h1 { 
                background: rgba(255, 255, 255, 0.1);
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                color: white; 
                margin: 0; 
                padding: 25px; 
                text-align: center; 
                font-size: 28px; 
                font-weight: 600;
                letter-spacing: -0.5px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            .chat-container { 
                height: 550px; 
                overflow-y: auto; 
                padding: 30px; 
                display: flex;
                flex-direction: column;
                gap: 20px;
                scrollbar-width: thin;
                scrollbar-color: rgba(255,255,255,0.5) transparent;
            }

            .chat-container::-webkit-scrollbar {
                width: 6px;
            }
            .chat-container::-webkit-scrollbar-thumb {
                background: rgba(255,255,255,0.5);
                border-radius: 10px;
            }

            .message { 
                padding: 16px 20px; 
                border-radius: 20px; 
                max-width: 80%; 
                word-wrap: break-word; 
                line-height: 1.6; 
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                animation: slideUp 0.3s ease-out forwards;
                opacity: 0;
                transform: translateY(10px);
            }
            
            /* Markdown Styles inside message */
            .message p { margin-top: 0; margin-bottom: 10px; }
            .message p:last-child { margin-bottom: 0; }
            .message ul, .message ol { margin-top: 0; padding-left: 20px; }
            .message code { background: rgba(0,0,0,0.05); padding: 2px 4px; border-radius: 4px; font-family: monospace; }
            .message pre { background: rgba(0,0,0,0.05); padding: 10px; border-radius: 8px; overflow-x: auto; }
            
            @keyframes slideUp {
                to { opacity: 1; transform: translateY(0); }
            }

            .user { 
                background: var(--user-bg); 
                color: var(--text-light); 
                align-self: flex-end; 
                border-bottom-right-radius: 4px; 
            }

            .bot { 
                background: var(--bot-bg); 
                color: var(--text-dark); 
                align-self: flex-start; 
                border-bottom-left-radius: 4px; 
                backdrop-filter: blur(8px);
            }

            .message-sender { 
                display: block; 
                margin-bottom: 8px; 
                font-weight: 600;
            }

            form { 
                display: flex; 
                padding: 20px; 
                background: rgba(255, 255, 255, 0.1); 
                border-top: 1px solid rgba(255, 255, 255, 0.2); 
                gap: 15px; 
                align-items: center;
            }

            input { 
                flex: 1; 
                padding: 15px 20px; 
                background: rgba(255, 255, 255, 0.9);
                border: 2px solid transparent; 
                border-radius: 30px; 
                font-size: 15px; 
                font-family: 'Inter', sans-serif;
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }

            input:focus { 
                outline: none; 
                border-color: var(--primary); 
                box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
            }

            button { 
                padding: 15px 35px; 
                background: var(--primary); 
                color: white; 
                border: none; 
                border-radius: 30px; 
                cursor: pointer; 
                font-weight: 600; 
                font-size: 15px;
                font-family: 'Inter', sans-serif;
                transition: all 0.3s ease; 
                box-shadow: 0 4px 6px rgba(99, 102, 241, 0.3);
            }

            button:hover { 
                background: var(--primary-dark); 
                transform: translateY(-2px); 
                box-shadow: 0 6px 12px rgba(99, 102, 241, 0.4);
            }

            a { 
                color: white; 
                text-decoration: none; 
                font-size: 14px;
                font-weight: 500;
                padding: 10px 15px; 
                border-radius: 20px; 
                background: rgba(255,255,255,0.1);
                transition: all 0.2s;
            }

            a:hover { 
                background: rgba(255,255,255,0.2); 
            }

            table { 
                width: 100%; 
                border-collapse: separate; 
                border-spacing: 0;
                margin-top: 15px; 
                margin-bottom: 15px;
                font-size: 0.95em; 
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                background: white;
            }

            th, td { 
                padding: 12px 15px; 
                border-bottom: 1px solid rgba(0,0,0,0.05);
                line-height: 1.5;
                text-align: left;
            }

            th { 
                background-color: rgba(99, 102, 241, 0.1); 
                font-weight: 600; 
                color: var(--primary-dark);
                text-transform: uppercase;
                font-size: 0.85em;
                letter-spacing: 0.5px;
            }

            tr:last-child td {
                border-bottom: none;
            }

            tr:hover td { 
                background-color: #f8fafc; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✨ Smart Product Assistant</h1>
            <div class="chat-container" id="chat">
                {% for msg in messages %}
                <div class="message {{ 'user' if msg.sender == 'User' else 'bot' }}">
                    <strong class="message-sender">{{ msg.sender }}:</strong> 
                    <div class="message-content" style="display:none;">{{ msg.text }}</div>
                    <div class="rendered-content"></div>
                </div>
                {% endfor %}
            </div>
            <form method="post" id="chatForm">
                <input type="text" id="message" name="message" placeholder="Ask about a product, reviews, or just say hi..." required autofocus autocomplete="off">
                <button type="submit">Send</button>
                <a href="/clear">Clear Chat</a>
            </form>
        </div>
        <script>
            // Parse all markdown content
            document.querySelectorAll('.message').forEach(msgDiv => {
                const rawDiv = msgDiv.querySelector('.message-content');
                if (rawDiv) {
                    const renderedDiv = msgDiv.querySelector('.rendered-content');
                    // Render markdown and set it
                    renderedDiv.innerHTML = DOMPurify.sanitize(marked.parse(rawDiv.textContent));
                }
            });
            
            // Scroll to bottom
            const chat = document.getElementById('chat');
            chat.scrollTop = chat.scrollHeight;
        </script>
    </body>
    </html>
    ''', messages=messages)

@app.route('/clear')
def clear():
    session.pop('messages', None)
    return "<script>window.location.href='/';</script>"

if __name__ == "__main__":
    app.run(debug=True)