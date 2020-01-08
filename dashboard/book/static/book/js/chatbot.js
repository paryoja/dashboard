$("#message_form").submit(function (e) {
    e.preventDefault();
    var message = $("#message").val();
    var csrf_token = $("input[type='hidden']").val();

    $.ajax({
        type: "POST",
        url: "/book/query_chatbot/",
        data: {'message': message, 'csrfmiddlewaretoken': csrf_token},
        dataType: "json",
        success: function (response) { // 통신 성공시 - 동적으로 좋아요 갯수 변경, 유저 목록 변경

            let message_area = $("#message_area");
            message_area.append("\nYou: " + message + "\nRasa: " + response[0].text);
            message_area.css('height', message_area.height() + 62);
        },
        error: function (request, status, error) { // 통신 실패시 - 로그인 페이지 리다이렉트
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        },
    });
})
