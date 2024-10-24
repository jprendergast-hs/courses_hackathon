document.addEventListener('DOMContentLoaded', function () {
    const jobList = document.getElementById('job-list');
    const jobTitle = document.getElementById('job-title');
    const jobDescription = document.getElementById('job-description');
    const courseList = document.getElementById('course-list')
    const jobDetailsList = document.getElementById('job-details')
    // Fetch all job titles
    fetch('/jobs')
        .then(response => response.json())
        .then(jobs => {
            jobs.forEach(job => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = '#';
                a.textContent = job.title;
                a.dataset.jobId = job.id;

                // Add a click event listener to fetch job details
                a.addEventListener('click', function (event) {
                    event.preventDefault();
                    const jobId = this.dataset.jobId;

                    // Fetch job details
                    fetch(`/jobs/${jobId}`)
                        .then(response => response.json())
                        .then(jobDetails => {
                            // Populate the job details section
                            jobTitle.textContent = jobDetails.title;
                            jobDescription.innerHTML = `Description: ${jobDetails.description}`;
                            courseList.replaceChildren()
                            const tempList = document.createElement('ul')
                            jobDetails.courses.forEach(course => {
                                const cli = document.createElement('li');
                                
                                // const img = document.createElement('img');
                                // img.src = "file:///Users/jprendergast/courses_hackathon/flask_app/static/udemy_icon.png";
                                // img.alt = `${course.title} icon`;
                
                                const a = document.createElement('a');
                                a.textContent = course.title;
                                a.href = `http://www.udemy.com${course.url}`
                                cli.appendChild(a);
                                tempList.appendChild(cli);
                                });
                            courseList.replaceChildren(tempList)

                        })
                        .catch(error => {
                            console.error('Error fetching job details:', error);
                        });
                });

                li.appendChild(a);
                jobList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error fetching job titles:', error);
        });
});
