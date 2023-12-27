# TRANSLATION


## Getting started
> **_NOTE:_** Before starting translating project text make sure you have installed and configured the gettext from GNU
https://www.gnu.org/software/gettext/ 

To  make the translation just use the command above (in this case for pt-BR):
```
django-admin makemessages --locale=pt_BR --ignore 'venv' --ignore 'requirements.txt'
```

After the command access the 'locale' folder and check the django.po file of the language
you want to translate. Make the translation and compile it with the command above:
```
django-admin compilemessages --locale=pt_BR --ignore 'venv' --ignore 'requirements.txt'
```