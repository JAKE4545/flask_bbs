
$(function () {
    $("#get_captcha").click(function (event) {
        event.preventDefault();     // 阻止默认行为
        let email = $("#emailaddr").val();
        if (!email){
            $("#captchatip").css({"display":""});
            $("#captchatip").text('请输入邮箱地址!');
            return false;
        }
        $.ajax({
            'url': '/cms/email_captcha/',
            'type': "GET",
            'data': {
                'email': email
            },
            'success': function (data) {
                if (data["code"] == 200) {
                    alert("邮件已发送！请注意查收");
                } else {
                    alert(data["message"]);
                }
            },
            'fail': function (error) {
                alert("网络错误");
            }
        })
    })
});

$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var csrftoken = $('input[name="csrf_token"]').val();
        
        var emailE = $("input[name='email']");
        var captcheE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captcheE.val();
        if (!captcha) {
            $("#emailtip").css({"display": ""});
            $("#emailtip").text('请输入验证码!');
            return false;
        }
        
        $.ajax({
            'url': '/cms/setemail/',
            'type': 'post',
            'data': {
                'email': email,
                'captcha': captcha,
                'csrf_token': csrftoken
            },

            'success': function (data) {
                if (data["code"] == 200) {
                    emailE.val("");
                    captcheE.val("");
                    alert("修改成功");
                }else {
                    alert(data["message"]);
                }
            },
            'fail': function (error) {
                alert("网络错误");
            }
        })
    })
})