# NanoBlog
Nano-Blogsite realized by Django2.1/ Python3.7/ HTML/CSS/JavaScript/JQuery/Ajax

# Grumblr - Nano Blogsite realized by Django

### Introduction
Grumblr is a nano-blog-website that allows user to "register through email confirmation" / "login" / "logout" / "write a post" / "delete a post" / "check all the posts" / "check posts by 8 categories" / "follow other users" / "unfollow users" / "check followers' posts" / "edit user profile" / "reset password through email confirmation" / "reset password through old-password authentication" and more.

### Result Display
URL: 

### Important Function Specification
* Register: 
  * User needs to logout first to register a new user, since after successfully registered, the user would be redirected to his/her personal profile.
  * User need to provide his/her username, password, age, tel, firstname and lastname to successfully register. If any of these parameter miss, an error massage would pop up to remind the user to try again.
  * If User choose a username that already existed in the database, an error massage would pop up to remind the user to try another one.
  
* Login:
  * User can login by providing matching password and username. If the username and password does not match, a error massage would pop up. 
  * If user only provide the password or username while leaving another blank, an error massage would pop up to remind user to enter the value.
  * If user successfully login, the user would be redirected to his/her user profile page. 
  
* Logout:
  * The user may logout by pressing "logout" button on the navigation bar to log out. Notice that if there is no user logged in the grumblr, the navigation bar would only show "login" button. After a user logged in, the "login" button would disappear and "logout" would appear.
  
* User Profile:
  * After a user logged in, he/she could check his/her profile by pressing "My Account" button on the navigation bar. In this page, the personal information like username, firstname, lastname, telephone, email, and whatsup would shown on the left side. The right side of the page is used to show user's posts based on reverse chronological order. These posts are divided into several pages with a limit of 4 posts per page. There is also a "quick post" section so that the user can post just in this page.
  * If user want to change their profile, they can click the "Edit Your Profile" button to change.
  
* Edit Profile:
  * The user may edit their personal information anytime they want. But notice that the username could not be changed since it is unique and non-modifiable. 
  * Password and Firstname are required and should not be none. Since password is required for login and firstname is required for shown in the user profile page. If user try to leave them blank, an error massage would pop up.
  * The user's email should follow the normal email address format. If the email address doesn't follow the format, an error massage would pop up.
  
* Check posts:
  * In the homepage of the grumblr(globalStream), there is a "Check All Posts!" button which allows user to check all the posts that had been posted by members based on reverse chronological order. The posts would be updated every 5 seconds automatically (realized by Ajax)
  * Every post would show the author name, category and publish time. The author name is highlighted. And user can click the author name to check this author's profile information. This profile display is different from the user's own personal profile.
  * In the homepage of the grumblr, the user may check the posts by 8 different categories which includes General, Programmer Zone, Gamer, Delicacy, Pets, Sports, Making Friends, and Movies. The posts are classfied by categories and based on reverse chronological order.
  
* Write a post:
  * User can post a short massage less than 42 words anywhere where they can see the "quickpost" section.
  * User can select a category among eight categories to decide where they want to post.
  * User can only delete the post made by themselves.
  
* Comment:
  * User can comment any post everywhere where they can see the posts.
  * Users can only delete the comment made by themselves.
  
* Follow/Unfollow Other Users and check followStream page: 
  * There is a 'followerStream' button on the navigation bar. If a user hasn't follow anyone, an error massage would pop up to remind the user that he/she hasn't follow anyone yet.
  * Logged in users may view globalStream to see posts from other users. There is a "follow" button on each posts. So when this logged-in user is especially interested in a post and want to follow the author, he/she can click the 'follow' button and the page would be redirect to 'followerStream' to display the posts from all the users he/she is following.
  * Logged-in user could not follow him/herself since there is no follow button on his/her own posts.
  * All the posts from the users that the logged-in user is following would be shown in the 'followerStream' page, which are ordered in reverse-chronological order. There is an 'unfollow' button on the each post. The logged-in user can click this button to unfollow the user he/she does not want to follow anymore.
  * The follow relationship is unidirectional, which means if you follow another user, that user would not automatically follow you.

* Change profile and password:
  * The logged-in user may click 'Edit Your Profile' button in the 'userProfile' page. 
  * The user may edit their personal information anytime they want. But notice that the username and email could not be changed since they are unique and non-modifiable. 
  * Firstname and lastname are required and should not be none. Since they are required for shown in the user profile page and other users' friends list. If the user try to leave them blank, an error massage would pop up.
  * The default value of Age is 0. And Age could not be less than 0 or higher than 100.
  * Tel and Short BIO are not required for users.
  * There is an 'Profile Picture' field that allows user to upload a picture to be their avatar/profile picture. There is a default picture for user's 'Profile Picture' if they do not set it by themselves. The pictures uploaded by users would be store in 'media/grumblr-avators' folder.
  * Rather than changing normal profile information, if the user wants to change their password, he/she can click the 'Change Password' button on the buttom of this page, and the page would be redirect to the 'changePassword' page.
  * Unlike 'reset password', 'change password' requires user to provide his/her old password to verify his/her identity. If the password does not match, an error massage would pop up. If user really forget his/her old password, he/she can click the 'Reset Password By Email' button on this page, and the page would be redirect to the 'reset password' page.

* Reset Email Validation:
  * The reset email validation part is based on the views and forms provided by 'django.contrib.auth'. Four original pages were overwrited by 'password_reset.html, password_reset_done.html, password_reset_confirm.html and password_reset_complete.html'. 

* Activate User by Email Validation:
  * When user try to register Grumblr, a valid email address is required for future validation. After user entered the correct information, an 'User' object would be created without activation (user.is_active = 0). At this time, although there is already a user object in the database, but user could not login before they activate their account through email.
  * After user press the link that the activate email provided, this User object would be activated and the page would be redirect to another info page saying that the user has alreay sucessfully registered. The user can click the 'Login' button on this page to login with username and password.
  
### Reference: Develop Environment
- Python version: python 3.7
- Django version: Django 2.1
- Deployment Platform: DigitalOcean / Nginx / Gunicorn
- Email Server: Gmail SMTP server
- Database: postgresql_psycopg2
  
### Reference: CSS Library
- Bootstrap 3.3.7
- W3CSS Library (https://www.w3schools.com/w3css/4/w3.css)
- Googleapis Lobster Fonts (https://fonts.googleapis.com/css?family=Lobster)

### Reference: Picture Library
- Qiantu Website: http://www.58pic.com/ (copyright: Commercially available)
