import streamlit as st
# from openai import OpenAI
# import openai
import base64
# Set your OpenAI API key


# Define a function to interact with OpenAI API
def generate_questions(course, chapter, difficulty, num_questions):
    prompt = f"Can you give me {num_questions} practice questions of {course}, {chapter} with difficulty scale {difficulty}/100? Please just list the questions without saying anything else such as the sentence before \n\n1."
    client = OpenAI()
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}]
    )
    content = completion.choices[0].message.content
    questions = [f"Question-{i+1}: {line.strip()}" for i, line in enumerate(content.split("\n")) if line.strip()]
    return questions
def chat_with_gpt(prompt):
    client = OpenAI()
    completion = client.chat_completion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content

# Define a function to check if the user input is related to the generated questions
def is_related_to_generated_questions(user_input, generated_questions):
    for question in generated_questions:
        if question.lower() in user_input.lower():
            return True
    return False

# Define the Streamlit chatbot component
def chatbot_component(generated_questions):
    st.sidebar.subheader("Chat with the ChatGPT")
    user_input = st.sidebar.text_input("You:", "")
    if st.sidebar.button("Send"):
        if user_input.strip():
            if is_related_to_generated_questions(user_input, generated_questions):
                response = chat_with_gpt(user_input)
                st.sidebar.text_area("ChatGPT:", value=response, height=200)
            else:
                st.sidebar.text_area("ChatGPT:", value="Sorry, please ask questions related to the generated questions.", height=200)


def generate_answers(questions):
    client = OpenAI(api_key="------------")
    answers = []
    for i, question in enumerate(questions, 1):
        prompt = "Question: {}\nAnswer:".format(question)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        answer = completion.choices[0].message.content.strip()
        answers.append(answer)
    return answers

def write_to_file(questions, answers):
    file_content = ""
    for question, answer in zip(questions, answers):
        file_content += f"{question}\n{answer}\n\n"

    # Encode file content as base64
    file_content_encoded = base64.b64encode(file_content.encode()).decode()

    return file_content_encoded
def main():
    st.sidebar.markdown(
        """
        <style>
            .sidebar .sidebar-content {
                background-color: black;
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Center the title
    st.markdown("<h1 style='text-align: center;'>🎆 𝐸𝓍𝒶𝓂 𝒫𝓇𝑒𝓅𝒜𝐼🎆</h1>", unsafe_allow_html=True)

    # Sidebar for input fields
    st.sidebar.header("Input Fields")
    course = st.sidebar.text_input("Enter the course name:")
    chapter = st.sidebar.text_input("Enter the chapter name:")
    difficulty = st.sidebar.slider("Select the difficulty level:", 1, 100)
    num_questions = st.sidebar.number_input("Enter the number of questions:", min_value=1, step=1, value=5)

    # Generate button
    generate_button = st.sidebar.button("Generate Questions")

    # Display generated questions and answers
    if generate_button:
        if course and chapter:
            st.subheader("Prompt:")
            prompt = f"Can you give me {num_questions} practice questions of {course}, {chapter} with difficulty scale {difficulty}/100?"
            st.write(prompt)

            st.subheader("Generated Questions:")
            questions = generate_questions(course, chapter, difficulty, num_questions)
            st.write(questions)

            st.subheader("Generated Answers:")
            answers = generate_answers(questions)
            
            for i, answer in enumerate(answers, 1):
                st.write(f"Question {i}: {questions[i-1]}")
                st.write(f"Answer {i}: {answer}")

            # Write questions and answers to a text file
            file_content_encoded = write_to_file(questions, answers)

            # Provide download link for the text file
            href = f'data:file/txt;base64,{file_content_encoded}'
            st.markdown(
                f'<a href="{href}" download="questions_and_answers.txt">Download query</a>',
                unsafe_allow_html=True )
        else:
            st.sidebar.error("Please fill in the course and chapter fields.")
     

  

if __name__ == "__main__":
    main()
