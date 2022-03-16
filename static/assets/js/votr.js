$(document).ready(() => {
  window.$ = $;
  window.jQuery = jQuery;
});

$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$(document).ready(() => {
  var options = {
    valueNames: ["user_id", "username", "email_address"],
  };
  var userList = new List("users", options);
});
