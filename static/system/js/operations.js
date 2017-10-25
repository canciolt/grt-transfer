jQuery(document).ready(function () {
    if (moneda == "MX") {
        $('#id_costo_usd').prop('disabled', true);
    } else if (moneda == "USD") {
        $('#id_costo_mx').prop('disabled', true);
    }
    $('#sello-button').click(function () {
        ajaxPost('/ajax/operacion/change_sello/', $("#sello-form").serialize(), function (data) {
            if (data == 1) {
                $('#responsive-modal').modal('hide')
                location.reload()
            } else {
                $('#modal-body-sello').html('');
                $('#modal-body-sello').html(data);
            }
        })
    });
    $('#evento-button').click(function () {
        ajaxPost('/ajax/operacion/evento_add/', $("#evento-form").serialize(), function (data) {
            if (data == 1) {
                $('#responsive-modal').modal('hide')
                location.reload()
            } else {
                $('#modal-body-evento').html('');
                $('#modal-body-evento').append(data);
            }
        })
    });
    $('#concepto-button').click(function () {
        ajaxPost('/ajax/operacion/concepto_add/', $("#concepto-form").serialize(), function (data) {
            if (data == 1) {
                $('#responsive-modal').modal('hide')
                location.reload()
            } else {
                $('#modal-body-concepto').html('');
                $('#modal-body-concepto').append(data);
                if (moneda == "MX") {
                    $('#id_costo_usd').prop('disabled', true);
                } else if (moneda == "USD") {
                    $('#id_costo_mx').prop('disabled', true);
                }
            }
        })
    });

});

function DataTime(id) {
    $("#" + id).datetimepicker({
        language: 'es',
        weekStart: 1,
        todayBtn: 1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        forceParse: 0,
        showMeridian: 2
    });
}

function evento_select(option) {
    $("#evento-form input").each(function () {
        if ($(this).attr('name') != 'operacion') {
            $(this).val("")
        }
    });
    if (option == "AMXR" || option == "AUSR") {
        $('#div-anden').show();
        $('#div-vista').show();
        $('#div-fecha_terminacion').hide();
        $('#div-recibio').hide();
        $('#div-fecha_inicio').show();
    } else if (option == "FIN") {
        $('#div-fecha_inicio').hide();
        $('#div-anden').hide();
        $('#div-vista').hide();
        $('#div-recibio').show();
        $('#div-fecha_terminacion').show();
    } else if (option == "") {
        $('#div-recibio').hide();
        $('#div-anden').hide();
        $('#div-vista').hide();
        $('#div-fecha_terminacion').hide();
        $('#div-fecha_inicio').hide();
    } else {
        $('#div-recibio').hide();
        $('#div-anden').hide();
        $('#div-vista').hide();
        $('#div-fecha_terminacion').hide();
        $('#div-fecha_inicio').show();
    }
}