var counter_flag=1;
$(".counter").click(function () {
    if (counter_flag===1){
        $(".counter").animate({top:"35%"},250);
        $(".search-box").animate({top:"50%"},250);
        $(".news").hide(100);
        $(".weather").hide(100);
        $(".tools").hide(100);
        $(".icons").hide(100);
        counter_flag=0;
    }
    else {
        $(".counter").animate({top:"15%"},250);
        $(".search-box").animate({top:"30%"},250);
        $(".news").show(100);
        $(".weather").show(100);
        $(".tools").show(100);
        $(".icons").show(100);
        counter_flag=1;
    }
});
