// API URLs
const coursesApi = "/api/courses/";
const enrollmentsApi = "/api/enrollments/";

// Fetch courses from backend
async function fetchCourses() {
    try {
        const response = await fetch(coursesApi);
        const courses = await response.json();
        const container = document.getElementById('course-list');

        container.innerHTML = courses.map(course => `
            <div class="course-card">
                <h3>${course.title}</h3>
                <p>${course.description}</p>
                <p><strong>Duration:</strong> ${course.duration} hours</p>
                <p><strong>Fee:</strong> $${course.fee}</p>
                <p><strong>Category:</strong> ${course.category}</p>
                ${course.status !== 'Approved' ? '<span style="color:#ff9800; font-weight:600;">Pending Approval</span>' : ''}
                <div style="margin-top:10px;">
                    ${course.status === 'Approved' ? `<button class="enroll-btn" onclick="enroll(${course.id})">Enroll</button>` : ''}
                    ${course.status !== 'Approved' ? `<button class="btn-approve" onclick="approve(${course.id})">Approve</button>
                    <button class="btn-reject" onclick="reject(${course.id})">Reject</button>` : ''}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error("Error fetching courses:", error);
    }
}

// Enroll function for students
async function enroll(courseId) {
    try {
        const res = await fetch(enrollmentsApi, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ course: courseId })
        });
        if (res.ok) {
            alert("Enrolled successfully!");
        } else {
            const data = await res.json();
            alert("Error: " + JSON.stringify(data));
        }
    } catch (error) {
        console.error("Error enrolling:", error);
    }
}

// Approve course (admin)
async function approve(courseId) {
    try {
        const res = await fetch(`${coursesApi}${courseId}/approve/`, { method: 'POST' });
        if (res.ok) {
            alert("Course Approved");
            fetchCourses();
        }
    } catch (error) {
        console.error("Error approving course:", error);
    }
}

// Reject course (admin)
async function reject(courseId) {
    try {
        const res = await fetch(`${coursesApi}${courseId}/reject/`, { method: 'POST' });
        if (res.ok) {
            alert("Course Rejected");
            fetchCourses();
        }
    } catch (error) {
        console.error("Error rejecting course:", error);
    }
}

// Load courses on page load
document.addEventListener('DOMContentLoaded', fetchCourses);
