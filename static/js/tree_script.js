// pop up
function openEditPopup(id) {
    document.getElementById('popupA'+id).style.display = 'block';
    }

function closePopupA(id) {
    document.getElementById('popupA'+id).style.display = 'none';
    }

function openAddPopup(id) {
    document.getElementById('popupE'+id).style.display = 'block';
    }

function closePopupE(id) {
    document.getElementById('popupE'+id).style.display = 'none';
    }



function confirmDelete(itemId) {
    var isConfirmed = confirm("Are you sure you want to delete this item?");

    if (isConfirmed) {
        window.location.href = "/edit/delscript/" + itemId;
    } else {
        console.log("Deletion canceled.");
    }
}


function validateRussian(input) {
    var russianRegex = /^[\u0400-\u04FF]+$/;
    if (!russianRegex.test(input.value)) {
        // Display an error message below the input
        document.getElementById('error_message').innerText = 'Please enter text in Russian.';
        // Optionally, you can add a class to style the input or error message
        input.classList.add('error-input');
    } else {
        // Clear the error message and any added classes when input is valid
        document.getElementById('error_message').innerText = '';
        input.classList.remove('error-input');
    }
}
