from django.shortcuts import render, redirect
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from . forms import SignupForm, BookForm




@login_required
def index(request):
    """View function for home page of site."""

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_instances_loan = BookInstance.objects.filter(status__exact='l').count()
    num_instances_reserved = BookInstance.objects.filter(status__exact='r').count()
    num_instances_maintenance = BookInstance.objects.filter(status__exact='m').count()




    # The 'all()' is implied by default.


    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_instances_loan': num_instances_loan,
        'num_instances_reserved': num_instances_reserved,
        'num_instances_maintenance': num_instances_maintenance,
        'num_visits': num_visits,
    }

    # Render the HTML template base.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'all_books'

    def get_queryset(self):
        return Book.objects.all()     # Get 5 books containing the title war

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context
    # login_url = '/login/'
    # redirect_field_name = 'home.html'
    template_name = 'books.html'


class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    context_object_name = 'all_authors'

    def get_queryset(self):
        return Author.objects.all()   # Get 5 books containing the title war

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(AuthorListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context

    template_name = 'authors.html'


class AuthorDetailView(generic.DetailView):
    model = Author

    def author_detail_view(request, primary_key):
        # author = get_object_or_404(Author, pk=primary_key)
        authors = Author.objects.all()
        author = authors.get(id=primary_key)
        authored = author.book_set.all()
        context = {
            'author': author,
            'authored': authored,

        }
        return render(request, 'catalog/author_detail.html', context)


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@login_required
def bookentry(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book')
    context = {
        'form': form
    }
    return render(request, 'forms/bookform.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    # initial = {'date_of_death': '11/06/2020'}


class AuthorUpdate(UpdateView):
    model = Author
    fields = '__all__'


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author')


def signup(request):
    sign_up = SignupForm()
    if request.method == 'POST':
        sign_up = SignupForm(request.POST)
        if sign_up.is_valid():
            sign_up.save()
            return redirect('/')
    context = {
        'signup': sign_up,
    }
    return render(request, 'account/register.html', context)



