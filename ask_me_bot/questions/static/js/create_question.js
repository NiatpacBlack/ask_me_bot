$(document).ready(function () {
    $("#addQuestionForm").submit(function (e) {
        e.preventDefault();
        let submitForm = $(this).serializeArray()
        $.ajax({
            type: "POST",
            url: "/question/create/",
            data: submitForm,
            success: function () {
                getAdminPanel();
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });
    });
});