# Probase: CMIMC's Problem Database

## Getting Started

### Setup
1. Make sure you have [Python](https://www.python.org/downloads/) installed on your computer.
2. Clone this repository: `git clone https://github.com/CMU-Math/probase.git`
3. In the newly created folder, run `pip install -r requirements.txt`
4. Then run Django migrations: `python manage.py migrate`
5. Start the Django development server: `python manage.py runserver`
6. Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser, and you should see the home page. It should look like the image below:

    ![Home Page](static/img/homepage.png)

### Making user accounts
1. First, create a super user account: `python manage.py createsuperuser`. You can enter any name, email, and password.
2. Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) again, and you should be redicted to the 'All Problems' page. There won't be any problems yet, but you can create one with the 'New Problem' button.
3. The super user account you created in step 1 has all permissions enabled: problem writer, testsolver, and staff. If you create a new account normally (click 'log out', then 'sign up' in the top right), it will have no permissions enabled by default. You have to go to the [Manage Users](http://127.0.0.1:8000/manage-users/) page to change their permissions.

### Tutorials
For anyone new to either Python, Django, or Bootstrap, here are some tutorials.

Python Tutorials:
- [https://www.learnpython.org/](https://www.learnpython.org/)
- [https://thepythonguru.com/](https://thepythonguru.com/)
- [https://pythonbasics.org/](https://pythonbasics.org/)

Django Tutorials:
- [https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/](https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/)
- [https://docs.djangoproject.com/en/3.0/intro/tutorial01/](https://docs.djangoproject.com/en/3.0/intro/tutorial01/)
- [Django Documentation](https://docs.djangoproject.com/en/3.0/topics/)

Bootstrap:
- [https://www.youtube.com/playlist?list=PL41lfR-6DnOovY0t3nBg8Zb6aqm_H70mR](https://www.youtube.com/playlist?list=PL41lfR-6DnOovY0t3nBg8Zb6aqm_H70mR)
