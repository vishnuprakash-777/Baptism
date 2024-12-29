from django.shortcuts import render, redirect
from .forms import BaptismForm,ParishDetailsForm,BaptismAdvancedForm,FieldTableForm,AnswerForm
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




def upload_answer_details(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to a success page
    else:
        form = AnswerForm()
    return render(request, 'baptism/upload_answer_details.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Answer
from .forms import AnswerForm

# List all answers with pagination and search
def answer_list(request):
    query = request.GET.get('q', '')
    answers = Answer.objects.all()

    if query:
        answers = answers.filter(q_id__icontains=query) | answers.filter(option_id__icontains=query)

    paginator = Paginator(answers, 10)  # Show 10 answers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'answer_list.html', {'page_obj': page_obj, 'query': query})

# Add a new answer
def answer_add(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new answer record
            return redirect('answer_list')  # Redirect to the list page after saving
    else:
        form = AnswerForm()
    return render(request, 'answer_add.html', {'form': form})

# Edit an existing answer
def answer_edit(request, pk):
    answer = get_object_or_404(Answer, pk=pk)  # Retrieve the existing answer record
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # Update the answer record
            return redirect('answer_list')  # Redirect to the list page after saving
    else:
        form = AnswerForm(instance=answer)  # Prepopulate form with existing answer data
    return render(request, 'answer_edit.html', {'form': form})

# Delete an answer
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()  # Delete the answer record
    return redirect('answer_list')  # Redirect to the list page after deletion


from .forms import QuestionForm

def upload_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to a list page or success page
    else:
        form = QuestionForm()
    return render(request, 'baptism/upload_question.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import OptionForm

def upload_option(request):
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to the option list page
    else:
        form = OptionForm()
    return render(request, 'baptism/upload_option.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Option,Question
from .forms import OptionForm,QuestionForm

# List all options with pagination and search
def option_list(request):
    query = request.GET.get('q', '')
    options = Option.objects.all()

    if query:
        options = options.filter(q_id__icontains=query) | options.filter(option_id__icontains=query)

    paginator = Paginator(options, 10)  # Show 10 options per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'option_list.html', {'page_obj': page_obj, 'query': query})

# Add a new option
def option_add(request):
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new option record
            return redirect('option_list')  # Redirect to the list page after saving
    else:
        form = OptionForm()
    questions = Question.objects.all()  # Get all questions
    return render(request, 'option_add.html', {'form': form, 'questions': questions})

# Edit an existing option
def option_edit(request, pk):
    option = get_object_or_404(Option, pk=pk)  # Retrieve the existing option record
    if request.method == 'POST':
        form = OptionForm(request.POST, instance=option)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # Update the option record
            return redirect('option_list')  # Redirect to the list page after saving
    else:
        form = OptionForm(instance=option)  # Prepopulate form with existing option data
    questions = Question.objects.all()  # Get all questions
    return render(request, 'option_edit.html', {'form': form, 'questions': questions})






# Delete an option
def option_delete(request, option_id):
    option = get_object_or_404(Option, pk=option_id)
    option.delete()  # Delete the option record
    return redirect('option_list')  # Redirect to the list page after deletion


# List of questions
def question_list(request):
    query = request.GET.get('q', '')
    questions = Question.objects.all()

    if query:
        questions = questions.filter(q_id__icontains=query) 

    paginator = Paginator(questions, 10)  # Show 10 questions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'question_list.html', {'page_obj': page_obj, 'query': query})

# Add a new question
def question_add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new question record
            return redirect('question_list')  # Redirect to the list page after saving
    else:
        form = QuestionForm()
    return render(request, 'question_add.html', {'form': form})

# Edit an existing question
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)  # Retrieve the existing question record
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # Update the question record
            return redirect('question_list')  # Redirect to the list page after saving
    else:
        form = QuestionForm(instance=question)  # Prepopulate form with existing question data
    return render(request, 'question_edit.html', {'form': form})

# Delete a question
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()  # Delete the question record
    return redirect('question_list')  # Redirect to the list page after deletion


from django.shortcuts import render
from .models import Question, Option

from django.shortcuts import render, redirect
from .models import Question

# Define the sections in the desired order
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Question

SECTIONS = [
    "READING DETAILS", "THE PRAYER OF THE ASSEMBLY", "SONG SELECTION", "SPECIAL SAINTS TO COMMEMORATE", "REMARKS",
    "AUTHORIZATION", "FINANCIAL PARTICIPATION"
]

SECTION_DESCRIPTIONS = {
    "READING DETAILS": "Please choose one of the reading details, Psalm or Gospel (page 25-41).",
    "THE PRAYER OF THE ASSEMBLY": "The prayer of the assembly includes selecting one from each category.",
    "SONG SELECTION": "Please select songs for the baptism celebration.",
    "SPECIAL SAINTS TO COMMEMORATE": "We add here the names of the patron saints of the child, family, and church, and finish.",
    "REMARKS": "If you have any doubts or questions, please feel free to contact Father Jomy by email or in the space below. To contact jomykollithanath@gmail.com",
    "AUTHORIZATION": "I would like to baptize my child.",
    "FINANCIAL PARTICIPATION": "You are probably wondering what you should give to the parish to compensate it for its expenses and to show your solidarity. Your parish usually suggests an indicative amount, but the amount can be adjusted according to your means. To do this, you must contact the parish secretariat. This sum is intended to cover the costs of preparation and celebration."
}

def section_questions(request, section_name):
    # Validate section_name
    section_name = section_name.upper()
    if section_name not in SECTIONS:
        messages.error(request, "Invalid section. Redirecting to the first section.")
        return redirect('section_questions', section_name=SECTIONS[0].lower())

    questions = Question.objects.filter(section=section_name, status="active")
    current_index = SECTIONS.index(section_name)
    prev_section = SECTIONS[current_index - 1].lower() if current_index > 0 else None
    next_section = SECTIONS[current_index + 1].lower() if current_index < len(SECTIONS) - 1 else None
    section_description = SECTION_DESCRIPTIONS.get(section_name, "")

    if request.method == "POST":
        for question in questions:
            answer_key = f"answer_{question.q_id}"

            # Check for checkbox answers
            if question.answer_type == "checkbox":
                answers = request.POST.getlist(answer_key)  # Get multiple selected options
                if question.compulsary == "yes" and not answers:
                    messages.error(request, f"Question {question.order_id} is compulsory and must be answered.")
                    break

            # Check for non-checkbox answers
            else:
                answer = request.POST.get(answer_key)
                if question.compulsary == "yes" and not answer:
                    messages.error(request, f"Question {question.order_id} is compulsory and must be answered.")
                    break
        else:
            # All questions are answered properly, save answers (if needed), and proceed
            for question in questions:
                answer_key = f"answer_{question.q_id}"
                answer = request.POST.get(answer_key) if question.answer_type != "checkbox" else request.POST.getlist(answer_key)
                # You might want to save this answer to your model here
                # Example: Answer.objects.create(question=question, answer=answer)
            
            if next_section:
                return redirect('section_questions', section_name=next_section)
            else:
                messages.success(request, "You have completed the questionnaire!")
                return redirect('home_page')

    # Context for rendering the template
    context = {
        "section_name": section_name.capitalize(),
        "section_description": section_description,
        "questions": questions,
        "prev_section": prev_section,
        "next_section": next_section,
    }
    return render(request, "section_questions.html", context)






def home_page(request):
    # Redirect to the first section when "Next" is clicked
    return render(request, "home.html")


from django.shortcuts import render, redirect
from .forms import DeaneryForm

def upload_deanery(request):
    if request.method == 'POST':
        form = DeaneryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to a success page after submission
    else:
        form = DeaneryForm()
    
    return render(request, 'baptism/upload_deanery.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Deanery
from .forms import DeaneryForm

# List all deaneries
def deanery_list(request):
    query = request.GET.get('q', '')
    deaneries = Deanery.objects.all()

    if query:
        deaneries = deaneries.filter(deanery_name__icontains=query) | deaneries.filter(deanery_id__icontains=query)

    paginator = Paginator(deaneries, 10)  # Show 10 deaneries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'deanery_list.html', {'page_obj': page_obj, 'query': query})

# Add a new deanery
def deanery_add(request):
    if request.method == 'POST':
        form = DeaneryForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new deanery record
            return redirect('deanery_list')  # Redirect to the list page after saving
    else:
        form = DeaneryForm()
    return render(request, 'deanery_add.html', {'form': form})

# Edit an existing deanery
def deanery_edit(request, pk):
    deanery = get_object_or_404(Deanery, pk=pk)  # Retrieve the existing deanery record
    if request.method == 'POST':
        form = DeaneryForm(request.POST, instance=deanery)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # Update the deanery record
            return redirect('deanery_list')  # Redirect to the list page after saving
    else:
        form = DeaneryForm(instance=deanery)  # Prepopulate form with existing deanery data
    return render(request, 'deanery_edit.html', {'form': form})

# Delete a deanery
def deanery_delete(request, deanery_id):
    deanery = get_object_or_404(Deanery, pk=deanery_id)
    deanery.delete()  # Delete the deanery record
    return redirect('deanery_list')  # Redirect to the list page after deletion
