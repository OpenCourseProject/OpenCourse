$(function() {
  if (authenticated == 'True') {
    $('button[name="schedule-button"]').each(function(i, obj) {
      var button = $(this)
      var course = button.attr('data-course-crn');
      $.get('/schedule/has/', {term: term, course: course}, function(data) {
        state = $.trim(data);
        update_schedule_button(button, state);
      });
    });
    $('button[name="follow-button"]').each(function(i, obj) {
      var button = $(this)
      var course = button.attr('data-course-crn')
      $.get('/follow/has/', {term: term, course: course}, function(data) {
        state = $.trim(data);
        update_follow_button(button, state);
      });
    });
  }
});
$('button[name="schedule-button"]').click(function() {
  var button = $(this)
  var course = button.attr('data-course-crn')
  var state = button.attr('data-schedule-state')
  if (state == '0') {
    $.get('/schedule/add/', {term: term, course: course}, function(data) {
      update_schedule_button(button, '1');
    });
  } else {
    $.get('/schedule/remove/', {term: term, course: course}, function(data) {
      update_schedule_button(button, '0');
    });
  }
});
$('button[name="follow-button"]').click(function() {
  var button = $(this)
  var course = button.attr('data-course-crn')
  var state = button.attr('data-follow-state')
  if (state == '0') {
    $.get('/follow/add/', {term: term, course: course}, function(data) {
      update_follow_button(button, '1');
    });
  } else {
    $.get('/follow/remove/', {term: term, course: course}, function(data) {
      update_follow_button(button, '0');
    });
  }
});

function update_schedule_button(button, state) {
  button.attr('data-schedule-state', state)
  button.removeClass("btn-default");
  if (state == '0') {
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
  if (state == '0') {
    button.html('<span class="glyphicon glyphicon-flag" aria-hidden="true"></span> Get Updates');
    button.removeClass("btn-danger");
    button.addClass("btn-success");
  } else {
    button.html('<span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Stop Updates');
    button.removeClass("btn-success");
    button.addClass("btn-danger");
  }
}
