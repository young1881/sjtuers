$(function () {
    // 初始化
    var counter_flag=0;
    $("#author").hide();

    // 诗词悬停
    $("#sentence").hover(function () {
        $("#author").slideToggle(500);
    });

  // 简洁模式
  $(".counter").click(function () {
    if (counter_flag===1){
        $(".counter").animate({top:"35%"},250);
        $(".search-box").animate({top:"45%"},250);
        $(".news").hide(200);
        $(".weather").hide(200);
        $(".tools").hide(200);
        $(".icons").hide(200);
        counter_flag=0;
    }
    else {
        $(".counter").animate({top:"15%"},250);
        $(".search-box").animate({top:"25%"},250);
        $(".news").show(200);
        $(".weather").show(200);
        $(".tools").show(200);
        $(".icons").show(200);
        counter_flag=1;
    }
});
});
