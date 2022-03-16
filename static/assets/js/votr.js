$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$(document).ready(function handleFindUserById() {
  $("#users-find-by-id-btn").click(async function (event) {
    event.preventDefault();

    let findUserByIdForm = document.getElementById("find-user-by-id-form");

    let response = await fetch("find_user_by_id", {
      method: "POST",
      body: new FormData(findUserByIdForm),
    });

    let user_data = await response.json();

    document.getElementById(
      "users-find-by-id-username"
    ).value = `${user_data.username}`;

    document.getElementById(
      "users-find-by-id-email"
    ).value = `${user_data.email_address}`;

    if (user_data.site_permissions.includes("guest")) {
      document.getElementById(
        "users-find-by-id-site-permissions-guest"
      ).checked = true;
    } else {
      document.getElementById(
        "users-find-by-id-site-permissions-guest"
      ).checked = false;
    }

    if (user_data.site_permissions.includes("user")) {
      document.getElementById(
        "users-find-by-id-site-permissions-user"
      ).checked = true;
    } else {
      document.getElementById(
        "users-find-by-id-site-permissions-user"
      ).checked = false;
    }

    if (user_data.site_permissions.includes("admin")) {
      document.getElementById(
        "users-find-by-id-site-permissions-admin"
      ).checked = true;
    } else {
      document.getElementById(
        "users-find-by-id-site-permissions-admin"
      ).checked = false;
    }

    if (user_data.site_permissions.includes("superadmin")) {
      document.getElementById(
        "users-find-by-id-site-permissions-superadmin"
      ).checked = true;
    } else {
      document.getElementById(
        "users-find-by-id-site-permissions-superadmin"
      ).checked = false;
    }
  });
});

$(document).ready(async function putAllUsersInLocalStorage(event) {
  let response = await fetch("get_all_users", {
    method: "GET",
  });

  let all_users_data = await response.json();

  console.log(all_users_data);
});
