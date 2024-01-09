# IA_Cloud_G3

### Install requirements:

pip install -r requirements.txt

### Initialize the mySql database (from trustPilot data => McdonaldFr):

```docker-compose up```

```python retrieveData/parseData.py```

```python scrapping/trustpilot.py ```

### To directly have access to the mySql database:

```mysql -h 127.0.0.1 -P 3307 -u root -ppassword reviews```
