console.log("hi")
$(function () {
    $('#btn_search_certificate').click(function () {
        var has = $('#form_certificate_search').hasClass("was-validated")
        if (!has) {
            $('#form_certificate_search').addClass("was-validated")
        }
    });
});
