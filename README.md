# django project

<h2>This is a sample Django project covering both backend and frontend development</h2>
<h3>Structure;</h3>
<ul>
  <li><b>App:</b>The frontend <b>Django</b> application which serves pages</li>
  <li><b>Api:</b>The backend <b>Django-rest</b> framework which processes requests and manages a database</li>
  <li><b>pyTest:</b>Pytest frontend tests</li>
</ul>

This sample app creates an application management system where users can create applications and attach goods, and admins can accept or decline their application requests.

<hr>
<h2>Setup</h2>
Step 1: Clone this repo and cd into the project

Step 2: Create a python environment (anaconda, virtualenv etc.) and run
```
pip install -r requirements.txt
```

Step 3: Create a secure key file
<ol>
  <li>Go to https://mkjwk.org/</li>
  <li>Set key size to 2048, key use to encryption and algorithm to RS256</li>
  <li>Click generate</li>
  <li>Copy everything in keypair set into a file</li>
  <li>Remove the outer array starting with '"keys": [' so that it is now just { *content* } and no outer object</li>
  <li>Save as key.json in the root directory of the project</li>
</ol>
 
This is the secret key file used for encrypting/decrpyting user tokens in the front and backend

Step 3: Build the database by running
```
python api/manage.py migrate
python app/manage.py migrate
```

Step 4: Run setup either using the runserver script (./runserver) or run the following commands manually

Option 1: Using runserver script
```
chmod -x runserver
./runserver
```
This script also checks if any migrations have occured before running which is handy.
You can now run <b>./runserver</b> every time you want to run the project.
You may also need to run <b>killall python</b> if you get an error saying the port is in use (means the front or backend didn't shutdown properly.

Option 2: Manually doing what the script does
```
python api/manage.py runserver 0.0.0.0:8001
```
Then open a second terminal and execute
```
python app/manage.py runserver 0.0.0.0:8000
```
This runs the api locally on port 8001 and the app locally on port 8000.

If you now navigate to localhost:8000/login you're ready to go

<hr>
<h3>App</h3>
This was developed using the documentation at https://www.djangoproject.com/

Within the app folder multiple components are defined;
<ul>
  <li>admin: Manages the admin pages where all pending applications can be viewed and processed</li>
  <li>applications: Manages user application pages for viewing, editing and deleting</li>
  <li>goods: Manages user good pages for viewing, editing and deleting</li>
  <li>login: Manages the login and signup pages</li>
</ul>

Within each of these components two key files are defined;
<ul>
  <li><b>views.py:</b> Defines the functions which are called when a page is requested</li>
  <li><b>urls.py:</b> Defines the url paths for the different view functions</li>
</ul>
All other files are created by default when django creates a component

The main folder inside this is <b>app</b> which defines the settings and root urls of the project. The key files in this folder are;
<ul>
  <li><b>urls.py (standard):</b> Defines which urls should be included (appended onto url stated in this file)</li>
  <li><b>settings.py (standard):</b> Defines settings for the app. All is standard except for declaring the static and templates default folder</li>
  <li><b>apiRequest.py (custom):</b> Handles backend api requests using the requests python library. Also defines the address and url of api endpoints</li>
  <li><b>tools.py (custom):</b> Handles various tasks such as decoding form post data into a json/dict and getting messages stored in the session</li>
  <li><b>userChecks.py (custom):</b> Handles decoding the user session cookie and checking the user can access a given page usng the check_is_user and check_is_admin annotation</li>
</ul>

Finally there are two folders; <b>templates</b> and <b>static</b>. These contain the html and css for the app and hvae been added to settings.py to be used for looking for these asset types
  
<hr>
<h3>Api</h3>
This was developed using the documentation at https://www.django-rest-framework.org/

Similar to the frontend app components for the api addresses are declared with the only difference being that login is called users in the backend as thios refers to thte object type it handles.

These components include mostly the same files but also add some new ones;
<ul>
  <li><b>models.py:</b> Declares the object that we want to store (Django auto generates the SQL and handles the database interactions for us)</li>
  <li><b>serializers.py</b> Serialises data to be saved to the db. In the case FlexSerializer is being used to simply extend the model so that the fields don't need to be redeclared</li>
</ul>

<hr>
<h3>Explaining urls</h3>
Urls aren't too complicated but it's useful to understand how they're built. 
If you look at urls.py in apps you'll see lines such as 

```
path('applications/', include('applications.urls'))
```
What this means is all the urls in applications urls.py are appended onto 'applications/'. For example if there is a url in applications called 'abc/' this means the full url would be localhost:8000/applications/abc/.

If you look in the urls.py in applications you'll also see

```
path('', views.index, name='index'),
```
What this means is that theres no additional path for this enpoint and so is simply reached at localhost:8000/applications/. You also see that it's poiting this request to the function index in views.py.

Another important example to note is

```
path('edit/<int:application_id>/', views.edit_application, name='editApplication'),
```
The <b><int:application_id></b> in the url is converted into an integer variable called application_id. For example if the user requested localhost:8000/applications/edit/10/ it would pass 10 to the view edit_application. 
  
This works the same way in the backend API.
  
  
<hr>
<h3>Explaining views</h3>
Views as discussed earlier are the functions that handle url requests.
Within each of these functions the different request types are checked such as GET and POST.


<h4>App</h4>
GET's in the app generally return a page with data. These typically end with a <b>render</b> which returns a HTML page with any data that should be given to it. For example;

```
if request.method == "GET":
    return render(request, 'createuser.html')
```
simply returns the createuser.html page when a get request is made to login/create/.

A more complex example would be where data is passed to the page such as;

```
if request.method == "GET":
    data = {"isAdmin": is_admin(request), "good": get_good(good_id, request)}
    msg = get_message_or_error(request)
    if msg:
        data.update(msg)
    return render(request, 'editGood.html', data)
```
This involves building a data dictionary which will include a message if one is found in the session (see get_message_or_error in tools.py). This dict is passed to the render and is used by the page as outlined in the editGood.html template.

POST's in the app generally send data to the api to be processed and redirect the user accordingly (HttpResponseRedirect). For example;

```
data = form_body_to_json(request.body.decode('utf-8'))
post_request(request, "create_account", data)
request.session['message'] = "User created"
return HttpResponseRedirect('/login/')
```
This firstly takes the form request data and converts to a JSON using the form_body_to_json method defined in tools.py. It then sends these to the backend using post_request defined in apiRequests.py. It then sets a session message to say the user was create successfully. Finally it redurects them to the login page.
These can be extended to check for error such as;

```
data = form_body_to_json(request.body.decode('utf-8'))
r = post_request(request, "goods", data)
if r.status_code == 400:
    request.session["error"] = handle_error_response(json.loads(r.content.decode('utf-8')))
    return HttpResponseRedirect('/goods/create/')
else:
    request.session["message"] = "Successfully created a good"
    return HttpResponseRedirect('/goods/')
```
in create_good which similarly posts form data to the backend but then will do different things depending on the status code. if it returns a 400 (error) we set a variable called error to the error message after being formatted by handle_error_response. It will then redirect back to the create page. Otherwise it was successful so sets a success message and redirects to goods homepage.
