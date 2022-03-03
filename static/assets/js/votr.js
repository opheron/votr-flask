$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$(document).ready(function () {
  console.log("workin");
  $("#find-user-by-id").submit(function (event) {
    console.log("Handler for search user by id .submit() called.");
    alert("Handler for search user by id .submit() called.");
    event.preventDefault();
  });
});
