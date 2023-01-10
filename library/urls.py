from django.urls import path

from .views import (
    add_book,
    delete_book,
    delete_fine,
    get_all_books,
    get_all_fines,
    get_user_fines,
    get_user_issues,
    issue_book,
    issue_request,
    pay_fine,
    pay_status,
    requested_issues,
    return_book,
    search,
    sort,
)

urlpatterns = [
    path("", get_all_books, name="home"),
    path("search/", search),
    path("sort/", sort),
    path("add_book/", add_book),
    path("delete_book/<int:bookID>/", delete_book),
    path("request_book_issue/<int:bookID>/", issue_request),
    path("my_issues/", get_user_issues),
    path("my_fines/", get_user_fines),
    path("pay_fine/<int:fineID>/", pay_fine),
    path("pay_status/<int:fineID>/", pay_status),
    path("all_issues/", requested_issues),
    path("all_fines/", get_all_fines),
    path("issue_book/<int:issueID>/", issue_book),
    path("return_book/<int:issueID>/", return_book),
    path("delete_fine/<int:fineID>/", delete_fine),
]
