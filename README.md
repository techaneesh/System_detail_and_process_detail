## Clone the repository using this command
```bash
git clone https://github.com/techaneesh/System_detail_and_process_detail.git

```

## 1. Create and Activate Virtual Environment in both folder agent and monitor_backend

### On Windows:

```bash
cd monitor_backend
python -m venv venv
venv\Scripts\activate

cd agent
python -m venv venv
venv\Scripts\activate
```

---

## 2. Install Dependencies

Reach to project root where `requirements.txt` is located.

```bash
pip install -r requirements.txt
```
and then reach inside agent folder there is also requirement.txt file available. In another terminal inside activated environment same for that also.
---

## 3. Run Django Backend

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 4. Run the Agent

From the folder where `agent.py` is located:

```bash
pyinstaller --onefile agent.py
```

This will collect system and process information and send it to the backend API.

---

## Notes

* Ensure the backend server is running before you execute the agent.


Then inside your browser check this url
```bash
http://127.0.0.1:8000/api/
```

For any doubt or issue mail or call me at: 
Aneeshmishra784@gmail.com
7985720988