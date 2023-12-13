$('.validate-file').change(function(){
   
    if (this.files[0].size > 3145728 ){

        $(this).val(null)

        var notyf = new Notyf({position:{x:'center',y:'top'},duration: 3000,});

        notyf.error('Maximum file size is 3mb');


    }

})