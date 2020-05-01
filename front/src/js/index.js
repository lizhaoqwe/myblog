function Index() {
    var self = this;
    self.page = 2;
    self.articleGroup = $('.articles-wrapper');
    self.category_id = 0;
}
//监听点击header菜单事件
Index.prototype.clickHeaderMenuEvent = function () {
    $('.category-header .header-menu li').click(function () {
        $(this).css("border-bottom", "5px solid #5c87d9").siblings().css('border-bottom','');
    });
};

//监听点击查看更多事件
Index.prototype.clickmore = function() {
    var self = this;
    $('.more').click(function () {
        xfzajax.get({
            'url': '/articles/article_list/',
            'data': {
                'p': self.page,
                'category_id': self.category_id
            },
            'success': function (result) {
                if (result['code']===200){
                    var articles = result['data'];
                    if (articles.length>0) {
                        var tpl = template("article-item",{"articles":articles});
                        self.articleGroup.append(tpl);
                        self.page += 1
                    }else {
                        $('.more').hide();
                    }
                }else {
                    console.log(result['code'])
                }
            }

        });
    })
};



//监听点击分类事件
Index.prototype.clickcategory = function () {
    var self = this;
    $('.header-menu li').click(function () {
        var li = $(this);
        var category_id = li.attr('data-category');
        console.log(category_id);
        var page = 1;
        xfzajax.get({
            'url': '/articles/article_list/',
            'data':{
                'category_id': category_id,
                'p': page,
            },
            'success': function (result) {
                if (result['code']===200) {
                    var articles = result['data'];
                    var tpl = template("article-item",{"articles":articles});
                    self.articleGroup.empty();
                    self.articleGroup.append(tpl);
                    self.page = 2;
                    self.category_id = category_id;
                    $('.more').show();
                }
            }
        })
    })

};


Index.prototype.run = function () {
    var self = this;
    self.clickmore();
    self.clickcategory();
    self.clickHeaderMenuEvent();

};


$(function () {
    var index = new Index();
    index.run()
});