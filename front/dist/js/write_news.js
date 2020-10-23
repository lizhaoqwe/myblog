function News() {

}

//上传图片事件
News.prototype.uploadimage = function() {
    var upload_btn = $('#upload-btn');
    upload_btn.change(function () {
        var file = upload_btn[0].files[0];
        var formData = new FormData();
        formData.append('file', file);
        xfzajax.post({
            'url': '/cms/upload/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success':function (result) {
                if (result['code']===200) {
                    var url = result['data']['url'];
                    $('#thumbnail_url').val(url);
                }
            }
        })
    })
};


//初始化ueditor
News.prototype.initUeditor = function () {
    window.ue = UE.getEditor('editor',{
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
};


//发布新闻按钮
News.prototype.publish_news = function () {
    var publish_btn = $('#publish_btn');
    publish_btn.click(function (event) {
        event.preventDefault();
        var title = $('input[name="title"]').val();
        var category = $('select[name="category"]').val();
        var desc = $('input[name="desc"]').val();
        var thumbnail = $('input[name="thumbnail"]').val();
        var content = window.ue.getContent();
        console.log(title,category,desc,thumbnail,content)
        var url = '';
        var article_id = publish_btn.attr('data-news-id');
        if (article_id) {
            url = '/cms/edit/111'
        }else {
            url = '/cms/write_articles/'
        }
        xfzajax.post({
            'url': url,
            'data': {
                'pk': article_id,
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content
            },
            'success': function (result) {

                if(result['code'] === 200) {
                    if(article_id) {
                        xfzalert.alertSuccess('修改新闻成功！',function () {
                            window.location.reload();
                        })
                    }else {
                        console.log(url);
                        xfzalert.alertSuccess('发布新闻成功！',function () {
                            window.location.reload();
                        })
                    }

                }else {
                    console.log(result.message);
                    console.log(result.code);
                }
            }
        })
    })
};
News.prototype.run = function () {
    self = this;
    self.uploadimage();
    self.initUeditor();
    self.publish_news();
};


$(function () {
    var news = new News();
    news.run();
});