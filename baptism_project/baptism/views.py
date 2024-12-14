from django.shortcuts import render, redirect
from .forms import BaptismForm,ParishDetailsForm,BaptismAdvancedForm,FieldTableForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import LoginDetails
from .forms import LoginForm, RegisterForm
from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import FieldTable

def baptism_form_view(request):
    if request.method == "POST":
        form = BaptismForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Replace with your success URL
    else:
        form = BaptismForm()
    return render(request, 'baptism/baptism_form.html', {'form': form})


from django.shortcuts import redirect

def upload_parish_details(request):
    if request.method == 'POST':
        form = ParishDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to the success page
    else:
        form = ParishDetailsForm()
    return render(request, 'baptism/upload_parish_details.html', {'form': form})


def success_page(request):
    return render(request, 'baptism/success.html')




def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']

            try:
                user = LoginDetails.objects.get(user_name=user_name)
                if check_password(password, user.password):
                    user.last_login = now()
                    user.save()
                    return redirect('/baptism/')  # Redirect to baptism page
                else:
                    messages.error(request, "Invalid username or password")
            except LoginDetails.DoesNotExist:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'baptism/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'baptism/register.html', {'form': form})





def upload_baptism_advanced(request):
    if request.method == 'POST':
        form = BaptismAdvancedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to the desired page
    else:
        form = BaptismAdvancedForm()
    return render(request, 'baptism/upload_baptism_advanced.html', {'form': form})



def upload_field_table(request):
    if request.method == 'POST':
        form = FieldTableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Update this with your success page URL name
    else:
        form = FieldTableForm()
    
    return render(request, 'baptism/upload_field_table.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import FieldTable,BaptismAdvanced

def field_table_list(request):
    query = request.GET.get('q', '')
    fields = FieldTable.objects.all()

    if query:
        fields = fields.filter(field_id__icontains=query) | fields.filter(q_id__icontains=query)

    paginator = Paginator(fields, 10)  # Show 10 fields per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'field_table_list.html', {'page_obj': page_obj, 'query': query})

from django.http import HttpResponse

def field_table_add(request):
    if request.method == 'POST':
        form = FieldTableForm(request.POST)
        if form.is_valid():
            form.save()  # This will save the new record in the database
            return redirect('field_table_list')  # Redirect to list page after saving
    else:
        form = FieldTableForm()
    return render(request, 'field_table_add.html', {'form': form})

def field_table_edit(request, pk):
    field_table = get_object_or_404(FieldTable, pk=pk)  # Retrieve the existing record
    if request.method == 'POST':
        form = FieldTableForm(request.POST, instance=field_table)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # This will update the existing record in the database
            return redirect('field_table_list')  # Redirect to list page after saving
    else:
        form = FieldTableForm(instance=field_table)  # Prepopulate the form with the existing record's data
    return render(request, 'field_table_edit.html', {'form': form})

def field_table_delete(request, field_id):
    field = get_object_or_404(FieldTable, pk=field_id)
    field.delete()
    return redirect('field_list')

  # Ensure you import your model



from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import BaptismAdvanced
from .forms import BaptismAdvancedForm

# List View
def baptism_advanced_list(request):
    query = request.GET.get('q', '')
    baptisms = BaptismAdvanced.objects.all()

    if query:
        baptisms = baptisms.filter(q_id__icontains=query) | baptisms.filter(field_id__icontains=query)

    paginator = Paginator(baptisms, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'baptism_advanced_list.html', {'page_obj': page_obj, 'query': query})

# Add View
def baptism_advanced_add(request):
    if request.method == 'POST':
        form = BaptismAdvancedForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new record in the database
            return redirect('baptism_advanced_list')  # Redirect to list page
    else:
        form = BaptismAdvancedForm()
    return render(request, 'baptism_advanced_add.html', {'form': form})

# Edit View
def baptism_advanced_edit(request, pk):
    baptism = get_object_or_404(BaptismAdvanced, pk=pk)  # Retrieve the existing record
    if request.method == 'POST':
        form = BaptismAdvancedForm(request.POST, instance=baptism)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # Update the existing record in the database
            return redirect('baptism_advanced_list')  # Redirect to list page
    else:
        form = BaptismAdvancedForm(instance=baptism)  # Prepopulate form with the existing data
    return render(request, 'baptism_advanced_edit.html', {'form': form})

# Delete View
def baptism_advanced_delete(request, advanced_baptism_id):
    baptism = get_object_or_404(BaptismAdvanced, pk=advanced_baptism_id)
    baptism.delete()  # Delete the record from the database
    return redirect('baptism_advanced_list')


from .models import ParishDetails


# List view with search and pagination
def parish_details_list(request):
    query = request.GET.get('q', '')
    parishes = ParishDetails.objects.all()

    if query:
        parishes = parishes.filter(name_of_parish__icontains=query) | parishes.filter(place_of_parish__icontains=query)

    paginator = Paginator(parishes, 10)  # Show 10 parishes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'parish_details_list.html', {'page_obj': page_obj, 'query': query})

# Add new parish view
def parish_details_add(request):
    if request.method == 'POST':
        form = ParishDetailsForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new parish record
            return redirect('parish_details_list')  # Redirect to list page after saving
    else:
        form = ParishDetailsForm()
    return render(request, 'parish_details_add.html', {'form': form})

# Edit existing parish view
def parish_details_edit(request, pk):
    parish = get_object_or_404(ParishDetails, pk=pk)  # Retrieve the existing parish record
    if request.method == 'POST':
        form = ParishDetailsForm(request.POST, instance=parish)  # Bind form to existing record
        if form.is_valid():
            form.save()  # Update the parish record
            return redirect('parish_details_list')  # Redirect to list page after saving
    else:
        form = ParishDetailsForm(instance=parish)  # Prepopulate form with existing parish data
    return render(request, 'parish_details_edit.html', {'form': form})

# Delete parish view
def parish_details_delete(request, parish_id):
    parish = get_object_or_404(ParishDetails, pk=parish_id)
    parish.delete()  # Delete the parish record
    return redirect('parish_details_list')  # Redirect to the list page after deletion


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Baptism
from .forms import BaptismForm  # Assuming you have a form for Baptism model

# View for listing Baptism records with search functionality
def baptism_list(request):
    query = request.GET.get('q', '')
    baptisms = Baptism.objects.all()

    if query:
       baptisms = baptisms.filter(basic_baptism_id__icontains=query) | baptisms.filter(child_name_first__icontains=query) | baptisms.filter(child_name_second__icontains=query)

    paginator = Paginator(baptisms, 10)  # Show 10 baptisms per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'baptism_list.html', {'page_obj': page_obj, 'query': query})

# View for adding a new Baptism record
def baptism_add(request):
    if request.method == 'POST':
        form = BaptismForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new baptism record to the database
            return redirect('baptism_list')  # Redirect to baptism list page after saving
    else:
        form = BaptismForm()
    return render(request, 'baptism_add.html', {'form': form})

# View for editing an existing Baptism record
def baptism_edit(request, pk):
    baptism = get_object_or_404(Baptism, pk=pk)  # Retrieve the existing baptism record
    if request.method == 'POST':
        form = BaptismForm(request.POST, instance=baptism)  # Bind form to the existing baptism record
        if form.is_valid():
            form.save()  # Update the baptism record in the database
            return redirect('baptism_list')  # Redirect to baptism list page after saving
    else:
        form = BaptismForm(instance=baptism)  # Prepopulate the form with the baptism record data
    return render(request, 'baptism_edit.html', {'form': form})

# View for deleting a Baptism record
def baptism_delete(request, baptism_id):
    baptism = get_object_or_404(Baptism, pk=baptism_id)
    baptism.delete()
    return redirect('baptism_list')  # Redirect to the baptism list page after deletion
