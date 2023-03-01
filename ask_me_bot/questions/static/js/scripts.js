$(document).ready(function () {
    $("#addQuestionForm").submit(function (e) {
        e.preventDefault();
        let submitForm = $(this).serializeArray()
        $.ajax({
            type: "POST",
            url: "/",
            data: submitForm,
            success: function () {
                window.location.href = "/";
            },
            error: function (response) {
                alert(response.responseJSON);
            }
        });
    });
});