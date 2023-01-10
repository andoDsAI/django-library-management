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
7. Create, delete fine ,search fines for student_id
8. Toggle fine paid status (if paid in cash)
9. Search, modify, add, delete students, filter them based on department and check all fines and issues of that student
10. Can see the last-login , date joined & the student associated to a particular user
11. Can change password for any user

### More

1. While signing up if studentID is already associated to a user in this platform then it will show a error without reloading the page and as soon as correct id is given then the error will go away
2. Books in homepage will show status of `issued` , `issue requested` or `request issue` based on whether the book is issued or requested for a issue or is not requested for logged-in students only
