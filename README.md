# Online Course Web Application using Django and Python
This project is an **Online Course Web Application** built using the **Django framework**. It provides a platform enabling users to register, log in, explore various courses, enroll in them, and complete interactive exams, and have their exam graded.

## ✨ Key Features Added
* **User Authentication & Management:**
    * **Registration:** Allows new users to create an account.
    * **Login/Logout:** Provides secure authentication for registered users to access and exit their sessions.

* **Course Management:**
    * **Course Listing:** Presents a comprehensive list of all available courses.
    * **Course Details:** Displays detailed information for each course, including its associated lessons.
    * **Enrollment System:** Enables authenticated users to enroll in courses, with checks to prevent duplicate enrollments.

* **Exam & Grading System:**
    * **Exam Submission:** Facilitates enrolled users in taking and submitting exams for their courses.
    * **Automated Grading:** Automatically evaluates submitted exams based on the correctness of answers.
    * **Exam Results Display:** Provides immediate and detailed feedback to users upon exam submission, including:
        * Their **total score** achieved.
        * The **maximum possible score** for the exam.
        * A clear **pass or fail** status, determined by a 70% passing threshold.
        * **Detailed results per question**, showing user-selected choices, correct answers, and an indication of whether each individual question was answered correctly.

* **User Interface (UI):**
    * The application styled with **Bootstrap**, enhancing the overall user experience.

* **Administrative Features:**
    * An administrator can **create new courses**, **add questions** to existing courses, and **provide answer keys** for exams through the Django admin interface.

## 🚀 Getting Started (Local Development)
To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Krausjm7/Online-Course-App-Using-Django-Kraus-Final-Project.git](https://github.com/Krausjm7/Online-Course-App-Using-Django-Kraus-Final-Project.git)
    cd Online-Course-App-Using-Django-Kraus-Final-Project
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt # You'll need to create this file if it doesn't exist
    ```
    *(If `requirements.txt` doesn't exist, you can create one with `pip freeze > requirements.txt` after installing your necessary Django version and other libraries like Pillow if used for images).*

4.  **Apply migrations:**
    ```bash
    python manage.py makemigrations onlinecourse
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your admin user.

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000/`.

## 🛠️ Technologies Used
* **Django** (Python Web Framework)
* **HTML5**
* **CSS3**
* **JavaScript**
* **Bootstrap** (for responsive UI)
* **SQLite3** (default database for development)

**ER Diagram**
For your reference, this is the ER diagram design for the new assesement feature.

![Onlinecourse ER Diagram](https://github.com/ibm-developer-skills-network/final-cloud-app-with-database/blob/master/static/media/course_images/onlinecourse_app_er.png)
