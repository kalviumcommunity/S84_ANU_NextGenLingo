def execute_action(action_name, params):
    """
    Executes backend actions based on intent.
    """
    if action_name == "send_email":
        # Here, simulate sending email
        to = params.get("to")
        subject = params.get("subject")
        body = params.get("body", "")
        # In real app, integrate with email service here
        print(f"Sending email to {to} with subject '{subject}'. Body: {body}")
        return f"Email has been sent to {to} with subject '{subject}'."
    
    elif action_name == "add_todo":
        task = params.get("task")
        # Simulate adding to a todo list
        print(f"Added TODO task: {task}")
        return f"Task '{task}' added to your to-do list."
    
    elif action_name == "weather":
        location = params.get("location", "your area")
        # Simulate weather API call
        print(f"Fetching weather for {location}")
        return f"The weather in {location} is sunny and warm today."
    
    else:
        return "Sorry, I don't recognize that action."

# Sample usage
if __name__ == "__main__":
    print(execute_action("send_email", {"to": "user@example.com", "subject": "Meeting Reminder", "body": "Don't forget the meeting at 3 PM."}))
    print(execute_action("add_todo", {"task": "Finish the project report"}))
    print(execute_action("weather", {"location": "New York"}))
