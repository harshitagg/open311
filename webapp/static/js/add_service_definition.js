var i=1;
var serviceAttributeJSONObject = {"attribute":[]};

$(document).ready(function(){
    $("form").submit(function(e){
	console.log("entered");
	var data = {};
	var attributes = [];
	var counter = 1;
	var innerCounter;
	$('form').find('#attribute').each(function(){
	    console.log("in loop");
	    var attribute = {};
	    var values = [];
	    attribute['order'] = $('form').find('#order'+counter).val();
	    attribute['variable'] = $('form').find('#variable'+counter).val();
	    attribute['attr_code'] = $('form').find('#attr_code'+counter).val();
	    attribute['datatype'] = $('form').find('#datatype'+counter).val();
	    attribute['required'] = $('form').find('#required'+counter).val();
	    innerCounter = 1;
	    $(this).find('#values').each(function(){
		console.log('innerLoop');
		var value = {};
		value['key'] = $(this).find("#key").val();
		value['name'] = $(this).find("#name").val();
		values[innerCounter-1] = value;
		innerCounter++;
	    });
	    attribute['values'] = values;
	    attributes[counter-1] = (attribute);
	    counter+=1;
	});
	data['attributes'] = attributes;
	console.log(data);
	$.post(document.URL, data);
    });
    $('#addAttributeButton').click(function(){
        var serial = [ {order:i} ];
        i++;
        var htmlElement = $("#attributeTemplate").tmpl(serial);
        htmlElement.appendTo("#attributeContainer");
        $(htmlElement).find('.addValueButton').click(function(){
            $("#valueTemplate").tmpl().appendTo(htmlElement.find(".valueContainer"));
        });
    });
});
