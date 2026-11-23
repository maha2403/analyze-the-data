
// DataInsight Dashboard Interactions

document.addEventListener("DOMContentLoaded", function () {

    // Sidebar navigation

    const menuItems = document.querySelectorAll(".menu-item");

    menuItems.forEach(function (item) {

        item.addEventListener("click", function () {

            menuItems.forEach(function (menu) {
                menu.classList.remove("active");
            });

            this.classList.add("active");

        });

    });


    // Upload box animation

    const uploadBox = document.getElementById("dropArea");

    if (uploadBox) {

        uploadBox.addEventListener("mouseenter", function () {
            this.style.transition = "0.3s";
        });

    }


    // Table row highlighting

    const tableRows = document.querySelectorAll("tbody tr");

    tableRows.forEach(function (row) {

        row.addEventListener("mouseenter", function () {
            this.style.transition = "0.2s";
        });

    });


    // Console message

    console.log("DataInsight Dashboard Loaded Successfully!");

});
