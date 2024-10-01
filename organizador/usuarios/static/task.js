function showTaskDetail(taskId) {
    const modal = document.getElementById('task-detail-modal');
    const taskTitle = document.getElementById('task-title');
    const taskItemsContainer = document.getElementById('task-items');

    // Limpar os itens de tarefa existentes
    taskItemsContainer.innerHTML = '';

    // Simulação de uma requisição para pegar os detalhes da tarefa via AJAX
    fetch(`/tarefas/${taskId}/json/`)
        .then(response => response.json())
        .then(data => {
            taskTitle.textContent = data.title;

            data.task_lines.forEach(line => {
                const taskItem = document.createElement('div');
                taskItem.classList.add('task-item');

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.checked = line.is_done;

                const taskText = document.createElement('input');
                taskText.type = 'text';
                taskText.value = line.text;  // Correção: usar 'text'

                taskItem.appendChild(checkbox);
                taskItem.appendChild(taskText);
                taskItemsContainer.appendChild(taskItem);
            });

            modal.classList.remove('hidden');
        });
}

function saveTaskModifications() {
    const taskId = document.querySelector('.task-square').getAttribute('data-task-id');
    const taskItems = document.querySelectorAll('.task-item');
    const updatedData = [];

    taskItems.forEach(item => {
        const checkbox = item.querySelector('input[type="checkbox"]');
        const textInput = item.querySelector('input[type="text"]');
        updatedData.push({
            is_done: checkbox.checked,
            text: textInput.value  // Correção: usar 'text'
        });
    });

    fetch(`/tarefas/${taskId}/update/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({task_lines: updatedData})
    }).then(response => {
        if (response.ok) {
            // Esconder o modal e recarregar a lista de tarefas
            document.getElementById('task-detail-modal').classList.add('hidden');
            location.reload();  // Recarregar a página para refletir as mudanças
        }
    });
}

document.getElementById('task-form').addEventListener('submit', function(e) {
    e.preventDefault();
    saveTaskModifications();
});
