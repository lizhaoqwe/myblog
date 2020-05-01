function Auth() {

}

Auth.prototype.loginAuth = function () {
    $('.loginBtn').click(function (event) {
        event.preventDefault();
        var telephone = $('input[name="telephone"]').val();
        var password = $('input[name="password"]').val();
        var remember = $('input[name="remember"]').prop('checked');
        xfzajax.post({
            url: '/auth/login/',
            data: {
                telephone: telephone,
                password: password,
                remember: remember,
            },
            success: function (result) {
                if (result.code === 200) {
                    window.location.href = '/cms/index/'
                }else {
                    messageBox.showError('用户名或者密码错误')
                    console.log(result.message)
                }
            }
        })
    });

};

Auth.prototype.run = function () {
    var self = this;
    self.loginAuth();
};


$(function () {
    var auth = new Auth();
    auth.run();
});