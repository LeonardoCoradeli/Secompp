document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('taskModal');
    const closeButton = document.querySelector('.close-button');
    const addTaskButton = document.getElementById('addTaskButton');
    const submitTaskButton = document.getElementById('submitTaskButton');
    const taskList = document.getElementById('taskList');
    const taskInput = document.getElementById('taskInput');
    const taskTitle = document.getElementById('taskTitle');

    // Open modal
    document.querySelector('.square-button').addEventListener('click', function () {
        modal.style.display = 'flex';
    });

    // Close modal
    closeButton.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // Add task to list
    addTaskButton.addEventListener('click', function () {
        const taskText = taskInput.value.trim();
        if (taskText) {
            const taskItem = document.createElement('div');
            taskItem.className = 'task-item';
            taskItem.innerHTML = `
                <span>${taskText}</span>
                <button class="delete-task-button">Del</button>
            `;
            taskList.appendChild(taskItem);
            taskInput.value = '';

            // Add delete functionality
            taskItem.querySelector('.delete-task-button').addEventListener('click', function () {
                taskList.removeChild(taskItem);
            });
        }
    });

    // Submit task
    submitTaskButton.addEventListener('click', function () {
        const tasks = [];
        taskList.querySelectorAll('.task-item').forEach(function (taskItem) {
            tasks.push({
                taskLineText: taskItem.querySelector('span').textContent,
                taskLineCheckbox: false
            });
        });
    
        const taskData = {
            taskTitle: taskTitle.value,
            taskLines: tasks
        };
    
        // Send taskData to backend
        fetch('/tarefas/add-task/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Ajuste se estiver usando Django
            },
            body: JSON.stringify(taskData)
        }).then(response => {
            if (response.ok) {
                // Handle success
                modal.style.display = 'none';
                location.reload();
                // Optionally, refresh the task list or update the UI
            } else {
                // Handle error
                console.error('Failed to submit task');
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    });

    // Utility function to get CSRF token (for Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});