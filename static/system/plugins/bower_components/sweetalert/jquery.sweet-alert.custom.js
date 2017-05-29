
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
    },
    //init
    $.SweetAlert = new SweetAlert, $.SweetAlert.Constructor = SweetAlert
}(window.jQuery),

//initializing 
function($) {
    "use strict";
    $.SweetAlert.init()
}(window.jQuery);