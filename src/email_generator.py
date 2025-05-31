from utils.logger import log
from utils.model_manager import get_model

def generate_work_status_email(changes: str):
    log("[generate_work_status_email] Attempting to retrieve LLM model...")
    llm = get_model()
    
    if llm is None:
        log("[generate_work_status_email] No model available. Aborting email generation.")
        print("No model available for email generation.")
        return

    log("[generate_work_status_email] Model retrieved successfully. Constructing prompt...")

    prompt = f"""
You are an AI assistant tasked with composing a professional and detailed daily work status email based on the provided summary of completed tasks.

The email should:
- Begin with a courteous greeting and brief introduction.
- List all completed tasks provided in the input, no matter how many, each with a clear, concise explanation describing what was done, its purpose, key results, and any next steps.
- Present the tasks as a numbered list.
- Use proper formatting for readability: include blank lines between paragraphs and tasks, consistent indentation, and clear separation of sections.
- Maintain a formal, respectful, and polished tone throughout.
- Offer availability for any follow-up questions or clarifications.
- Close with a polite sign-off.

Use the following template as a guideline, but generate a well-formatted email that is easy to read:

Subject: Daily Work Status - Abhishek Mishra - [Today's Date in DD/MM/YYYY]

Dear Sir,

I hope this email finds you well. Please find below a detailed summary of the work I completed today:

Completed Tasks:

1. Task 1: [Description of the task, accomplishments, significance, and next steps]

2. Task 2: [Description of the task, accomplishments, significance, and next steps]

3. Task 3: [And so on for all tasks provided…]

Please let me know if you require any additional information or clarification on any of the above tasks. I am happy to provide further details as needed.

Thank you for your time and consideration.

Best regards,  
Abhishek Mishra

Kindly update the email content based on the following work done today:  
{changes}
"""

    log("[generate_work_status_email] Prompt constructed. Sending to model for response...")
    
    try:
        response = llm.parse(prompt)
        log("[generate_work_status_email] Response received successfully from model.")
        return response
    except Exception as e:
        log(f"[generate_work_status_email] Error while generating response from model: {e}")
        return None
