# Project report

Flaws listed are from the OWASP 2021 top ten list: https://owasp.org/www-project-top-ten/ . 

## FLAW 1:
### A01 Broken access control 

The flaw can be found in views.py file lines [61 to 71](https://github.com/NuiS4ncE/kyberfailapp/blob/main/src/kyberfail/views.py#L61-L69). 

For viewing the notes in the singular note viewing page, it’s possible for a user to view another user’s note with its title, description and date. This is not a secure way of handling individual notes as they are supposed to be seen only by doctors defined as a true/false value in Accounts model or the persons who have been written the note by the doctor(s). 

This can be fixed by making a check in the views.py, where you check that if the note’s user id is not the same as the logged in user id and they are not a doctor, they are redirected to the homepage. Fix can be found in the [working](https://github.com/NuiS4ncE/kyberfailapp/tree/working) branch in lines [61 to 71](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/kyberfail/views.py#L61-L71), specifically lines [68 to 69](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/kyberfail/views.py#L68-L69).

## FLAW 2:
#### A07 Identification and Authentication Failures

Flaw is found in the `initialmigration.py` file in lines [36 to 52](https://github.com/NuiS4ncE/kyberfailapp/blob/main/src/kyberfail/migrations/initialmigration.py#L36-L52), specifically line [41](https://github.com/NuiS4ncE/kyberfailapp/blob/main/src/kyberfail/migrations/initialmigration.py#L41) and line [43](https://github.com/NuiS4ncE/kyberfailapp/blob/main/src/kyberfail/migrations/initialmigration.py#L43).

The admin username and password has been set in the `initialmigration.py` file as “admin” and “admin”. They are also in plain-text form in the database migration file.  In identification and authentication failures logins and authentication can be for example brute forced by using dictionary attacks.

This can be fixed by introducing a dotenv file with the [python-dotenv package](https://pypi.org/project/python-dotenv/). By setting hidden environment variables that are unknown to the possible attacker (and to the viewer of the repo,) and that are complicated enough, the admin credentials aren’t as easy to guess or to do a dictionary attack with. Fix can be found in the `working` branch in the files `config/settings.py` lines [14 to 17](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/config/settings.py#L14-L17), where dotenv library is imported and configured for the app and `initialmigration.py` in lines [36 to 52](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/kyberfail/migrations/initialmigration.py#L36-L52), specifically line [41](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/kyberfail/migrations/initialmigration.py#L41), where the username is fetched from the `.env` file and line [43](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/kyberfail/migrations/initialmigration.py#L43), where the password is fetched from the `.env` file.

## FLAW 3:
#### A03 Injection 

The flaw is visible in the `views.py` file lines [138 to 153](https://github.com/NuiS4ncE/kyberfailapp/blob/main/src/kyberfail/views.py#L138-L153), specifically lines [146 to 150](https://github.com/NuiS4ncE/kyberfailapp/blob/main/src/kyberfail/views.py#L146-L150), where connection to the SQLite database is established and then an unsanitized query is allowed to be sent to the database.
In the search view it’s possible for users to view other patients’ notes by doing an SQL injection. By writing `3=8’ UNION SELECT * FROM kyberfail_note –` into the search bar, you can see all notes. You can also see usernames and hashed passwords by writing `3=8' UNION ALL SELECT auth_user.id, auth_user.username, auth_user.password, auth_user.is_superuser, null FROM auth_user JOIN kyberfail_note ON auth_user.id = kyberfail_note.user_id –`. There might be other possible ways to do injections.  

The fix is found in the `working` branch in `views.py` lines [139 to 155](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/kyberfail/views.py#L139-L155), specifically lines [147 to 151](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/kyberfail/views.py#L147-L151). The Django ORM (Object-Relational Mapper) is used instead of custom SQL query. The ORM sanitizes inputs by default and is much more secure than the custom query. Checks for doctor and superuser status have also been introduced. 

## FLAW 4:
#### A04 Insecure Design

The page template file `search.html` is missing a check for doctor status in lines [93 to 99](https://github.com/NuiS4ncE/kyberfailapp/blob/main/src/kyberfail/templates/pages/search.html#L93-L99).
Again in the search view, it’s possible to remove notes from yourself. By using the other aforementioned SQL injection, you can also remove notes from other patients. This can be done directly from the front-end search input or by making a POST request using other tools. 

This can be fixed by adding an if-statement in line [95](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/kyberfail/templates/pages/search.html#L95) and line [83](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/kyberfail/templates/pages/search.html#L83) as well as by adding sanitation for the backend in `notesView` in line [97](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/kyberfail/views.py#L97). By checking user privilege status in the backend, possible POST requests sent using tools can be blocked. Line 83 statement is somewhat for cosmetic reasons, though, as to not reveal to normal users that there should be something. 

## FLAW 5:
#### A05 Security Misconfiguration

The flaw can be found in the `settings.py` file on line [26](https://github.com/NuiS4ncE/kyberfailapp/blob/main/src/config/settings.py#L26).  

By allowing the [Debug mode](https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-DEBUG) to be turned on such as it is in the settings.py on line [26](https://github.com/NuiS4ncE/kyberfailapp/blob/main/src/config/settings.py#L26), Django provides detailed error pages that might reveal possible sensitive information such as error traceback, metadata and settings set up in the `settings.py` file. Revealing sensitive information gives more tools for the attacker to figure out a way to hack in to the website.

This flaw can be amended by setting the Debug mode to `False` in the `settings.py` as it is in here in the working branch on line [30](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/config/settings.py#L30) and by sanitizing error messages such as it is in the working branch in `views.py` file on the lines [44 to 47](https://github.com/NuiS4ncE/kyberfailapp/blob/working/src/kyberfail/views.py#L44-L47).

