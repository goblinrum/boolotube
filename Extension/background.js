chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {

    if (request.action === 'openUrl') {
        var project = request.project;

        fetch('http://localhost:8000/project/' + project, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            // Now, fetch the timestamps
            return fetch('http://localhost:8000/timestamps/' + data.project_id, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            .then(response => response.json())
            .then(timestampData => {
                // Add the fetched timestamps to the response data
                data.timestamps = timestampData.result;
                sendResponse({ message: 'URLs sent successfully', data: data });
            });
        })
        .catch(error => {
            sendResponse({ message: 'Error sending URLs', error: error });
        });

        return true;
    }
});
