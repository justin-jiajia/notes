$(function () {
    mdui.mutation();
    const flash_alert = $('.message');
    const flash_alert2 = $('.error-alert')
    flash_alert.hide().slideDown(250)
    flash_alert2.hide().slideDown(250)
    setTimeout(function () {
        flash_alert.slideUp(1000);
        flash_alert2.slideUp(1000)
    }, 3000)
})