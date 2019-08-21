$( document ).ready(function() {
    
	console.log( "ready!" );
	
    $( '#id_has_doubt' ).on( 'click', function() {
    if( $(this).is(':checked') ){
        // Add the input for the doubt
     	$("#id_ammount_of_doubt").show();
		$("#monto").show();
    } else {
    	//Elimitar el input para introducir la deuda
    	$("#id_ammount_of_doubt").hide();
		$("#monto").hide();
		    }
    });

    $(".dropdown-trigger").dropdown();
    $('.sidenav').sidenav();
    $('input#id_idnum').characterCounter();
    $('select').formSelect();
    $('.modal').modal();
	$('#modal2').modal();
    
    $("#botonborrar").click(function(submit) {
        var $form = $('#pkform')
            $form.submit()
            
            console.log($form)


    });

    // Addning nuevas personas a la base de datos
    var $personasform = $('.addpersonas')
    $personasform.submit(function(event) {
        event.preventDefault()
        console.log("Pincha!!!!")
        $datospersona = $(this).serialize()
        console.log($datospersona)
        var $thisURL = $(this).attr('data-url') || window.location.href
        console.log($thisURL)
        $.ajax({
                method: "POST",
                url: $thisURL,
                data: $datospersona,
                success: successFunction,
                error: errorFunction,

            });

    });

    $("#closemodal").click(function() {
        location.reload();
        console.log("Pinchado el cerrar")
    });

    function successFunction(data, textStatus, jqXHR) {
        console.log(data)
        console.log(textStatus)
        console.log(jqXHR)
        $personasform[0].reset();
        M.toast({html: 'Persona añadida satisfactoriamente!!!'})
    }

    function errorFunction( jqXHR, textStatus, errorThrown) {
        //alert( "Request Failed");
        console.log(errorThrown);
        console.log(textStatus);
        console.log(jqXHR);
       // var errorparseado = JSON.parse(responseText) 
        //M.toast({ html: 'ERROR!!!! '+ errorparseado.idnum })
        
    }

    $('.tooltipped').tooltip();  

    $('.fixed-action-btn').floatingActionButton();

    $('.tap-target').tapTarget();
 

}); 




