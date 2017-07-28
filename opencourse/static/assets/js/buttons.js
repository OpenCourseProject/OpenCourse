$(document).ready(function() {
  var API_PARAM = '?username=' + api_username + '&api_key=' + api_key;
  $('button[name="schedule-button"]').each(function(i, obj) {
    var button = $(this);
    var term = button.data('term-id');
    var course = button.data('course-crn');
    var params = {
      'username': api_username,
      'api_key': api_key,
      'term__value': term,
      'course_crn': course,
      'format': 'json',
    }
    $.get('/api/v1/schedule/', params, function(data) {
      state = data.meta.total_count;
      update_schedule_button(button, state);
    });
  });
  $('button[name="follow-button"]').each(function(i, obj) {
    var button = $(this);
    var term = button.attr('data-term-id');
    var course = button.attr('data-course-crn');
    var params = {
      'username': api_username,
      'api_key': api_key,
      'term__value': term,
      'course_crn': course,
      'format': 'json',
    }
    $.get('/api/v1/follow/', params, function(data) {
      state = data.meta.total_count;
      update_follow_button(button, state);
    });
  });

  $('button[name="schedule-button"]').click(function() {
    var button = $(this);
    var term = button.attr('data-term-id');
    var course = button.attr('data-course-crn');
    var state = button.attr('data-schedule-state');
    if (state == '0') {
      var headers = {
        'Authorization': 'ApiKey ' + api_username + ':' + api_key,
      }
      var data = {
        'term': '/api/v1/term/' + term + '/',
        'course_crn': course,
      }
      $.ajax({
        url: '/api/v1/schedule/' + API_PARAM,
        type: 'POST',
        data: JSON.stringify(data),
        headers: headers,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        processData: false,
        success: function (data, status, jqXHR) {
          update_schedule_button(button, 1);
        },
        error: function (jqXHR, status, error) {
          update_schedule_button(button, 1);
        }
      });
    } else {
      var params = {
        'username': api_username,
        'api_key': api_key,
        'term__value': term,
        'course_crn': course,
        'format': 'json',
      }
      $.get('/api/v1/schedule/', params, function(data) {
        uri = data.objects[0].resource_uri + API_PARAM;
        headers = {
          'Authorization': 'ApiKey ' + api_username + ':' + api_key,
        }
        $.ajax({
          url: uri,
          type: 'DELETE',
          headers: headers,
          success: function(data) {
            update_schedule_button(button, 0);
          }
        });
      });
    }
  });

  $('button[name="follow-button"]').click(function() {
    var button = $(this);
    var term = button.attr('data-term-id');
    var course = button.attr('data-course-crn');
    var state = button.attr('data-follow-state');
    if (state == '0') {
      var headers = {
        'Authorization': 'ApiKey ' + api_username + ':' + api_key,
      }
      var data = {
        'term': '/api/v1/term/' + term + '/',
        'course_crn': course,
      }
      $.ajax({
        url: '/api/v1/follow/' + API_PARAM,
        type: 'POST',
        data: JSON.stringify(data),
        headers: headers,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        processData: false,
        success: function (data, status, jqXHR) {
          update_follow_button(button, 1);
        },
        error: function (jqXHR, status, error) {
          update_follow_button(button, 1);
        }
      });
    } else {
      var params = {
        'username': api_username,
        'api_key': api_key,
        'term__value': term,
        'course_crn': course,
        'format': 'json',
      }
      $.get('/api/v1/follow/', params, function(data) {
        uri = data.objects[0].resource_uri + API_PARAM;
        headers = {
          'Authorization': 'ApiKey ' + api_username + ':' + api_key,
        }
        $.ajax({
          url: uri,
          type: 'DELETE',
          headers: headers,
          success: function(data) {
            update_follow_button(button, 0);
          }
        });
      });
    }
  });
});

function update_schedule_button(button, state) {
  button.attr('data-schedule-state', state)
  button.removeClass("btn-default");
  if (state == 0) {
    button.html('<span class="glyphicon glyphicon-ok" aria-hidden="true"></span> Add to Schedule');
    button.removeClass("btn-danger");
    button.addClass("btn-success");
  } else {
    button.html('<span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Remove from Schedule');
    button.removeClass("btn-success");
    button.addClass("btn-danger");
  }
}

function update_follow_button(button, state) {
  button.attr('data-follow-state', state)
  button.removeClass("btn-default");
  if (state == 0) {
    button.html('<span class="glyphicon glyphicon-flag" aria-hidden="true"></span> Get Updates');
    button.removeClass("btn-danger");
    button.addClass("btn-success");
  } else {
    button.html('<span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Stop Updates');
    button.removeClass("btn-success");
    button.addClass("btn-danger");
  }
}
