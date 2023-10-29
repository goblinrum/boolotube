document.addEventListener('DOMContentLoaded', function() {
  var submitButton = document.getElementById('submit');

  submitButton.addEventListener('click', function() {
    var project = document.getElementById('project').value;
    chrome.runtime.sendMessage({project: project, action: 'openUrl'}, function(response) {
      chrome.windows.create({
          url: response.data.original_video_url,
          type: 'popup', width: 400, height: 400,
      });
    });

  });
});
