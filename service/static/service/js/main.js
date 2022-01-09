function CreateProject() {
    const name = $('#name').val();
	const name2 = document.getElementById('name').value
	console.log(name2)
	$.ajax({
		url:    	'add_project',
		method:		'POST',
		cache: 		false,
		data:   	JSON.stringify({'name': name2}),
		contentType: 'application/json; charset=utf-8',
        dataType:	'html',
		success: function(data) {
			$('body').html(data);
		}
	});
}

