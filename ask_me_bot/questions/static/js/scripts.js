function success_notification(message) {
    setTimeout($.bootstrapGrowl(message, {
            type: "success",
            ele: "body",
            align: "left",
            width: 300,
            allow_dismiss: false,
            stackup_spacing: 3
        }
    ), 2000);
}

function error_notification(data) {
    let error_message = data?.["error"] ? data["error"] : "Something went wrong!";

    setTimeout($.bootstrapGrowl(error_message, {
            type: "danger", // info, success, warning and danger
            ele: "body", // parent container
            align: "left", // right, left or center
            width: 300,
            allow_dismiss: false,
            stackup_spacing: 3
        }
    ), 2000);
}


$(document).ready(function () {

    let questionTable = $('#questionsTable').DataTable();

    questionTable.on('click', 'tbody tr', function () {
        let question_id = $(this).attr('question-id');
        $.ajax({
            type: "GET",
            url: `/question/${question_id}/`,
            success: function () {
                window.location.href = `/question/${question_id}/`;
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });

    });

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
                error_notification(response.responseJSON);
            }
        });
    });

    $("#pushToDatabaseButton").on('click', function (e) {
        $.ajax({
            type: "GET",
            url: "/push/",
            success: function () {
                success_notification("Data successfully added to the database");
            },
            error: function (response) {
                error_notification(response.responseJSON);
            }
        });
    });

});