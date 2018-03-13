function messages(tag,message){
    $.toast({
            heading: 'Sistema GRT-Transfer',
            text: message,
            position: 'top-right',
            loaderBg:'#ff6849',
            icon: tag,
            hideAfter: 3500,
            stack: 6
          });
}
