# IA_Cloud_G3

## Install requirements:

pip install -r requirements.txt


## Initialize the mySql database (from trustPilot data => McdonaldFr):

- To do once, then once it's initialized you only have to do: ```docker-compose up```

```docker-compose up```

```python scrapping/trustpilot.py ```

#### To delete the container (to restart the database  from scratch):

```docker rm ia_cloud_g3_mysql_1```


#### To directly have access to the mySql database (for manual check):

```mysql -h 127.0.0.1 -P 3307 -u root -ppassword reviews```
