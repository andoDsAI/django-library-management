import datetime

from django.utils import timezone

from student.models import Student

from .models import Book, Fine


def calc_fine(issue):
    "Calculate fines of each issue if any"
    if issue.issued and not issue.returned:
        y, m, d = str(timezone.now().date()).split("-")
        today = datetime.date(int(y), int(m), int(d))
        y2, m2, d2 = str(issue.return_date.date()).split("-")
        lastdate = datetime.date(int(y2), int(m2), int(d2))
        if today > lastdate:
            diff = today - lastdate
            fine, _ = Fine.objects.get_or_create(issue=issue, student=issue.student)
            if not fine.paid:
                fine.amount = diff.days * 10
                fine.save()
            else:
                print("fine paid")
        else:
            return "no fine"
    else:
        return "no fine"


def get_user_books(user):
    "Get issued books or requested books of a student, takes a user & returns a tuple"
    requested_books = []
    issued_books = []
    if user.is_authenticated:
        student = Student.objects.filter(student_id=user)
        if student:
            for b in Book.objects.all():
                for i in b.issue_set.all():
                    if i.student == student[0]:
                        if i.issued:
                            issued_books.append(b)
                        else:
                            requested_books.append(b)
    return [requested_books, issued_books]
