# Library Management System

## Technology

![HTML5](https://www.w3.org/html/logo/downloads/HTML5_Logo_64.png) , ![CSS3](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/CSS3_logo_and_wordmark.svg/48px-CSS3_logo_and_wordmark.svg.png) , ![Vanilla JS](https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Unofficial_JavaScript_logo_2.svg/64px-Unofficial_JavaScript_logo_2.svg.png) , ![Python](https://www.quintagroup.com/++theme++quintagroup-theme/images/logo_python_section.png) , ![Django](https://www.quintagroup.com/++theme++quintagroup-theme/images/logo_django_section.png) ,
<img alt="Tailwind CSS" width="350" src="https://refactoringui.nyc3.cdn.digitaloceanspaces.com/tailwind-logo.svg" />

---

## Run project

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Features of this project

### Anyone can

1. See all the books in homepage
2. Search books based on author or name of the book or category of the book
3. Sort books or author alphabetically

### Student can

1. Login / sign-up ,
2. Can request book
3. See their own issues and filter them based on :

    - Requested issues ,
    - Issued books or
    - All of them together

4. Check their own fines
5. Can see

    - The days remaining to return a particular book
      **or**
    - The number of days passed the return date of a particular book in the my fines page

6. Pay their fines online (powered by RazorPay)

### Admin can

1. Login to admin dashboard
2. Check all issues :

    - See issues ,
    - Delete issues ,
    - Search issues by student_id
    - Filter issues based on :
      - Issued or not,
      - Returned or not ,

3. Accept a issue :

    - From the dashboard where admin has to manually select return date
      **or**
    - From the Issue requests page where return date is automatically calculated

4. Add , delete search books and filter books based on author
5. Add , delete , search author
6. Calculate fine by clicking a button ,
7. Create, delete fine ,search fines for studentid
8. Toggle fine paid status (if paid in cash)
9. Search, modify, add, delete students, filter them based on department and check all fines and issues of that student
10. Can see the last-login , date joined & the student associated to a particular user
11. Can change password for any user

### More

1. While signing up if studentID is already associated to a user in this platform then it will show a error without reloading the page and as soon as correct id is given then the error will go away
2. Books in homepage will show status of `issued` , `issue requested` or `request issue` based on whether the book is issued or requested for a issue or is not requested for logged-in students only

---

## Behind the scenes

### Student app

We need this for writing our authentication views as well as student & department models. Student model has the first+last name ,department FOREIGN_KEY and studentID which is one-to-one field to Django' User model. We use Django's User Model for authentication . There will be 3 views: login, sign-up and logout. The urls will have `/student/< login or sign up or logout >/`.

### Library app

This is our main app where we will write our library system's main logic. It comprises of 4 models:

- **Author** - for storing name & description of author
- **Book** - for storing name , image ,category of a book & connecting to the author
- **Issue** - for tracking each & every issue a student requests. It will also track the book for which issue is requested , issue status (whether issued or not) , return status (whether returned or not) , return date (last date to return the book) and more...
- **Fine** - for tracking the fines & calculating fines automatically for each student whose issued book/s is/are not returned and the last date is passed

---

## Some important logics

### **Student ID**

- Username of Django's User Model serves as our studentID

### **Signing Up**

- So every student who signs up creates a new user instance with his/her student id as the username and then a student instance is also created with the names and department and this user we just created.

### **Calculating Fine - How ??**

We run a for loop and pass all the issues to this calculate fine function. Then:

- For each issue, check whether the issue is issued or not (if issue is not issued then no need to calculate fines)
  - If issue is issued then check whether issue is returned or not (if issue is returned then no need to calculate fines)
    - If issue is not returned then check whether the issue's return date is passed or not (if not passed then no calculation of fines is needed)
      - Create or get a fine instance with student & issue then calculate the amount and save it to the amount field

### **Calculating Fine - When ??**

- Whenever admin clicks on "_Calculate Fine_" button
- Whenever a student opens his "_My Fines_" page

### **Payment of Fines**

- When a student clicks on pay button (in my fines page)
- We create a razor pay order with a dict containing fine amount (converted to int and multiplied by 100 because razor_pay wants in paisa) , order_id, currency
- Then we send the user to the pay fines page (pay_fine.html) with the amount (in paisa), razor pay key id, razor_pay order id & amount (which should be displayed)
- User chooses proceed to payment online , selects payment mode (Net banking, Card, Wallet etc.) and pays the amount
- We verify the payment status whether success or failure
- Then payment is (successful/failure) message is shown on my fines page with (paid status / pay button) beside that fine

## Screenshots

- Sign-up Page
  ![sign-up](./screenshots/signup.png)
- Login Page
  ![login](./screenshots/login.png)
- If Student ID already signed up
  ![sign-up](./screenshots/signup_same_id.png)

- Home Page for student
  ![homepage](./screenshots/homepage_student.png)
- Search Book
  ![search-book](./screenshots/search_book.png)
- Search Author
  ![search-author](./screenshots/search_author.png)

- My Issues
  ![get_user_issues](./screenshots/my_issues.png)
- My Fines
  ![my fines](./screenshots/my_fines.png)
- Confirm Payment
  ![payment_mode](./screenshots/confirm_payment.png)
- Choose Payment Modes
  ![payment_mode](./screenshots/choose_pay_mode.png)
- Pay Success
  ![payment_mode](./screenshots/pay_success.png)

- Admin Dashboard
  ![admin](./screenshots/admin_dashboard_home.png)

- All Books (Admin)
  ![all_books](./screenshots/all_books.png)

- All issues , can be filtered ,searched (Admin)
  ![all_issues](./screenshots/all_issues.png)
- Requested Issues (Admin)
  ![all_issues](./screenshots/issue_requests.png)

- All fines , can be filtered ,searched (Admin)
  ![all_fines](./screenshots/all_fines.png)

- All Students , can be filtered ,searched (Admin)
  ![all_students](./screenshots/all_students.png)
- Student Details (Admin)
  ![student_details](./screenshots/student_details.png)
- User Details (Admin)
  ![student_details](./screenshots/user_details.png)
  19
