# Clone of Shatel.ir

<img src="./Storage/media/logo/logo.png">

<br>
<br>
Shatel is an Iranian Internet Service Provider and a "large" Local Internet registry based in Tehran, Iran . Shatel is the first ADSL2+ service provider in the country, and the first gigabit wireless network operator based on registered microwave frequency.


<img src="./GithubDoc/image/index-full.png">
<img src="./GithubDoc/image/register.png">
<img src="./GithubDoc/image/login.png">
<img src="./GithubDoc/image/reset.png">
<img src="./GithubDoc/image/job-hire.png">
<img src="./GithubDoc/image/varanty.png">





    python -m venv venv
    python3 -m venv venv
<br>

    pip install -r requirements.txt 
    pip3 install -r requirements.txt 

<br>

    flask db init 
    flask db migrate
    flask db upgrade


<br>

    ./scripts/runCelery.bat # for windows
    ./scripts/runCelery.sh # for linux & mac


<br>

    python app.py
    or
    flask run
    

