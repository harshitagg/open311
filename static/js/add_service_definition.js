var i=1;


$(document).ready(function(){
    $('#addAttributeButton').click(function(){
        var serial=[ {order:i} ];
        i++;
        var htmlElement = $("#attributeTemplate").tmpl(serial);
        htmlElement.appendTo("#attributeContainer");
        console.log(htmlElement);
        $(htmlElement).find('.addValueButton').click(function(){
            $("#valueTemplate").tmpl().appendTo(htmlElement.find(".valueContainer"));
        });
    });
});
