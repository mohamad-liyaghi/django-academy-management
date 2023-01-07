# Django Academy Management

## Introduction
<hr>
<p>
As it is obvious from repo's name, this project is an academy management system api, using <a  href="django-rest-framework.org/">DRF</a>. Users can sell their courses or search for courses and buy them.
</p><hr>
<p>
    We have 4 types of users in this system.
</p>
<ol>
    <li>Superuser</li>
    <li>Admin</li>
    <li>Teacher</li>
    <li>Student</li>
</ol>
<p>
    By default all users status is 'Student'. They can simply create a request to promote. <br><br>
    Superusers accept/decline/block teachers and admin requests.<br><br>
    Admins accept/decline/block teachers requests.<br><br>
    Teachers can add courses and students can purchase them.
</p>
<hr>
<p>
    This project consists of 2 applications.
</p>
<ol>
    <li>Accounts</li>
    <li>Classes</li>
</ol>

### Accounts

<p>
    This project is using <a href="https://djoser.readthedocs.io/en/latest/">Djoser</a> for authentication purposes like registering and creating jwt token. <br><br>
    Also there is a profile viewset implemented in this application that helps users to update and examine their profiles. By default profiles will be created after a user creates an account (Using signals).<br><br>
    Alongside Profile viewset, there is a Request viewset too. <br><br>
    Users can simply request to promote their status (become a teacher or admin) and admin users can accept or decline them.<br><br>
</p>

### Classes

<p>
    Users can request to become a teacher. After they approved, they can simply add new courses on our website. <br><br>
    After teacher published the course, it will become available on others home page and if they want, they would purchase that item.<br><br>
    Teachers can add links for their courses and students can simply download or visit that link in order to access expected content.<br><br>
</p><hr>

## How to use

### Step 1
<p>For accessing code, you should clone this project.</p>

```commandline
> git clone https://github.com/mohamad-liyaghi/django-academy-management.git
```

### Step 2
<p>This project is dockerised. Thanks to docker, you can start this project with one simple command.</p>

```
> docker-compose up --build
```

## Tests

<p>Also there are some tests for implementation. You can run by using following command:</p>

```
> pytest
```

<p>Good luck.</p>
