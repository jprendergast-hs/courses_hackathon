from flask import Flask, render_template, jsonify, request
import json
import requests
import os
UDEMY_CLIENT_ID = os.getenv("UDEMY_CLIENT_ID")
UDEMY_CLIENT_SECRET = os.getenv("UDEMY_CLIENT_SECRET")

app = Flask(__name__)

# Load the jobs data from the JSON file
with open('jobs.json') as f:
    jobs = json.load(f)

def get_top_k_courses(skill, k=3):
    url = "https://www.udemy.com/api-2.0/courses/"
    params = {"page":1,
            "page_size":k,
            "search":skill,
            "price":"price-paid",
            "is_affiliate_agreed":True,
            "ratings": 4.5}
    with requests.Session() as s:
        s.auth = (UDEMY_CLIENT_ID, UDEMY_CLIENT_SECRET)
        s.headers.update({'Content-Type': "application/json"})
        req = requests.Request('GET',  url, params=params, headers=s.headers)
        prepped = s.prepare_request(req)
        resp = s.send(prepped)
        resp.raise_for_status()
        return json.loads(resp.content)

@app.route('/')
def index():
    return render_template('index.html')

# API route to get all job titles
@app.route('/jobs')
def get_jobs():
    # Return only the job titles and IDs
    job_titles = [{"id": job["id"], "title": job["title"]} for job in jobs]
    return jsonify(job_titles)

# API route to get a single job's details
@app.route('/jobs/<int:job_id>')
def get_job_details(job_id):
    job = next((job for job in jobs if job['id'] == str(job_id)), None)
    if job:
        if not job.get('courses'):
            courses = []
            for skill in job['skills']:
                course = get_top_k_courses(skill, 1)['results'][0]
                print(course)
                trunk_course = {k:v for k, v in course.items() if k in ["image_50x50","title","price","url"]}
                courses.append(trunk_course)
            job['courses'] = courses
        return jsonify(job)
    else:
        print(job_id)
        return jsonify({"error": "Job not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
