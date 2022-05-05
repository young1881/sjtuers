function openSiteDialog(){
    document.getElementById('add_site').style.display='block';
}
function closeSiteDialog(){
    document.getElementById('add_site').style.display='none';
}

function openCountdownDialog(){
    document.getElementById('countdown_dialog').style.display='block';
}
function closeCountdownDialog(){
    document.getElementById('countdown_dialog').style.display='none';
}


var layer=document.createElement("div");
layer.id="layer";
function noPermissions(date){
    var style={
        background:"RGB(92,92,92,0.9)",
        color:"#fff",
        position:"absolute",
        zIndex:"1000",
        width:"500px",
        height:"40px",
        left:"30%",
        top:"45%",
        borderRadius:"20px",
    }
    for(var i in style)
        layer.style[i]=style[i];

    // 当找不到id为layer的控件时
    if(document.getElementById("layer")==null){
        // 在body中添加layer控件（layer在上面创建的）
        document.body.appendChild(layer);
        layer.innerHTML=date;
        layer.style.textAlign="center";
        layer.style.lineHeight="40px";
        layer.style.letterSpacing="5px";
        layer.style.fontWeight="border";
        layer.style.fontSize="19px";
        setTimeout("document.body.removeChild(layer)",2000)
    }
}


