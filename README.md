# `paiji2_utils` #
===================

##`profile` template tags library ##
-----------------------------------

### `profile_url` ###

URL to the user’s profile page.

For instance :

```
{% load profile %}

<a href="{% profile_url request.user %}">hello</a>
```

### `profile_link` ###

A link to the user’s profile page, that shows the user’s first name.

For instance :

```
{% load profile %}

{% profile_link user %}
```

### `mail_link ###

A link to send an email to the user. The `text` is the text shown on the html page, the `subject` is the subject of the email.

```
{% load profile %}

{% with subject='send a mail to :'|add:user.first_name %}
{% mail_link user '[paiji2] Re: welcome !' subject %}
{% endwith %}

```
