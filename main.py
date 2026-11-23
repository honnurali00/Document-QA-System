
# ==================================================
# DOCUMENT QUESTION ANSWERING SYSTEM
# Rule-Based AI Application
# ==================================================


# STEP 1: READ DOCUMENT AND CREATE KNOWLEDGE BASE

def read_document(filename):

    knowledge_base = {}

    try:
        with open(filename, "r", encoding="utf-8") as file:

            for line in file:

                if ":" in line:

                    key, value = line.split(":", 1)

                    key = key.strip().lower()
                    value = value.strip()

                    if key and value:
                        knowledge_base[key] = value

        return knowledge_base

    except FileNotFoundError:
        print("Error: Document not found!")
        return {}


# STEP 2: DEFINE QUESTION RULES

question_rules = {

    "assignment submission date": [
        "submission date",
        "due date",
        "when is the assignment due"
    ],

    "course code": [
        "course code",
        "code of the course"
    ],

    "course title": [
        "course title",
        "course name",
        "subject name"
    ],

    "institution": [
        "institution",
        "university",
        "college"
    ],

    "department": [
        "department",
        "branch"
    ],

    "programme": [
        "programme",
        "program",
        "degree"
    ],

    "semester": [
        "semester",
        "batch"
    ],

    "course leader": [
        "course leader",
        "faculty",
        "leader"
    ],

    "maximum marks": [
        "maximum marks",
        "max marks",
        "total marks"
    ],

    "obtained marks": [
        "obtained marks",
        "marks obtained"
    ],

    "assignment": [
        "assignment",
        "assessment"
    ],

    "document processing": [
        "document processing",
        "how is the document processed"
    ],

    "question processing": [
        "question processing",
        "how are questions processed"
    ],

    "answer generation": [
        "answer generation",
        "how are answers generated"
    ],

    "prohibited techniques": [
        "prohibited techniques",
        "which techniques are not allowed"
    ]
}


# STEP 3: IDENTIFY THE QUESTION FIELD

def identify_field(question):

    question = question.lower().strip()

    for field, keywords in question_rules.items():

        for keyword in keywords:

            if keyword in question:
                return field

    return None


# STEP 4: GENERATE ANSWERS

def generate_answer(field, value):

    if field == "maximum marks":
        return "The maximum marks are " + value + "."

    elif field == "prohibited techniques":
        return "The prohibited techniques are " + value + "."

    elif field == "assignment":
        return "The assignment is " + value + "."

    elif field == "document processing":
        return "Document processing involves: " + value

    elif field == "question processing":
        return "Question processing involves: " + value

    elif field == "answer generation":
        return "Answer generation involves: " + value

    else:
        return "The " + field + " is " + value + "."


# STEP 5: PROCESS QUESTIONS AND APPLY INFERENCE

def process_question(question, knowledge_base):

    question = question.lower().strip()

    print("\n--- REASONING TRACE ---")
    print("Step 1: Question received:", question)

    # Inference rule: Calculate percentage

    if "percentage" in question:

        if "maximum marks" not in knowledge_base or \
           "obtained marks" not in knowledge_base:

            return "Required marks information is missing."

        try:

            maximum = float(knowledge_base["maximum marks"])
            obtained = float(knowledge_base["obtained marks"])

            if maximum <= 0:
                return "Maximum marks must be greater than zero."

            if obtained < 0 or obtained > maximum:
                return "Obtained marks must be between zero and maximum marks."

            percentage = (obtained / maximum) * 100

            print("Step 2: Retrieved obtained marks:", obtained)
            print("Step 3: Retrieved maximum marks:", maximum)
            print("Step 4: Applied percentage formula")
            print("Step 5: Calculated percentage:", percentage)

            return (
                "The calculated percentage is "
                + str(round(percentage, 2)) + "%."
            )

        except ValueError:

            return "Marks must be numeric values."

    # Rule-based question processing

    field = identify_field(question)

    if field:

        print("Step 2: Matching field identified:", field)

        if field in knowledge_base:

            answer = knowledge_base[field]

            print("Step 3: Information retrieved from knowledge base.")
            print("Step 4: Answer generated successfully.")

            return generate_answer(field, answer)

    print("Step 2: No matching information found.")

    return (
        "Sorry, the requested information "
        "could not be found in the document."
    )


# STEP 6: EVALUATE SYSTEM PERFORMANCE

def evaluate_system(knowledge_base):

    test_questions = [

        ("What is the course code?", "AID201A"),

        ("What is the course title?", "Artificial Intelligence"),

        ("What are the maximum marks?", "15"),

        ("What is the assignment submission date?",
         "20th November 2026")

    ]

    correct = 0
    total = len(test_questions)

    print("\n========== SYSTEM EVALUATION ==========")

    for question, expected in test_questions:

        field = identify_field(question)

        if field and field in knowledge_base:

            answer = knowledge_base[field]

        else:

            answer = ""

        if expected.lower() in answer.lower():

            print("PASS:", question)
            correct += 1

        else:

            print("FAIL:", question)
            print("Expected:", expected)
            print("Received:", answer)

    accuracy = (correct / total) * 100

    print("\n========== EVALUATION RESULTS ==========")
    print("Total Questions:", total)
    print("Correct Answers:", correct)
    print("Incorrect Answers:", total - correct)
    print("Test Accuracy:", str(round(accuracy, 2)) + "%")


# STEP 7: MAIN APPLICATION

def main():

    print("=" * 50)
    print(" DOCUMENT QUESTION ANSWERING SYSTEM")
    print("=" * 50)

    knowledge_base = read_document("document.txt")

    if not knowledge_base:

        print("Knowledge base could not be created.")
        return

    print("\nDocument processed successfully!")
    print("Knowledge base created successfully!")

    # Automatically evaluate the system

    evaluate_system(knowledge_base)

    print("\nYou can now ask questions about the document.")
    print("Type 'exit' to close the application.")

    # Interactive question-answering loop

    while True:

        question = input("\nEnter your question: ")

        if question.lower().strip() == "exit":

            print("Thank you for using the system!")
            break

        if not question.strip():

            print("Please enter a question.")
            continue

        answer = process_question(
            question,
            knowledge_base
        )

        print("\nAnswer:", answer)


# STEP 8: START APPLICATION

if __name__ == "__main__":

    main()
