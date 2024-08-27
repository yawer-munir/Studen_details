import streamlit as st
import sqlite3
st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Connect to the SQLite database
conn = sqlite3.connect('student_details.db')
c = conn.cursor()

# Create a table to store the name and father's name
c.execute('''
          CREATE TABLE IF NOT EXISTS student_details
          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
          name TEXT, 
          rollNo INTEGER,
          semester INTEGER,
          subject TEXT)''')
conn.commit()

# Form visible for students
with st.form(key='student_details'):
    st.markdown('<h1 class="title">Student Card Details</h1>', unsafe_allow_html=True)
    name = st.text_input("Please Enter Your Name",placeholder="Type your name here...")
    # rollNo = st.number_input("Please Enter Your Roll#")
    rollNo = st.number_input(
    "Please Enter Your RollNo:", 
    format="%d",       # This specifies that only integers should be accepted
    step=1             # This ensures the input increments by 1
)
    semester = st.selectbox('Semester',[1,3,5,7])
    subject = st.selectbox('Subject',['Computer Science','Electronics','Maths'])
    submit_button = st.form_submit_button(label='Submit')

# storing data

if submit_button:
    # Insert form data into the database
    c.execute("INSERT INTO student_details (name, rollNo,semester,subject) VALUES (?, ?,?,?)", (name, rollNo,semester,subject))
    conn.commit()
    st.success("Data saved successfully!")
    # Clear the form inputs
    st.session_state.name = ""
    st.session_state.rollNo = ""
    st.session_state.semester = ""
    st.session_state.subject = ""

# Option to display stored data
if st.button('Show Data'):
    c.execute("SELECT * FROM student_details")
    data = c.fetchall()
    if data:
        for row in data:
            st.write(f"ID: {row[0]} | name: {row[1]} | rollNo: {row[2]} | semester: {row[3]} | subject:{row[4]}")
    else:
        st.write("No data found.")

# Close the database connection when the app finishes
conn.close()
