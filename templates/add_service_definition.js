var i=1;

$("#addAttributeButton").click(function(){
    var serial=[ {order:i} ];
    i++;
    $("#attributeTemplate").tmpl(serial).appendTo("#attributeContainer");
});

$("#addValueButton").click(function(){
    console.log("Add Value");
    $("#valueTemplate").tmpl().appendTo("#valueContainer");
});
