# [Panem](http://panem.be)

Panem is een webshop voor bakkers waar hun klanten online bestellingen kunnen plaatsen en betalen. 

## Inhoudstafel
- [Werkomgeving opzetten](#werkomgeving-opzetten)
- [Git workflow](#git-workflow)
- [Versienummering](#versienummering)
- [Building](#building)

## Werkomgeving opzetten
De uitleg hieronder is van toepassing op ubuntu. Er wordt verondersteld dat deze repository gecloned is op een locatie die verder met `clone_root` wordt aangegeven. De setup is geldig voor ubuntu 16.xx, niet voor ubuntu 14.xx!

### Nodige software
- git (`sudo apt-get install git`)
- nginx (`sudo apt-get install nginx`)
- virtualenv (`sudo pip install virtualenv`)
- gunicorn (`sudo pip install gunicorn`)

### Herstellen van de virtuele omgeving
`clone_root/dist/` bevat een map die heet `panem_env`. Dit is een virtuele omgeving die kopietje bevat van python (2.7) met de nodige libraries voor de website (django, asana...). Om er voor te zorgen dat deze virtuele omgeving werkt op jouw computer, moet je eerst navigeren naar de map `clone_root/dist/`. Daar voer je het volgende commando uit : `virtualenv panem_env`. **Dit moet je ook steeds opnieuw doen nadat je gepulled hebt van Git.** De configuraties die hieronder beschreven zijn, moet je maar eenmalig uitvoeren. 

### Configuratie van gunicorn

Creeer een configuratie file `gunicorn.service` in de map `/etc/systemd/system/`. In het codeblok hieronder vind je wat in deze file moet staan. Let hierbij vooral op twee woorden die specifiek zijn voor je eigen installatie:
  - **username** (1x) vervang je door de naam van je ubuntu user
  - **clone_root** (3x) vervang je door het pad naar de virtuele omgeving, bijvoorbeeld `/home/nero/GIT/panem/`
  
<pre><code>
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=<b>username</b>
Group=www-data
WorkingDirectory=<b>clone_root</b>/src
ExecStart=<b>clone_root</b>/src/panem_env/bin/gunicorn --workers 3 --bind unix:<b>clone_root</b>/src/panem_project.sock panem_project.wsgi:application

[Install]
WantedBy=multi-user.target
</code></pre>
Je kan nu gunicorn starten met het commando `sudo systemctl start gunicorn`
Om er voor te zorgen dat je dit niet steeds hoeft te doen kun je instellen dat dit automatisch gebeurt bij het opstarten van je computer met het commando `sudo systemctl enable gunicorn`

### Configuratie van nginx

Je maakt opnieuw een configuratiefile aan, ditmaal de file `panem_project` in de map `/etc/nginx/sites-available/`. Let opnieuw op **clone_root** die tweemaal moet vervangen worden door de juiste map. 

<pre><code>
server {
    listen 8000;
    server_name localhost;

    location / {
        include proxy_params;
        proxy_pass http://unix:<b>clone_root</b>/src/panem_project.sock;
    }
}

server {
    listen 80;
    server_name localhost;

    location = /favicon.ico {access_log off; log_not_found off; }
    location / {
        root <b>clone_root</b>/src/static/frontend;
    }
}
</code></pre>

Voer daarna het commando `sudo ln -s /etc/nginx/sites-available/panem_project /etc/nginx/sites-enabled` uit. 
Herstart nu nginx : `sudo systemctl restart nginx`

### Installatie van python libraries
Het is belangrijk dat libraries geinstalleerd worden in de virtuele omgeving. Op deze manier worden ze deel van de source code van de website en zal ook de library mee gepushed worden naar de Git server. Om binnen te gaan in de virtuele omgeving navigeer je eerst met je terminal tot in de `clone_root/src` map. Je typt volgend commando om de virtuele omgeving op te starten : `source panem_env/bin/activate`. Met pip kun je nu libraries installeren, bv. `pip install numpy`. Let op om hierbij **niet het prefix sudo** te gebruiken. Anders wordt de library toegevoegd aan je lokale versie van python, niet aan de versie binnenin de virtuele omgeving.  

Je kunt een lijst van alle geinstalleerde libraries en hun versienummer opvragen met het commando `pip freeze`. 

## Git workflow
Deze repository is georganiseerd volgens [dit](http://nvie.com/posts/a-successful-git-branching-model/#feature-branches) systeem. Development gebeurt altijd in de src directory, niet in de dist. 

## Versienummering
- alle versienummers bestaan uit drie getallen x.y.z
- x.y is het zelfde als x.y.0
- x.y is de releaseversie
- z verschillend van 0 wordt gebruikt om hotfix releases aan te duiden
- versies kunnen ook een naam hebben, maar die wordt op Git niet gebruikt

## Building
Het script build.py in de root directory doet het nodige werk om in de dist directory een build te maken uit de source (src) files. Het script wordt als volgt aangeroepen: 
`python build.py 4.6.3` waarbij 4.6.3 het versienummer is van dit voorbeeld

