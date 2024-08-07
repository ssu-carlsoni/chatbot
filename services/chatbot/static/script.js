$(document).ready(function () {
    $('#search-form').on('submit', function (event) {
        event.preventDefault();

        $('#results').empty().append(
            '<div class="spinner-border text-primary" role="status">' +
            '  <span class="visually-hidden">Loading...</span>' +
            '</div>'
        );

        $.ajax({
            url: '/openai/invoke',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                'input': {
                    'messages': [{'role': 'user', 'content': $('#search').val()}]
                }
            }),
            dataType: 'json',
            success: function (data) {
                console.log(data)
                $('#results').empty().append(
                    '<p><strong>Bot:</strong> '
                    + data.output.content
                    + '</p>'
                );
            },
            error: function (xhr, status, error) {
                $('#results').empty().append(
                    '<p>Error: ' + error + '</p>'
                );
            }
        });
    });
});
