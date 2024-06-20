window.onload = function() {
    let div = document.querySelector('.chat-container');
    div.scrollTop = div.scrollHeight;
};

document.addEventListener("DOMContentLoaded", function() {
    const offcanvas = document.getElementById('offcanvasScrolling');
    const mainContent = document.getElementById('main-content');
    const navbar = document.getElementById('navbar');
    const promptDiv = document.getElementById('prompt-div');
    // const markdownText = document.getElementById('response-bot').textContent;
    // const htmlText = marked(markdownText);

    offcanvas.addEventListener('show.bs.offcanvas', function () {
        mainContent.classList.add('offcanvas-open');
        navbar.classList.remove('fixed-top');
        promptDiv.classList.add('ms-5');
        // document.getElementById("response-bot").innerHTML = htmlText;
    });

    offcanvas.addEventListener('hide.bs.offcanvas', function () {
        mainContent.classList.remove('offcanvas-open');
        navbar.classList.add('fixed-top');
        promptDiv.classList.remove('ms-5');
    });
});

$('.rename-thread').click(function(e) {
    e.preventDefault();
    var threadId = $(this).data('thread-id');
    const buttonThreadId = document.getElementById('thread-name-' + threadId);
    buttonThreadId.classList.remove('text-truncate');
    $('#thread-name-' + threadId).prop('contenteditable', true).focus();
});

// Cuando se presiona enter, enviar una solicitud POST a rename_thread_route con el nuevo nombre
$('.thread-name').keypress(function(e) {
    if (e.which == 13) {  // Enter key
        e.preventDefault();
        $(this).prop('contenteditable', false);
        var newName = $(this).text();
        var threadId = $(this).attr('id').split('-')[2];
        const buttonThreadId = document.getElementById('thread-name-' + threadId);

        // Realiza una solicitud a tu API para cambiar el nombre del hilo
        fetch(`/threads/${threadId}/rename`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ new_name: newName }),
        })
        .then(response => response.json())
        .then(data => {
            // Actualiza el nombre del hilo en la interfaz de usuario
            document.getElementById(`thread-name-${threadId}`).textContent = newName;
            buttonThreadId.classList.add('text-truncate');
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});