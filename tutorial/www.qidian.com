<!DOCTYPE html><html><head><meta charset="UTF-8"><title>起点中文网_阅文集团旗下网站</title><meta name="keywords" content="小说,小说网,玄幻小说,武侠小说,都市小说,历史小说,网络小说,言情小说,青春小说,原创网络文学"><meta name="description" content="小说阅读,精彩小说尽在起点中文网. 起点中文网提供玄幻小说,武侠小说,原创小说,网游小说,都市小说,言情小说,青春小说,历史小说,军事小说,网游小说,科幻小说,恐怖小说,首发小说,最新章节免费"><meta name="robots" content="all"><meta name="googlebot" content="all"><meta name="baiduspider" content="all"><meta name="updatetime" content="2018-11-12,15:18:41"><meta http-equiv="mobile-agent" content="format=wml; url=https://m.qidian.com"><meta http-equiv="mobile-agent" content="format=xhtml; url=https://m.qidian.com"><meta http-equiv="mobile-agent" content="format=html5; url=http://h5.qidian.com/bookstore.html"><meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1"><meta name="renderer" content="webkit"><meta name="baidu-site-verification" content="d4rhkT9Dh0"><script>document.domain = 'qidian.com';</script><script>function getCookie(name) {
    LBF.config({"paths":{"site":"//qidian.gtimg.com/qd/js","qd":"//qidian.gtimg.com/qd","common":"//qidian.gtimg.com/common/1.0.0"},"vars":{"theme":"//qidian.gtimg.com/qd/css"},"combo":true,"debug":false});
    LBF.use(['lib.jQuery'], function ($) {
        window.$ = $;
    });</script><script>LBF.use(['monitor.SpeedReport', 'qd/js/component/login.a4de6.js', 'qd/js/index/index.51de2.js' ], function (SpeedReport, Login, Index) {
        // 页面逻辑入口
        if(Login){
            Login.init().always(function(){
                Index && typeof Index === 'function' && new Index();
            })
        }
        if(219 && 219 != ''){
            $(window).on('load.speedReport', function () {
                // speedTimer[onload]
                speedTimer.push(new Date().getTime());
                var f1 = 7718, // china reading limited's ID
                        f2 = 219, // site ID
                        f3 = 4; // page ID
                // chrome & IE9 Performance API
                SpeedReport.reportPerformance({
                    flag1: f1,
                    flag2: f2,
                    flag3IE: f3,
                    flag3Chrome: f3,
                    rate:0.1,
                    url: '//isdspeed.qidian.com/cgi-bin/r.cgi'
                });
                // common speedTimer:['dom ready', 'onload']
                var speedReport = SpeedReport.create({
                    flag1: f1,
                    flag2: f2,
                    flag3: f3,
                    start: speedZero,
                    rate:0.1,
                    url: '//isdspeed.qidian.com/cgi-bin/r.cgi'
                });
                // chrome & IE9 Performance API range 1~19, common speedTimer use 20+
                for (var i = 0; i < speedTimer.length; i++) {
                    speedReport.add(speedTimer[i], i + 20)
                }
                // http://isdspeed.qq.com/cgi-bin/r.cgi?flag1=7718&flag2=224&flag3=1&1=38&2=38&…
                speedReport.send();
            })
        }
    });
    speedTimer.push(new Date().getTime());</script><script>var _mtac = {};
    (function() {
        var mta = document.createElement("script");
        mta.src = "//pingjs.qq.com/h5/stats.js?v2.0.2";
        mta.setAttribute("name", "MTAH5");
        mta.setAttribute("sid", "500451537");
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(mta, s);
    })();</script></body></html>