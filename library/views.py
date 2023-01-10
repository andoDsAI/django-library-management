import datetime

import razorpay
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

from core import settings
from student.models import Student

from .models import Author, Book, Fine, Issue
from .utilities import calc_fine, get_user_books

razor_pay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# Book
def get_all_books(request):
    requested_books, issued_books = get_user_books(request.user)
    all_books = Book.objects.all()

    return render(
        request,
        "library/home.html",
        {"books": all_books, "issued_books": issued_books, "requested_books": requested_books},
    )


def sort(request):
    sort_type = request.GET.get("sort_type")
    sort_by = request.GET.get("sort")
    requested_books, issued_books = get_user_books(request.user)
    if "author" in sort_type:
        author_results = Author.objects.filter(name__startswith=sort_by)
        return render(
            request,
            "library/home.html",
            {
                "author_results": author_results,
                "issued_books": issued_books,
                "requested_books": requested_books,
                "selected": "author",
            },
        )
    else:
        books_results = Book.objects.filter(name__startswith=sort_by)
        return render(
            request,
            "library/home.html",
            {
                "books_results": books_results,
                "issued_books": issued_books,
                "requested_books": requested_books,
                "selected": "book",
            },
        )


def search(request):
    search_query = request.GET.get("search-query")
    search_by_author = request.GET.get("author")
    requested_books, issued_books = get_user_books(request.user)

    if search_by_author is not None:
        author_results = Author.objects.filter(name__icontains=search_query)
        return render(
            request,
            "library/home.html",
            {
                "author_results": author_results,
                "issued_books": issued_books,
                "requested_books": requested_books,
            },
        )
    else:
        books_results = Book.objects.filter(
            Q(name__icontains=search_query) | Q(category__icontains=search_query)
        )
        return render(
            request,
            "library/home.html",
            {
                "books_results": books_results,
                "issued_books": issued_books,
                "requested_books": requested_books,
            },
        )


@login_required(login_url="/student/login/")
@user_passes_test(lambda u: u.is_superuser, login_url="/student/login/")
def add_book(request):
    authors = Author.objects.all()
    if request.method == "POST":
        name = request.POST["name"]
        category = request.POST["category"]
        author = Author.objects.get(id=request.POST["author"])
        image = request.FILES["book-image"]
        if author is not None or author != "":
            new_book, created = Book.objects.get_or_create(
                name=name, image=image, category=category, author=author
            )
            messages.success(request, "Book - {} Added successfully ".format(new_book.name))
            return render(
                request,
                "library/add_book.html",
                {
                    "authors": authors,
                },
            )
        else:
            messages.error(request, "Author not found !")
            return render(
                request,
                "library/add_book.html",
                {
                    "authors": authors,
                },
            )
    else:
        return render(request, "library/add_book.html", {"authors": authors})


@login_required(login_url="/student/login/")
@user_passes_test(lambda u: u.is_superuser, login_url="/student/login/")
def delete_book(request, bookID):
    book = Book.objects.get(id=bookID)
    messages.success(request, "Book - {} Deleted successfully ".format(book.name))
    book.delete()
    return redirect("/")


#  ISSUES


@login_required(login_url="/student/login/")
@user_passes_test(lambda u: not u.is_superuser, login_url="/student/login/")
def issue_request(request, bookID):
    student = Student.objects.filter(student_id=request.user)
    if student:
        book = Book.objects.get(id=bookID)
        _, _ = Issue.objects.get_or_create(book=book, student=student[0])
        messages.success(request, "Book - {} Requested successfully ".format(book.name))
        return redirect("home")

    messages.error(request, "You are Not a Student !")
    return redirect("/")


@login_required(login_url="/student/login/")
@user_passes_test(lambda u: not u.is_superuser, login_url="/student/login/")
def get_user_issues(request):
    if Student.objects.filter(student_id=request.user):
        student = Student.objects.filter(student_id=request.user)[0]

        if request.GET.get("issued") is not None:
            issues = Issue.objects.filter(student=student, issued=True)
        elif request.GET.get("not_issued") is not None:
            issues = Issue.objects.filter(student=student, issued=False)
        else:
            issues = Issue.objects.filter(student=student)

        return render(request, "library/my_issues.html", {"issues": issues})

    messages.error(request, "You are Not a Student !")
    return redirect("/")


@login_required(login_url="/admin/")
@user_passes_test(lambda u: u.is_superuser, login_url="/admin/")
def requested_issues(request):
    if request.GET.get("studentID") is not None and request.GET.get("studentID") != "":
        try:
            user = User.objects.get(username=request.GET.get("studentID"))
            student = Student.objects.filter(student_id=user)
            if student:
                student = student[0]
                issues = Issue.objects.filter(student=student, issued=False)
                return render(request, "library/all_issues.html", {"issues": issues})
            messages.error(request, "No Student found")
            return redirect("/all_issues/")
        except User.DoesNotExist:
            messages.error(request, "No Student found")
            return redirect("/all_issues/")

    else:
        issues = Issue.objects.filter(issued=False)
        return render(request, "library/all_issues.html", {"issues": issues})


@login_required(login_url="/admin/")
@user_passes_test(lambda u: u.is_superuser, login_url="/student/login/")
def issue_book(request, issueID):
    issue = Issue.objects.get(id=issueID)
    issue.return_date = timezone.now() + datetime.timedelta(days=15)
    issue.issued_at = timezone.now()
    issue.issued = True
    issue.save()
    return redirect("/all_issues/")


@login_required(login_url="/student/login/")
@user_passes_test(lambda u: u.is_superuser, login_url="/admin/")
def return_book(request, issueID):
    issue = Issue.objects.get(id=issueID)
    calc_fine(issue)
    issue.returned = True
    issue.save()
    return redirect("/all_issues/")


#  FINES


@login_required(login_url="/student/login/")
@user_passes_test(lambda u: not u.is_superuser, login_url="/student/login/")
def get_user_fines(request):
    if Student.objects.filter(student_id=request.user):
        student = Student.objects.filter(student_id=request.user)[0]
        issues = Issue.objects.filter(student=student)
        for issue in issues:
            calc_fine(issue)
        fines = Fine.objects.filter(student=student)
        return render(request, "library/my_fines.html", {"fines": fines})
    messages.error(request, "You are Not a Student !")
    return redirect("/")


@login_required(login_url="/student/login/")
@user_passes_test(lambda u: u.is_superuser, login_url="/admin/")
def get_all_fines(request):
    issues = Issue.objects.all()
    for issue in issues:
        calc_fine(issue)
    return redirect("/admin/library/fine/")


@login_required(login_url="/student/login/")
@user_passes_test(lambda u: u.is_superuser, login_url="/admin/")
def delete_fine(request, fineID):
    fine = Fine.objects.get(id=fineID)
    fine.delete()
    return redirect("/all_fines/")


@login_required(login_url="/student/login/")
@user_passes_test(lambda u: not u.is_superuser, login_url="/student/login/")
def pay_fine(request, fineID):
    fine = Fine.objects.get(id=fineID)
    order_amount = int(fine.amount) * 100
    order_currency = "INR"
    order_receipt = fine.order_id

    razor_pay_order = razor_pay_client.order.create(
        dict(
            amount=order_amount,
            currency=order_currency,
            receipt=order_receipt,
        )
    )
    print(razor_pay_order)

    return render(
        request,
        "library/pay_fine.html",
        {
            "amount": order_amount,
            "razor_id": settings.RAZORPAY_KEY_ID,
            "receipt": razor_pay_order["id"],
            "amount_displayed": order_amount / 100,
            "address": "a custom address",
            "fine": fine,
        },
    )


@login_required(login_url="/student/login/")
@user_passes_test(lambda u: not u.is_superuser, login_url="/student/login/")
def pay_status(request, fineID):
    if request.method == "POST":
        params_dict = {
            "razorpay_payment_id": request.POST["razorpay_payment_id"],
            "razorpay_order_id": request.POST["razorpay_order_id"],
            "razorpay_signature": request.POST["razorpay_signature"],
        }
        try:
            status = razor_pay_client.utility.verify_payment_signature(params_dict)
            if status is None:
                fine = Fine.objects.get(id=fineID)
                fine.paid = True
                fine.datetime_of_payment = timezone.now()
                fine.razorpay_payment_id = request.POST["razorpay_payment_id"]
                fine.razorpay_signature = request.POST["razorpay_signature"]
                fine.razorpay_order_id = request.POST["razorpay_order_id"]
                fine.save()

            messages.success(request, "Payment successfully")
        except Exception as e:
            print(e)
            messages.error(request, "Payment Failure")
    return redirect("/my_fines/")
