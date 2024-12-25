from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import *
from .models import *
from django.contrib.messages import get_messages
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
import pandas as pd
import csv
from .anonypy_utils import *
from django.http import FileResponse

'''
Renders the 'Home' page, which displays general information about the application.
'''
def home(request):
    return render(request, 'home.html')


'''
Renders the 'How we do it' page, which provides details on the anonymization process.
'''
def how_we_do_it(request):
    return render(request, 'how_we_do_it.html')

'''
Handles user registration and displays errors if the form is invalid. 
If successful, the user is registered, their data is saved in the database, and they get redirected to login.
'''
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

'''
Handles user login by validating credentials and logs the user in if successful. 
Displays error messages for invalid login attempts.
'''
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #Authenticate the user
            user = form.get_user() 
            #Log the user in
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            
            # Redirect to home page after successful login
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

'''
Logs out the user and redirects them to the home page with a success message.
'''
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')

'''
Handles uploaded files and converts .xlsx files to .csv format.
This is necessary because the application processes only CSV files.
'''
def handle_uploaded_file(uploaded_file, user_dir):
    #Save the uploaded file temporarily in the user's upload directory
    temp_path = os.path.join(user_dir, uploaded_file.name)
    with open(temp_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    #Check if the file is an XLSX file
    if uploaded_file.name.endswith('.xlsx'):
        #Convert XLSX to CSV
        csv_filename = uploaded_file.name.replace('.xlsx', '.csv')
        csv_path = os.path.join(user_dir, csv_filename)
        df = pd.read_excel(temp_path)
        df.to_csv(csv_path, index=False)

        #Remove the original XLSX file
        os.remove(temp_path)

        #Return the new CSV filename
        return csv_filename 
    
    #If not an XLSX file don't need to do anything
    else:
        return uploaded_file.name

'''
Handles file uploads, deletions, and search functionality.
Displays a paginated list of files for the user, with support for search queries.
'''
@login_required
def upload_file(request):
    form = FileUploadForm()
    if request.method == 'POST':
        #Handle file upload
        if 'file' in request.FILES:
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']

                #Define the user's upload directory and create it if it doesnt exist
                user_dir = os.path.join(settings.MEDIA_ROOT, request.user.username, 'uploads')
                os.makedirs(user_dir, exist_ok=True)

                #Save the file to the user's upload directory
                saved_filename = handle_uploaded_file(file, user_dir)
                
                #Save file information to databse
                Dataset.objects.create(
                    user=request.user,
                    filename=saved_filename,
                    file_path=os.path.join(user_dir, saved_filename)
                )
                messages.success(request, f"{file} was successfully uploaded!")
                return redirect('upload_file')  # Refresh the page
            else:
                messages.error(request, "Something went wrong uploading your file. Please try again.")
        
        #Handle file deletion
        elif 'delete_file' in request.POST:
            file_to_delete = request.POST.get('delete_file')
            user_dir = os.path.join(settings.MEDIA_ROOT, request.user.username, 'uploads')
            file_path = os.path.join(user_dir, file_to_delete)

            if os.path.exists(file_path):
                os.remove(file_path) 
                messages.success(request, f"Your file was successfully deleted!")

            return redirect('upload_file') 
            messages.error(request, "No file was selected for upload. Please try again.")

    else:
        form = FileUploadForm()

    #Handle search queries and view mode
    search_query = request.GET.get('search', '')
    search_date = request.GET.get('search_date', '')
    view_mode = request.GET.get('view_mode', '')

    if view_mode == 'current':
        #Fetch current files stored in media/<username>/uploads
        current_files = []
        user_dir = os.path.join(settings.MEDIA_ROOT, request.user.username, 'uploads')
        if os.path.exists(user_dir):
            for file_name in os.listdir(user_dir):
                full_path = os.path.join(user_dir, file_name)
                if os.path.isfile(full_path):
                    #for each file get its name and modifcation time (which should be upload time)
                    file_data = {
                        'filename': file_name,
                        'upload_date': datetime.fromtimestamp(os.path.getmtime(full_path))
                    }
                    #Apply search filters
                    if search_query and search_query.lower() not in file_name.lower():
                        continue
                    if search_date:
                        try:
                            search_date_obj = datetime.strptime(search_date, '%Y-%m-%d').date()
                            file_date = datetime.fromtimestamp(os.path.getmtime(full_path)).date()
                            if file_date != search_date_obj:
                                continue
                        except ValueError:
                            pass
                    current_files.append(file_data)

        #Sort current files by modification date (most recent first)
        current_files = sorted(current_files, key=lambda x: x['upload_date'], reverse=True)

        #Paginate current files to show 10 per page
        paginator = Paginator(current_files, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'file_upload.html', {
            'form': form,
            'page_obj': page_obj,
            'search_query': search_query,
            'search_date': search_date,
            'view_mode': view_mode,
        })

    #If we are here, the view mode isnt current so we and grab files from database.
    #Fetch uploaded files from the database and sort by the most recent upload date
    uploaded_files = Dataset.objects.filter(user=request.user).order_by('-upload_date')

    #Apply search filters
    if search_query:
        uploaded_files = uploaded_files.filter(filename__icontains=search_query)

    if search_date:
        try:
            #Parse the date and filter files uploaded on that date
            search_date_obj = datetime.strptime(search_date, '%Y-%m-%d')
            uploaded_files = uploaded_files.filter(upload_date__date=search_date_obj.date())
        except ValueError:
            pass

    #Paginate uploaded files to show 10 per page
    paginator = Paginator(uploaded_files, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'file_upload.html', {
        'form': form,
        'page_obj': page_obj,
        'search_query': search_query,
        'search_date': search_date,
        'view_mode': view_mode,
    })


'''
Allows users to select algorithms and apply them to uploaded files.
The parameters are validated, stored in the database, and the processing is applied.
'''
@login_required
def algorithm_selection(request):
    #Fetch the current user's uploaded files from their "uploads" directory
    user_dir = os.path.join(settings.MEDIA_ROOT, request.user.username, 'uploads')
    
    #Get path to current user's processed filed directory or create one if it doesnt exist
    processed_dir = os.path.join(settings.MEDIA_ROOT, request.user.username, 'processed')
    os.makedirs(processed_dir, exist_ok=True)
    
    #Fetch and display users uploaded filed as choice for selection.
    file_choices = [(f, f) for f in os.listdir(user_dir) if os.path.isfile(os.path.join(user_dir, f))] if os.path.exists(user_dir) else []

    if request.method == 'POST':
        form = AlgorithmSelectionForm(request.POST, file_choices=file_choices)
        if form.is_valid():
            #Process the form data
            
            #Collect selected file name and senstive field inputed.
            selected_file = form.cleaned_data['file']
            sensitive_fields = form.cleaned_data['sensitive_fields']

            # Collect algorithm types and their parameters
            algorithm_type = ""
            k_anonymity_k_value = form.cleaned_data.get('k_anonymity_k_value')
            l_value = form.cleaned_data.get('l_value')
            l_diversity_k_value = form.cleaned_data.get('l_diversity_k_value')
            t_value = form.cleaned_data.get('t_value')
            t_closeness_k_value = form.cleaned_data.get('t_closeness_k_value')

            #Depending on which algorithms are selected we updated the type.
            #This will be used information storage purposes in database.
            if form.cleaned_data.get('k_anonymity'):
                algorithm_type += "K"
            if form.cleaned_data.get('l_diversity'):
                algorithm_type += "L"
            if form.cleaned_data.get('t_closeness'):
                algorithm_type += "T"

            #Get dataset entry in database for the selected file and validate it exists.
            dataset = Dataset.objects.filter(user=request.user, filename=selected_file).first()
            if not dataset:
                messages.error(request, "Selected file is not associated with any dataset entry.")
                return render(request, 'algorithm_selection_and_processing.html', {'form': form})

            #Load the selected file to validate the fields and select algorithm paramters
            selected_file_path = os.path.join(user_dir, selected_file)
            try:
                with open(selected_file_path, 'r', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file)
                    #Read the first row as the header
                    header = next(reader) 
                    #Strip spaces from the column names
                    header = [col.strip() for col in header]

                    #Remove spaces user from user input
                    sensitive_fields_list = [field.strip() for field in sensitive_fields.split(',')]

                    #Check if senstive field matches one of the fields in the dataset
                    missing_fields = [
                        field for field in sensitive_fields_list if field not in header
                    ]
                    #If the sensitve value doesnt match then we display error message to user.
                    if missing_fields:
                        messages.error(
                            request,
                            f"The following fields are missing from the file: {', '.join(missing_fields)}. "
                            "Please double-check your input as it is case, character, and space-sensitive."
                        )
                        return render(request, 'algorithm_selection.html', {'form': form})
            
                    #Count total number of rows in the file except for the header
                    row_count = sum(1 for _ in reader) -1
                    
                    #Keep track if issues happen for inputed values.
                    error_occured = False

                    #Check that none of the vlaues are greater than number of rows in file and return error message at top of screen and one in the form.
                    if k_anonymity_k_value:
                        if k_anonymity_k_value > row_count:
                            form.add_error('k_anonymity_k_value',f'This value can not be bigger than the number of rows in the file which is: {row_count}')
                            messages.error(request,f'Please check your K-Anonymity K-value.')
                            error_occured = True
            
                    if l_diversity_k_value:
                        if l_diversity_k_value > row_count:
                            form.add_error('l_diversity_k_value',f'This value can not be bigger than the number of rows in the file which is: {row_count}')
                            messages.error(request,f'Please check your L-Diversity K-value.')
                            error_occured = True

                    if l_value:
                        if l_value > row_count:
                            form.add_error('l_value',f'This value can not be bigger than the number of rows in the file which is: {row_count}')
                            messages.error(request,f'Please check your L-Diversity L-value.')
                            error_occured = True
                            
                    if t_closeness_k_value:
                        if t_closeness_k_value > row_count:
                            form.add_error('t_closeness_k_value',f'This value can not be bigger than the number of rows in the file which is: {row_count}')
                            messages.error(request,f'Please check your T-Closeness K-value.')
                            error_occured = True
                    
                    #If some error occured we dont allow further execution and users need to address issue before continuing
                    if error_occured:
                        return render(request, 'algorithm_selection.html', {'form': form})
            
            #If there is some accessing the selected file inform the user and dont allow them to continue.
            except Exception as e:
                messages.error(request, f"Error reading the selected file: {str(e)}. Please try again and if the issue persisits try re-uploading the file.")
                return render(request, 'algorithm_selection.html', {'form': form})
            
            #If all inputs are validated save parameters to the database
            AlgorithmParameter.objects.create(
                dataset=dataset,
                algorithm_type=algorithm_type,
                k_anonymity_k_value=k_anonymity_k_value,
                l_value=l_value,
                l_diversity_k_value = l_diversity_k_value,
                t_value=t_value,
                t_closeness_k_value=t_closeness_k_value
            )
            #Provide success feedback indicating processing request has gone through
            messages.success(request, f"Algorithm parameters saved for {selected_file}! Processing will now begin.")
            
            #Attempt to process datasets with each selected algorithm
            try:
                #Apply K-Anonymity and display any errors
                if form.cleaned_data.get('k_anonymity'):
                    try:
                        output_path = os.path.join(processed_dir, f'k_anonymized_{selected_file}')
                        apply_k_anonymity(selected_file_path,sensitive_fields, k_anonymity_k_value ,output_path)
                        messages.success(request, f"K-Anonymity applied successfully")
                        
                        ProcessedDataset.objects.create(
                            dataset=dataset,
                            algorithm_type="K",
                            processed_file_path=output_path
                        )
                        
                    except Exception as e:
                        messages.error(request, f"Error applying K-Anonymity: {e}")
               
                #Apply L=Diversity and display any errors
                if form.cleaned_data.get('l_diversity'):
                    try:
                        output_path = os.path.join(processed_dir, f'l_diversified_{selected_file}')
                        apply_l_diversity(selected_file_path, sensitive_fields, l_diversity_k_value, l_value,output_path)
                        messages.success(request, f"L-Diversity applied successfully")
                    
                        ProcessedDataset.objects.create(
                            dataset=dataset,
                            algorithm_type="L",
                            processed_file_path=output_path
                        )
                        
                    except Exception as e:
                        messages.error(request, f"Error applying L-Diversity: {e}") 
                
                 #Apply T-Closeness and display any errors
                if form.cleaned_data.get('t_closeness'):
                    try:
                        output_path = os.path.join(processed_dir, f't_close_{selected_file}')
                        apply_t_closeness(selected_file_path, sensitive_fields, t_closeness_k_value, t_value, output_path)
                        messages.success(request, f"T-Closeness applied successfully")
                    
                        ProcessedDataset.objects.create(
                            dataset=dataset,
                            algorithm_type="T",
                            processed_file_path=output_path,
                        )
                        
                    except Exception as e:
                        messages.error(request, f"Error applying T-Closeness: {e}") 
                                        
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                print(str(e))
                messages.error(request, f"Unexpected error: {str(e)}")
            
            #Display message informing user all algorithms were applied.
            messages.success(request, f"All algorithms have been applied. Please go to your Processed Datasets page.")   
            return redirect('algorithm_selection')  # Redirect to clear the form
        
        #Display error if user form isnt valid
        else:
            messages.error(request, 'There is some error with your form. Please double check it.')
    
    #When no form is submitted just display page.
    else:
        form = AlgorithmSelectionForm(file_choices=file_choices)

    return render(request, 'algorithm_selection.html', {'form': form})

'''
Displays a paginated list of processed datasets and provides options to download or delete them.
'''
@login_required
def processed_datasets(request):
    #Fetch path to the current users processed directory 
    processed_dir = os.path.join(settings.MEDIA_ROOT, request.user.username, 'processed')
    
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        action = request.POST.get('action')
        file_path = os.path.join(processed_dir, file_name)

        #Handle download action
        if action == 'download':
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
            else:
                messages.error(request, f"File '{file_name}' does not exist.")

        #Handle delete action
        elif action == 'delete':
            if os.path.exists(file_path):
                os.remove(file_path)
                messages.success(request, f"File '{file_name}' was successfully deleted.")
            else:
                messages.error(request, f"File '{file_name}' does not exist.")

        return redirect('processed_datasets')  # Redirect after handling action

    #Fetch processed files
    processed_files = []
    if os.path.exists(processed_dir):
        for file_name in os.listdir(processed_dir):
            full_path = os.path.join(processed_dir, file_name)
            if os.path.isfile(full_path):
                processed_files.append({
                    'filename': file_name,
                    'upload_date': datetime.fromtimestamp(os.path.getmtime(full_path))  # Get file modification time
                })

    #Sort files by modification date (aka upload date)
    processed_files = sorted(processed_files, key=lambda x: x['upload_date'], reverse=True)

    #Paginate processed files to show 10 files per page.
    paginator = Paginator(processed_files, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'processed_datasets.html', {
        'page_obj': page_obj,
    })
