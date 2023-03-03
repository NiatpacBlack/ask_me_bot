function success_notification(message) {
    $.bootstrapGrowl(message, {
            type: "success",
            ele: "body",
            offset: {
                from: "top",
                amount: 20
            },
            align: "right",
            width: 400,
            delay: 4000,
            allow_dismiss: true,
            stackup_spacing: 10
        }
    );
}

function error_notification(data) {
    let message = data?.["error_message"] ? "Something went wrong!" : data["error_message"];

    $.bootstrapGrowl(message, {
            type: "danger", // info, success, warning and danger
            ele: "body", // parent container
            offset: {
                from: "top",
                amount: 20
            },
            align: "right", // right, left or center
            width: 400,
            delay: 4000,
            allow_dismiss: true,
            stackup_spacing: 10
        }
    );
}


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

    $("#pushToDatabaseButton").submit(function (e) {
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