# 🏥 Health Consulting App

## 🎯 Purpose
The purpose of this application is to provide a platform for **health consultation** by connecting **patients** with **doctors**.  
It allows users to interact through comments, ratings, and messages, and offers a marketplace to explore and purchase medicines.  
The system ensures a personalized experience based on whether the user is a doctor or a patient.

---

## 🛠 General Description
The Health Consulting app is designed to allow users to either **sign up** or **log in**.  
Before logging in, users can view the **Home** and **About** pages.  
After logging in, the experience changes based on whether the user is a **Doctor** or a **Patient**.

---

## 👤 As a User
- I can choose to **sign up** or **log in** from the homepage.
- I can view the **Home** page (a welcoming page) and the **About** page (an overview of the app).

---

## 🩺 As a Doctor
- I can log in and access **My Account** page:
  - I can view the **comments** I received from different patients.
  - I can **edit** or **delete** my own replies to patient comments.
- I can view a **Doctors List** page:
  - I can see information about all doctors (e.g., name, specialization, hospital affiliation).
  - By clicking on a doctor, I can view:
    - The **comments** made by patients about that doctor (read-only).
    - The **ratings** given to that doctor (1 to 5 stars).
- I can access a **Medicines** page:
  - I can view available medicines along with their information.
  - I can **prescribe** medicines for patients if needed.
- I can still access the **Home** and **About** pages after logging in.

---

## 🧑‍⚕️ As a Patient
- I can log in and access **My Profile** page:
  - I can see the **comments** I have made on different doctors.
  - I can see the **replies** from doctors to my comments.
  - I can **edit** or **delete** my own comments.
- I can view the **Doctors List** page:
  - I can select a doctor and:
    - Write a **new comment**.
    - Give a **rating** (from 1 to 5 stars).
    - **Edit** or **delete** my own comments.
- I can access a **Medicines** page:
  - I can view available medicines with their details.
- I can access the **Home** and **About** pages after logging in.

---

## 📄 Key Pages
- **Home Page**: Welcome message and introduction to the app.
- **About Page**: Brief description about the purpose and features of the app.
- **Login/Signup Pages**: Choose to sign up or log in as a Doctor or Patient.
- **Doctor's Account Page**: Manage received comments and interact with patients.
- **Patient's Profile Page**: Manage personal comments and interactions with doctors.
- **Doctors List Page**: View all doctors and their details, rate and comment.
- **Medicines Page**: View, explore, and purchase medicines.

---
## 💡Health Consulting App Overview 
![Diagram](<Database ER diagram (crow's foot)(4).png>)
---

## 📚 API Endpoints

### 👤 User Endpoints

| Action   | Method | URL             | Description                         |
|:---------|:-------|:-----------------|:------------------------------------|
| Register | POST   | `/user/signup/`  | Create a new user (doctor or patient) |
| Login    | POST   | `/user/login/`   | Log in user                        |
| Logout   | POST   | `/user/logout/`  | Log out user                       |

---

### 🩺 Doctor Endpoints

| Action                | Method  | URL                         | Description                                           |
|:----------------------|:--------|:----------------------------|:------------------------------------------------------|
| List Doctors          | GET     | `/doctors/`                 | View all doctors                                     |
| Doctor Detail         | GET     | `/doctors/<doctor_id>/`      | View a specific doctor’s profile, comments, and ratings |
| My Doctor Page        | GET     | `/doctors/<doctor_id>/`      | View your own doctor page with patient comments       |
| Update Doctor Info    | PUT     | `/doctors/<doctor_id>/`      | Update your doctor profile                           |
| Delete Doctor Account | DELETE  | `/doctors/<doctor_id>/`      | (Optional) Deactivate doctor account                 |

---

### 🧑‍⚕️ Patient Endpoints

| Action                | Method  | URL                         | Description                      |
|:----------------------|:--------|:----------------------------|:---------------------------------|
| List Patients         | GET     | `/patients/`                | (Optional) List all patients (admin use) |
| Patient Detail        | GET     | `/patients/<patient_id>/`   | View a specific patient profile  |
| My Patient Page       | GET     | `/patients/<patient_id>/`   | View your own comments and interactions |
| Update Patient Info   | PUT     | `/patients/<patient_id>/`   | Update patient profile           |
| Delete Patient Account| DELETE  | `/patients/<patient_id>/`   | (Optional) Deactivate patient account |
| Prescribe Medicine  | POST    | `/patients/<patient_id>/medicines/<medicine_id>/prescribe/`| Prescribe a specific medicine     |

---

### 💊 Medicine Endpoints

| Action              | Method  | URL                                  | Description                        |
|:--------------------|:--------|:-------------------------------------|:-----------------------------------|
| List Medicines      | GET     | `/medicines/`                       | View all available medicines      |
| Medicine Detail     | GET     | `/medicines/<medicine_id>/`          | View specific medicine information |


---

### 📝 Review Endpoints

| Action                  | Method  | URL                                | Description                                |
|:-------------------------|:--------|:-----------------------------------|:-------------------------------------------|
| List Doctor Reviews      | GET     | `/doctors/<doctor_id>/reviews/`    | See all comments and ratings for a doctor |
| Add Review               | POST    | `/doctors/<doctor_id>/reviews/`    | Add a comment + rating to a doctor        |
| Update Review            | PUT     | `/reviews/<review_id>/`            | Edit your own comment or rating           |
| Delete Review            | DELETE  | `/reviews/<review_id>/`            | Delete your own comment or rating         |
| Doctor Reply to Review   | POST    | `/reviews/<review_id>/reply/`       | Doctor replies to a patient comment       |

---

