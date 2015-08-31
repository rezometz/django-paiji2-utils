# `paiji2_utils` #
===================

## `readmore` tags library ##
----------------------------

### `readmore` filter ###

TODO: this function is not clean, are you trying to write PHP guys?

Uses javascript to show only the first words (15 by default) of a text, and enables visitor to read the rest by clicking on a link.

For instance :
```
{% load readmore %}

{{ 'my beautiful text [...]'|readmore:20 }}

{{ message|readmore }}
```

## `urlize2` tags library ##
---------------------------

### `urlize2` filter ###

Replace urls beginning with `ftp://` and `http(s)://` in a text with a html link: [link]`

For instance :
```
{% load urlize2 %}

{{ item.content|urlize2 }}

{{ item.content|urlize2|readmore:20 }}
```

##`profile` tags library ##
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

### `mail_link` ###

A link to send an email to the user. The `text` is the text shown on the html page, the `subject` is the subject of the email.
The `subject` doesn’t need to be url encoded, `mail_link` does it.

```
{% load profile %}

{% mail_link user text subject %}

{% mail_link user '' subject %} {# only a mail icon is shown #}

{% with subject='send a mail to :'|add:user.first_name %}
{% mail_link user 'send a mail' subject %}
{% endwith %}

```
