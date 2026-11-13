
import streamlit as st
import sqlite3
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StudentHub | Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DATABASE ----------------
def get_connection():
    return sqlite3.connect("students.db")

def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE,
            name TEXT,
            age INTEGER,
            course TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

create_table()

def get_students():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM students ORDER BY id DESC", conn)
    conn.close()
    return df

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Main application */
.stApp {
    background-color: #f4f6fc;
    color: #111827;
}

/* Main page text */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp label,
.stApp .stMarkdown,
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricValue"] {
    color: #111827;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #202b46);
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Brand */
.brand {
    font-size: 27px;
    font-weight: 800;
    color: #a5b4fc !important;
    padding: 12px 0 4px 0;
}

.brand-sub {
    color: #cbd5e1 !important;
    font-size: 12px;
    margin-bottom: 25px;
}

/* Page headings */
.main-title {
    font-size: 32px;
    font-weight: 800;
    color: #172554 !important;
}

.subtitle {
    color: #64748b !important;
    font-size: 14px;
    margin-bottom: 25px;
}

.section-heading {
    font-size: 21px;
    font-weight: 700;
    color: #1e293b !important;
    margin-top: 20px;
    margin-bottom: 12px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricValue"] {
    color: #111827 !important;
}

/* Input boxes */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    border: 1px solid #cbd5e1;
}

/* Input placeholders */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
}

/* Dropdown */
.stSelectbox div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #111827 !important;
}

.stSelectbox div[data-baseweb="select"] * {
    color: #111827 !important;
}

/* Forms */
div[data-testid="stForm"] {
    background: #ffffff;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #e2e8f0;
}

/* Buttons */
div.stButton > button,
div.stFormSubmitButton > button {
    background-color: #4f46e5;
    color: #ffffff !important;
    border: none;
    border-radius: 9px;
    font-weight: 600;
}

div.stButton > button *,
div.stFormSubmitButton > button * {
    color: #ffffff !important;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background-color: #3730a3;
}

/* Tables */
[data-testid="stDataFrame"] {
    background: #ffffff;
    color: #111827;
}

/* Download button */
.stDownloadButton button {
    background-color: #4f46e5;
    color: white !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b !important;
    font-size: 12px;
    padding: 30px 0 10px;
}
</style>

""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown('<div class="brand">🎓 StudentHub</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="brand-sub">STUDENT MANAGEMENT PORTAL</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    menu = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "➕ Add Student",
            "📋 Student Directory",
            "✏️ Update Student",
            "🗑️ Delete Student"
        ]
    )

    st.markdown("---")
    st.markdown("**StudentHub v1.0**")
    st.caption("Academic Record Management")


# ---------------- FETCH DATA ----------------
df = get_students()


# ---------------- DASHBOARD ----------------
if menu == "🏠 Dashboard":

    st.markdown('<div class="main-title">Welcome to StudentHub 👋</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">Your centralized student record management dashboard.</div>',
        unsafe_allow_html=True
    )

    total_students = len(df)
    total_courses = df["course"].nunique() if not df.empty else 0
    average_age = round(df["age"].mean(), 1) if not df.empty else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("👨‍🎓 Total Students", total_students)
    col2.metric("📚 Total Courses", total_courses)
    col3.metric("📊 Average Age", average_age)

    st.markdown('<div class="section-heading">Recent Students</div>',
                unsafe_allow_html=True)

    if not df.empty:
        recent = df[["roll_no", "name", "course", "email"]].head(5)
        recent.columns = ["Roll Number", "Student Name", "Course", "Email"]

        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No student records yet. Start by adding your first student!")

    st.markdown('<div class="section-heading">Quick Overview</div>',
                unsafe_allow_html=True)

    if not df.empty:
        course_count = df["course"].value_counts().reset_index()
        course_count.columns = ["Course", "Students"]

        st.bar_chart(
            course_count.set_index("Course"),
            use_container_width=True
        )
    else:
        st.caption("Course statistics will appear once students are registered.")


# ---------------- ADD STUDENT ----------------
elif menu == "➕ Add Student":

    st.markdown('<div class="main-title">Add New Student</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">Register a student and add their academic information.</div>',
        unsafe_allow_html=True
    )

    with st.form("add_form"):

        st.subheader("Personal & Academic Details")

        col1, col2 = st.columns(2)

        with col1:
            roll_no = st.text_input("Roll Number *", placeholder="e.g. 101")
            name = st.text_input("Full Name *", placeholder="Enter student name")
            age = st.number_input("Age", min_value=1, max_value=100, value=18)

        with col2:
            course = st.text_input("Course *", placeholder="e.g. B.Tech CSE")
            email = st.text_input("Email Address *", placeholder="student@email.com")

        submitted = st.form_submit_button(
            "➕ Register Student",
            use_container_width=True
        )

        if submitted:
            if not all([roll_no.strip(), name.strip(),
                        course.strip(), email.strip()]):
                st.warning("Please fill in all required fields.")

            elif "@" not in email or "." not in email.split("@")[-1]:
                st.warning("Please enter a valid email address.")

            else:
                try:
                    conn = get_connection()

                    conn.execute("""
                        INSERT INTO students
                        (roll_no, name, age, course, email)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        roll_no.strip(),
                        name.strip(),
                        age,
                        course.strip(),
                        email.strip()
                    ))

                    conn.commit()
                    conn.close()

                    st.success("Student registered successfully! 🎉")
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("This roll number already exists.")


# ---------------- STUDENT DIRECTORY ----------------
elif menu == "📋 Student Directory":

    st.markdown('<div class="main-title">Student Directory</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">View and search all registered student records.</div>',
        unsafe_allow_html=True
    )

    search = st.text_input(
        "🔍 Search Students",
        placeholder="Search by name, roll number or course..."
    )

    if not df.empty:

        filtered_df = df.copy()

        if search:
            mask = (
                filtered_df["name"].str.contains(search, case=False, na=False) |
                filtered_df["roll_no"].str.contains(search, case=False, na=False) |
                filtered_df["course"].str.contains(search, case=False, na=False)
            )
            filtered_df = filtered_df[mask]

        st.caption(f"Showing {len(filtered_df)} of {len(df)} students")

        display_df = filtered_df[
            ["id", "roll_no", "name", "age", "course", "email"]
        ].copy()

        display_df.columns = [
            "ID", "Roll Number", "Name", "Age", "Course", "Email"
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        csv = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Student Records",
            data=csv,
            file_name="student_records.csv",
            mime="text/csv"
        )

    else:
        st.info("No student records available.")


# ---------------- UPDATE STUDENT ----------------
elif menu == "✏️ Update Student":

    st.markdown('<div class="main-title">Update Student Details</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">Modify existing student information.</div>',
        unsafe_allow_html=True
    )

    if not df.empty:

        selected_roll = st.selectbox(
            "Select Student Roll Number",
            df["roll_no"].tolist()
        )

        student = df[df["roll_no"] == selected_roll].iloc[0]

        with st.form("update_form"):

            col1, col2 = st.columns(2)

            with col1:
                st.text_input("Roll Number", value=student["roll_no"],
                              disabled=True)

                new_name = st.text_input(
                    "Student Name", value=student["name"]
                )

                new_age = st.number_input(
                    "Age", min_value=1, max_value=100,
                    value=int(student["age"])
                )

            with col2:
                new_course = st.text_input(
                    "Course", value=student["course"]
                )

                new_email = st.text_input(
                    "Email", value=student["email"]
                )

            update = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True
            )

            if update:

                if not all([new_name.strip(), new_course.strip(),
                            new_email.strip()]):
                    st.warning("Please fill in all fields.")

                else:
                    conn = get_connection()

                    conn.execute("""
                        UPDATE students
                        SET name=?, age=?, course=?, email=?
                        WHERE roll_no=?
                    """, (
                        new_name.strip(),
                        new_age,
                        new_course.strip(),
                        new_email.strip(),
                        selected_roll
                    ))

                    conn.commit()
                    conn.close()

                    st.success("Student record updated successfully!")
                    st.rerun()

    else:
        st.info("No student records available to update.")


# ---------------- DELETE STUDENT ----------------
elif menu == "🗑️ Delete Student":

    st.markdown('<div class="main-title">Delete Student Record</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">Remove a student record from the database.</div>',
        unsafe_allow_html=True
    )

    if not df.empty:

        selected_roll = st.selectbox(
            "Select Student",
            df["roll_no"].tolist(),
            format_func=lambda x:
                f"{x} - {df[df['roll_no'] == x].iloc[0]['name']}"
        )

        student = df[df["roll_no"] == selected_roll].iloc[0]

        st.warning("You are about to delete this student record.")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Student Name:**", student["name"])
            st.write("**Roll Number:**", student["roll_no"])

        with col2:
            st.write("**Course:**", student["course"])
            st.write("**Email:**", student["email"])

        confirm = st.checkbox("I confirm that I want to delete this record.")

        if st.button("🗑️ Delete Student", disabled=not confirm):

            conn = get_connection()

            conn.execute(
                "DELETE FROM students WHERE roll_no=?",
                (selected_roll,)
            )

            conn.commit()
            conn.close()

            st.success("Student record deleted successfully!")
            st.rerun()

    else:
        st.info("No student records available to delete.")


# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">StudentHub © 2026 | Student Record Management System</div>',
    unsafe_allow_html=True
)
