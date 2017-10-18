
!function($) {
    "use strict";
    var SweetAlert = function() {};
    //examples
    SweetAlert.prototype.init = function() {
    $('#close-session').click(function(){
        swal({   
            title: "Esta seguro ?",
            text: "Pulse cerrar para salir de la sesión",
            type: "warning",   
            showCancelButton: true,   
            confirmButtonColor: "#DD6B55",   
            confirmButtonText: "Cerrar",
            cancelButtonText:"Cancelar",
            closeOnConfirm: false 
        }, function(){
            ajaxPost('/logout/',{}, function(content){});
        });
    });
     $('#activebtn').click(function(){
         var opid = $( this ).attr('opid')
         swal({
            title: "Activar Operación",
            text: "Pulse activar para iniciar operación",
            type: "success",
            showCancelButton: true,
            confirmButtonColor: "#00c292",
            confirmButtonText: "Activar",
            cancelButtonText:"Cancelar",
            closeOnConfirm: false
        }, function(){
             ajaxPost('/ajax/operacion/startop/',{operacion:opid}, function(content){location.reload();});

        });
    });
    },
    //init
    $.SweetAlert = new SweetAlert, $.SweetAlert.Constructor = SweetAlert
}(window.jQuery),

//initializing 
function($) {
    "use strict";
    $.SweetAlert.init()
    $('#tasa-cambio').click(function(){
        ajaxPost('/ajax/system/get_tasa_cambio/', function(content){
            $('div.mail-contnet h5').html("1 USD = "+content['tasa']+" MNX")
            $('div.mail-contnet span.time').html(content['fecha'])
        });
    });
}(window.jQuery);