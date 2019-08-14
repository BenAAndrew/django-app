# django project

<h2>This is a sample Django project covering both backend and frontend development</h2>
<h3>Structure;</h3>
<ul>
  <li><b>App:</b>The frontend <b>Django</b> application which serves pages</li>
  <li><b>Api:</b>The backend <b>Django-rest</b> framework which processes requests and manages a database</li>
  <li><b>pyTest:</b>Pytest frontend tests</li>c
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
cd api
```

Step 4: Run setup either using the runserver script (./runserver) or run the following commands manually

<hr>
<h3>App</h3>
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
