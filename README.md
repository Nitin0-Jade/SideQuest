# SIDEQUEST

#### Video Demo: https://youtu.be/CVvRvjffP2I

#### Description:

SideQuest is a student focused web application which I made to solve some common everyday problems that students face in college. The main idea behind this project is very simple. Many students need help with small things like finding a ride, finding a lost item, or splitting an expense with friends, but usually these things are done through WhatsApp groups, personal messages or asking people directly.

The problem with that is that messages can get missed very easily. If someone posts that they need a ride in a big WhatsApp group, the message can go down after some time. The same thing can happen with a lost item post or an expense request. Because of this, students can have difficulty finding the right person or even seeing that a particular request was posted.

So I made SideQuest as one common platform where students can post these types of needs and other students can discover them and help.

The main flow of the website is:

**POST → DISCOVER → CONNECT → COMPLETE**

A student can post a quest, other students can see the available quests, they can connect by joining the quest, and finally the quest can be completed.

## Why I Made SideQuest

I wanted to make something that is not only a normal CRUD website but something which can actually be useful for students in a college campus.

In a college there are already many communication platforms but most of them are not really made for structured requests. WhatsApp, for example, is good for communication, but it is not really designed for finding a particular ride, tracking an expense split, or keeping lost and found posts organized.

SideQuest tries to solve this by giving these problems a proper place.

I also wanted the project to be modular so that more student features can be added later without changing the whole application.

## Main Features

SideQuest currently has three main modules.

### 1. Carpool / Fare Split

The carpool feature is the main working part of the project.

A student can create a carpool quest by entering the starting location, destination, travel date, travel time, available seats and estimated fare.

After creating the quest, other students can go to the Find Ride section and search for available rides using the origin, destination and date.

When a student finds a suitable ride, they can open the quest details and join it.

The backend checks how many people have already joined the ride before allowing another person to join. This helps prevent the number of participants from going above the available seat limit.

The fare can also be divided equally between the people in the ride. For example, if a ride has an estimated fare of ₹600 and 3 people are sharing it, the fare per person becomes ₹200.

The creator can also mark the quest as completed after the ride is finished.

This is currently the most complete workflow in SideQuest.

### 2. Lost & Found

The second module is for lost and found items.

A student can create a quest and give it a title and description about the item. For example, someone could post about a missing wallet, ID card, bottle or other item.

The main idea is to have a common place where students can post these things instead of sending the message into different groups.

Other students can open the quest and read the information provided by the person who created it.

This feature is currently a simple MVP and there are more things which I want to add in the future, like image uploads and better search.

### 3. Expense Split

The third module is for splitting common expenses between students.

A student can create an expense quest and enter the total amount. Other students can join the expense and the application calculates an equal share based on the number of participants.

For example, if the total expense is ₹1000 and 4 people are participating, each person's equal share will be ₹250.

This can be useful for things like food, travel or other shared student expenses.

At the moment it is mainly focused on equal splitting and does not have a full payment or settlement system.

## How The Website Works

The application uses Flask as the backend framework.

When a student opens a page, Flask handles the route and communicates with the SQLite database when needed. The database stores users, quests and the information related to different quest types.

Jinja templates are used for displaying the information dynamically inside the HTML pages.

For example, when the homepage is opened, Flask gets the quests from the database and sends them to the template. The template then displays the quest information.

There are also login and registration systems in the application.

Users can create an account with a username and password. Passwords are not stored directly in the database. They are hashed using Werkzeug before being stored.

Flask-Session is used to keep track of logged in users.

I also created a login_required function so that pages which need a logged in user can check the session before allowing access.

## Database

I used SQLite for the database because it was simple to setup and works well for an MVP.

The database contains tables such as:

- users
- quests
- quest_participants
- carpools
- lost_items
- expenses
- expense_participants

The `quests` table is used as the common base for the different types of requests.

This means a carpool, lost and found post and expense can all be represented as quests while still having their own additional information in separate tables.

I chose this structure because it makes the application easier to expand later.

## Technology Used

The main technologies used in this project are:

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- Jinja
- Flask-Session
- Werkzeug
- Git
- GitHub

I used Bootstrap for some of the common UI components and also wrote my own CSS for the main design.

The project was developed using VS Code and the code is stored in GitHub.

## Project Structure

The main backend file is:

`app.py`

The HTML templates are stored inside:

`templates/`

The CSS is stored inside:

`static/`

The main database file is:

`sidequest.db`

There is also a `requirements.txt` file which contains the Python packages needed to run the project.

Some of the important templates include the homepage, login page, register page, create quest page, quest detail page and my quests page.

## How To Run The Project

To run the project locally, first install the required packages:

```bash
pip install -r requirements.txt

python app.py

Then open the local URL shown by Flask in the browser.

The project is also deployed online so that it can be tested without running it locally.

Challenges I Faced

One of the biggest challenges was making all the different quest types work while keeping the structure simple.

I also had to handle things like login sessions, checking invalid input, preventing users from joining a full carpool and connecting the different database tables correctly.

Another challenge was making the website look good while still keeping the code manageable. I used Bootstrap for some parts but also wrote custom CSS because I wanted SideQuest to have its own design.

Deployment also created some issues because SQLite on a normal hosted web service does not work like a fully persistent production database. This is something I would improve in the next version.

Future Improvements

There are many features that I would like to add in the future.

For carpool, I would like to add smarter matching based on route and travel time instead of only using exact values.

For Lost & Found, I want to add image uploading, better search and more location based information.

For Expense Split, I want to make a more advanced settlement system where different people can pay different amounts instead of only doing equal splits.

I also want to add notifications, user reputation or trust scores, better moderation and possibly a PWA or mobile application.

Another important improvement would be moving from SQLite to a hosted database like PostgreSQL for better persistence and scaling.

AI And Development Tools

I used AI tools during development for learning, debugging, understanding errors and getting ideas for implementation. I still tested the code myself and changed the code according to the requirements of the project.

I also used GitHub for version control and Render for deployment.

Conclusion

SideQuest is my attempt to make a simple but useful platform for students.

The project is still an MVP and there are some limitations, but the main idea is to make everyday student problems more organized instead of depending completely on large chat groups.

The most important part for me was learning how a complete web application works, from frontend pages and forms to Flask routes, databases, authentication and deployment.

I also learned that making a project work is only one part of the process. Testing, handling errors, designing the UI and thinking about future scaling are also important.

Overall, SideQuest helped me understand how the different parts of a web application connect together, and I would like to keep improving it after the first version.