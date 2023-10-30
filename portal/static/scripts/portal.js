let main_table=new DataTable('#regitration-table',{order:[[2,"desc"]]});

let searchParams = new URLSearchParams(window.location.search)
let table_name=searchParams.get('table-name')

$.ajaxSetup({
    headers: { 'table-name': table_name }
});

$('#add-registration-form').submit(function (e) {
    e.preventDefault();
    
    var _FormData=new FormData($(e.target)[0])
    _FormData.append('csrfmiddlewaretoken',csrf_token)
    $.ajax({
        type: "POST",
        url: "submit-add-registration",
        data:_FormData ,
        processData: false,
        contentType: false,
        dataType: "json",
        success: function (response) {
           
            if(response.success){
                $('#add-registration').modal('hide')
                
                main_table.row.add($(response.row)).draw(false)  
                main_table.order([2,"desc"]).draw(false) 
                
                
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Your work has been saved',
                    showConfirmButton: false,
                    timer: 1500
                  })

                $(e.target)[0].reset()

            }
            else{
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong!',
                  
                  })
            }
               
        }
    });
    
})
var edit_id=0
var edit_row;
var edit_btn;
function onEditRegistration(elm) {

    edit_id=$(elm).attr('reg-id')
    edit_row=$('#reg-'+edit_id)
    edit_btn=elm
    $.ajax({
        type: "GET",
        url: "get-registration-details",
        data: {edit_id:edit_id,csrfmiddlewaretoken:csrf_token},
        dataType: "json",
        success: function (response) {
            
            if (response.success){
              
                $('.edit-model-content-body').html(response.content_html)

            }
            else{
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong!',
                  
                  })
            }
        },
       
    });
}


function onSubmitEditForm (e) {
    e.preventDefault();

    var _FormData=new FormData($(e.target)[0])
    _FormData.append('edit-id',edit_id)
    _FormData.append('csrfmiddlewaretoken',csrf_token)

    $.ajax({
        type: "POST",
        url: "submit-edit-registration",
        data: _FormData,
        processData: false,
        contentType: false,
        dataType: "json",

        success: function (response) {
            console.log(response.success)
            if (response.success){

                $('#edit-registration .btn-close').click()

                $(edit_row).html(response.row.replace(/<tr[^>]*>/g, '').replace(/<\/tr>/g, ''))
                main_table.order([2,"desc"]).draw(false)
                $('#regitration-table').DataTable()

                
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Your work has been saved',
                    showConfirmButton: false,
                    timer: 1500
                  })

                $(e.target)[0].reset()
               
                if ($(edit_btn).attr('profile-edit')=='true'){
                    onProfileClick(edit_id)
                }

            }else{
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong!',
                  
                  })
            }

        }
    });

}


function onSubmitEditBulkForm(e){
    e.preventDefault(); 

    var ids_array=[]
    
    $('.reg-check-box:checked').each(function () {
        ids_array.push($(this).attr('reg-id'))
    })

    var _FormData=new FormData($(e.target)[0])
    _FormData.append('edit-ids',JSON.stringify(ids_array))
    _FormData.append('csrfmiddlewaretoken',csrf_token)

    $.ajax({
        type: "POST",
        url: "submit-bulk-edit-registration",
        data: _FormData,
        processData: false,
        contentType: false,
        dataType: "json",

        success: function (response) {
           
            if (response.success){

                $('#edit-bulk-registration .btn-close').click()
                $('.deselect-all-bulk-btn').click()
                // $(edit_row).html(response.row.replace(/<tr[^>]*>/g, '').replace(/<\/tr>/g, ''))
                // main_table.order([2,"desc"]).draw(false)
                // $('#regitration-table').DataTable()

                
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Your work has been saved',
                    showConfirmButton: false,
                    timer: 1500
                  })

                $(e.target)[0].reset()
               
                // if ($(edit_btn).attr('profile-edit')=='true'){
                //     onProfileClick(edit_id)
                // }

            }else{
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong! Error :'+response.reason,
                  
                  })
            }

        }
    });


}   

function onDeleteRegistration(elm) {



    id=$(elm).attr('reg-id')



    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
        if (result.isConfirmed) {

            $.ajax({
                type: "POST",
                url: "delete-registration",
                data: {id:id,csrfmiddlewaretoken:csrf_token},
                dataType: "json",
                success: function (response) {
                    
                    if (response.success){
                        main_table.row($(elm).closest('tr')).remove().draw(false)

                        Swal.fire(
                            'Deleted!',
                            'Your file has been deleted.',
                            'success'
                          )

                    }
                }
            });

         
        }
      })

    
    
}


function onCollect(elm) {   
    id=$(elm).attr('reg-id')
    
    $.ajax({
        type: "POST",
        url: "collect-registration",
        data: {csrfmiddlewaretoken:csrf_token,id:id},
        dataType: "json",
        success: function (response) {
            if (response.success){
                $(elm).closest('tr').html(response.row.replace(/<tr[^>]*>/g, '').replace(/<\/tr>/g, ''))
                main_table.order([2,"desc"]).draw(false)
                $('#regitration-table').DataTable()
            }
              
        }
    });
}

function onPrint(elm) {



        var id=$(elm).attr('reg-id')

        var printWindow = window.open( "print-page?table-name="+table_name+"&reg-id="+id, 'Print', 'left=200, top=200, width=950, height=500, toolbar=0, resizable=0');
      

      printWindow.addEventListener('load', function() {
      if (Boolean(printWindow.chrome)) {
          printWindow.print();
          console.log('printed and closed')
          setTimeout(function(){
              printWindow.close();
              
              var id=$(elm).attr('reg-id')
    
                $.ajax({
                    type: "POST",
                    url: "on-change-print-count",
                    data: {id:id,method:'plus',csrfmiddlewaretoken:csrf_token},

                    dataType: "json",
                    success: function (response) {
                        if(response.success){
                            
                            $(elm).closest('tr').html(response.row.replace(/<tr[^>]*>/g, '').replace(/<\/tr>/g, ''))
                            main_table.order([2,"desc"]).draw(false)
                            $('#regitration-table').DataTable()

                        }
                    }
                });


          }, 500);
        } else {
            printWindow.print();
            printWindow.close();
            console.log('printed')
        }
     }, true);


    
}

function onChageRemark(elm) {
    id=$(elm).attr('reg-id')
    content=$(elm).val()
    
    console.log(content)
    $.ajax({
        type: "POST",
        url: "change-registration-remark",
        data: {id:id,content:content,csrfmiddlewaretoken:csrf_token},
        dataType: "json",
        success: function (response) {
            
        }
    });
}

//bulk 

function onClickCheckBox(elm) {

 
    if ($('.reg-check-box:checked').length){
        $('#bulk-buttons-top-row').removeClass('d-none')
    }
    else{
        $('#bulk-buttons-top-row').addClass('d-none')
    }
    
}

$('.deselect-all-bulk-btn').click(function(){
    $('#bulk-buttons-top-row').addClass('d-none')
    $('.reg-check-box').prop('checked',false)
})

$('.select-all-bulk-btn').click(function(){
    
    $('.reg-check-box').prop('checked',true)
})

$('.bulk-print-btn').click(function () {
    
    var ids_array=[]
    $('.reg-check-box:checked').each(function () {
        ids_array.push($(this).attr('reg-id'))
    })

    var printWindow = window.open( "registration-bulk-print-page?table-name="+table_name+"&reg-ids="+JSON.stringify(ids_array), 'Print', 'left=200, top=200, width=950, height=500, toolbar=0, resizable=0');
    printWindow.addEventListener('load', function() {
        if (Boolean(printWindow.chrome)) {
            printWindow.print();
            console.log('printed and closed')
            setTimeout(function(){
                printWindow.close();
                $('#bulk-buttons-top-row').addClass('d-none')
                $('.reg-check-box').prop('checked',false)

                $.ajax({
                    type: "POST",
                    url: "on-change-bulk-print-count",
                    data: {ids:JSON.stringify(ids_array),csrfmiddlewaretoken:csrf_token},

                    dataType: "json",
                    success: function (response) {
                        if(response.success){
                            
                            // $(elm).closest('tr').html(response.row.replace(/<tr[^>]*>/g, '').replace(/<\/tr>/g, ''))
                            // main_table.order([2,"desc"]).draw(false)
                            // $('#regitration-table').DataTable()

                        }
                    }
                });
  
  
            }, 500);
          } else {
              printWindow.print();
              printWindow.close();

              $('#bulk-buttons-top-row').addClass('d-none')
              $('.reg-check-box').prop('checked',false)
              console.log('printed')
          }
       }, true);

})

$('#excel-upload-btn').click(function () {

    $('#excel-upload-file-inp').click()
    
})


var list_data;
$('#excel-upload-file-inp').change(function (event) {

    const file = event.target.files[0];
    const reader = new FileReader()
    reader.onload = function (e) {
        const contents=e.target.result;
        const workbook = XLSX.read(contents, { type: 'binary' });
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

        var tr_html=''
        list_data=jsonData.slice(1,jsonData.length)
        // console.log(list_data)
        list_data.forEach(element => {
            if (element.length < 4){
                print(element)
            }
            
            tr_html+=`<tr><td>${element[0]}</td> <td>${element[1]}</td> <td>${element[2]}</td> <td>${element[3]}</td> </tr>`
        });

        $('#excel-upload-modal').modal('toggle')

        $('#excel-upload-modal tbody').html(tr_html)

    }

    reader.readAsBinaryString(file);



})
function onSaveExcel(elm) {

    $.ajax({
        type: "POST",
        url: "submit-upload-excel-data",
        data: {data:JSON.stringify(list_data),csrfmiddlewaretoken:csrf_token},
        dataType: "json",
        success: function (response) {
            $('#excel-upload-modal').modal('toggle')
            window.location.reload()
        }
    });
    
}

function onMinusCount(elm) {

    var id=$(elm).attr('reg-id')
    
    $.ajax({
        type: "POST",
        url: "on-change-print-count",
        data: {id:id,method:'minus',csrfmiddlewaretoken:csrf_token},

        dataType: "json",
        success: function (response) {
            if(response.success){
                
                $(elm).closest('tr').html(response.row.replace(/<tr[^>]*>/g, '').replace(/<\/tr>/g, ''))
                main_table.order([2,"desc"]).draw(false)
                $('#regitration-table').DataTable()

            }
        }
    });
    
}


function ExportToExcel(type, fn, dl) {
     
    var myClone=document.getElementById('regitration-table');
    myClone = myClone.cloneNode(true);

    $(myClone).find('#th-action').remove();
    $(myClone).find('#th-user').remove();
    $(myClone).find('#td-user').remove();
    $(myClone).find('#th-tick').remove();
    $(myClone).find('.td-tick').remove();
    $(myClone).find('.td-action').remove();
    $(myClone).find('.td-remark').remove();
    $(myClone).find('.th-remark').remove();
    
    // $(myClone).find('#td-action').remove();

    // $(myClone).find('#th-user').remove();
    // $(myClone).find('#td-user').remove();
    // $(myClone).find('#th-tick').remove();
    // $(myClone).find('#td-tick').remove();
    // $(myClone).find('#td-none-tick').remove();
    
    // $(myClone).find('thead > tr ').append('<th>Signature</th>')
    // $(myClone).find('tbody > tr ').append('<td></td>')
    
     var elt = myClone

     var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
     return dl ?
       XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }):
       XLSX.writeFile(wb, fn || ('applicnat.' + (type || 'xlsx')));
    }

function onChangeVerification(elm) {
    id=$(elm).attr('reg-id')
    method=$(elm).attr('method')

    $.ajax({
        type: "POST",
        url: "change-verification",
        data: {id:id,method:method,csrfmiddlewaretoken:csrf_token},
        dataType: "json",
        success: function (response) {
            if(response.success){
                
                $('#reg-'+id).html(response.row.replace(/<tr[^>]*>/g, '').replace(/<\/tr>/g, ''))
                main_table.order([2,"desc"]).draw(false)
                $('#regitration-table').DataTable()
                
                if ($(elm).hasClass('profile-verification-btn')){
                    
                    onProfileClick(id)
                    console.log('profile')
                }
                $('#rejection-reason-model').modal('hide')
                sendMail(id,method)
            }
        }
    });

}

function onClickRejectBtn(elm){

    if ($(elm).hasClass('profile-verification-btn')){
        console.log('has')
        $('.rejection-reason-submit').addClass('profile-verification-btn')
    }else{
        $('.rejection-reason-submit').removeClass('profile-verification-btn')
    }

    id=$(elm).attr('reg-id')
    $('#rejection-reason-model').modal('show')
    $('.rejection-reason-submit').attr('reg-id',id)
    

}


function sendMail(id,method='approved'){
    reason=$('#rejection-reason-textarea').val()
    console.log(reason)

    $.ajax({
        type: "POST",
        url: "send-mail-in-portal",
        data: {id:id,reason:reason,method:method,'csrfmiddlewaretoken':csrf_token},
        dataType: "json",
        success: function (response) {
            $('#rejection-reason-textarea').val('')
        }
    });
}

// SSE ----------------------------------------------------------------------------------------


setInterval(() => {
    getLatestData()
}, 5000);

function getLatestData(){
    $.ajax({
        type: "GET",
        url: "get-latest-data",
        data: {"table-name":table_name},
        dataType: "json",
        success: function (response) {
       
            const data=response

           if (data.new_data){

                for (let i = 0; i < data.ids.length; i++) {
                    
                    if ($('#reg-'+data.ids[i])){
                    // $('#reg-'+data.ids[i]).html(data.rows[i].replace(/<tr[^>]*>/g, '').replace(/<\/tr>/g, ''))
                    main_table.row('#reg-'+data.ids[i]).remove().draw(false)
                    main_table.row.add($(data.rows[i])).draw(false)
                        main_table.draw(false)
                        $('#regitration-table').DataTable()
                    }
                    
                    
                }

           }
             

        }
    });
}
// let eventSource = new EventSource('sse?table-name='+table_name);

// eventSource.onmessage = (event) => {
//     updateDataSSE(event)
// };


// eventSource.onerror = function (error) {
//     // Handle any errors here
    
//     reconnectEventSource();
// };

// function updateDataSSE(event){
//     const data = JSON.parse(event.data);
//     // Update the page with the received data
//     console.log('Received data:', data);

//     for (let i = 0; i < data.ids.length; i++) {
       
//         if ($('#reg-'+data.ids[i])){
//            // $('#reg-'+data.ids[i]).html(data.rows[i].replace(/<tr[^>]*>/g, '').replace(/<\/tr>/g, ''))
//            main_table.row('#reg-'+data.ids[i]).remove().draw(false)
//            main_table.row.add($(data.rows[i])).draw(false)
//             main_table.draw(false)
//             $('#regitration-table').DataTable()
//         }
        
        
//     }
// }


// /// in live enviroment we using the gunicorn ---reload it will restart the server after a perticular time it cuassig the continues sse connction so 
// /// i don like this to reconnect after sse connection lost :) 
// function reconnectEventSource() {
//     console.log('reconnection started ---')
//     setTimeout(() => {
//       eventSource.close(); // Close the existing connection
//       eventSource = new EventSource('sse?table-name='+table_name);
//       eventSource.onopen = (event) => {
//         console.log('Reconnected');
//       };

//       eventSource.onmessage = (event) => {
//         updateDataSSE(event)
//         };

//         eventSource.onerror = function (error) {
//             // Handle any errors here
           
//             reconnectEventSource();
//         };
    
//     }, 1000); // Delay before reconnection (adjust as needed)
//   }