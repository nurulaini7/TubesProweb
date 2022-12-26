$(document).ready(function () {
    // Selector input yang akan menampilkan autocomplete.
    $("#automplete-2").autocomplete({
        source: "../../includes/autocomplete.php",
        minLength: 2
    });
})