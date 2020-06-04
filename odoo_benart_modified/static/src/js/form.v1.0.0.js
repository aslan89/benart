var recaptcha_success_callback = function () {
  event.preventDefault();
   $('#btn_search_certificate').prop("disabled", false);
};
var recaptcha_expired_callback = function () {
   $('#btn_search_certificate').prop("disabled", true);
};
$(function () {
    $('#btn_search_certificate').click(function () {
        var has = $('#form_certificate_search').hasClass("was-validated")
        if (!has) {
            $('#form_certificate_search').addClass("was-validated")
        }
    });


});


