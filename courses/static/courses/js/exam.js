var index_question = 1;
var previous = "";
var index_input = 1;
var flag = true;

function add_question(question_row){
	if(question_row && flag){
		flag = false;
		index_question = parseInt($("#question_row").val()) + 1 ;
	}
	var div = "<div id='question"+ index_question +"' class='row question' >"+
				"<input type='text' class='form-control mt-2 col-11' placeholder='Agrega tu pregunta'/>"+
				"<button class='btn btn-danger' onclick='remove_element(\"question"+index_question+"\");'><span class='fa fa-trash'></span></button>"+
				"<select class='form-control col-4' id='option"+index_question+"' onchange='add_answers("+index_question+", true);'>"+
				"<option value='null'>Tipo de pregunta</option>"+
				"<option value='closed'>Seleccion multiple</option>"+
				"<option value='open'>Pregunta abierta</option></select>"

	$("#list_questions").append(div);
	var div_ans = "<div class='col-12 mt-3' id='answers"+index_question+
	"'></div><button style='display:none;' class='btn btn btn-outline-primary mr-2' id='add_answer"+index_question+
	"' onclick='add_answers("+index_question+", false)'>Agregar respuesta</button><button id='btn_select"+
	index_question+"' style='display:none;' class='btn btn btn-outline-primary' onclick='enable_checkbox("+index_question+")'>Selecciona respuesta</button>"+
	"<button id='btn_edit"+
	index_question+"' style='display:none;' class='btn btn btn-outline-primary' onclick='edit_answers("+index_question+")'>Editar pregunta</button>";

	$("#question"+index_question).append(div_ans);
	index_question ++;
}

function add_answers(index, clear, input_row){
	var option = $("#option"+index).val();
	
	if(clear){
		$("#answers"+index).empty();
	}

	if(input_row){
		index_input = input_row+1;
	}
	
	previous = option;

	switch(option){
		case 'closed':
			var input = "<div class='row mb-3' id='answer"+index_input+"'><input type='checkbox' id='checkbox"+index_input+"' class='checkbox"+index+" col-md-1' disabled='True' onchange='check_correct("+index_input+", "+index_question+")' />"+
				"<input class='form-control col-md-10' data-is_correct='False' id='input"+index_input+"' type='text'  placeholder='Respuesta'/>"+
				"<button class='btn btn-danger' onclick='remove_element(\"answer"+index_input+"\");'><span class='fa fa-remove'></span></button>"+
				"</div>";
			$("#answers"+index).prepend(input);

			$("#add_answer"+index).css("display", "block");
			$("#btn_select"+index).css("display", "block");
			break;
		case 'open':
			var text = "<textarea class='form-control' data-is_correct='True'></textarea>";
			$("#answers"+index).prepend(text);
			$("#add_answer"+index).css("display", "none");
			$("#btn_select"+index).css("display", "none");
			break;
	}
	index_input++;

}

function check_correct(index_input){
	var is_checked = $("#input"+index_input).attr("data-is_correct");
	if(is_checked == "False"){
		$("#input"+index_input).attr("data-is_correct", "True");
	}else{
		$("#input"+index_input).attr("data-is_correct", "False");
	}
}

function enable_checkbox(id){
	$("#add_answer"+id).css("display", "none");
	$("#btn_select"+id).css("display", "none");
	$("#btn_edit"+id).css("display", "block");
	$(".checkbox"+id).prop( "disabled", false );
	$("#option"+id).css("display", "none");
}


function edit_answers(id){
	$("#option"+id).css("display", "block");
	$("#add_answer"+id).css("display", "block");
	$("#btn_select"+id).css("display", "block");
	$("#btn_edit"+id).css("display", "none");
	$(".checkbox"+id).prop( "disabled", true );
}

function remove_element(id){
	$("#"+id).remove();
}

function send_data(){
	var exam = [];
	var unity_id = $("#unity_id").val();
	exam.push({
		'tittle': $("#title_exam").val(),
		'date' : $("#date_exam").val(),
		'unity_id': unity_id,
	});
	var questions = [];
	$(".question").each(function(){
		var data = $(this).children();
		console.log(data);
		var children_answers = data[3].children;
		var answers = [];
		var type = data[2].value;
		console.log("type", type);
		for(i=0; i<= children_answers.length-1; i++){

			if(children_answers[i].children.length> 0){
				answers.push({
					"answer": children_answers[i].children[1].value,
					"is_correct": children_answers[i].children[1].dataset.is_correct
				});
			}else{
				answers.push({
					"answer": children_answers[i].value,
					"is_correct": "True"
				});
			}
		}
		console.log("-----", answers);
		questions.push({"question": data[0].value, "answers" : answers, "type": type});
	});
	exam.push(questions);
	console.log("exam", exam);
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
				// Only send the token to relative URLs i.e. locally.
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		}
	});
	
	$.ajax({
		type: 'POST',
		dataType: 'json',
		contentType: 'application/json; charset=utf-8',
		url: '../save_exam/',
		data: JSON.stringify(exam),
		beforeSend: function(xhr, settings) {
			console.log("Before Send");
			$.ajaxSettings.beforeSend(xhr, settings);
		},
		success: function(result) {
			console.log(result);
		}
	});

}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



/*     delete courses and unities         */

function delete_course(id_course){
	$.confirm({
        title: 'Eliminar curso!',
        content: '¿Desea eliminar este curso?',
        type: 'red',
        typeAnimated: true,
        buttons: {
            accept: {
                text: 'Aceptar',
                btnClass: 'btn-red',
                action: function(){
					document.forms['form_delete'+id_course].submit();
                }
            },
            cancelar: function () {
            }
        }
    });
	
}
/*
function delete_unity(id_unity){
	$.confirm({
        title: 'Eliminar curso!',
        content: '¿Desea eliminar está unidad?',
        type: 'red',
        typeAnimated: true,
        buttons: {
            accept: {
                text: 'Aceptar',
                btnClass: 'btn-red',
                action: function(){
					document.forms['form_delete'+id_unity].submit();
                }
            },
            cancelar: function () {
            }
        }
    });
	
}*/